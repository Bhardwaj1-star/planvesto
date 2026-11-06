# Step 3 — Investor Profile Feature Transfer

## Mandatory clarification gate — no assumptions or invented implementation

- इस implementation plan और इससे जुड़े किसी भी project document में external source chapter numbers/names या chapter-based navigation references नहीं रखे जाएँगे। आवश्यक product rules, definitions, formulas, data contracts और constraints यहीं सीधे लिखे जाएँगे।
- इस दस्तावेज़ में कोई field, schema, API, enum, threshold, formula, scoring model, workflow, default, validation, permission या business rule स्पष्ट रूप से निर्धारित नहीं है, तो AI agent उसे स्वयं से नहीं बनाएगा।
- ऐसी हर कमी या अस्पष्टता को **Open Question / Decision Required** के रूप में दर्ज करें। Implementation रोकें और आगे बढ़ने से पहले product owner से स्पष्ट उत्तर लें।
- केवल स्पष्ट रूप से स्वीकृत और इस दस्तावेज़ में दर्ज व्यवहार ही implement करें। उदाहरण, अनुमान, पुराने code का व्यवहार या architecture tree अपने-आप में approval नहीं हैं।
- कोई विरोधाभास मिले तो चुपचाप चुनाव न करें; दोनों statements दिखाकर clarification माँगें। मौजूदा frontend/API compatibility और पुराने backend behavior को बिना प्रमाण बदलें नहीं।
- जहाँ जानकारी उपलब्ध नहीं है, वहाँ साफ़ लिखें **Not specified — clarification required**; placeholder के नाम पर invented behavior न जोड़ें।


## Step 3 का उद्देश्य

Step 1 में backend foundation और Step 2 में shared canonical domain rules/calculations की तैयारी के बाद, पहला product feature **Investor Profile** नए modular-monolith architecture में लाना है। यह feature आगे Moneywheel, Goal Planner और बाकी planning features को investor context तथा validated financial inputs उपलब्ध कराएगा।

यह feature implementation step है — केवल code audit या feature-list बनाने का चरण नहीं। फिर भी migration feature-by-feature होगी: पुराने backend का मौजूदा व्यवहार पहले समझें, फिर उसी व्यवहार और approved contracts को नए layers में transfer करें। पुराने backend branch को न बदलें।

## 1. Feature boundary — Investor Profile

Investor Profile एक top-level product feature है। इसके चार अलग components हैं:

1. **Financial State** — investor/household की वास्तविक financial facts और numeric records, dated financial baseline, evidence/provenance, data readiness और data-quality limitations।
2. **Risk Profile** — risk profile से संबंधित जानकारी और outcomes। जहाँ assess किया गया हो, risk capacity, risk tolerance और risk willingness को अलग-अलग रखें।
3. **Behavioural Profile** — relevant behavioural traits, observed या investor-stated decision patterns और downstream planning के लिए behavioural context।
4. **Investor Preferences & Needs** — investor द्वारा बताई गई preferences, priorities, objectives और planning needs।

ये चार components Investor Profile के हिस्से हैं; इन्हें चार अलग top-level product features, अलग deployable services या एक ही financial record में न बदलें।

## 2. Ownership और data separation

- Financial State में केवल वास्तविक financial facts/records रखें; derived measurements, hypothetical scenario values और accepted decisions को actual financial facts के रूप में न लिखें।
- Risk Profile, Behavioural Profile और Investor Preferences & Needs को Financial State के numeric records में merge न करें।
- Investor-reported, documented, independently verified, estimated, assumed, hypothetical, missing और conflicting information के बीच distinction बनाए रखें जहाँ source contract उपलब्ध हो।
- Ownership, household relationship, ownership share, access/control, restrictions, provenance, record dates और version/traceability को preserve करें।
- किसी asset का portfolio/Financial State में होना अपने-आप उसे available, liquid या किसी goal के लिए eligible सिद्ध नहीं करता।
- Missing या conflicting facts को अनुमान से भरकर definitive assessment न दें। Data-readiness/clarification outcome स्पष्ट रखें।
- approved product specification की canonical IDs/categories और Step 2 में embedded approved product specification/06 contracts को reuse करें; feature के भीतर duplicate IDs, formulas या thresholds न बनाएँ।

## 3. Decision-specific assessment contract

Investor Profile से जुड़े assessment में:

