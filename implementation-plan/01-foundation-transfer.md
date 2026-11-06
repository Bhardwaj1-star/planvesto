# Step 1 — बुनियादी ढाँचा, Security, API और Database Connection

## Implementation Scope — अभी केवल Backend

**इस implementation plan में अभी केवल Backend का development और modification करना है। Frontend की कोई coding, refactoring या file modification इस चरण का हिस्सा नहीं है।**

फिर भी Backend बनाते समय मौजूदा Frontend को compatibility reference की तरह जाँचना जरूरी है:
- Frontend के मौजूदा API endpoints, HTTP methods, request/response fields, authentication/session flow और error expectations को inspect और document करें।
- नए Backend के API contracts को मौजूदा Frontend की अपेक्षाओं से compare/test करें, ताकि आगे integration के समय breaking changes न आएँ।
- जहाँ पुराने और नए API contracts में अंतर हो, उसे दर्ज करें और Backend में उचित compatibility strategy तय करें; Frontend में अभी बदलाव न करें।
- इस चरण का acceptance यह है कि Backend की compatibility verify हो और integration के लिए स्पष्ट contract उपलब्ध हो—Frontend को नए Backend से वास्तव में migrate करना बाद के अलग Frontend implementation चरण में होगा।

---

## 0. सबसे पहले — पूरा Target Directory Tree

**Coding Agent, कोई code बदलने से पहले इस tree को समझें।** यही नए backend का approved target structure है। पुराने folders को देखकर अपनी तरफ से नया structure न बनाएँ और न ही पुराने folders को सीधे नए नाम से rename करें।

```text
backend/
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── investor_profile/
│   │   │   ├── moneywheel/
│   │   │   ├── goal_planner/
│   │   │   ├── strategy_builder/
│   │   │   ├── participate_with_your_finances/
│   │   │   ├── multi_goal_planning/       # Reserved — अभी implementation नहीं
│   │   │   ├── reports/
│   │   │   ├── history/
│   │   │   └── action_plan/
│   │   └── schemas/
│   ├── application/
│   │   ├── features/
│   │   │   ├── investor_profile/
│   │   │   ├── moneywheel/
│   │   │   ├── goal_planner/
│   │   │   ├── strategy_builder/
│   │   │   ├── participate_with_your_finances/
│   │   │   ├── multi_goal_planning/       # Reserved — अभी implementation नहीं
│   │   │   ├── reports/
│   │   │   ├── history/
│   │   │   └── action_plan/
│   │   ├── workflows/
│   │   │   ├── investor_situation_assessment/
│   │   │   ├── budgeting_cash_flow_affordability/
│   │   │   ├── planning_lifecycle/
│   │   │   ├── report_preparation/
│   │   │   └── plan_acceptance/
│   │   ├── ports/
│   │   │   └── repositories/
│   │   └── shared/
│   ├── domain/
│   │   ├── canonical/
│   │   │   ├── goal_taxonomy.py
│   │   │   ├── financial_categories.py
│   │   │   └── measurements.py
│   │   ├── features/
│   │   │   ├── investor_profile/
│   │   │   ├── moneywheel/
│   │   │   ├── goal_planner/
│   │   │   ├── strategy_builder/
│   │   │   ├── participate_with_your_finances/
│   │   │   ├── multi_goal_planning/       # Proposed — approval के बाद
│   │   │   ├── reports/
│   │   │   ├── history/
│   │   │   └── action_plan/
│   │   └── shared/
│   │       ├── calculations/
│   │       ├── constraints/
│   │       ├── evidence/
│   │       ├── readiness/
│   │       ├── versioning/
│   │       └── value_objects.py
│   ├── infrastructure/
│   │   ├── persistence/
│   │   │   ├── mappers/
│   │   │   └── repositories/
│   │   ├── providers/
│   │   │   └── supabase/
│   │   ├── reporting/
│   │   └── observability/
│   ├── security/
│   └── core/
├── data/
│   ├── reference/
│   └── fixtures/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── end_to_end/
│   ├── security/
│   ├── regression/
│   └── fixtures/
└── scripts/
```

### इस tree को कैसे समझना है

