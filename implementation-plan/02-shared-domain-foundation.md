# Step 2 — Shared Domain Foundation: Canonical Rules & Calculations

## Step 2 का उद्देश्य

Step 1 में backend की foundation तैयार होने के बाद, इस चरण में पूरे सिस्टम में साझा होने वाले canonical business concepts, measurements, formulas और approved constraints को नए `app/domain/` layer में व्यवस्थित करना है। आगे के features इन्हीं shared definitions का उपयोग करेंगे; हर feature में अलग-अलग formula या rule implementation नहीं बनेगी।

यह चरण feature migration नहीं है। Investor Profile, Moneywheel, Goal Planner, Strategy Builder या किसी अन्य feature का पूरा logic इस चरण में migrate नहीं करना है।

## 1. Authoritative references

काम शुरू करने से पहले इन स्रोतों को पढ़ें और इनके recorded status/open decisions का पालन करें:

- [Backend Folder Structure — Target Architecture](https://app.notion.com/p/40f57e71b7b88194a6cdeee083a2568c)
- [Backend Redesign — Migration Plan](https://app.notion.com/p/41057e71b7b881139bc2eb448ff838bb)
- [Chapter 03 — Canonical Identity, Categories & Goal Taxonomy](https://app.notion.com/p/3fc57e71b7b8817783aaeb3abbb4d9bf)
- [Chapter 05 — Canonical Measurements, Formulas & Assumptions](https://app.notion.com/p/3fc57e71b7b8818baa08d87180038633)
- [Chapter 06 — Constraints, Thresholds & Decision Gates](https://app.notion.com/p/3fc57e71b7b881ccb7e4d84d6ba02c20)
- [Chapter 04 — Financial State & Data Readiness](https://app.notion.com/p/3fc57e71b7b88123b516f3e745dc38b7)

इन chapters में दर्ज content को runtime implementation का प्रमाण न मानें। जहाँ status, approval या method unresolved है, उसे unresolved ही रखें।

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

## 3. Chapter 03 से सीधे लेने वाली canonical definitions और tables

**Coding agent के लिए निर्देश:** नीचे की tables Chapter 03 से इस plan में उतारी गई हैं ताकि Notion access की जरूरत न हो। इन्हें canonical specification मानें। IDs/definitions को rename, extend या reinterpret न करें। Chapter 03 में runtime ID/enum parity और persisted-record compatibility unverified हैं। पहले पुराने code/database में actual values और usage inspect करें; mismatch को report करें, बिना approval silent migration न करें।

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

ये Chapter 03 के policy inventory IDs हैं; insurance policy अपने-आप asset नहीं है।

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

### 3.4 Chapter 03 rules — implementation contract

| Rule | Coding agent को क्या करना है |
|---|---|
| Stable identity | Canonical IDs को display names, custom labels और contextual details से अलग रखें। |
| Goal priority | Priority को goal identity/feasibility/resource allocation से अलग रखें; category से priority infer न करें। |
| Category boundary | Category ID केवल financial information का प्रकार बताती है; liquidity, access, tax treatment, ratio eligibility, suitability या goal availability नहीं। |
| Data ownership | Chapter 03 catalogue financial facts/provenance नहीं रखता। Financial State, provenance, ownership/access, history और readiness Chapter 04 के हैं। |
| Formula ownership | Measurements/formulas Chapter 05 के हैं; category module में formulas duplicate न करें। |
| Constraint ownership | Constraints, thresholds और decision gates Chapter 06 के हैं; category definitions में decision logic न डालें। |
| Flows vs stocks | Income/expenses period flows; assets/liabilities as-of-date balances। बिना defined method combine न करें। |
| Amount basis | Gross/net income, business revenue/profit, debt balance/payment, asset value/cost अलग label करें। |
| No double-counting | Same amount दो बार नहीं; investment income/asset, insurance premium/policy value, debt balance/payment अलग। |
| Transfers | Own-account transfers external income/expense नहीं। Household transfer treatment owning chapter से लें; universal rule invent न करें। |
| Other fallback | `*_other` केवल तब जब कोई listed category fit न हो; descriptive context दें। |
| Units and dates | Income/expense period; asset/liability valuation/balance date। Missing material unit/currency/ownership/amount basis/date पर guess नहीं। |
| Governance | Taxonomy/category/ID/alias change के लिए explicit approval, impact review और backward-compatibility plan। |

### 3.5 Chapter 03 acceptance criteria

| Requirement | Acceptance criteria |
|---|---|
| C03-R01 Goal catalogue | Exactly 10 approved goal IDs; unapproved extra type नहीं |
| C03-R02 Stable identity | Display/custom label change से canonical ID नहीं बदलता |
| C03-R03 Priority separation | Priority change goal type नहीं बदलता, resources auto-allocate नहीं करता, hard constraint override नहीं करता |
| C03-R04 Category classification | Approved IDs से consistent classification; Other केवल fallback |
| C03-R05 No derived verdict from label | Category-only input liquidity, availability, tax, eligibility या suitability verdict नहीं देता |
| C03-R06 Flow/stock separation | Period flows और dated balances mix नहीं; gross/net और revenue/profit स्पष्ट |
| C03-R07 No double-counting | Debt balance/payment, investment/income, premium/policy value duplicate नहीं |
| C03-R08 Ownership boundaries | Chapter 04 facts; Chapter 05 formulas; Chapter 06 constraints; Chapter 10 goals/feasibility; Chapter 11 strategy |
| C03-R09 Missing data | Material detail missing हो तो clarification/limitation; fabricated values नहीं |
| C03-R10 Governed changes | Approval और compatibility/migration plan बिना taxonomy change नहीं |

**Verification status:** ये documentation-level contracts हैं। Runtime IDs/enums, aliases, persisted data और migration compatibility को tests और repository evidence के बिना verified न बताएं।

---

## 4. Canonical measurements और calculations — Chapter 05

Chapter 05 measurements, formulas, calculation methods, units, periods और assumptions का canonical owner है।

इस चरण में:

1. Chapter 05 के Measurement Register, Formula Register, Assumption Register, Calculation Rules Register और Validation Rules Register को implementation reference की तरह उपयोग करें।
2. Formula references को उनके canonical Measurement IDs से जोड़ें; अपनी तरफ से competing Formula IDs या duplicate definitions न बनाएँ।
3. Calculation code को measurement families के अनुसार `domain/shared/calculations/` में व्यवस्थित करें।
4. हर measurement के inputs, output, unit, period, as-of basis, assumptions, limitations और missing-data behavior को source contract से मिलाएँ।
5. Chapter 05 में unresolved या provisional methods को approved formula/default में convert न करें।
6. Existing implementation को source chapters से compare करें; parity verified होने का दावा केवल tests/evidence के आधार पर करें।

एक measurement के लिए अलग-अलग tiny files न बनाएँ। Architecture blueprint के अनुसार calculations को measurement families के आधार पर group करें; grouping का नाम और सीमा source contract तथा वास्तविक code inspection से तय करें।

## 5. Constraints और decision gates — Chapter 06

Chapter 06 constraints, thresholds, applicability और decision effects का authoritative owner है।

- Approved constraint definitions को `domain/shared/constraints/` में रखें।
- Constraint identity, applicability conditions, required evidence, threshold, effect और missing-evidence behavior को Chapter 06 से traceable रखें।
- Chapter 06 में जो threshold, rule या applicability unresolved है, उसे code में अनुमान से तय न करें।
- Feature-specific decisions को shared constraint catalogue में तभी रखें जब Chapter 06 उनका shared owner हो।
- किसी constraint को formula या category definition के भीतर duplicate न करें।

## 6. Financial State और evidence boundary — Chapter 04

Chapter 04 Financial State facts, provenance, ownership/access, history और data readiness का owner है। Step 2 में इसका अर्थ केवल इतना है:

- Chapter 05 calculations को Chapter 04 के defined inputs/evidence/readiness contracts के अनुसार consume करना चाहिए।
- Canonical measurement या category definition को investor की stored financial fact, its provenance या readiness record का replacement न बनाएँ।
- Missing या incomplete evidence को fabricated zero/default से replace न करें।
- Financial State की पूरी feature implementation या persistence migration इस चरण में न करें; वह संबंधित अगले चरणों में आएगी।

## 7. Existing backend से migration का तरीका

पुराने backend में calculations, rules, categories और IDs जहाँ भी मौजूद हों, उन्हें पहले inspect करें। केवल folder या filename देखकर ownership तय न करें।

हर relevant existing implementation के लिए दर्ज करें:

- वास्तविक file path और public function/constant/ID;
- callers और dependent features;
- inputs, outputs, units और periods;
- संबंधित Chapter 03/05/06 contract;
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
- प्रत्येक migrated calculation के लिए Chapter 05 के approved examples/expected values पर unit tests लिखें; fixtures synthetic हों।
- Units, periods, denominator validation, missing inputs, provisional/unavailable outcomes और double-counting safeguards को संबंधित source rules के अनुसार test करें।
- Constraints के लिए applicability, threshold और decision-effect tests केवल वहीं लिखें जहाँ Chapter 06 में rule defined है।
- Regression tests से migrated code के पुराने behavior और approved contract का अंतर स्पष्ट करें।
- Unapproved examples या provisional values को test fixtures में authoritative policy न बनाएँ।

## 10. इस चरण में क्या नहीं करना है

- किसी feature का पूरा migration या नया feature implementation नहीं।
- Investor Profile / Financial State की पूरी feature या database persistence migration नहीं।
- Database schema, tables, columns या RLS policies में बदलाव नहीं।
- API endpoints या Frontend में बदलाव नहीं।
- Chapter 03/05/06 के unresolved decisions को अनुमान से बंद नहीं करना।
- Chapter 05 formulas या Chapter 06 constraints की duplicate feature-level copies नहीं बनानी।
- Chapter 10 Goal Planner और Chapter 11 Strategy Builder की ownership boundaries नहीं बदलनी।
- Multi-Goal Planning या किसी unapproved workflow का logic नहीं बनाना।

## 11. Step 2 acceptance checklist

- [ ] Chapter 03, 04, 05 और 06 के relevant contracts पढ़े और source references दर्ज किए गए।
- [ ] Existing canonical IDs, categories, measurements, formulas और constraints का code inventory तैयार है।
- [ ] Confirmed canonical vocabulary सही target domain area में रखी गई है।
- [ ] केवल source-defined और sufficiently specified calculations migrate की गई हैं।
- [ ] Shared constraints केवल Chapter 06 के defined rules के अनुसार रखे गए हैं।
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
