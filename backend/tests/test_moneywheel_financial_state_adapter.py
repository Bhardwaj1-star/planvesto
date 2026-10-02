from models.financial_state import FinancialState, Metric
from engines.moneywheel.financial_state_adapter import MoneywheelFinancialStateAdapter


def metric(value):
    return Metric(value=value, available=value is not None)


def make_state():
    return FinancialState(
        scope="family",
        planning_unit_id="pu-1",
        income_monthly=metric(100000),
        income_annual=metric(1200000),
        expenses_monthly=metric(40000),
        expenses_annual=metric(480000),
        investable_surplus_monthly=metric(50000),
        investable_surplus_annual=metric(600000),
        cash_flow_ratio=metric(0.5),
        savings_investment_rate=metric(0.5),
        total_assets=metric(1000000),
        total_liabilities=metric(200000),
        emi_burden_monthly=metric(10000),
        net_worth=metric(800000),
        safety_reserve_months=metric(6),
        safety_reserve_required_amount=metric(300000),
    )


def test_adapter_maps_existing_financial_state_fields():
    data = MoneywheelFinancialStateAdapter().build(
        make_state(),
        essential_monthly_expenses=30000,
        liquid_assets=250000,
        financial_assets=700000,
    )

    assert data.gross_monthly_income == 100000
    assert data.monthly_surplus == 50000
    assert data.monthly_expenses == 40000
    assert data.monthly_debt_payments == 10000
    assert data.total_assets == 1000000
    assert data.total_liabilities == 200000
    assert data.liquid_assets == 250000
    assert data.financial_assets == 700000


def test_adapter_does_not_infer_classification_dependent_fields():
    data = MoneywheelFinancialStateAdapter().build(make_state())

    assert data.essential_monthly_expenses is None
    assert data.liquid_assets is None
    assert data.financial_assets is None
