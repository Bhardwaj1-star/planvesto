import hashlib
import json

from fastapi import HTTPException

from data.financial_data import FinancialDataRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from engines.financial_state.engine import FinancialStateEngine
from models.financial_state import FinancialState


class FinancialStateService:
    def __init__(
        self,
        repository: FinancialDataRepository | None = None,
        snapshot_repository: FinancialStateSnapshotRepository | None = None,
        engine: FinancialStateEngine | None = None,
    ):
        self.repository = repository or FinancialDataRepository()
        self.snapshot_repository = snapshot_repository or FinancialStateSnapshotRepository()
        self.engine = engine or FinancialStateEngine()

    @staticmethod
    def _validate_context(planning_unit_id: str, scope: str, investor_id: str | None) -> None:
        if not planning_unit_id.strip():
            raise HTTPException(status_code=400, detail="planning_unit_id is required")
        if scope not in {"family", "individual"}:
            raise HTTPException(status_code=400, detail="scope must be family or individual")
        if scope == "individual" and not investor_id:
            raise HTTPException(status_code=400, detail="investor_id is required for individual scope")
        if scope == "family" and investor_id is not None:
            raise HTTPException(status_code=400, detail="investor_id is only valid for individual scope")

    @staticmethod
    def _revision(inputs: dict[str, list[dict]]) -> str:
        normalized = {
            key: sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, default=str))
            for key, rows in inputs.items()
        }
        encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def _inputs(self, planning_unit_id: str, scope: str, investor_id: str | None):
        self._validate_context(planning_unit_id, scope, investor_id)
        inputs = self.repository.get_financial_state_inputs(planning_unit_id)
        if scope == "individual" and not any(
            row.get("investor_id") == investor_id for row in inputs["investors"]
        ):
            raise HTTPException(status_code=404, detail="Investor not found in planning unit")
        return inputs

    def _build_from_inputs(
        self,
        planning_unit_id: str,
        scope: str,
        investor_id: str | None,
        inputs: dict[str, list[dict]],
    ) -> FinancialState:
        return self.engine.build(
            planning_unit_id=planning_unit_id,
            investors=inputs["investors"],
            income_rows=inputs["income"],
            expense_rows=inputs["expenses"],
            asset_rows=inputs["assets"],
            liability_rows=inputs["liabilities"],
            asset_owner_rows=inputs["asset_owners"],
            liability_responsibility_rows=inputs["liability_responsibilities"],
            expense_participant_rows=inputs["expense_participants"],
            scope=scope,
            investor_id=investor_id,
        )

    def build(self, planning_unit_id: str, scope: str = "family", investor_id: str | None = None):
        """Return the current state, rebuilding only when its raw-input binding is stale."""
        return self.current(planning_unit_id, scope, investor_id)

    def get_current_snapshot(
        self,
        planning_unit_id: str,
        scope: str = "family",
        investor_id: str | None = None,
    ) -> dict:
        """Return a fresh, lineage-bound snapshot, rebuilding when raw inputs changed."""
        inputs = self._inputs(planning_unit_id, scope, investor_id)
        input_revision = self._revision(inputs)
        snapshot = self.snapshot_repository.get_latest(planning_unit_id, scope, investor_id)
        if snapshot is not None:
            stored_state = snapshot.get("financial_state") or {}
            authority = stored_state.get("__snapshot_authority")
            state = {
                key: value for key, value in stored_state.items()
                if key != "__snapshot_authority"
            }
            action_lineage_valid = True
            if isinstance(authority, dict) and authority.get("source") == "action_completion":
                action_lineage_valid = bool(
                    snapshot.get("snapshot_id")
                    and authority.get("action_id")
                    and authority.get("strategy_version_id")
                    and self.snapshot_repository.has_completed_action_lineage(
                        planning_unit_id,
                        authority["action_id"],
                        snapshot["snapshot_id"],
                        authority["strategy_version_id"],
                    )
                )
            if (
                isinstance(authority, dict)
                and authority.get("source") in {"backend_derived", "action_completion"}
                and authority.get("input_revision") == input_revision
                and action_lineage_valid
                and snapshot.get("planning_unit_id") == planning_unit_id
                and snapshot.get("scope") == scope
                and snapshot.get("investor_id") == investor_id
                and state.get("planning_unit_id") == planning_unit_id
                and state.get("scope") == scope
                and state.get("investor_id") == investor_id
            ):
                FinancialState.model_validate(state)
                return {**snapshot, "financial_state": state, "authority": authority}

        rebuilt = self._build_from_inputs(planning_unit_id, scope, investor_id, inputs)
        row = self.snapshot_repository.save_snapshot(
            planning_unit_id=planning_unit_id,
            scope=scope,
            investor_id=investor_id,
            financial_state=rebuilt.model_dump(mode="json"),
            authority={
                "source": "backend_derived",
                "input_revision": input_revision,
            },
        )
        return {
            **row,
            "financial_state": rebuilt.model_dump(mode="json"),
            "authority": {
                "source": "backend_derived",
                "input_revision": input_revision,
            },
        }

    def current(self, planning_unit_id: str, scope: str = "family", investor_id: str | None = None):
        row = self.get_current_snapshot(planning_unit_id, scope, investor_id)
        return FinancialState.model_validate(row["financial_state"])

    def save_actual_state(
        self,
        actual_state: FinancialState,
        action_id: str,
        strategy_version_id: str,
        source_snapshot_id: str,
        expected_input_revision: str,
    ) -> dict:
        """Persist D1 client state with raw-input revision and action lineage."""
        if not action_id.strip() or not strategy_version_id.strip():
            raise ValueError("Action and StrategyVersion lineage are required")
        actual_state = FinancialState.model_validate(actual_state)
        self._validate_context(
            actual_state.planning_unit_id,
            actual_state.scope,
            actual_state.investor_id,
        )
        current_snapshot = self.get_current_snapshot(
            actual_state.planning_unit_id,
            actual_state.scope,
            actual_state.investor_id,
        )
        inputs = self._inputs(
            actual_state.planning_unit_id,
            actual_state.scope,
            actual_state.investor_id,
        )
        input_revision = self._revision(inputs)
        if (
            input_revision != expected_input_revision
            or current_snapshot.get("snapshot_id") != source_snapshot_id
            or current_snapshot.get("authority", {}).get("input_revision") != expected_input_revision
        ):
            raise HTTPException(
                status_code=409,
                detail="FinancialState changed during action completion; refresh and retry.",
            )
        return self.snapshot_repository.save_snapshot(
            planning_unit_id=actual_state.planning_unit_id,
            scope=actual_state.scope,
            investor_id=actual_state.investor_id,
            financial_state=actual_state.model_dump(mode="json"),
            authority={
                "source": "action_completion",
                "input_revision": input_revision,
                "action_id": action_id,
                "strategy_version_id": strategy_version_id,
            },
        )
