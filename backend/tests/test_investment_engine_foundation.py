from engines.investment.engine import InvestmentEngine
from engines.investment.models import InvestmentEngineInput


def test_investment_engine_requires_complete_risk_profile():
    result = InvestmentEngine().build(
        InvestmentEngineInput(
            risk_profile={
                "risk_required": {"available": True, "value": 10.0, "unit": "%"},
                "risk_capacity": {"available": True, "value": 8.0, "unit": "score"},
                "risk_tolerance": {"available": False},
            }
        )
    )

    assert result.status == "requires_review"
    assert len(result.layers) == 5
    assert result.risk_boundary["risk_tolerance"]["available"] is False


def test_investment_engine_creates_implementation_layers_when_profile_complete():
    result = InvestmentEngine().build(
        InvestmentEngineInput(
            risk_profile={
                "risk_required": {"available": True, "value": 10.0, "unit": "%"},
                "risk_capacity": {"available": True, "value": 8.0, "unit": "score"},
                "risk_tolerance": {"available": True, "value": 7.0, "unit": "score"},
            },
            current_portfolio={"allocation": {"equity": 0.6, "debt": 0.4}},
        )
    )

    assert result.status == "ready"
    assert [layer.layer for layer in result.layers] == [
        "strategic_asset_allocation",
        "sub_asset_allocation",
        "product_category",
        "product_selection",
        "allocation_amount",
    ]
    assert result.current_allocation == {"equity": 0.6, "debt": 0.4}
