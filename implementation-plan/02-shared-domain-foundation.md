# Step 2 — Shared Domain Foundation: Canonical Rules & Calculations

## Step 2 का उद्देश्य

Step 1 में backend की foundation तैयार होने के बाद, इस चरण में पूरे सिस्टम में साझा होने वाले canonical business concepts, measurements, formulas और approved constraints को नए `app/domain/` layer में व्यवस्थित करना है। आगे के features इन्हीं shared definitions का उपयोग करेंगे; हर feature में अलग-अलग formula या rule implementation नहीं बनेगी।

यह चरण feature migration नहीं है। Investor Profile, Moneywheel, Goal Planner, Strategy Builder या किसी अन्य feature का पूरा logic इस चरण में migrate नहीं करना है।

## 1. इस implementation plan का specification status

इस plan में approved product specification, 05 और 06 के Step 2-संबंधित contracts, IDs, formulas, calculation methods, assumptions, constraints और decision effects सीधे शामिल हैं। Coding agent को इन विवरणों को लागू करने के लिए Notion access की आवश्यकता नहीं होनी चाहिए।

यह specification documentation-level contract है—यह existing code parity, runtime behavior, test coverage या हर दर्ज method की approval का प्रमाण नहीं है। हर item का status नीचे स्पष्ट किया गया है; unresolved/provisional items को अनुमान से approved या executable policy में न बदलें। approved product specification के Financial State facts, provenance, ownership/access, history और data-readiness contracts अपनी owning boundary में ही रहेंगे।

## 2. इस चरण का target area

केवल इस चरण से संबंधित domain areas पर काम करें:

```text
backend/app/domain/
├── canonical/
│   ├── goal_taxonomy.py
│   ├── financial_categories.py
│   └── measurements.py
└── shared/
    ├── calculations/
    ├── constraints/
    └── value_objects.py
```

यह target architecture का relevant हिस्सा है, complete directory tree नहीं। किसी file को तभी बनाएँ जब उसके लिए वास्तविक approved contract और उपयोग मौजूद हो। केवल खाली structure या अनुमानित abstractions न बनाएँ।

## 3. approved product specification से सीधे लेने वाली canonical definitions और tables

**Coding agent के लिए निर्देश:** नीचे की tables approved product specification से इस plan में उतारी गई हैं ताकि Notion access की जरूरत न हो। इन्हें canonical specification मानें। IDs/definitions को rename, extend या reinterpret न करें। approved product specification में runtime ID/enum parity और persisted-record compatibility unverified हैं। पहले पुराने code/database में actual values और usage inspect करें; mismatch को report करें, बिना approval silent migration न करें।

### 3.1 Goal taxonomy — `goal_taxonomy.py`

Exactly ये 10 goal types रखें:

| Canonical ID | Display name | Goal definition | Contextual details |
|---|---|---|---|
| `goal_retirement` | Retirement | Retirement के बाद financial needs और living expenses की planning | Retirement timing, post-retirement expenses और income needs |
| `goal_marriage` | Marriage | Marriage/wedding expenses की planning | किसके लिए, event date, cost details |
| `goal_vehicle` | Vehicle | Vehicle purchase funding | Vehicle type, new/used preference, purchase details |
| `goal_dream_home` | Dream Home | Home/residential property acquire करने की funding | Location, property details, purchase context |
| `goal_education` | Education | Investor या designated beneficiary के education expenses | Beneficiary और education details; Child Education अलग ID/type/alias नहीं |
| `goal_vacation` | Vacation | Holiday/leisure trip costs | Trip type, destination, frequency |
| `goal_debt_freedom` | Debt Freedom | Outstanding liabilities repay करके debt freedom | चुनी गई liability का reference |
| `goal_wealth_creation` | Wealth Creation | Assets/investment corpus से long-term wealth accumulation | Target corpus, horizon, funding details |
| `goal_fire_passive_income` | FIRE / Passive Income / Financial Freedom | Employment dependence घटाने/हटाने के लिए पर्याप्त assets/income बनाना | Target independence age, desired income, work-dependence preference |
| `goal_others` | Others | ऐसा personal financial goal जो अन्य approved type में fit न हो | Investor custom name/description; canonical type `goal_others` ही |

Goal priority, timing, amount, beneficiary, funding path, strategy और feasibility goal identity से अलग हैं। Priority investor की relative preference है; category से priority infer न करें और priority hard constraint override नहीं कर सकती। Custom goal label से नया canonical goal type न बनाएँ।

### 3.2 Financial categories — `financial_categories.py`

ये चार top-level planning groups हैं; यह accounting ledger, transaction register या complete Chart of Accounts नहीं है। Extra account IDs/subaccounts/accounting rules न बनाएँ।

#### Income

| Canonical ID | Category | Definition / classification guidance |
|---|---|---|
| `income_salary` | Salary | Employment compensation; employer/pay frequency; gross salary और take-home अलग |
| `income_business` | Business | Business operation income; revenue और profit अलग label |
| `income_professional_freelance` | Professional/Freelance | Independent professional/freelance fees; receipts और work-costs के बाद income अलग |
| `income_rental` | Rental | Property/asset rent; rent received और related costs के बाद income अलग |
| `income_interest` | Interest | Deposits/savings/debt instruments पर interest; underlying holding अलग asset |
| `income_dividend` | Dividend | Investment distributions; underlying investment अलग asset |
| `income_pension` | Pension | Pension receipts; expected और actually received अलग |
| `income_other` | Other | अन्यथा unclassified income; descriptive source दें, केवल fallback |