- `app/api/` — frontend से आने वाली requests और responses।
- `app/application/` — कौन-सा काम कब और किस क्रम में चलेगा।
- `app/domain/` — असली financial rules, calculations और feature के फैसले।
- `app/infrastructure/` — database, Supabase और report बनाने जैसी बाहरी तकनीकी चीज़ें।
- `app/security/` — login, user identity और data access की सुरक्षा।
- `app/core/` — settings, startup और पूरे backend की साझा सुविधाएँ।
- `data/`, `migrations/`, `tests/`, `scripts/` — reference/test data, database changes, जाँच और maintenance scripts।

**काम का रास्ता:** मौजूदा Frontend → Backend API → Application → Domain. जरूरत पड़ने पर Application, Ports के जरिए Infrastructure से database/provider का काम करवाएगा। Infrastructure, Ports को implement करेगा। इस चरण में केवल Backend बदलेगा; Frontend मौजूदा स्थिति में रहेगा और उसके contracts compatibility जाँच के लिए reference होंगे।

**Dependency के जरूरी नियम:**
- Domain में FastAPI, Supabase SDK या database client का import नहीं होना चाहिए।
- API में financial calculations या database queries नहीं लिखनी हैं।
- Application सीधे Supabase SDK या concrete database repository पर निर्भर नहीं होगा; वह Ports इस्तेमाल करेगा।
- Infrastructure database/provider से जुड़ेगा, लेकिन financial rules का मालिक नहीं बनेगा।
- Multi-Goal Planning की जगह tree में reserve रहेगी; इसकी detailed design approval से पहले कोई logic न बनाएँ।

### Step 1 में tree का कितना हिस्सा बनाना है?

इस चरण में पहले पूरे tree को reference मानें, लेकिन केवल foundation के लिए जरूरी folders/files तैयार करें: `app/api/`, `app/core/`, `app/security/`, `app/infrastructure/persistence/`, `app/infrastructure/providers/supabase/`, `data/`, `migrations/`, `tests/` और `scripts/`। बाकी feature/workflow folders को तभी बनाएँ जब उनका अगला implementation step शुरू हो। खाली folders बनाने के लिए feature logic का अनुमान न लगाएँ।

---

> **यह दस्तावेज़ Coding Agent के लिए काम करने का निर्देश है।** इसे पढ़कर पहले मौजूदा सिस्टम को समझें, फिर नए ढाँचे की नींव तैयार करें। इस चरण में किसी भी फीचर का पूरा बिज़नेस लॉजिक दोबारा न लिखें।

## 1. इस चरण का आसान मतलब

हम पुराने backend को हटाकर शून्य से नया सिस्टम नहीं बना रहे हैं। पुराने backend में जो काम सही चल रहा है—लॉगिन, यूज़र की पहचान, database से जुड़ना, API चलाना और settings पढ़ना—उसे समझकर नए तय किए गए ढाँचे में सही जगह लाना है।

इस Step 1 का लक्ष्य है कि नया backend:
- सही तरीके से शुरू हो सके।
- सुरक्षित तरीके से यूज़र की पहचान कर सके।
- सभी API के लिए एक जैसा नियम अपनाए।
- Database से एक ही भरोसेमंद तरीके से जुड़े।
- आगे आने वाले सभी फीचर्स इसी नींव का इस्तेमाल कर सकें।

**ध्यान दें:** Investor Profile, Moneywheel, Goal Planner, Strategy Builder, Action Plan और Reports का पूरा logic इस चरण में migrate नहीं करना है। उनके पुराने code और dependencies की सूची बनानी है, ताकि अगले चरणों में उन्हें एक-एक करके सही जगह ले जाया जा सके।

## 2. पहले पुराने backend को समझें

मौजूदा branch में backend का मुख्य code `backend/` के अंदर है। Agent इन जगहों को ध्यान से देखे:

| पुरानी जगह | अभी इसमें क्या देखना है | नए ढाँचे में संभावित जगह |
|---|---|---|
| `backend/main.py` | App शुरू होना, routers जोड़ना, middleware और startup काम | नया application entry point / API setup |
| `backend/config/settings.py` | Environment variables, app settings और configuration | `core/config.py` या तय architecture का config हिस्सा |
| `backend/api/auth.py` | Login, token या user identity से जुड़े API | `security/` और auth API router |
| `backend/api/profile.py` | Profile endpoints और user access checks | आगे Investor Profile feature; साझा access checks `security/` में |
| `backend/db/supabase.py` (यदि branch में मौजूद हो) | Supabase client और database connection | `infrastructure/persistence/` |
| `backend/data/` | पुराने repositories और database queries | `infrastructure/persistence/` |
| `backend/api/` | सभी मौजूदा endpoints, request/response format | `api/routers/` और `api/schemas/` |
| `backend/tests/` | मौजूदा tests और sample data | नए tests के लिए आधार |