- पहले investor का प्रश्न/निर्णय, timing, relevant people/household, goals और decision scope समझें।
- केवल वही अतिरिक्त context collect करें जो निर्णय को materially बदल सकता है।
- Confirmed facts, reported facts, estimates, assumptions और hypothetical events को अलग दिखाएँ।
- हर material input के लिए evidence status, relevance, limitations और sufficiency पर विचार करें।
- Missing, stale, invalid या conflicting information का प्रभाव बताएं और आवश्यक clarification/evidence की जरूरत surface करें।
- Shared resources/liabilities के लिए ownership, practical access/control, payment responsibility, consent, existing commitments और uncertainty को अलग-अलग जाँचें।
- Ownership या portfolio inclusion को availability का प्रमाण न मानें। Asset availability/constraints के लिए approved product specification और संबंधित Financial State evidence लागू होगा।
- Investor की preference को acceptance न मानें; reported preference, recommendation और explicit investor decision अलग अवस्थाएँ हैं।
- Investor priorities या competing goals का फैसला Investor Profile स्वयं न करे। Conflicts को surface करे; allocation/priority decision संबंधित owning feature और investor decision boundary में रहेगा।

## 4. Layer responsibilities और target locations

Approved target structure के अनुसार feature को layers में बाँटें। वास्तविक code तभी बनाएँ जब संबंधित responsibility और existing behavior inspect हो चुका हो।

```text
backend/app/
├── api/
│   ├── routers/investor_profile/
│   └── schemas/
├── application/
│   ├── features/investor_profile/
│   ├── workflows/investor_situation_assessment/
│   └── ports/repositories/
├── domain/
│   └── features/investor_profile/
├── infrastructure/
│   └── persistence/
│       ├── mappers/
│       └── repositories/
└── security/
```

- **API:** Investor Profile endpoints और typed request/response schemas; financial calculations या direct database queries नहीं।
- **Application:** use-case orchestration, decision-specific assessment flow और repository ports के जरिए persistence interaction।
- **Domain:** Investor Profile के business concepts, evidence/readiness interpretation और component-specific rules; FastAPI, Supabase SDK या database client imports नहीं।
- **Infrastructure:** existing database/Supabase persistence को repository ports के पीछे implement करना; financial business rules यहाँ नहीं।
- **Security:** authenticated investor identity और record-level ownership/access enforcement को shared security boundary से लागू करना।

File names, table names, columns या नए schema fields अनुमान से न बनाएँ। पहले existing backend, database usage और approved data architecture से वास्तविक contract verify करें।

## 5. Existing backend transfer procedure

हर component के लिए:

1. पुराने backend में संबंधित routes, schemas, models, services, repositories, queries, validation, access checks और tests खोजें।
2. वास्तविक request/response contract, persisted fields, ownership rules और frontend dependencies दर्ज करें। Frontend केवल read-only compatibility reference रहेगा।
3. पुराने behavior को approved Investor Profile boundary और नए layers से map करें।
4. पुराने behavior और approved specification में mismatch, missing behavior या unresolved policy मिले तो उसे अलग दर्ज करें; चुपचाप बदलें नहीं।
5. एक component/use-case को नए layers में migrate करें; duplicate business logic न छोड़ें।
6. Unit, integration, contract, security और regression tests चलाएँ; जहाँ उपलब्ध हों, पुराने परिणामों से parity जाँचें।
7. API contract की मौजूदा frontend expectations के साथ compatibility जाँचें। इस step में frontend files न बदलें।
8. Evidence के साथ migration status दर्ज करें; सफल test के बिना पुराने endpoint/path को बंद न करें।

## 6. Cross-feature hand-offs

- **Moneywheel** को validated Financial State inputs मिलेंगे; canonical measurements और ratios Step 2 के approved product specification definitions से calculate होंगे। Investor Profile Moneywheel की calculations या health assessment own नहीं करता।
- **Goal Planner** को goal-relevant investor context, actual financial facts और readiness/limitations मिलेंगे। Goal feasibility या funding calculations Investor Profile में नहीं बनेंगे।
- **Strategy Builder** को investor context और source evidence मिल सकते हैं; asset-level liquidity, suitability और funding-path decisions Strategy Builder के ownership में रहेंगे।
- Budgeting/Cash Flow/Affordability का operating workflow approved product specification के ownership में है; Investor Profile इसे अपने अंदर duplicate नहीं करेगा।

## 7. Out of scope

- Moneywheel measurements/financial-health assessment।
- Goal Requirement Planning और Fund Feasibility।
- Strategy Builder, asset-level suitability और funding-path comparison।
- Scenario exploration, Accepted Plan, Action Plan, Reports और History।
- Detailed Multi-Goal Planning; इसकी design deferred/open है।
- Frontend refactoring या migration।
- Unapproved database redesign, new thresholds, mandatory fields, evidence-freshness periods या inferred policies।