Income frequency: Monthly या Annual; period स्पष्ट होना चाहिए।

#### Expenses

| Canonical ID | Category | Definition / classification guidance |
|---|---|---|
| `expense_housing` | Housing | Rent, maintenance, society charges; same cost दो बार नहीं |
| `expense_food_groceries` | Food & Groceries | Household groceries/food; dining-out convention consistent रखें |
| `expense_utilities` | Utilities | Electricity, water, gas, phone, internet |
| `expense_transportation` | Transportation | Fuel, public transport, cab, commute, vehicle upkeep; holiday travel नहीं |
| `expense_education` | Education | Education spending; Education Loan balance से अलग |
| `expense_healthcare` | Healthcare | Treatment, medicines, appointments; insurance premium अलग |
| `expense_insurance` | Insurance | Policy premiums; claims expenses नहीं |
| `expense_debt_payments` | Debt Payments | Loan/liability cash payments; total payment एक बार, balance अलग; principal/interest split केवल ज्ञात हो तो |
| `expense_family_support` | Family Support | Family support खर्च/transfer; recipient, purpose, recurring/one-off |
| `expense_travel` | Travel | Trip/accommodation खर्च; routine commute Transportation है |
| `expense_entertainment` | Entertainment | Leisure/entertainment spending |
| `expense_shopping` | Shopping | Personal/household goods; specific category fit हो तो वही |
| `expense_other` | Other | अन्यथा unclassified spending; descriptive purpose, केवल fallback |

Expense frequency: Monthly या Annual; period स्पष्ट होना चाहिए। Savings/investments Expenses से अलग हैं। Full EMI एक ही बार expense है। Own-account transfers Income/Expenses नहीं। Credit-card purchase purchase month में expense है; bill settlement पर दोबारा नहीं। Refund original expense adjust करता है, नया income नहीं।

#### Assets

| Canonical ID | Category | Definition / classification guidance |
|---|---|---|
| `asset_bank_cash` | Bank / Cash | Cash/bank balances; account, ownership, balance date, restrictions; तुरंत accessible assume न करें |
| `asset_fixed_deposits` | Fixed Deposits | Fixed-term deposits; institution, maturity, terms, early access |
| `asset_mutual_funds` | Mutual Funds | Fund holdings; scheme, value/date; current value और invested cost अलग |
| `asset_stocks_equity` | Stocks / Equity | Direct shares; holding, quantity, market value/date; value और cost अलग |
| `asset_bonds_debt` | Bonds / Debt | Owned debt securities; issuer, instrument, maturity, value; investor का asset है |
| `asset_epf_ppf` | EPF / PPF | Scheme balances; account, date, withdrawal conditions |
| `asset_nps` | NPS | NPS holdings; account, date, withdrawal conditions |
| `asset_gold` | Gold | Physical/financial gold; form, quantity, purity, valuation date; immediate cash नहीं मानें |
| `asset_real_estate` | Real Estate | Owned property; type/location, ownership share, value/date; immediate liquidity assume न करें |
| `asset_business_ownership` | Business Ownership | Business ownership interest; share, valuation basis/date; revenue ownership value नहीं |
| `asset_vehicle` | Vehicle | Owned vehicle; type, ownership share, estimated value/date; related loan अलग |
| `asset_other` | Other | अन्यथा unclassified asset; type/value/date, केवल fallback |

Asset value के साथ relevant valuation/estimate date रखें।

#### Liabilities

| Canonical ID | Category | Definition / classification guidance |
|---|---|---|
| `liability_home_loan` | Home Loan | Home/property secured debt; borrower, balance, rate, payment; balance/EMI/property value अलग |
| `liability_car_loan` | Car Loan | Vehicle finance debt; borrower, balance, payment; vehicle value अलग |
| `liability_personal_loan` | Personal Loan | Personal borrowing; lender, borrower, balance, rate, repayment period |
| `liability_education_loan` | Education Loan | Education borrowing; beneficiary, lender, balance, terms; beneficiary अलग category नहीं |
| `liability_business_loan` | Business Loan | Business borrowing; liable party, purpose, balance, terms; evidence बिना personal liability न मानें |
| `liability_credit_card` | Credit Card | Card outstanding; account, statement period, amount, due date; balance/minimum due/statement/limit अलग |
| `liability_other` | Other | अन्यथा unclassified liability; type, borrower, balance/payment terms, केवल fallback |

Liability payment frequency जहाँ लागू हो Monthly, Quarterly या Annual हो सकती है। Outstanding balance और regular payment अलग रखें।

### 3.3 Insurance policy reference

ये approved product specification के policy inventory IDs हैं; insurance policy अपने-आप asset नहीं है।

