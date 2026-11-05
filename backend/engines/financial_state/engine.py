from __future__ import annotations

from collections import defaultdict
from typing import Any

from engines.calculation.engine import annual_amount, monthly_amount, percentage, round_money
from engines.calculation.canonical import calculate_net_worth
from models.financial_state import FinancialState, Metric
from rules.financial_state import MISSING_INPUT
from rules.financial_metrics import is_essential_expense


class FinancialStateEngine:
    def build(self, planning_unit_id: str, investors: list[dict[str, Any]], income_rows: list[dict[str, Any]],
              expense_rows: list[dict[str, Any]], asset_rows: list[dict[str, Any]],
              liability_rows: list[dict[str, Any]], asset_owner_rows: list[dict[str, Any]],
              liability_responsibility_rows: list[dict[str, Any]], expense_participant_rows: list[dict[str, Any]],
              asset_type_master: list[dict[str, Any]] | None = None,
              insurance_rows: list[dict[str, Any]] | None = None,
              scope: str = "family", investor_id: str | None = None) -> FinancialState:
        income = self._income(income_rows, scope, investor_id)
        expenses = self._expenses(expense_rows, scope, investor_id, expense_participant_rows)
        assets = self._assets(asset_rows, asset_owner_rows, asset_type_master or [], scope, investor_id)
        liabilities = self._liabilities(liability_rows, liability_responsibility_rows, scope, investor_id)
        insurance = self._insurance(insurance_rows or [], scope, investor_id)

        surplus_m = None
        surplus_a = None
        if income.available and expenses.available:
            surplus_m = round_money(income.monthly - expenses.monthly)
            surplus_a = round_money(surplus_m * 12)

        return FinancialState(
            scope=scope, planning_unit_id=planning_unit_id, investor_id=investor_id,
            income_monthly=Metric(value=round_money(income.monthly), available=income.available, reason=income.reason),
            income_annual=Metric(value=round_money(income.annual), available=income.available, reason=income.reason),
            income_breakdown=income.breakdown,
            expenses_monthly=Metric(value=round_money(expenses.monthly), available=expenses.available, reason=expenses.reason),
            expenses_annual=Metric(value=round_money(expenses.annual), available=expenses.available, reason=expenses.reason),
            essential_monthly_expenses=self._metric(expenses.essential_monthly),
            expense_breakdown=expenses.breakdown,
            investable_surplus_monthly=self._metric(surplus_m),
            investable_surplus_annual=self._metric(surplus_a),
            total_assets=self._metric(assets.total),
            liquid_assets=self._metric(assets.liquid_assets, assets.classification_available),
            financial_assets=self._metric(assets.financial_assets, assets.classification_available),
            asset_breakdown=assets.breakdown,
            asset_allocation=assets.allocation,
            liquidity_breakdown=assets.liquidity_breakdown,
            total_liabilities=self._metric(liabilities.total),
            liability_breakdown=liabilities.breakdown,
            liability_allocation=liabilities.allocation,
            emi_burden_monthly=Metric(value=liabilities.emi, available=liabilities.emi_available, reason=None if liabilities.emi_available else MISSING_INPUT),
            net_worth=self._metric(calculate_net_worth(assets.total, liabilities.total)),
            total_insurance_sum_assured=self._metric(insurance.total_sum_assured, insurance.available),
            total_insurance_annual_premium=self._metric(insurance.total_annual_premium, insurance.available),
            total_insurance_monthly_premium=self._metric(insurance.total_monthly_premium, insurance.available),
            total_insurance_current_value=self._metric(insurance.total_current_value, insurance.available),
            insurance_breakdown=insurance.breakdown,
        )

    @staticmethod
    def _metric(value, available=True):
        return Metric(value=value, available=available and value is not None, reason=None if available and value is not None else MISSING_INPUT)

    def _income(self, rows, scope, investor_id):
        selected = rows if scope == "family" else [r for r in rows if r.get("investor_id") == investor_id]
        monthly = annual = 0.0
        breakdown = defaultdict(float)
        available = bool(selected)
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
        monthly = 0.0; essential_monthly = 0.0; breakdown = defaultdict(float); available = bool(selected)
        for r in selected:
            m = monthly_amount(float(r.get("amount") or 0), str(r.get("frequency") or ""))
            if m is None:
                available = False; continue
            m *= factors.get(r.get("expense_id"), 1.0)
            monthly += m
            if is_essential_expense(r.get("expense_type")):
                essential_monthly += m
            breakdown[str(r.get("expense_type") or "Other")] += m
        return _ExpenseComponent(monthly, monthly * 12, essential_monthly, available, None if available else MISSING_INPUT,
                          [{"type": k, "monthly": round_money(v), "annual": round_money(v * 12)} for k, v in breakdown.items()])

    def _assets(self, rows, owners, classifications, scope, investor_id):
        owner_map = defaultdict(list)
        for row in owners: owner_map[row.get("asset_id")].append(row)
        lookup = {}
        for item in classifications:
            if item.get("is_active", True):
                for key in (item.get("name"), item.get("code")):
                    if key:
                        lookup[str(key).strip().lower()] = item
        breakdown=[]; total=0.0; liquid=0.0; financial=0.0; liquidity=defaultdict(float); classification_available=True
        for r in rows:
            value=float(r.get("current_value") or 0); owner_rows=owner_map.get(r.get("asset_id"), [])
            if not owner_rows: share=1.0
            elif scope == "family": share=sum(float(o.get("ownership_percentage") or 0) for o in owner_rows)/100
            else:
                matching=[o for o in owner_rows if o.get("investor_id")==investor_id]
                share=float(matching[0].get("ownership_percentage") or 100)/100 if matching else 0.0
            owned=value*share; total+=owned
            raw_type = str(r.get("asset_type") or r.get("asset_name") or "").strip()
            master = lookup.get(raw_type.lower())
            if master is None:
                classification_available = False
                liquidity["Unclassified"] += owned
            else:
                if master.get("is_liquid") is True: liquid += owned
                if master.get("is_financial") is True: financial += owned
                liquidity[str(master.get("name") or raw_type)] += owned
            breakdown.append({"asset_id":r.get("asset_id"),"name":r.get("asset_name"),"current_value":round_money(owned),"ownership_applied":round_money(share*100),"liquidity":None})
        allocation=[{"asset_id":x["asset_id"],"name":x["name"],"percentage":percentage(x["current_value"],total)} for x in breakdown] if total else []
        liquidity_breakdown=[{"classification":k,"value":round_money(v),"percentage":percentage(v,total)} for k,v in liquidity.items()]
        return _AssetComponent(total, liquid, financial, classification_available, breakdown, allocation, liquidity_breakdown)

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
        return _LiabilityComponent(total,breakdown,allocation,emi if emi_available else None,emi_available)

    def _insurance(self, rows, scope, investor_id):
        selected = rows or []
        if scope == "individual" and investor_id:
            selected = [r for r in selected if not r.get("investor_id") or r.get("investor_id") == investor_id]
        breakdown = []
        total_sa = 0.0
        total_m_prem = 0.0
        total_a_prem = 0.0
        total_cv = 0.0
        available = True

        for r in selected:
            sa = float(r.get("sum_assured") or 0)
            cv = float(r.get("current_value") or 0)
            raw_premium = float(r.get("premium") or 0)
            freq = str(r.get("premium_frequency") or "Monthly")

            m_prem = monthly_amount(raw_premium, freq)
            a_prem = annual_amount(raw_premium, freq)
            if m_prem is None:
                m_prem = round_money(raw_premium)
            if a_prem is None:
                a_prem = round_money(raw_premium * 12)

            total_sa += sa
            total_cv += cv
            total_m_prem += m_prem
            total_a_prem += a_prem

            breakdown.append({
                "policy_id": r.get("policy_id"),
                "policy_name": r.get("policy_name"),
                "insurer": r.get("insurer"),
                "policy_type": r.get("policy_type"),
                "premium": round_money(raw_premium),
                "premium_frequency": freq,
                "premium_monthly": round_money(m_prem),
                "premium_annual": round_money(a_prem),
                "sum_assured": round_money(sa),
                "current_value": round_money(cv),
                "maturity_date": r.get("maturity_date"),
                "maturity_value": round_money(float(r.get("maturity_value") or 0)) if r.get("maturity_value") else None,
            })

        return _InsuranceComponent(
            total_sum_assured=round_money(total_sa),
            total_monthly_premium=round_money(total_m_prem),
            total_annual_premium=round_money(total_a_prem),
            total_current_value=round_money(total_cv),
            available=available,
            breakdown=breakdown,
        )