## 8. Acceptance criteria

Step 3 तभी complete माना जाएगा जब:

- चारों Investor Profile components की ownership और data separation लागू तथा documented हो।
- Existing backend behavior और persisted data contracts का relevant transfer evidence उपलब्ध हो।
- Authenticated user और record ownership/access checks server-side लागू और tested हों।
- Evidence/provenance, data readiness और material data-quality limitations खोए बिना उपलब्ध हों।
- Missing/conflicting/stale inputs को unsupported assumptions से replace न किया जाए।
- API request/response contracts और frontend compatibility verified हों; frontend code unchanged रहे।
- Unit, integration, contract, security और regression tests के परिणाम दर्ज हों।
- Moneywheel/Goal Planner/Strategy Builder के ownership boundaries में duplication न हो।
- Unresolved decisions स्पष्ट रूप से open रहें; उन्हें approved behavior न माना जाए।

## 9. Specification status और source coverage

यह step Investor Profile की feature boundary और approved product specification के decision-specific assessment principles को implementation instructions में बदलता है। approved product specification के Financial State facts/evidence/data-readiness contract और Risk Profile, Behavioural Profile तथा Investor Preferences & Needs के विस्तृत owner specifications को implementation से पहले उनके canonical source chapters से पूरा verify करके इस document में आवश्यक detail सहित embed करना होगा। केवल इस document के आधार पर unverified schema fields या unresolved rules implement न करें।

Developer Ready Operating Manual में दर्ज product ownership, canonical data separation, system flow और cross-cutting engineering requirements इस step के architectural guardrails हैं। approved product specification/05/06 के Step 2 contracts को दोबारा define नहीं करना है।

**यह दस्तावेज़ implementation scope है, implementation completion का प्रमाण नहीं।** इस commit से कोई backend code, frontend code, database schema या पुरानी branch modify नहीं होती।

## 9. Financial State — embedded approved product specification implementation contract

### 9.1 Purpose and ownership

Financial State is a dated, evidence-aware record of actual financial facts and estimates. It owns financial-state records, provenance, decision-specific readiness checks, corrections and material-change handling. It does not independently determine financial health, goal feasibility or strategy suitability.

Use approved product specification canonical identities/categories. approved product specification owns measurement formulas and input scope; approved product specification owns constraints and decision gates; approved product specification owns budgeting/cash-flow application; approved product specification owns financial-health interpretation; approved product specification owns goal feasibility. Generic persistence, history/versioning and deletion mechanisms belong to the approved data architecture; processing mechanics belong to system logic. Financial State must not create competing formula, threshold or domain-policy definitions.

### 9.2 Core record groups

- **Income:** amount, currency, gross/net basis, frequency/period, source, as-of date and actual/reported/estimated status. Monthly Surplus uses actual Net Income belonging to that calendar month. Keep irregular/one-off receipts separate from regular monthly surplus. Expected future income is not income already received.
- **Expenses and commitments:** amount, category, transaction date/period, source and actual/budgeted/planned/estimated status. Full EMI is an Expense. Savings/investments are recorded separately from Expenses. A credit-card purchase is an Expense in its purchase month; paying the bill is not a second Expense. Identify own-account transfers so they are not Income or Expenses. Adjust refunds against the original Expense. For annual/irregular expenses, retain actual amount and payment month; separately record monthly planning allocation where available.
- **Assets and resources:** value/currency, valuation basis/date, evidence source, ownership/share where known, liquidity/practical access, restrictions, pledges, joint control and existing commitments. Asset value is not cash currently available. No universal liquid-reserve threshold or adequacy rule is approved.
- **Liabilities:** borrower, outstanding balance/date, interest rate/type, required payment/period, term/maturity, security, arrears, source and verification status where known. Keep original principal, current balance and payment impact distinct.
- **Insurance/protection facts:** where relevant/available, policy type, insured person, cover, premium, term, expiry, known exclusions/restrictions, evidence source and evidence date. Recording policy facts does not determine protection adequacy.

### 9.3 Evidence and dated baseline

Each material record must be interpretable in context: source, relevant date/period, currency and basis, actual/reported/estimated status, known limitations and conflicts. Evidence may come from investor input, supporting documents, connected records or a stated estimate. Evidence required and acceptable age depend on the decision; no universal freshness period is defined.

A baseline states its scope and as-of date and distinguishes observed facts from estimates, plans and projections. Preserve unresolved source conflicts; source-precedence rules remain open. For material facts retain source, owner where relevant, date/period, currency/value basis, access restrictions, verification status and limitations. A worksheet value or investor report proves what was supplied, not that it is persistently stored or independently verified.