| Canonical ID | Policy type | Capture fields / checks |
|---|---|---|
| `insurance_term_life` | Term Life | Insurer/reference, policyholder, life assured, nominee, dates, premium/frequency, paying term, sum assured, status; death benefit, riders, exclusions, employer/individual cover |
| `insurance_whole_life_endowment` | Whole Life / Endowment / Money-Back | Insurer/reference, policyholder, life assured, nominee, dates, premium/frequency, paying term, status; death/maturity benefits, guaranteed vs non-guaranteed, bonuses, surrender value, paid-up status, riders |
| `insurance_ulip` | ULIP | Insurer/reference, policyholder, life assured, nominee, start, premium, policy/paying term, status; sum assured, fund value/date, allocation, charges, lock-in, maturity, death benefit, switch restrictions |
| `insurance_health` | Health — Individual / Family Floater | Insurer/reference, proposer, insured members/DOB, policy period, premium, sum insured, status; floater/individual, room-rent, co-pay, waiting/pre-existing terms, sub-limits, restoration, NCB, network, exclusions |
| `insurance_critical_illness_accident_disability` | Critical Illness / Personal Accident / Disability | Insurer/reference, insured, period, premium, cover, status; covered events, benefit type, disability terms, exclusions, waiting/survival periods, riders |
| `insurance_motor` | Motor — Vehicle | Insurer/reference, policyholder, vehicle identity, period, premium, status; third-party/own-damage, IDV, add-ons, deductibles, NCB, exclusions |
| `insurance_home_property` | Home / Property | Insurer/reference, policyholder, property, period, premium, sum insured, status; building/contents, risks, valuation basis, deductibles, exclusions, lender interest |
| `insurance_travel` | Travel | Insurer/reference, travellers, destination, trip dates, premium, status; medical/emergency, evacuation, cancellation, baggage/delay, activity restrictions, exclusions |
| `insurance_other_business_liability` | Other / Business / Liability | Insurer/reference, insured entity, period, premium, limit, status; risk, covered parties/assets, indemnity, deductible, exclusions, claims-made/occurrence, endorsements |

हर policy में जहाँ लागू हो policyholder/proposer, insured person/asset, nominee, start/end/renewal dates, premium/frequency, cover/limit, status, riders, exclusions, claim/contact details और latest document source/date capture करें। Sensitive identifiers आवश्यकता पर ही रखें और protect करें। Premium `expense_insurance` है। Policy default से asset नहीं; cash/surrender/fund value हो तो अलग record करें।

### 3.4 approved product specification rules — implementation contract

| Rule | Coding agent को क्या करना है |
|---|---|
| Stable identity | Canonical IDs को display names, custom labels और contextual details से अलग रखें। |
| Goal priority | Priority को goal identity/feasibility/resource allocation से अलग रखें; category से priority infer न करें। |
| Category boundary | Category ID केवल financial information का प्रकार बताती है; liquidity, access, tax treatment, ratio eligibility, suitability या goal availability नहीं। |
| Data ownership | approved product specification catalogue financial facts/provenance नहीं रखता। Financial State, provenance, ownership/access, history और readiness approved product specification के हैं। |
| Formula ownership | Measurements/formulas approved product specification के हैं; category module में formulas duplicate न करें। |
| Constraint ownership | Constraints, thresholds और decision gates approved product specification के हैं; category definitions में decision logic न डालें। |
| Flows vs stocks | Income/expenses period flows; assets/liabilities as-of-date balances। बिना defined method combine न करें। |
| Amount basis | Gross/net income, business revenue/profit, debt balance/payment, asset value/cost अलग label करें। |
| No double-counting | Same amount दो बार नहीं; investment income/asset, insurance premium/policy value, debt balance/payment अलग। |
| Transfers | Own-account transfers external income/expense नहीं। Household transfer treatment owning chapter से लें; universal rule invent न करें। |
| Other fallback | `*_other` केवल तब जब कोई listed category fit न हो; descriptive context दें। |
| Units and dates | Income/expense period; asset/liability valuation/balance date। Missing material unit/currency/ownership/amount basis/date पर guess नहीं। |
| Governance | Taxonomy/category/ID/alias change के लिए explicit approval, impact review और backward-compatibility plan। |

### 3.5 approved product specification acceptance criteria

| Requirement | Acceptance criteria |
|---|---|
| C03-R01 Goal catalogue | Exactly 10 approved goal IDs; unapproved extra type नहीं |
| C03-R02 Stable identity | Display/custom label change से canonical ID नहीं बदलता |
| C03-R03 Priority separation | Priority change goal type नहीं बदलता, resources auto-allocate नहीं करता, hard constraint override नहीं करता |
| C03-R04 Category classification | Approved IDs से consistent classification; Other केवल fallback |
| C03-R05 No derived verdict from label | Category-only input liquidity, availability, tax, eligibility या suitability verdict नहीं देता |
| C03-R06 Flow/stock separation | Period flows और dated balances mix नहीं; gross/net और revenue/profit स्पष्ट |
| C03-R07 No double-counting | Debt balance/payment, investment/income, premium/policy value duplicate नहीं |
| C03-R08 Ownership boundaries | approved product specification facts; approved product specification formulas; approved product specification constraints; approved product specification goals/feasibility; approved product specification strategy |
| C03-R09 Missing data | Material detail missing हो तो clarification/limitation; fabricated values नहीं |
| C03-R10 Governed changes | Approval और compatibility/migration plan बिना taxonomy change नहीं |

**Verification status:** ये documentation-level contracts हैं। Runtime IDs/enums, aliases, persisted data और migration compatibility को tests और repository evidence के बिना verified न बताएं।

---

## 4. Canonical measurements और calculations — approved product specification

approved product specification canonical measurements, formulas, calculation methods, units, periods और assumptions का owner है। नीचे की specification उसी chapter के registers का Step 2 implementation extract है। Formula references संबंधित Measurement IDs हैं—अलग Formula IDs invent न करें।

### 4.1 Measurement Register — canonical IDs और contracts