class _Component:
    def __init__(self, monthly, annual, available, reason, breakdown): self.monthly=monthly; self.annual=annual; self.available=available; self.reason=reason; self.breakdown=breakdown
class _ExpenseComponent:
    def __init__(self, monthly, annual, essential_monthly, available, reason, breakdown): self.monthly=monthly; self.annual=annual; self.essential_monthly=essential_monthly; self.available=available; self.reason=reason; self.breakdown=breakdown
class _AssetComponent:
    def __init__(self,total,liquid_assets,financial_assets,classification_available,breakdown,allocation,liquidity_breakdown): self.total=total; self.liquid_assets=liquid_assets; self.financial_assets=financial_assets; self.classification_available=classification_available; self.available=True; self.breakdown=breakdown; self.allocation=allocation; self.liquidity_breakdown=liquidity_breakdown
class _LiabilityComponent:
    def __init__(self,total,breakdown,allocation,emi,emi_available): self.total=total; self.available=True; self.breakdown=breakdown; self.allocation=allocation; self.emi=emi; self.emi_available=emi_available
class _InsuranceComponent:
    def __init__(self, total_sum_assured, total_monthly_premium, total_annual_premium, total_current_value, available, breakdown):
        self.total_sum_assured = total_sum_assured
        self.total_monthly_premium = total_monthly_premium
        self.total_annual_premium = total_annual_premium
        self.total_current_value = total_current_value
        self.available = available
        self.breakdown = breakdown

