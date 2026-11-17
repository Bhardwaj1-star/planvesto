"""
infrastructure/persistence/mappers/financial_state.py
Bi-directional translation between Supabase/Postgres raw rows and Domain FinancialState objects.
"""

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.domain.canonical.financial_categories import (
    CanonicalAssetCategoryId,
    CanonicalExpenseCategoryId,
    CanonicalIncomeCategoryId,
    CanonicalInsurancePolicyTypeId,
    CanonicalLiabilityCategoryId,
)
from app.domain.features.investor_profile.financial_state.models import (
    AssetRecord,
    ExpenseRecord,
    FinancialStateSnapshot,
    IncomeRecord,
    InsuranceRecord,
    LiabilityRecord,
)
from app.domain.shared.value_objects import (
    CalendarMonth,
    EvidenceStatus,
    FlowFrequency,
    Money,
    Rate,
)


def _map_income_category(cat: str) -> CanonicalIncomeCategoryId:
    cat_lower = str(cat).lower()
    for item in CanonicalIncomeCategoryId:
        if item.value == cat_lower or item.name.lower() == cat_lower or item.value.replace("income_", "") == cat_lower:
            return item
    return CanonicalIncomeCategoryId.OTHER


def _map_expense_category(cat: str) -> CanonicalExpenseCategoryId:
    cat_lower = str(cat).lower()
    for item in CanonicalExpenseCategoryId:
        if item.value == cat_lower or item.name.lower() == cat_lower or item.value.replace("expense_", "") == cat_lower:
            return item
    return CanonicalExpenseCategoryId.OTHER


def _map_asset_category(cat: str) -> CanonicalAssetCategoryId:
    cat_lower = str(cat).lower()
    for item in CanonicalAssetCategoryId:
        if item.value == cat_lower or item.name.lower() == cat_lower or item.value.replace("asset_", "") == cat_lower:
            return item
    return CanonicalAssetCategoryId.OTHER


def _map_liability_category(cat: str) -> CanonicalLiabilityCategoryId:
    cat_lower = str(cat).lower()
    for item in CanonicalLiabilityCategoryId:
        if item.value == cat_lower or item.name.lower() == cat_lower or item.value.replace("liability_", "") == cat_lower:
            return item
    return CanonicalLiabilityCategoryId.OTHER


def map_row_to_income_record(row: Dict[str, Any], default_period: CalendarMonth) -> IncomeRecord:
    amount = Money(amount=Decimal(str(row.get("amount", 0))))
    category = _map_income_category(row.get("category", "other"))
    frequency_text = str(row.get("frequency", "monthly")).strip().lower().replace("-", "_")
    frequency = {
        "annual": FlowFrequency.ANNUAL,
        "annually": FlowFrequency.ANNUAL,
        "yearly": FlowFrequency.ANNUAL,
        "quarterly": FlowFrequency.QUARTERLY,
        "quarter": FlowFrequency.QUARTERLY,
        "semi_annual": FlowFrequency.SEMI_ANNUAL,
        "semiannual": FlowFrequency.SEMI_ANNUAL,
        "half_yearly": FlowFrequency.SEMI_ANNUAL,
        "one_time": FlowFrequency.ONE_OFF,
        "one_off": FlowFrequency.ONE_OFF,
    }.get(frequency_text, FlowFrequency.MONTHLY)

    return IncomeRecord(
        id=str(row.get("income_id", row.get("id", ""))),
        category=category,
        amount=amount,
        is_net=bool(row.get("is_net", True)),
        frequency=frequency,
        period=default_period,
        status=EvidenceStatus(row.get("status", "investor_reported")),
        source=str(row.get("source", "investor_declared")),
        notes=row.get("notes"),
    )