| Group | Measurement ID | Measure | Inputs / basis | Unit / output | मुख्य limitation |
|---|---|---|---|---|---|
| Basic financial position | `metric_net_worth` | Net Worth | Total Assets; Total Liabilities; same valuation basis/date | Currency | Assets/liabilities की consistent valuation और valid inputs जरूरी |
| Monthly cash flow | `metric_monthly_surplus` | Available Monthly Surplus | Actual Net Monthly Income − Actual Monthly Expenses − Actual Monthly Savings and Investments; same calendar month | Currency/month | Negative result shortfall है; incomplete records पर Provisional; EMI और SIP exactly once |
| Monthly cash flow | `metric_savings_rate` | Savings Ratio | Actual Monthly Savings and Investments ÷ Actual Net Monthly Income | %; same calendar month | Net income positive होना चाहिए; own-account transfers exclude |
| Monthly cash flow | `metric_monthly_variance` | Monthly Spending Variance | Actual spending − budget limit; same category/month | Currency/month | Spending-budget variance only; missing data zero नहीं; zero budget valid |
| Financial health/debt | `metric_debt_to_income_ratio` | Debt-to-Income Ratio | Monthly Debt Payments; Gross Monthly Income | % | Payment burden है, liabilities/assets नहीं; gross income positive |
| Financial health/debt | `metric_leverage_ratio` | Leverage Ratio | Total Liabilities; Total Assets | % | Valid positive denominator / denominator validation |
| Asset composition | `metric_liquid_asset_ratio` | Liquid Asset Ratio | Liquid Assets; Total Assets | % | Approved eligibility mapping चाहिए; category/display label से liquidity infer नहीं |
| Asset composition | `metric_financial_asset_ratio` | Financial Asset Ratio | Financial Assets; Total Assets | % | Approved consistent financial-asset mapping चाहिए |
| Asset composition | `metric_portfolio_concentration` | Portfolio Concentration | Largest Single Asset Value; Total Asset Value | % | Total asset value > 0; percentage-scaled convention |
| Debt cost | `metric_weighted_debt_rate` | Weighted Debt Rate | Current outstanding principal and current comparable annual rate for each eligible debt; as-of date | % per year | Original sanctioned amount नहीं; missing rate पर Provisional, missing को 0% न मानें |
| Debt comparison | `metric_investment_debt_spread` | Investment–Debt Spread | Annualised overall portfolio return − Weighted Debt Rate | Percentage points | Same portfolio scope/date/method; portfolio return method approved न हो तो authoritative नहीं |
| Goal funding | `metric_future_goal_target` | Future Goal Target | Today's Goal Cost; applicable Inflation Rate; Duration in Years | Currency | Applicable approved inflation assumption और valid duration |
| Goal funding | `metric_projected_asset_value` | Projected Asset Value | Current Allocated Amount; periodic return; number of periods | Currency | Return/frequency/duration/allocation basis disclosed and approved |
| Goal funding | `metric_goal_funding_gap` | Goal Funding Gap | Future Goal Target; projected value of eligible funding assigned to goal | Currency | Accessibility, restrictions, timing, competing commitments और double-counting अलग से validate |
| Goal funding | `metric_goal_funding_ratio` | Goal Funding Ratio | Current eligible funding explicitly allocated to goal; current goal cost | % | Current/today's-cost basis; mapped asset automatically earmarked/available नहीं; standalone feasibility verdict नहीं |
| Goal funding | `metric_future_funding_ratio` | Future Funding Ratio | Projected Goal Funding; Future Goal Target | % | Approved return/period/duration/allocation assumptions; ratio confirmed feasibility नहीं |
| Goal funding | `metric_required_monthly_contribution` | Required Monthly Contribution / Required SIP | Remaining future-value gap after eligible existing funding projection; whole monthly periods; approved effective annual return | Currency/month | Standard contribution timing month-end; current funding twice subtract न करें; affordability अलग check |
| Goal affordability | `metric_monthly_sip_surplus_gap` | Monthly SIP / Surplus Gap | Additional Required SIP after existing goal-linked SIP; same-scenario Available Monthly Surplus | Currency/month | Gross SIP compare न करें अगर existing goal SIP accounted है |
| Goal affordability | `metric_required_surplus_increase` | Required Surplus Increase | Monthly SIP / Surplus Gap; Available Monthly Surplus | % | केवल positive surplus पर percentage; zero/negative पर amount दें, percentage N/A |
| Goal return | `metric_risk_required_return` | Risk Required Return — individual goal | Future Goal Target; Current Goal Funding; Duration in Years | % per year | Scenario-implied return, forecast/recommendation नहीं; portfolio required return से अलग; individual returns average न करें |

### 4.2 Formula Register — canonical calculation methods