- Preserve date/period, source, currency/value basis and actual/reported/estimated status for income, expenses, debt payments, assets and goal-funding inputs.
- A recorded asset, portfolio inclusion or category label does not prove accessibility, liquidity, earmarking or availability for a goal. Record access restrictions, existing commitments and goal-allocation evidence separately.
- Planned payments, projected maturity values, estimated returns and unverified payoff amounts remain distinguishable from confirmed current facts.

### 9.4 Decision-specific readiness and validation

Readiness is decision-specific, not a universal claim that all data is complete. Identify, where relevant, missing inputs, incompatible units/periods, unsupported category mappings, implausible values, duplicates, undated/potentially stale evidence and conflicts about ownership, access, restrictions or commitments.

Do not invent readiness scores, freshness limits, fallback values or automatic acceptance rules. Record material limitations for downstream decisions. If a required input, approved method or reliable evidence is missing, mark the affected result provisional, pending or unavailable as appropriate and explain why; never fabricate or silently substitute a default.

### 9.5 Change events and state separation

Distinguish corrections to previously recorded facts, real-world financial changes, reclassifications, estimate updates and hypothetical scenario changes. Preserve what changed, when and the available evidence/reason. Material changes prompt review of affected downstream measurements/decisions; revalidate affected scope where possible. A Financial State edit must not silently mutate an Accepted Plan, complete an action or refresh unrelated decisions.

Keep actual Financial State separate from derived measurements/assessments/evaluations/reports, hypothetical scenarios, Accepted Plan/adoption records, and execution status/outcome evidence. A derived result is not a source fact; a scenario is not actual state; a recommendation/report is not proof of adoption; an action marked complete is not proof of financial outcome.

### 9.6 Privacy, access, retention and deletion

Apply the approved security/privacy/consent/access/retention/deletion policies and shared data-architecture mechanisms. Preserve record-level impact of correction/deletion and identify affected derived evaluations, exports, logs, replicas and backups. Deletion propagation and residual-data policy remain open until approved and verified. Do not invent a separate retention policy or claim regulatory compliance.

### 9.7 Financial State outputs

Expose, as applicable: record scope and baseline as-of date; values with source, period, currency/basis and actual/estimated status; evidence gaps, limitations and unresolved conflicts; ownership/access/restrictions/commitments where known; correction/material-change history; and a decision-specific readiness indication with reasons. Descriptive readiness states are not a mandated numeric score or runtime enum.

### 9.8 Open decisions and verification gaps

Keep these open until explicitly resolved: evidence/freshness standards by decision type; precedence/resolution of conflicting sources; shared/joint ownership, access rights and shared-resource allocation; retention by data class; deletion propagation across derived evaluations/exports/logs/replicas/backups; and verification of logical records against physical schema, validation, authorization, save/reload, history and downstream behaviour.

## 10. Risk Profile — available source content and maturity

The Investor Identity material distinguishes these dimensions and must not collapse them into one questionnaire score:

- **Risk Capacity:** financial ability to absorb loss, informed by financial circumstances such as income, assets, liabilities and liquidity.
- **Risk Tolerance:** psychological comfort with uncertainty/loss.
- **Risk Perception:** how risky the investor believes the current situation is.
- **Risk Attitude:** recurring natural response/behaviour in the face of uncertainty.
- **Risk Need / Requirement:** risk level potentially required to pursue stated goals; this is not permission to override capacity or approved constraints.
- **Time Horizon:** relevant temporal context for the investor/goal.
- **Behaviour under drawdown:** distinguish experienced historical response from hypothetical answers.

A questionnaire response alone is not a complete risk profile. For investors without market-cycle experience, hypothetical loss responses may reflect imagination, prior beliefs, family/social narratives or limited familiarity—not observed tolerance. Record the basis of each finding (observed experience, investor-stated belief, hypothetical response or evidence-backed financial circumstance) and uncertainty separately.

**Source maturity:** The located Risk Profiling and Risk Capacity pages are marked Idea and primarily contain outlines; the Risk Tolerance vs Risk Capacity page is also an outline. These concepts are useful source material but are not a fully approved scoring model, question bank, thresholds, weighting method or final risk classification. Do not implement numeric scores, cut-offs, risk bands or suitability decisions from these outlines. Detailed Risk Profile contract remains an explicit specification gap.

## 11. Behavioural Profile — available source content and maturity

