from __future__ import annotations

from collections import defaultdict
from typing import Any

from engines.calculation.engine import annual_amount, monthly_amount, percentage, round_money
from models.financial_state import FinancialState, Metric
from rules.financial_state import MISSING_INPUT, cash_flow_ratio, required_safety_reserve_months, savings_investment_rate


class FinancialStateEngine:
    def build(self, planning_unit_id: str, investors: list[dict[str, Any]], income_rows: list[dict[str, Any]],
              expense_rows: list[dict[str, Any]], asset_rows: list[dict[str, Any]],
              liability_rows: list[dict[str, Any]], asset_owner_rows: list[dict[str, Any]],
              liability_responsibility_rows: list[dict[str, Any]], expense_participant_rows: list[dict[str, Any]],
              scope: str = "family", investor_id: str | None = None) -> FinancialState:
        income = self._income(income_rows, scope, investor_id)
        expenses = self._expenses(expense_rows, scope, investor_id, expense_participant_rows)
        assets = self._assets(asset_rows, asset_owner_rows, scope, investor_id)
        liabilities = self._liabilities(liability_rows, liability_responsibility_rows, scope, investor_id)

        surplus_m = None
        surplus_a = None
        if income.available and expenses.available:
            surplus_m = round_money(income.monthly - expenses.monthly)
            surplus_a = round_money(surplus_m * 12)

        cfr = cash_flow_ratio(expenses.monthly, income.monthly) if surplus_m is not None else None
        savings = savings_investment_rate(surplus_m, income.monthly) if surplus_m is not None else None
        net_worth = round_money(assets.total - liabilities.total) if assets.available and liabilities.available else None

        reserve_months = None
        reserve_amount = None
        if cfr is not None:
            reserve_months = required_safety_reserve_months(cfr)
            reserve_amount = round_money(expenses.monthly * reserve_months)

        return FinancialState(
            scope=scope, planning_unit_id=planning_unit_id, investor_id=investor_id,
            income_monthly=Metric(value=round_money(income.monthly), available=income.available, reason=income.reason),
            income_annual=Metric(value=round_money(income.annual), available=income.available, reason=income.reason),
            income_breakdown=income.breakdown,
            expenses_monthly=Metric(value=round_money(expenses.monthly), available=expenses.available, reason=expenses.reason),
            expenses_annual=Metric(value=round_money(expenses.annual), available=expenses.available, reason=expenses.reason),
            expense_breakdown=expenses.breakdown,
            investable_surplus_monthly=self._metric(surplus_m),
            investable_surplus_annual=self._metric(surplus_a),
            cash_flow_ratio=self._metric(cfr),
            savings_investment_rate=self._metric(savings),
            total_assets=self._metric(assets.total),
            asset_breakdown=assets.breakdown,
            asset_allocation=assets.allocation,
            liquidity_breakdown=assets.liquidity_breakdown,
            total_liabilities=self._metric(liabilities.total),
            liability_breakdown=liabilities.breakdown,
            liability_allocation=liabilities.allocation,
            emi_burden_monthly=Metric(value=liabilities.emi, available=liabilities.emi_available, reason=None if liabilities.emi_available else MISSING_INPUT),
            net_worth=self._metric(net_worth),
            safety_reserve_months=Metric(value=reserve_months, available=reserve_months is not None, reason=None if reserve_months is not None else MISSING_INPUT),
            safety_reserve_required_amount=Metric(value=reserve_amount, available=reserve_amount is not None, reason=None if reserve_amount is not None else MISSING_INPUT),
        )

    @staticmethod
    def _metric(value):
        return Metric(value=value, available=value is not None, reason=None if value is not None else MISSING_INPUT)

    def _income(self, rows, scope, investor_id):
        selected = rows if scope == "family" else [r for r in rows if r.get("investor_id") == investor_id]
        monthly = annual = 0.0
        breakdown = defaultdict(float)
        available = True
        for r in selected:
            amount = float(r.get("amount") or 0)
            m = monthly_amount(amount, str(r.get("frequency") or ""))
            a = annual_amount(amount, str(r.get("frequency") or ""))
            if m is None or a is None:
                available = False
                continue
            monthly += m; annual += a
            breakdown[str(r.get("income_type") or "Other")] += m
        return _Component(monthly, annual, available, None if available else MISSING_INPUT,
                          [{"type": k, "monthly": round_money(v), "annual": round_money(v * 12)} for k, v in breakdown.items()])

    def _expenses(self, rows, scope, investor_id, participant_rows):
        factors = {}
        if scope == "individual":
            for p in participant_rows:
                if p.get("investor_id") == investor_id:
                    factors[p.get("expense_id")] = float(p.get("participation_percentage") or 100) / 100
        selected = rows if scope == "family" else [r for r in rows if r.get("expense_id") in factors]
        monthly = 0.0; breakdown = defaultdict(float); available = True
        for r in selected:
            m = monthly_amount(float(r.get("amount") or 0), str(r.get("frequency") or ""))
            if m is None:
                available = False; continue
            m *= factors.get(r.get("expense_id"), 1.0)
            monthly += m; breakdown[str(r.get("expense_type") or "Other")] += m
        return _Component(monthly, monthly * 12, available, None if available else MISSING_INPUT,
                          [{"type": k, "monthly": round_money(v), "annual": round_money(v * 12)} for k, v in breakdown.items()])

    def _assets(self, rows, owners, scope, investor_id):
        owner_map = defaultdict(list)
        for row in owners: owner_map[row.get("asset_id")].append(row)
        breakdown=[]; total=0.0; liquidity=defaultdict(float)
        for r in rows:
            value=float(r.get("current_value") or 0); owner_rows=owner_map.get(r.get("asset_id"), [])
            if not owner_rows: share=1.0
            elif scope == "family": share=sum(float(o.get("ownership_percentage") or 0) for o in owner_rows)/100
            else:
                matching=[o for o in owner_rows if o.get("investor_id")==investor_id]
                share=float(matching[0].get("ownership_percentage") or 100)/100 if matching else 0.0
            owned=value*share; total+=owned
            breakdown.append({"asset_id":r.get("asset_id"),"name":r.get("asset_name"),"current_value":round_money(owned),"ownership_applied":round_money(share*100),"liquidity":None})
            liquidity["Unclassified"] += owned
        allocation=[{"asset_id":x["asset_id"],"name":x["name"],"percentage":percentage(x["current_value"],total)} for x in breakdown] if total else []
        liquidity_breakdown=[{"classification":k,"value":round_money(v),"percentage":percentage(v,total)} for k,v in liquidity.items()]
        return _AssetComponent(total, breakdown, allocation, liquidity_breakdown)

    def _liabilities(self, rows, responsibilities, scope, investor_id):
        resp_map=defaultdict(list)
        for row in responsibilities: resp_map[row.get("liability_id")].append(row)
        breakdown=[]; total=0.0; emi=0.0; emi_available=True
        for r in rows:
            outstanding=float(r.get("outstanding_amount") or 0); lid=r.get("liability_id"); rr=resp_map.get(lid,[])
            if not rr: share=1.0
            elif scope == "family": share=sum(float(x.get("responsibility_percentage") or 0) for x in rr)/100
            else:
                match=[x for x in rr if x.get("investor_id")==investor_id]
                share=float(match[0].get("responsibility_percentage") or 100)/100 if match else 0.0
            owned=outstanding*share; total+=owned
            payment=r.get("emi_amount")
            if payment is None: emi_available=False
            else:
                pm=monthly_amount(float(payment), str(r.get("frequency") or ""))
                if pm is None: emi_available=False
                else: emi += pm*share
            breakdown.append({"liability_id":lid,"name":r.get("liability_name"),"outstanding_amount":round_money(owned),"responsibility_applied":round_money(share*100),"classification":None})
        allocation=[{"liability_id":x["liability_id"],"name":x["name"],"percentage":percentage(x["outstanding_amount"],total)} for x in breakdown] if total else []
        return _LiabilityComponent(total, breakdown, allocation, emi if emi_available else None, emi_available)


class _Component:
    def __init__(self, monthly, annual, available, reason, breakdown): self.monthly=monthly; self.annual=annual; self.available=available; self.reason=reason; self.breakdown=breakdown
class _AssetComponent:
    def __init__(self,total,breakdown,allocation,liquidity_breakdown): self.total=total; self.available=True; self.breakdown=breakdown; self.allocation=allocation; self.liquidity_breakdown=liquidity_breakdown
class _LiabilityComponent:
    def __init__(self,total,breakdown,allocation,emi,emi_available): self.total=total; self.available=True; self.breakdown=breakdown; self.allocation=allocation; self.emi=emi; self.emi_available=emi_available