| Measurement ID | Formula / calculation |
|---|---|
| `metric_net_worth` | Total Assets − Total Liabilities |
| `metric_monthly_surplus` | Actual Net Monthly Income − Actual Monthly Expenses − Actual Monthly Savings and Investments |
| `metric_savings_rate` | Actual Monthly Savings and Investments ÷ Actual Net Monthly Income × 100 |
| `metric_monthly_variance` | Actual Monthly Spending − Budgeted Monthly Spending Limit |
| `metric_debt_to_income_ratio` | Monthly Debt Payments ÷ Gross Monthly Income × 100 |
| `metric_leverage_ratio` | Total Liabilities ÷ Total Assets × 100 |
| `metric_liquid_asset_ratio` | Liquid Assets ÷ Total Assets × 100 |
| `metric_financial_asset_ratio` | Financial Assets ÷ Total Assets × 100 |
| `metric_portfolio_concentration` | Largest Single Asset Value ÷ Total Asset Value × 100 |
| `metric_weighted_debt_rate` | Σ(Current Outstanding Principalᵢ × Annual Interest Rateᵢ) ÷ Σ(Current Outstanding Principalᵢ), eligible positive-balance debt only |
| `metric_investment_debt_spread` | Annualised return from overall asset portfolio − Weighted Debt Rate |
| `metric_future_goal_target` | Today's Goal Cost × (1 + applicable Inflation Rate) ^ Duration in Years |
| `metric_projected_asset_value` | Current Allocated Amount × (1 + periodic return) ^ number of periods, only with approved inputs |
| `metric_goal_funding_gap` | Future Goal Target − Projected Value of eligible assets mapped to that goal |
| `metric_goal_funding_ratio` | Current Eligible Goal Funding ÷ Current Goal Cost × 100 |
| `metric_future_funding_ratio` | Projected Goal Funding ÷ Future Goal Target × 100 |
| `metric_required_monthly_contribution` | Future Goal Target minus projected future value of eligible existing funding = remaining future-value gap; solve constant month-end contribution using approved effective annual return and whole monthly periods. Do not subtract current funding twice. |
| `metric_monthly_sip_surplus_gap` | max(0, Additional Required SIP − Available Monthly Surplus), same scenario/period |
| `metric_required_surplus_increase` | If surplus > 0: Monthly SIP / Surplus Gap ÷ Available Monthly Surplus × 100; otherwise percentage unavailable/N/A and retain currency gap |
| `metric_risk_required_return` | Annualised return implied by current eligible goal funding, future goal target and time remaining; use approved input/period conventions; not a forecast |

### 4.3 Additional calculation methods and calculation rules

| Canonical ID | Type | Required method / rule |
|---|---|---|
| `method_portfolio_required_return` | Calculation method | Roll forward one portfolio balance through dated portfolio values, eligible goal withdrawals/dates, planned contributions/dates, commitments and horizon; solve one annualised return that funds all withdrawals and leaves the specified terminal residual/reserve. Never average individual-goal returns or assume zero terminal reserve. Missing dated inputs/reserve → unavailable/provisional; no solution → infeasible. |
| `method_required_lump_sum` | Calculation method | For one annual effective rate r and n years: max(0, (Future Goal Target − Future Value of eligible existing funding at goal date) ÷ (1+r)^n). For irregular dated cash flows use complete dated projection. Future target already includes inflation; do not inflate again. |
| `method_combined_lump_sum_monthly_contribution` | Calculation method | Project existing funding and lump sum to goal date, then add future value of month-end contributions. For constant month-end SIP: G=max(0,target−FV(existing funding)−FV(lump sum)); rm=(1+ra)^(1/12)−1; SIP=G×rm/((1+rm)^n−1), or G/n when rm=0. Reverse-solve lump sum for a supported affordable SIP. Multiple dated goal tranches require full dated cash-flow solver; do not collapse to one date. |
| `method_step_up_contribution` | Calculation method | Use explicit dated contribution schedule or explicit step-up rate/frequency and contribution dates. Future-value each dated contribution; solve starting contribution only where schedule is a fixed pattern. Never apply constant SIP formula to changing schedule. |
| `rule_portfolio_return_no_averaging` | Calculation rule | Portfolio-Level Return Required comes from portfolio dated cash flows; it is not average of individual-goal Risk Required Returns. |
| `rule_portfolio_asset_availability` | Calculation rule | Asset eligible for goal only when allocation, accessibility, restrictions, timing and competing commitments support that use. Portfolio inclusion alone is insufficient. |
| `rule_goal_target_basis` | Calculation rule | Identify today's cost vs future-date target. Inflate today's cost once; never re-inflate future-valued target. |
| `rule_surplus_measure_separation` | Calculation rule | Surplus deducts actual monthly expenses and actual monthly savings/investments from actual net monthly income; disclose annual/irregular planning adjustments separately and do not deduct twice. |
| `rule_no_double_counting` | Calculation rule | Count each asset, contribution, income and expense once; do not reuse resources across incompatible purposes. |
| `rule_result_validation` | Validation rule | Before use, confirm required inputs, assumptions and formula/question match; do not present calculation as forecast, recommendation or decision gate. |

### 4.4 Assumption Register — handling contract

- Goal-specific inflation is context-specific; use the applicable goal inflation input (approved product specification gives education inflation 10–12% only as an example where applicable, not a universal default).
- Expected return is determined from proposed investment mix and time horizon using an appropriate approved return basis; enter the scenario's actual rate and disclose its basis.
- Goal-funding return is specific to the funding scenario; document the basis and do not use an asset display label to infer return.
- Retirement return and longevity require an applicable supplied/approved rate and life-expectancy horizon; no universal default.
- Retirement unexpected-expense buffer must be specified by planner/investor as a currency amount or percentage; no hidden default.
- Contribution timing: use actual contribution dates when available; otherwise disclose the standard estimate date. Required Monthly Contribution's internal standard convention is month-end.
- Compounding: use product convention when known; otherwise disclose a consistent standard convention.
- Material assumptions must record source type, value, scope, as-of date, version and approval/review status.
- Sensitivity values are scenario inputs, not forecasts, guarantees or recommendations.