def map_row_to_expense_record(row: Dict[str, Any], default_period: CalendarMonth) -> ExpenseRecord:
    amount = Decimal(str(row.get("amount", 0)))
    frequency_text = str(row.get("frequency", "monthly")).strip().lower().replace("-", "_")
    if frequency_text in ("annual", "annually", "yearly"):
        amount /= Decimal("12")
    elif frequency_text in ("quarterly", "quarter"):
        amount /= Decimal("3")
    elif frequency_text in ("semi_annual", "semiannual", "half_yearly"):
        amount /= Decimal("6")
    elif frequency_text in ("one_time", "one_off", "oneoff", "once"):
        amount = Decimal("0")
    category = _map_expense_category(row.get("category", "other"))
    return ExpenseRecord(
        id=str(row.get("expense_id", row.get("id", ""))),
        category=category,
        amount=Money(amount=amount),
        period=default_period,
        is_emi=bool(row.get("is_emi", False)),
        is_own_account_transfer=bool(row.get("is_own_account_transfer", False)),
        status=EvidenceStatus(row.get("status", "investor_reported")),
        source=str(row.get("source", "investor_declared")),
        notes=row.get("notes"),
    )


def map_row_to_asset_record(row: Dict[str, Any]) -> AssetRecord:
    current_val = Money(amount=Decimal(str(row.get("current_value", row.get("amount", 0)))))
    category = _map_asset_category(row.get("category", "other"))
    as_of = date.fromisoformat(str(row.get("as_of_date", date.today().isoformat())))
    ownership_pct = Rate.from_percentage(str(row.get("ownership_percentage", 100)))

    exp_return = None
    if row.get("expected_annual_return") is not None:
        exp_return = Rate.from_percentage(str(row.get("expected_annual_return")))

    return AssetRecord(
        id=str(row.get("asset_id", row.get("id", ""))),
        name=str(row.get("asset_name", row.get("name", "Asset"))),
        category=category,
        value=current_val,
        as_of_date=as_of,
        ownership_share=ownership_pct,
        is_accessible=bool(row.get("is_accessible", True)),
        is_committed=bool(row.get("committed_to_existing_goal", row.get("is_committed", False))),
        access_restrictions=list(row.get("access_restrictions") or []),
        lock_in_until=date.fromisoformat(str(row["lock_in_until"])) if row.get("lock_in_until") else None,
        expected_annual_return=exp_return,
        status=EvidenceStatus(row.get("status", "investor_reported")),
        source=str(row.get("source", "investor_declared")),
    )


def map_row_to_liability_record(row: Dict[str, Any]) -> LiabilityRecord:
    balance = Money(amount=Decimal(str(row.get("outstanding_balance", row.get("amount", 0)))))
    monthly_payment = Money(amount=Decimal(str(row.get("monthly_payment", row.get("emi", 0)))))
    category = _map_liability_category(row.get("category", "other"))
    interest_rate = Rate.from_percentage(str(row.get("annual_interest_rate", row.get("interest_rate", 0))))
    as_of = date.fromisoformat(str(row.get("as_of_date", date.today().isoformat())))

    return LiabilityRecord(
        id=str(row.get("liability_id", row.get("id", ""))),
        name=str(row.get("liability_name", row.get("name", "Liability"))),
        category=category,
        outstanding_balance=balance,
        annual_interest_rate=interest_rate,
        monthly_payment=monthly_payment,
        as_of_date=as_of,
        remaining_tenure_months=int(row.get("remaining_tenure_months", 0)),
        is_high_interest=bool(row.get("is_high_interest", False)),
        status=EvidenceStatus(row.get("status", "investor_reported")),
        source=str(row.get("source", "investor_declared")),
    )


