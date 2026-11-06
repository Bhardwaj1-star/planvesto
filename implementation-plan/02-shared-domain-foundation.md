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

## 3. Canonical vocabulary — Chapter 03

Chapter 03 के अनुसार:

- Approved goal taxonomy और financial category identities को canonical IDs सहित एक authoritative definition में रखें।
- Stable IDs को display names, custom labels और contextual details से अलग रखें।
- Goal identity, priority, timing, amount, beneficiary, funding path और feasibility को एक ही concept न मानें।
- Category label से liquidity, accessibility, goal eligibility, suitability, tax treatment या recommendation infer न करें।
- Flow और stock, income और expense, asset और liability, debt balance और debt payment को अलग रखें।
- Canonical IDs/definitions बदलने से पहले explicit approval और compatibility impact review आवश्यक है।

मौजूदा code में IDs, enums, aliases और persisted values की जाँच करें। किसी mismatch को चुपचाप ठीक करने, नया ID जोड़ने या पुराने ID का अर्थ बदलने के बजाय documented gap के रूप में दर्ज करें।

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