ऊपर दिए गए नए paths target architecture के अनुसार हैं। अगर repository में कोई file या path अलग हो, तो पहले असली code खोजें; केवल नाम देखकर file मौजूद मानकर न चलें।

## 3. नए backend में इस Step के तहत क्या तैयार होगा

Target architecture के अनुसार नीचे दिए गए हिस्सों की नींव तैयार करें। यदि final architecture में नाम थोड़ा अलग तय है, तो उसी approved structure का पालन करें।

### A. Core — backend की साझा बुनियादी चीज़ें

नया `core/` हिस्सा ऐसी चीज़ों के लिए होगा जिन्हें कई फीचर इस्तेमाल करेंगे:
- App की settings और environment configuration।
- एक जगह से configuration पढ़ने का तरीका।
- सामान्य error handling और logging की व्यवस्था।
- App के startup और shutdown पर चलने वाले जरूरी काम।
- Environment के हिसाब से development/test/production settings।

**पुराने से क्या आएगा:** `backend/config/settings.py` की जरूरी settings और `backend/main.py` में मौजूद startup/configuration से जुड़ा काम। पहले उनका इस्तेमाल समझें, फिर नए स्थान पर व्यवस्थित करें। पुराने नाम या behavior पर निर्भर code टूटना नहीं चाहिए।

### B. Security — यूज़र और उसके डेटा की सुरक्षा

नया `security/` हिस्सा सभी फीचर्स के लिए साझा सुरक्षा नियम देगा:
- Login के बाद यूज़र की पहचान कैसे होगी।
- हर request में current user कैसे पहचाना जाएगा।
- कौन-सा यूज़र किस data को देख या बदल सकता है।
- बिना login वाले और गलत permission वाले request को कैसे रोका जाएगा।
- Token/session की जाँच और authentication errors का एक जैसा जवाब।

**पुराने से क्या आएगा:** `backend/api/auth.py`, profile या अन्य routers में मौजूद login, token, current-user और ownership checks को खोजें। जो नियम केवल किसी एक feature के हैं, उन्हें वहीं रहने दें; जो सभी features में समान हैं, उन्हें साझा security code में लाएँ।

**बहुत जरूरी:** केवल frontend से user_id लेना सुरक्षा नहीं है। Database में पढ़ने/लिखने से पहले server पर प्रमाणित user की पहचान और उस record का ownership check होना चाहिए। Secrets, service-role keys और passwords कभी frontend या Git में न रखें।

### C. API की समान व्यवस्था — सभी endpoints का एक जैसा तरीका

नया `api/` हिस्सा API को व्यवस्थित और एक जैसा बनाएगा:
- सभी routers को एक जगह register करने का तरीका।
- API version/prefix का एक समान नियम, यदि target architecture में तय है।
- Request और response के लिए स्पष्ट schemas।
- Validation errors और सामान्य errors का एक जैसा format।
- HTTP status codes का सही इस्तेमाल।
- Health check endpoint, जिससे पता चले कि app चल रहा है।

**पुराने से क्या आएगा:** `backend/api/` में मौजूद endpoints और उनके वास्तविक request/response fields की सूची बनाएँ। जैसे `auth.py`, `profile.py`, `moneywheel.py`, `goals.py`, `goal_basket.py`, `goal_funding.py`, `financial_plan.py`, `financial_state.py`, `action_plan.py`, `orchestration.py`, `dashboard.py`, `diary.py`, `basket_report.py` और `summary_report.py`। इनके endpoint paths, input fields, output fields और error behavior को दर्ज करें।

इस Step में इन सभी feature endpoints को नए routers में पूरा rewrite नहीं करना है। पहले साझा API setup तैयार करें और मौजूदा API behavior को सुरक्षित रखने की योजना बनाएँ। Feature-wise migration बाद के steps में होगी।

### D. Database Connection — database से जुड़ने का एक भरोसेमंद रास्ता

