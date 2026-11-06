# Step 3 — Investor Profile Feature Transfer

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
- Chapter 03 की canonical IDs/categories और Step 2 में embedded Chapter 05/06 contracts को reuse करें; feature के भीतर duplicate IDs, formulas या thresholds न बनाएँ।

## 3. Decision-specific assessment contract

Investor Profile से जुड़े assessment में:

- पहले investor का प्रश्न/निर्णय, timing, relevant people/household, goals और decision scope समझें।
- केवल वही अतिरिक्त context collect करें जो निर्णय को materially बदल सकता है।
- Confirmed facts, reported facts, estimates, assumptions और hypothetical events को अलग दिखाएँ।
- हर material input के लिए evidence status, relevance, limitations और sufficiency पर विचार करें।
- Missing, stale, invalid या conflicting information का प्रभाव बताएं और आवश्यक clarification/evidence की जरूरत surface करें।
- Shared resources/liabilities के लिए ownership, practical access/control, payment responsibility, consent, existing commitments और uncertainty को अलग-अलग जाँचें।
- Ownership या portfolio inclusion को availability का प्रमाण न मानें। Asset availability/constraints के लिए Chapter 06 और संबंधित Financial State evidence लागू होगा।
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

- **Moneywheel** को validated Financial State inputs मिलेंगे; canonical measurements और ratios Step 2 के Chapter 05 definitions से calculate होंगे। Investor Profile Moneywheel की calculations या health assessment own नहीं करता।
- **Goal Planner** को goal-relevant investor context, actual financial facts और readiness/limitations मिलेंगे। Goal feasibility या funding calculations Investor Profile में नहीं बनेंगे।
- **Strategy Builder** को investor context और source evidence मिल सकते हैं; asset-level liquidity, suitability और funding-path decisions Strategy Builder के ownership में रहेंगे।
- Budgeting/Cash Flow/Affordability का operating workflow Chapter 08 के ownership में है; Investor Profile इसे अपने अंदर duplicate नहीं करेगा।

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

यह step Investor Profile की feature boundary और Chapter 07 के decision-specific assessment principles को implementation instructions में बदलता है। Chapter 04 के Financial State facts/evidence/data-readiness contract और Risk Profile, Behavioural Profile तथा Investor Preferences & Needs के विस्तृत owner specifications को implementation से पहले उनके canonical source chapters से पूरा verify करके इस document में आवश्यक detail सहित embed करना होगा। केवल इस document के आधार पर unverified schema fields या unresolved rules implement न करें।

Developer Ready Operating Manual में दर्ज product ownership, canonical data separation, system flow और cross-cutting engineering requirements इस step के architectural guardrails हैं। Chapter 03/05/06 के Step 2 contracts को दोबारा define नहीं करना है।

**यह दस्तावेज़ implementation scope है, implementation completion का प्रमाण नहीं।** इस commit से कोई backend code, frontend code, database schema या पुरानी branch modify नहीं होती।
