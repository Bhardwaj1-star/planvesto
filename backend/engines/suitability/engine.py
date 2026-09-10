from typing import Any

from models.strategy_approval import SuitabilityAssessment


class SuitabilityEngine:
    """Rules-ready suitability boundary.

    Financial suitability rules are intentionally not invented here. Component
    diagnostics are supplied by future rule modules; this engine validates and
    normalizes the assessment contract used by approval.
    """

    RULE_SET_VERSION = "framework-1.0"
    VALID_STATUSES = {"Suitable", "Needs Attention", "Unsuitable"}

    def assess(
        self,
        status: str,
        diagnostics: list[dict[str, Any]] | None = None,
    ) -> SuitabilityAssessment:
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid suitability status: {status}")

        normalized_diagnostics = diagnostics or []
        return SuitabilityAssessment(
            status=status,  # type: ignore[arg-type]
            diagnostics=normalized_diagnostics,
            rule_set_version=self.RULE_SET_VERSION,
        )