नया `infrastructure/persistence/` हिस्सा database से जुड़ने का साझा तरीका देगा:
- Database client/connection एक जगह initialize हो।
- Environment variables से connection settings आएँ।
- Connection error साफ तरीके से handle हो।
- Database access के लिए reusable session/client dependency मिले।
- Queries और repositories को धीरे-धीरे feature के हिसाब से अलग रखा जा सके।
- Test के समय सुरक्षित test configuration इस्तेमाल हो।

**पुराने से क्या आएगा:** Supabase/database client बनाने वाला मौजूदा code (उदाहरण के लिए `backend/db/supabase.py`, अगर मौजूद हो), `backend/data/` में repositories और अलग-अलग files में फैली database connection logic को खोजें। पहले connection बनाने और query चलाने का तरीका समझें; फिर एक साझा connection layer बनाएँ।

Database schema, tables, columns, Row Level Security (RLS), policies और पुराने data को बिना जाँच बदला नहीं जाना चाहिए। इस Step में कोई destructive migration, table deletion या data reset न करें।

## 4. फीचर के हिसाब से पुराने code में क्या-क्या सुरक्षित रखना है

यह सूची Step 1 में feature code migrate करने के लिए नहीं, बल्कि सही inventory बनाने के लिए है। Agent हर feature के पुराने API, service, engine, repository, model, schema और tests खोजे और उनका आपसी संबंध दर्ज करे।

| फीचर | पुराने backend में पहले कहाँ खोजें | आगे नए ढाँचे में क्या जाएगा |
|---|---|---|
| Investor Profile | `backend/api/profile.py`, auth/user checks, संबंधित models/data/services | Profile API और schemas feature में; user identity/ownership साझा `security/` में; profile data access persistence में |
| Moneywheel | `backend/api/moneywheel.py`, संबंधित services, engines, rules, models और data | Moneywheel के endpoints, input/output schemas और feature logic अपने feature में; साझा database access persistence से |
| Goal Planner | `backend/api/goals.py`, `goal_basket.py`, `goal_funding.py`, संबंधित services/engines/data | Goal create/update, goal details, basket/funding logic और उनके schemas Goal feature में; database queries repositories में |
| Strategy Builder | `backend/api/financial_plan.py`, `financial_state.py`, `orchestration.py` और संबंधित services/engines/rules | Strategy बनाने के नियम, inputs, outputs और orchestration को पहचानकर feature/workflow में अलग करना; shared calculations को बाद में domain में रखना |
| Participate with Your Finances | संबंधित API, frontend flow, services और data खोजें; नाम से file मानकर न चलें | User participation/input, उसके validation और save/fetch flow को अलग feature में रखना |
| Action Plan | `backend/api/action_plan.py`, संबंधित services और `backend/data/` repository files | Action Plan API, schemas, generation/management logic और persistence को अलग करना |
| Reports और History | `backend/api/basket_report.py`, `summary_report.py`, `diary.py`, `backend/report_engine/` और संबंधित data files | Report generation, history/diary retrieval, PDF/output और schemas को संबंधित report/history feature में रखना |
| Dashboard और अन्य साझा flows | `backend/api/dashboard.py`, `orchestration.py` और frontend में इस्तेमाल होने वाले calls | यह तय करना कि कौन-सा हिस्सा dashboard feature है और कौन-सा multi-feature workflow; एक ही logic की duplicate copy न बनाना |

किसी feature का exact service, engine या repository file नाम इस table में नहीं दिया गया है, क्योंकि Agent को वास्तविक imports और code देखकर पुष्टि करनी है। अनुमान लगाकर file move या rewrite न करें।

## 5. मौजूदा Frontend के साथ Backend Compatibility

यह section केवल Backend को सही contract के साथ बनाने के लिए है। **Frontend repository की किसी file में इस Step के दौरान बदलाव नहीं करना है।**

- मौजूदा Frontend को read-only reference की तरह inspect करें: API calls, endpoints, HTTP methods, request/response formats, auth/session handling और error handling।
- पहचानें कि कौन-से flows Backend API इस्तेमाल करते हैं और कौन-से सीधे Supabase से जुड़े हैं। इस dependency को document करें; अभी frontend architecture बदलने की कोशिश न करें।
- नए Backend के endpoints और schemas को मौजूदा Frontend की अपेक्षाओं के विरुद्ध contract tests या उपयुक्त integration tests से verify करें।
- यदि नया Backend किसी पुराने contract से अलग है, तो अंतर और उसका प्रभाव दर्ज करें। जहाँ संभव और उचित हो, Backend में backward-compatible behavior/adapter रखें।
- मौजूदा Frontend को नए Backend पर switch करना, उसके API calls बदलना या UI/auth flow refactor करना इस Step में नहीं होगा। यह काम Backend तैयार और स्वीकृत होने के बाद अलग Frontend integration चरण में होगा।