### 4.5 Calculation and validation safeguards

1. Identify inputs, scope, units, period, as-of date, timing convention and missing-data behavior before calculating; do not mix incompatible periods/bases.
2. Available Monthly Surplus uses actual net monthly income less actual monthly expenses less actual monthly savings/investments for the same calendar month. Include household expenses and full applicable EMI once; include ongoing SIPs once; exclude own-account transfers and irregular one-off receipts from recurring income. Credit-card purchases count in purchase month, not bill settlement; refunds adjust original expense. Missing required records → Provisional, not zero.
3. Weighted Debt Rate uses current positive outstanding principal, not original sanctioned amount. Active debt is legally outstanding and not fully repaid/settled/cancelled/closed, with principal > 0 on valuation date; overdue debt remains active. Include genuine contractual 0%; missing/non-comparable rate is not 0% and makes result Provisional. No eligible principal/valid denominator → Unavailable. Fees/penalties/prepayment charges separately disclosed.
4. Ratio scale must remain consistent across consumers. Example: if 40% is represented as 40, do not reinterpret as 0.40 or apply percentage conversion twice.
5. Asset/portfolio inclusion does not establish liquidity, accessibility, earmarking or goal eligibility. Use approved product specification evidence and applicable approved mapping.
6. Positive cash-flow surplus alone does not prove investable capacity; consider verified commitments, irregular costs, liquidity needs, constraints and competing goal claims.
7. Monthly Spending Variance is spending-budget variance only; positive=over budget, negative=under budget, zero=equal. Missing actual/budget is unavailable/provisional, never zero by assumption; no tolerance judgement is implied.
8. If a method, input contract or assumption is unresolved, do not display an authoritative confirmed result.

### 4.6 Ownership and downstream dependency

| Item | Owner | Consumer boundary |
|---|---|---|
| Goal/category identity | approved product specification | approved product specification consumes categories; does not redefine them |
| Financial records, provenance, ownership/access, restrictions, history/readiness | approved product specification | approved product specification uses evidence; does not replace Financial State |
| Measurements, formulas, assumptions, calculation methods | approved product specification | approved product specifications, 10, 11 and 12 consume canonical definitions without duplicates |
| Constraints, thresholds, decision effects | approved product specification | approved product specification provides measures; it does not invent thresholds |
| Cash-flow/affordability evidence | approved product specification | Uses approved product specification surplus/formulas while preserving source evidence |
| Goal target/funding/feasibility workflow | approved product specification | Applies Ch03 identity, Ch04 evidence, Ch05 calculations, Ch06 constraints |
| Strategy evaluation | approved product specification | Consumes canonical measures and constraints; no duplicate rule/formula |
| Scenario analysis | approved product specification | Scenario inputs are hypothetical and must not mutate actual state |
| Acceptance/action lifecycle | approved product specification | A calculation is not recommendation acceptance or transaction authorization |

## 5. Constraints और decision gates — approved product specification

approved product specification constraint policy और decision effects का owner है। यह formulas, cash-flow evidence, goal workflow या plan acceptance का owner नहीं है। नीचे documented rules हैं; runtime enforcement unverified है।

### 5.1 Canonical constraint register

| Rule ID / measure | Trigger and required evidence | Required decision effect | Threshold / status |
|---|---|---|---|
| `CTR-DTI-001` | Gross monthly income और recurring monthly debt-payment/EMI evidence; approved product specification DTI | Available Monthly Surplus assessment को inform करे; DTI अकेले goal, investment या strategy block नहीं करता | कोई threshold approved नहीं; runtime unverified |
| `CTR-LIQ-001` | Specific candidate goal/strategy/action asset पर निर्भर हो; approved product specification ownership, access, restrictions, timing, commitments और context evidence | Unavailable asset exclude करें और impact/uncertainty बताएं; ownership/portfolio inclusion availability नहीं; asset sell/earmark/reassign न करें | कोई numeric threshold या universal eligibility mapping approved नहीं |
| `CTR-HIR-001` | Individual outstanding loan/liability rate strictly >14% p.a. और investment consideration चल रही हो; liability, rate, balance/status, terms, payoff quote, fees, cash-flow effect, funding source, expected return और strategy estimated return | Repayment interest saved, prepayment costs, alternative expected return और strategy return का comparable trade-off assessment + disclosure अनिवार्य; investor अंतिम निर्णय लेता है; investment/Goal Planner/Strategy Builder auto-block नहीं | Exactly 14% trigger नहीं; >14% threshold approved; runtime enforcement unverified |
| `metric_liquid_asset_ratio` | approved product specification measure; approved asset eligibility mapping और approved product specification access evidence | केवल relevant assessment को inform करे; ratio अकेले warning/pass-fail/infeasibility नहीं | कोई threshold नहीं; यह measure है, approved product specification rule ID नहीं |
| Individual-goal Required Return | Goal amount/date, funding path, eligible funding और approved approved product specification formula/assumptions | Affordability के साथ scenario assessment; forecast/guarantee या automatic block नहीं | कोई threshold नहीं; 15% approved hard limit/warning नहीं |
| `CTR-AFF-001` | Candidate contribution/lump sum; Ch05 Required SIP/amount and surplus; Ch08 cash-flow evidence; Ch04 asset/access evidence; irregular costs, liquidity, competing goals | Additional Required SIP (existing goal SIP के बाद) ≤ same-period Available Monthly Surplus होने पर SIP comparison pass. Gap हो तो canonical monthly shortfall दिखाएं; इससे goal impossible सिद्ध नहीं होता. Step-up हर scheduled period पर जाँचे. Lump sum केवल accessible, eligible, timely, uncommitted asset. Combined path एक dated projection में; double count नहीं. Multi-goal conflicts surface करें, auto-allocate नहीं | कोई universal buffer, surplus % या numeric threshold approved नहीं; runtime unverified |
| `CTR-RATIO-001` | Ratio measurement/calculation/rule/consumer के बीच pass हो | Owning measurement का unit और numeric scale जस का तस रखें; double percentage conversion रोकें | कोई threshold/standalone pass-fail नहीं; runtime unverified |
| `CTR-INS-001` | Insurance Coverage Ratio/required-cover evaluation; existing sum assured, approved required-cover method/inputs, reliable policy data | Method, scope और policy approved/validated न हों तो adequacy/decision infer न करें; Excellent/Healthy/Attention/Critical bands या automatic recommendation नहीं | Coverage bands/threshold approved नहीं; policy open; runtime unverified |
| `CTR-GATE-001` | Explicitly approved hard constraint अपने defined scope में apply हो | केवल उसी rule का explicitly approved effect लागू; warning/disclosure/restriction में से कोई भी केवल rule-specific approval से. Record rule/version, trigger, evidence, explanation, investor decision and reassessment trigger where applicable | “Hard constraint” शब्द अपने-आप blocking effect authorize नहीं करता; Foundation 00.2 wording reconciliation open; runtime unverified |