def map_financial_facts_to_snapshot(
    investor_id: str,
    as_of_date: date,
    facts: Dict[str, List[Dict[str, Any]]],
) -> FinancialStateSnapshot:
    """Map raw database rows dictionary to a domain FinancialStateSnapshot."""
    period = CalendarMonth(as_of_date.year, as_of_date.month)

    incomes = [
        map_row_to_income_record(row, period)
        for row in facts.get("income", [])
    ]
    expenses = [
        map_row_to_expense_record(row, period)
        for row in facts.get("expenses", facts.get("expense", []))
    ]
    assets = [
        map_row_to_asset_record(row)
        for row in facts.get("assets", facts.get("asset", []))
    ]
    liabilities = [
        map_row_to_liability_record(row)
        for row in facts.get("liabilities", facts.get("liability", []))
    ]
    monthly_savings_investments = []
    for row in facts.get("assets", facts.get("asset", [])):
        contribution = Decimal(str(row.get("monthly_contribution_amount", row.get("monthly_contribution", 0)) or 0))
        frequency_text = str(row.get("monthly_contribution_frequency", "monthly")).strip().lower().replace("-", "_")
        if frequency_text in ("annual", "annually", "yearly"):
            contribution /= Decimal("12")
        elif frequency_text in ("quarterly", "quarter"):
            contribution /= Decimal("3")
        elif frequency_text in ("semi_annual", "semiannual", "half_yearly"):
            contribution /= Decimal("6")
        elif frequency_text in ("one_time", "one_off", "oneoff", "once"):
            contribution = Decimal("0")
        if contribution > 0:
            monthly_savings_investments.append(Money(amount=contribution))

    return FinancialStateSnapshot(
        investor_id=investor_id,
        as_of_date=as_of_date,
        incomes=incomes,
        expenses=expenses,
        monthly_savings_investments=monthly_savings_investments,
        assets=assets,
        liabilities=liabilities,
        insurances=[],
    )


def snapshot_to_persistence_dict(snapshot: FinancialStateSnapshot) -> Dict[str, Any]:
    """Serialize FinancialStateSnapshot into a dictionary for JSON/Postgres persistence."""
    return {
        "investor_id": snapshot.investor_id,
        "as_of_date": snapshot.as_of_date.isoformat(),
        "incomes": [
            {
                "id": i.id,
                "category": i.category.value,
                "amount": str(i.amount.amount),
                "is_net": i.is_net,
                "frequency": i.frequency.value,
                "period": f"{i.period.year:04d}-{i.period.month:02d}",
                "status": i.status.value,
                "source": i.source,
                "notes": i.notes,
            }
            for i in snapshot.incomes
        ],
        "expenses": [
            {
                "id": e.id,
                "category": e.category.value,
                "amount": str(e.amount.amount),
                "period": f"{e.period.year:04d}-{e.period.month:02d}",
                "is_emi": e.is_emi,
                "is_own_account_transfer": e.is_own_account_transfer,
                "status": e.status.value,
                "source": e.source,
                "notes": e.notes,
            }
            for e in snapshot.expenses
        ],
        "monthly_savings_investments": [str(item.amount) for item in snapshot.monthly_savings_investments],
        "assets": [
            {
                "id": a.id,
                "name": a.name,
                "category": a.category.value,
                "current_value": str(a.current_value.amount),
                "as_of_date": a.as_of_date.isoformat(),
                "ownership_percentage": str(a.ownership_percentage.percentage),
                "is_accessible": a.is_accessible,
                "committed_to_existing_goal": a.committed_to_existing_goal,
                "expected_annual_return": str(a.expected_annual_return.percentage) if a.expected_annual_return else None,
                "status": a.status.value,
                "source": a.source,
            }
            for a in snapshot.assets
        ],
        "liabilities": [
            {
                "id": l.id,
                "name": l.name,
                "category": l.category.value,
                "outstanding_balance": str(l.outstanding_balance.amount),
                "annual_interest_rate": str(l.annual_interest_rate.percentage),
                "monthly_payment": str(l.monthly_payment.amount),
                "as_of_date": l.as_of_date.isoformat(),
                "remaining_tenure_months": l.remaining_tenure_months,
                "is_high_interest": l.is_high_interest,
                "status": l.status.value,
                "source": l.source,
            }
            for l in snapshot.liabilities
        ],
        "net_worth": str(snapshot.net_worth().amount),
        "total_assets": str(snapshot.total_assets().amount),
        "total_liabilities": str(snapshot.total_liabilities().amount),
    }