The Investor Identity framework separates Financial Identity, Goal Identity, Risk Identity, Behavioural Identity, Decision Identity, Portfolio Identity, Market Identity and Advanced Investor Identity. Behavioural Identity asks what the investor actually does in real situations, rather than relying only on self-description.

The current Behavioural Identity outline identifies these evidence areas:
- past investing behaviour;
- reactions to gains and losses;
- FOMO, panic, overconfidence and impatience as possible behavioural mechanisms;
- attention and information-seeking behaviour;
- social influence and herd behaviour;
- consistency or gaps between stated beliefs and actual actions;
- behaviour under stress and uncertainty;
- distinction between observed behavioural patterns and psychological explanations.

Useful prompts in the source include what the investor historically did during a market crash, whether decisions are postponed or impulsive, and where stated principles differ from actual actions. The intended output is an evidence-based behavioural profile.

The Investor Behaviour Content database categorises content under Risk & Return Perception, Biases, Decision Behaviour, Product Behaviour and Investor Psychology. These are content taxonomy labels, not automatically approved runtime enums or diagnostic labels.

**Source maturity:** Behavioural Identity is marked Outline; related content pages are Idea/Outline. Treat these as discovery and assessment prompts, not validated psychometric instruments. Do not diagnose the investor, infer a stable trait from one event, or create scoring/weighting/labels without an approved specification. Preserve observed event, investor explanation, context, recurrence and confidence separately where supported.

## 12. Investor Preferences & Needs — currently available contract

Investor Preferences & Needs captures investor-stated preferences, priorities, objectives and planning needs. The available operating blueprint establishes it as a distinct Investor Profile component. approved product specification assessment principles require capturing the investor's question, decision, timing, scope, priorities/concerns, relevant events and material dependencies, proportionate to the decision.

- A stated preference is evidence of what the investor said, not proof of acceptance or authorization.
- Preserve the investor's own wording/context where material; distinguish stated preference from system interpretation or recommendation.
- Goal identity, relative priority, target amount/date, funding path and strategy are separate concepts; do not infer priority from a goal category.
- Investor priorities and competing claims over shared resources must be surfaced for investor decision; this component must not silently allocate resources or resolve priority conflicts.
- Do not convert a preference into a hard constraint unless an approved rule says so.

**Specification gap:** No complete, dedicated Preferences & Needs field catalogue, mandatory-field contract, preference taxonomy or lifecycle schema was located in the reviewed material. Do not invent fields, enums, priority scales or persistence columns. Keep the component extensible and record unresolved contract items for specification review.

## 13. Cross-component assessment and hand-off

For a decision-specific Investor Profile assessment, establish the question/decision and why it matters; timing; people/household/finances/resources in scope; investor-stated priorities/concerns; confirmed, unconfirmed and hypothetical events; and material dependencies. Include extra context only if it could materially change the decision.

For shared resources/liabilities, clarify ownership/share, practical access/control/restrictions, payment responsibility, consent/agreement, existing commitments and uncertainty. Ownership/portfolio inclusion alone never proves availability. Use approved product specification for source records and approved product specification for approved availability/constraint effects; do not allocate resources here.

Use one decision-focused assessment output, containing only material information:
- decision context and scope;
- material findings about relevant goals, obligations, household/resources and circumstances;
- evidence status, limitations, uncertainty and unresolved questions;
- relevant investor profile context (risk, behaviour, preferences) with its evidence basis;
- implications for the decision without taking over the owning feature's calculation or recommendation;
- required clarification/evidence and the next hand-off.

## 14. Source maturity, unresolved items and implementation guardrails

- approved product specification is a working specification; runtime behaviour, physical schema, save/reload, authorization, deletion propagation and downstream consumers are unverified.
- approved product specification is a working draft; runtime implementation and test evidence are unverified.
- Risk Profiling and Behavioural Identity material located in the workspace is Idea/Outline-level, not a final approved scoring or assessment specification.
- Investor Preferences & Needs has a top-level ownership definition and approved product specification assessment principles, but no complete dedicated field/taxonomy contract was located.
- Do not invent mandatory fields, evidence-freshness periods, readiness scores, risk scoring, behavioural diagnoses, preference scales, database schema or runtime enums.
- Record unresolved items explicitly and implement only the contracts sufficiently specified and approved.

**यह दस्तावेज़ implementation scope है, implementation completion का प्रमाण नहीं।** इस दस्तावेज़ में source material का status स्पष्ट रखा गया है; कोई Idea/Outline अपने-आप approved runtime policy नहीं बनता। इस update से कोई backend code, frontend code, database schema या पुरानी branch modify नहीं होती।