### 5.2 Approved threshold register

| Rule | Exact boundary | Effect |
|---|---|---|
| `CTR-HIR-001` | Individual liability interest rate strictly greater than 14% p.a.; exactly 14% excluded | Mandatory trade-off assessment/disclosure; automatic investment block नहीं |
| `CTR-DTI-001` | None | Informational only; no automatic pass/fail/block |
| `metric_liquid_asset_ratio` | None | No ratio-only warning, pass/fail or block |
| Individual-goal Required Return | None; 15% threshold नहीं | Non-hard assessment only |
| `CTR-AFF-001` | No universal buffer or surplus percentage | Compare candidate path to period-matched surplus/eligible resources; show gaps |
| `CTR-INS-001` | No approved coverage bands | No adequacy labels or automatic gate |

Illustrative case values या दूसरे scope की policy से threshold copy न करें। नया threshold तभी जोड़ा जा सकता है जब owner, unit, exact boundary, evidence, effect, approval status और consumers documented हों।

### 5.3 Funding-path application contract for approved product specification

1. SIP/step-up SIP: हर scheduled period का additional Required SIP, उसी period के Available Monthly Surplus से compare करें; Ch08 evidence उपयोग करें।
2. Lump sum: `CTR-LIQ-001` के तहत asset-specific availability verify करें; unavailable/committed resources exclude कर funding gap बताएं।
3. Combined lump sum + SIP: एक consistent dated projection में दोनों को assess करें; liquidity और surplus checks दोनों लागू हों; double counting रोकें।
4. Multiple goals: same asset या surplus पर competing claims detect करके affected goals/consequences दिखाएं; priority या allocation स्वतः न चुनें। Allocation algorithm और priority persistence unresolved हैं।
5. Required Return: केवल approved approved product specification method/inputs; non-hard assessment, forecast या gate नहीं।
6. Missing/unresolved method/evidence: affected test undetermined / insufficient evidence; missing evidence से goal infeasible घोषित न करें।
7. एक comparison pass होने से goal automatically feasible, recommendation, Accepted Plan या transaction नहीं बनता।

### 5.4 Cross-chapter ownership

| Domain | Owner | approved product specification boundary |
|---|---|---|
| Financial facts, ownership/access, restrictions, liability evidence | approved product specification | Evidence consume करता है; source data redefine नहीं |
| Measures, formulas, return assumptions, contribution/lump-sum methods | approved product specification | Canonical outputs consume; formula recreate नहीं |
| Investor context/priorities | approved product specification | Investor decision rights preserve; automatic priority choice नहीं |
| Available Monthly Surplus | approved product specification; source cash flow approved product specification | Affordability effect apply; source evidence approved product specification से |
| Protection/insurance interpretation | approved product specification and approved calculation owner | केवल documented boundary; unapproved labels/gates नहीं |
| SIP/step-up/lump sum/combined/multi-goal feasibility | approved product specification | Constraint effects देता है; workflow/outcome approved product specification का |
| Strategy evaluation | approved product specification | Applicable constraints consume; duplicate rules/thresholds नहीं |
| What-If/scenario comparison | approved product specification | Relevant candidate scenarios पर apply; actual state mutate नहीं |
| Accepted Plan / Action Plan | approved product specification | Plan accept या transaction authorize नहीं |

### 5.5 approved product specification governance and unresolved items

- Rule IDs exactly preserve करें: `CTR-DTI-001`, `CTR-LIQ-001`, `CTR-HIR-001`, `CTR-AFF-001`, `CTR-RATIO-001`, `CTR-INS-001`, `CTR-GATE-001`. `metric_liquid_asset_ratio` approved product specification measurement ID है, constraint ID नहीं।
- Documented, proposed, approved और implementation-verified statuses अलग रखें; documentation alone runtime verification नहीं।
- Insurance coverage method/policy और asset-eligibility mapping अपने canonical owners से approved न हों तो unresolved रखें।
- Multi-goal allocation algorithm और priority persistence unresolved; automatic allocation नहीं।
- `CTR-GATE-001` की product-wide wording Foundation 00.2 से reconcile होनी बाकी है; इस plan में conflict silently resolve न करें।
- Rule change canonical owner में पहले करें, फिर downstream references/tests review करें।