## 6. Coding Agent के लिए काम करने का सही क्रम

1. Branch `backend-redesign` पर ही काम करें। किसी दूसरी branch या पुराने production branch में बदलाव न करें।
2. पहले repository और imports पढ़ें; मौजूदा tests चलाकर baseline result दर्ज करें।
3. Auth, configuration, API startup और database connection का flow diagram/छोटी सूची बनाएँ।
4. पुराने code से shared Core, Security, API setup और Database connection को नए target structure में व्यवस्थित करें।
5. नए modules के imports और app startup को काम करने लायक बनाएँ।
6. Health check, configuration loading, auth dependency, permission/ownership check और database connectivity के tests लिखें।
7. मौजूदा API contracts को Frontend की वर्तमान अपेक्षाओं से compare करें और Backend की compatibility verify करें; Frontend files न बदलें।
8. जहाँ जरूरी हो compatibility adapter रखें; एक ही behavior की दो अलग implementations न बनाएँ।
9. Changes के बाद tests चलाएँ और क्या बदला/क्या बाकी है, लिखें।

## 7. इस Step में क्या नहीं करना है

- सभी feature modules को एक साथ migrate नहीं करना।
- Financial calculations या investment rules को इस Step में rewrite नहीं करना।
- Database tables/columns या RLS policies को बिना स्पष्ट आवश्यकता और approval के नहीं बदलना।
- Existing endpoint paths या response fields अचानक नहीं बदलना।
- पुराने working code को delete नहीं करना।
- Secrets या वास्तविक credentials को code, logs या इस document में नहीं डालना।
- Multi-Goal Planning या दूसरे बड़े workflow का नया business logic अभी नहीं बनाना।

## 8. Step 1 पूरा कब माना जाएगा? (काम पूरा होने की जाँच)

- [ ] नया backend app सही तरीके से start होता है।
- [ ] Configuration environment variables से सुरक्षित तरीके से load होती है।
- [ ] Health check endpoint सफल response देता है।
- [ ] Authentication से current user server पर पहचाना जाता है।
- [ ] User ownership/permission check का test पास होता है।
- [ ] Database connection सफल है और connection failure सही तरीके से handle होता है।
- [ ] API routers register करने का एक समान तरीका तैयार है।
- [ ] पुराने endpoints और मौजूदा Frontend contracts की inventory उपलब्ध है।
- [ ] Backend के API contracts मौजूदा Frontend expectations के विरुद्ध verify किए गए हैं; Frontend में कोई बदलाव नहीं हुआ है।
- [ ] मौजूदा tests और नए foundation tests के results दर्ज हैं।
- [ ] कोई feature logic, endpoint या पुराना data बिना वजह delete/overwrite नहीं हुआ।

## 9. Agent से अंतिम रिपोर्ट

काम पूरा होने पर Coding Agent यह रिपोर्ट दे:
1. कौन-सी नई files/folders बनाई या बदलीं।
2. पुराने backend की कौन-सी files से code/behavior लिया गया।
3. Authentication, API और database connection कैसे काम कर रहे हैं।
4. कौन-कौन से tests चलाए और उनका result क्या रहा।
5. कौन-से पुराने endpoints compatibility के लिए जस के तस रखे गए हैं और मौजूदा Frontend contracts के साथ compatibility कैसे verify की गई।
6. पुष्टि करें कि इस Step में Frontend की किसी file/code में बदलाव नहीं किया गया।
6. कौन-से मुद्दे अगले Step से पहले तय करने होंगे।

**अंतिम नियम:** पहले नींव मजबूत करें और पुराने सिस्टम का behavior सुरक्षित रखें। हर feature को बाद के चरण में एक-एक करके Backend में migrate और test किया जाएगा। Frontend को नए Backend से जोड़ने/उसके API calls बदलने का काम अलग Frontend integration चरण में होगा।