## 6. Financial State और evidence boundary — approved product specification

approved product specification Financial State facts, provenance, ownership/access, history और data readiness का owner है। Step 2 में इसका अर्थ केवल इतना है:

- approved product specification calculations को approved product specification के defined inputs/evidence/readiness contracts के अनुसार consume करना चाहिए।
- Canonical measurement या category definition को investor की stored financial fact, its provenance या readiness record का replacement न बनाएँ।
- Missing या incomplete evidence को fabricated zero/default से replace न करें।
- Financial State की पूरी feature implementation या persistence migration इस चरण में न करें; वह संबंधित अगले चरणों में आएगी।

## 7. Existing backend से migration का तरीका

पुराने backend में calculations, rules, categories और IDs जहाँ भी मौजूद हों, उन्हें पहले inspect करें। केवल folder या filename देखकर ownership तय न करें।

हर relevant existing implementation के लिए दर्ज करें:

- वास्तविक file path और public function/constant/ID;
- callers और dependent features;
- inputs, outputs, units और periods;
- संबंधित approved product specification/05/06 contract;
- current behavior और source contract के बीच अंतर;
- उपलब्ध tests और missing regression coverage;
- migration का प्रस्तावित canonical/shared owner।

फिर केवल उन्हीं shared definitions/calculations को migrate करें जिनका owner और behavior source documents से स्पष्ट है। Ambiguous code को जबरन move न करें; उसे open item के रूप में दर्ज करें।

## 8. Dependency और code boundaries

- Domain code में FastAPI, HTTP request/response schemas, Supabase SDK, database clients या infrastructure repositories import न हों।
- Shared calculations pure domain behavior रहें; database access या I/O उनमें न जोड़ें।
- API schemas, ORM models और database rows को canonical domain types न मानें।
- Feature-specific business behavior को shared calculation/rule layer में केवल इसलिए न डालें कि वह दो जगह उपयोग होता दिख रहा है; ownership source chapter से तय होगी।
- एक ही canonical formula या constraint की parallel implementations न रखें।
- नया abstraction तभी बनाएँ जब मौजूदा approved contracts और वास्तविक use उसे आवश्यक बनाते हों।

## 9. Tests और verification

- Existing tests चलाकर baseline दर्ज करें।
- Canonical IDs/categories/taxonomy के लिए source-aligned tests जोड़ें।
- प्रत्येक migrated calculation के लिए approved product specification के approved examples/expected values पर unit tests लिखें; fixtures synthetic हों।
- Units, periods, denominator validation, missing inputs, provisional/unavailable outcomes और double-counting safeguards को संबंधित source rules के अनुसार test करें।
- Constraints के लिए applicability, threshold और decision-effect tests केवल वहीं लिखें जहाँ approved product specification में rule defined है।
- Regression tests से migrated code के पुराने behavior और approved contract का अंतर स्पष्ट करें।
- Unapproved examples या provisional values को test fixtures में authoritative policy न बनाएँ।

## 10. इस चरण में क्या नहीं करना है

- किसी feature का पूरा migration या नया feature implementation नहीं।
- Investor Profile / Financial State की पूरी feature या database persistence migration नहीं।
- Database schema, tables, columns या RLS policies में बदलाव नहीं।
- API endpoints या Frontend में बदलाव नहीं।
- approved product specification/05/06 के unresolved decisions को अनुमान से बंद नहीं करना।
- approved product specification formulas या approved product specification constraints की duplicate feature-level copies नहीं बनानी।
- approved product specification Goal Planner और approved product specification Strategy Builder की ownership boundaries नहीं बदलनी।
- Multi-Goal Planning या किसी unapproved workflow का logic नहीं बनाना।

## 11. Step 2 acceptance checklist

- [ ] approved product specification, 04, 05 और 06 के relevant contracts इस plan में embedded हैं और implementation के लिए स्पष्ट हैं।
- [ ] Existing canonical IDs, categories, measurements, formulas और constraints का code inventory तैयार है।
- [ ] Confirmed canonical vocabulary सही target domain area में रखी गई है।
- [ ] केवल source-defined और sufficiently specified calculations migrate की गई हैं।
- [ ] Shared constraints केवल approved product specification के defined rules के अनुसार रखे गए हैं।
- [ ] Domain imports और dependency boundaries verify किए गए हैं।
- [ ] Unit और regression tests चलाए गए; results दर्ज हैं।
- [ ] Unresolved/provisional items और runtime parity gaps स्पष्ट रूप से दर्ज हैं।
- [ ] इस चरण में कोई feature migration, database schema change या frontend change नहीं हुआ।

## 12. Coding Agent की अंतिम रिपोर्ट

1. बनाए/बदले गए files की exact list।
2. हर migrated definition/calculation/constraint का canonical source chapter और section।
3. पुराने implementation से किए गए mappings और छोड़े गए ambiguous items।
4. चलाए गए tests और उनके वास्तविक results।
5. Unresolved decisions, parity gaps और अगले चरण से पहले जरूरी blockers।
6. पुष्टि कि feature logic, database schema और frontend में कोई बदलाव नहीं किया गया।
