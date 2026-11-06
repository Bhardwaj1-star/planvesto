# 00 — Backend Foundation & Architecture (Single Source of Truth)

> **Status:** Master target-architecture blueprint for the backend redesign. This document preserves the complete content of the Notion page **Backend Folder Structure — Target Architecture**, including Sections 1 through 7 (and all subsections/file-level ownership details). It defines the target structure; it does not claim that the files already exist or are implemented.
>
> **Authority:** Use this document as the main architecture and file/folder ownership reference. Steps 01, 02, 03 and later feature plans define the ordered implementation work and feature-specific contracts. If a step plan appears to conflict with this target structure, stop and resolve the conflict rather than silently inventing or changing architecture.
>
> **Source page:** [Backend Folder Structure — Target Architecture](https://app.notion.com/p/40f57e71b7b88194a6cdeee083a2568c)

---

# 🏗️ Backend Folder Structure — File-Level Developer Blueprint

<quote color="blue_bg">
✨ <b>Developer navigation guide</b>

A visual map of the target backend architecture, file ownership, dependency direction and migration boundaries. Use the directory trees to navigate; use the ownership tables to understand what each file is allowed to own.
</quote>

## 🧭 Architecture Rule

<b>Architecture: Layer First + Feature-Based Subdivision in a Modular Monolith.</b> The top-level folders represent technical layers. Feature modules sit inside the relevant layer. There is no separate deployable service per feature and no generic top-level <b>engines/</b> folder: an engine is a logical domain capability implemented in <b>domain/shared/</b> or in its owning <b>domain/features/\<feature>/</b> module.

The dependency direction is:

<b>API → Application → Domain</b>

<b>Application → Ports (interfaces)</b>

<b>Infrastructure → implements Ports and connects to PostgreSQL / Supabase</b>

<quote color="orange_bg">
⛔ <b>Non-negotiable boundary</b>

Domain code must not import FastAPI, Supabase SDKs, database clients, HTTP schemas or infrastructure repositories. Infrastructure must not own financial formulas or product decision rules.
</quote>

## 🗺️ 1. Main Directory Structure — System at a Glance

This blueprint is organised in two views: (1) the main-directory view, showing what belongs inside each root-level technical directory; and (2) the feature-complete view, listing each feature's API, application, domain, persistence and test files together. The physical architecture remains a <b>layer-first modular monolith</b>. The feature view is an ownership map across layers; it does not collapse HTTP, domain and database code into one folder.

<quote color="blue_bg">
<b>backend/</b><br /><b>├── app/</b><br /><b>│   ├── api/</b><br /><b>│   │   ├── routers/</b><br /><b>│   │   │   ├── investor\_profile/</b><br /><b>│   │   │   ├── moneywheel/</b><br /><b>│   │   │   ├── goal\_planner/</b><br /><b>│   │   │   ├── strategy\_builder/</b><br /><b>│   │   │   ├── participate\_with\_your\_finances/</b><br /><b>│   │   │   ├── multi\_goal\_planning/</b> <b>(reserved)</b><br /><b>│   │   │   ├── reports/</b><br /><b>│   │   │   ├── history/</b><br /><b>│   │   │   └── action\_plan/</b><br /><b>│   │   └── schemas/</b><br /><b>│   ├── application/</b><br /><b>│   │   ├── features/</b><br /><b>│   │   │   ├── investor\_profile/</b><br /><b>│   │   │   ├── moneywheel/</b><br /><b>│   │   │   ├── goal\_planner/</b><br /><b>│   │   │   ├── strategy\_builder/</b><br /><b>│   │   │   ├── participate\_with\_your\_finances/</b><br /><b>│   │   │   ├── multi\_goal\_planning/</b> <b>(reserved)</b><br /><b>│   │   │   ├── reports/</b><br /><b>│   │   │   ├── history/</b><br /><b>│   │   │   └── action\_plan/</b><br /><b>│   │   ├── workflows/</b><br /><b>│   │   │   ├── investor\_situation\_assessment/</b><br /><b>│   │   │   ├── budgeting\_cash\_flow\_affordability/</b><br /><b>│   │   │   ├── planning\_lifecycle/</b><br /><b>│   │   │   ├── report\_preparation/</b><br /><b>│   │   │   └── plan\_acceptance/</b><br /><b>│   │   ├── ports/</b><br /><b>│   │   │   └── repositories/</b><br /><b>│   │   └── shared/</b><br /><b>│   ├── domain/</b><br /><b>│   │   ├── canonical/</b><br /><b>│   │   │   ├── goal\_</b>[<b>taxonomy.py</b>](http://taxonomy.py)<br /><b>│   │   │   ├── financial\_</b>[<b>categories.py</b>](http://categories.py)<br /><b>│   │   │   └── </b>[<b>measurements.py</b>](http://measurements.py)<br /><b>│   │   ├── features/</b><br /><b>│   │   │   ├── investor\_profile/</b> <b>(four sibling subfeatures)</b><br /><b>│   │   │   ├── moneywheel/</b><br /><b>│   │   │   ├── goal\_planner/</b><br /><b>│   │   │   ├── strategy\_builder/</b><br /><b>│   │   │   ├── participate\_with\_your\_finances/</b><br /><b>│   │   │   ├── multi\_goal\_planning/</b> <b>(proposed; approval required)</b><br /><b>│   │   │   ├── reports/</b><br /><b>│   │   │   ├── history/</b><br /><b>│   │   │   └── action\_plan/</b><br /><b>│   │   └── shared/</b><br /><b>│   │       ├── calculations/</b><br /><b>│   │       ├── constraints/</b><br /><b>│   │       ├── evidence/</b><br /><b>│   │       ├── readiness/</b><br /><b>│   │       ├── versioning/</b><br /><b>│   │       └── value\_</b>[<b>objects.py</b>](http://objects.py)<br /><b>│   ├── infrastructure/</b><br /><b>│   │   ├── persistence/</b><br /><b>│   │   │   ├── mappers/</b><br /><b>│   │   │   └── repositories/</b><br /><b>│   │   ├── providers/</b><br /><b>│   │   │   └── supabase/</b><br /><b>│   │   ├── reporting/</b><br /><b>│   │   └── observability/</b><br /><b>│   ├── security/</b><br /><b>│   └── core/</b><br /><b>├── data/</b><br /><b>│   ├── reference/</b><br /><b>│   └── fixtures/</b><br /><b>├── migrations/</b><br /><b>├── tests/</b><br /><b>│   ├── unit/</b><br /><b>│   ├── integration/</b><br /><b>│   ├── contract/</b><br /><b>│   ├── end\_to\_end/</b><br /><b>│   ├── security/</b><br /><b>│   ├── regression/</b><br /><b>│   └── fixtures/</b><br /><b>└── scripts/</b>
</quote>

## 📘 1.1 How to Read the Directory Map — One End-to-End Example

<b>Information flow:</b> Frontend → API Router → API Schema validation → Application Use Case / Workflow → Domain capability → Infrastructure (repository/provider, when data access is required) → Application result → API response schema → Frontend.

ध्यान दें: यह target architecture है। नीचे दिए गए examples समझाने के लिए हैं; directory map अपने-आप में यह प्रमाणित नहीं करता कि ये files या code पहले से implemented हैं।

### 📋 1.2 Main Directory Structure — Folder Responsibilities, Examples & Information Flow

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
<b>Folder Path</b>
</td>
<td color="blue_bg">
<b>Responsibility — यह क्या करेगा?</b>
</td>
<td color="blue_bg">
<b>PlanVesto Example — कहानी में इसका काम</b>
</td>
<td color="blue_bg">
<b>Information Flow — डेटा कहाँ से आएगा और कहाँ जाएगा?</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/api/routers/</u></b>
</td>
<td color="blue_bg">
<b>ऐप से आने वाली जानकारी लेना और उसे सही काम तक पहुँचाना।</b>
</td>
<td color="blue_bg">
<b>Goal Planner में नया goal बनाना और Investor Profile में जानकारी बदलना।</b>
</td>
<td color="blue_bg">
<b>ऐप से जानकारी आएगी → सही काम चुना जाएगा → goal या profile वाला काम शुरू होगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/api/schemas/</u></b>
</td>
<td color="green_bg">
<b>आने-जाने वाली जानकारी की जाँच करना और उसे सही रूप में रखना।</b>
</td>
<td color="green_bg">
<b>यह जाँचेगा कि रकम सही नंबर है और तारीख सही फॉर्मेट में है। फिर सही जानकारी आगे भेजेगा और नतीजा ऐप को लौटाएगा।</b>
</td>
<td color="green_bg">
<b>ऐप से रकम और तारीख आएगी → उनकी जाँच होगी → सही जानकारी हिसाब के लिए जाएगी → नतीजा ऐप को लौटेगा।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/application/features/</u></b>
</td>
<td color="blue_bg">
<b>माँगे गए काम को पूरा करने के लिए ज़रूरी कदम चलाना।</b>
</td>
<td color="blue_bg">
<b>Goal Planner goal की जानकारी लेकर हिसाब करवाएगा; Strategy Builder उसी नतीजे से निवेश की योजना बनाएगा।</b>
</td>
<td color="blue_bg">
<b>ऐप जानकारी भेजेगा → feature ज़रूरी हिसाब करवाएगा → तैयार नतीजा वापस मिलेगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/application/workflows/</u></b>
</td>
<td color="green_bg">
<b>कई जुड़े हुए कामों को सही क्रम में पूरा करवाना।</b>
</td>
<td color="green_bg">
<b>Goal Planner से मंज़ूर goal की जानकारी Strategy Builder तक पहुँचाना, ताकि आगे की योजना बन सके।</b>
</td>
<td color="green_bg">
<b>एक काम का तैयार नतीजा अगले काम को मिलेगा → अगला काम वहीं से आगे बढ़ेगा।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/application/ports/</u></b>
</td>
<td color="blue_bg">
<b>ज़रूरत पड़ने पर जानकारी लेने, सेव करने या दूसरे साधनों से काम कराने का तरीका तय करना।</b>
</td>
<td color="blue_bg">
<b>जब goal सेव करना हो, तो यह database से कहेगा कि इस investor का goal सेव करो या पुराना goal निकालकर दो।</b>
</td>
<td color="blue_bg">
<b>Application जानकारी माँगेगा या सेव करने को कहेगा → database से जानकारी आएगी या वहाँ सेव होगी।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/application/shared/</u></b>
</td>
<td color="green_bg">
<b>अलग-अलग जगह काम आने वाली सामान्य सुविधाएँ एक जगह रखना।</b>
</td>
<td color="green_bg">
<b>एक जैसा जवाब दिखाना और एक ही request दो बार आने पर काम दोबारा न करना।</b>
</td>
<td color="green_bg">
<b>अलग-अलग काम इस सुविधा का इस्तेमाल करेंगे → एक जैसा जवाब मिलेगा और दोहराया काम रुकेगा।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/domain/canonical/</u></b>
</td>
<td color="blue_bg">
<b>पूरे सिस्टम में इस्तेमाल होने वाले शब्दों, श्रेणियों और मापों का एक जैसा मतलब तय करना।</b>
</td>
<td color="blue_bg">
<b>Goal के प्रकार, खर्च की श्रेणियाँ और पैसों की माप का एक जैसा मतलब तय करना।</b>
</td>
<td color="blue_bg">
<b>सभी features इन्हीं तय श्रेणियों और मापों का इस्तेमाल करेंगे → जानकारी का मतलब हर जगह एक रहेगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/domain/features/</u></b>
</td>
<td color="green_bg">
<b>काम से जुड़े असली नियम, शर्तें और फैसले तय करना।</b>
</td>
<td color="green_bg">
<b>Goal Planner में देखना कि goal के लिए कितनी रकम चाहिए; Moneywheel में आर्थिक स्थिति का हिसाब लगाना।</b>
</td>
<td color="green_bg">
<b>Application संबंधित feature से नियम पूछेगा → feature जाँच करके नतीजा लौटाएगा।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/domain/shared/</u></b>
</td>
<td color="blue_bg">
<b>अलग-अलग हिस्सों में काम आने वाले सामान्य नियम और हिसाब एक जगह रखना।</b>
</td>
<td color="blue_bg">
<b>Net worth और हर महीने बचने वाली रकम जैसे हिसाब अलग-अलग features में एक ही तरीके से करना।</b>
</td>
<td color="blue_bg">
<b>किसी feature को साझा हिसाब चाहिए होगा → यहाँ से हिसाब मिलेगा → feature आगे काम करेगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/infrastructure/persistence/</u></b>
</td>
<td color="green_bg">
<b>जानकारी को सुरक्षित रखना और ज़रूरत पर वापस निकालना।</b>
</td>
<td color="green_bg">
<b>नया goal database में सेव करना और पुराना goal निकालकर application को देना।</b>
</td>
<td color="green_bg">
<b>Application goal सेव करने को कहेगा → database में सेव होगा → माँगने पर वापस मिलेगा।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/infrastructure/providers/</u></b>
</td>
<td color="blue_bg">
<b>बाहरी सेवाओं से जानकारी लेना और उन्हें जानकारी भेजना।</b>
</td>
<td color="blue_bg">
<b>Supabase से investor की जानकारी या सेव किए गए goals लेना और ज़रूरत पड़ने पर वहाँ सेव करना।</b>
</td>
<td color="blue_bg">
<b>Application जानकारी माँगेगा → Supabase से जानकारी मिलेगी या वहाँ सेव होगी → जवाब वापस आएगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/infrastructure/reporting/</u></b>
</td>
<td color="green_bg">
<b>तैयार जानकारी को रिपोर्ट या फ़ाइल के रूप में बनाना।</b>
</td>
<td color="green_bg">
<b>Goal और investment plan के तैयार नतीजों से PDF report बनाना; हिसाब दोबारा नहीं करना।</b>
</td>
<td color="green_bg">
<b>तैयार goal और योजना की जानकारी आएगी → PDF बनेगी → investor को report मिलेगी।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/infrastructure/observability/</u></b>
</td>
<td color="blue_bg">
<b>सिस्टम में हुए काम और आई गड़बड़ियों का रिकॉर्ड रखना।</b>
</td>
<td color="blue_bg">
<b>Goal बनाते समय कोई गड़बड़ी हो तो उसका रिकॉर्ड रखना, ताकि बाद में पता चल सके कि समस्या कहाँ आई।</b>
</td>
<td color="blue_bg">
<b>काम के दौरान गड़बड़ी होगी → उसका रिकॉर्ड बनेगा → टीम बाद में वजह देख सकेगी।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/app/security/</u></b>
</td>
<td color="green_bg">
<b>यह तय करना कि कौन सिस्टम में आ सकता है और किस जानकारी को देख या बदल सकता है।</b>
</td>
<td color="green_bg">
<b>यह पक्का करना कि investor सिर्फ अपनी profile और अपने goals ही देख या बदल सके।</b>
</td>
<td color="green_bg">
<b>Investor की पहचान जाँची जाएगी → अनुमति होगी तो जानकारी खुलेगी, नहीं तो रोक दी जाएगी।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/app/core/</u></b>
</td>
<td color="blue_bg">
<b>सिस्टम चलाने के लिए ज़रूरी सामान्य सेटिंग्स रखना।</b>
</td>
<td color="blue_bg">
<b>ऐप शुरू करने के लिए ज़रूरी सेटिंग्स, जैसे database का पता और दूसरी सामान्य सेटिंग्स रखना।</b>
</td>
<td color="blue_bg">
<b>ऐप शुरू होगा → ये सेटिंग्स पढ़ी जाएँगी → बाकी हिस्से इन्हें इस्तेमाल करेंगे।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/data/reference/</u></b>
</td>
<td color="green_bg">
<b>ऐसी तय जानकारी रखना जिसे सिस्टम ज़रूरत पड़ने पर पढ़ सके।</b>
</td>
<td color="green_bg">
<b>Goal के प्रकार या दूसरी तयशुदा जानकारी रखना, जिसे ऐप ज़रूरत पड़ने पर पढ़ सके।</b>
</td>
<td color="green_bg">
<b>तयशुदा जानकारी यहाँ रखी होगी → ज़रूरत पड़ने पर feature इसे पढ़ेगा।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/data/fixtures/</u></b>
</td>
<td color="blue_bg">
<b>जाँच और अभ्यास के लिए नमूने वाली जानकारी रखना।</b>
</td>
<td color="blue_bg">
<b>टेस्ट के लिए नकली investor और sample goals रखना, ताकि असली डेटा इस्तेमाल न करना पड़े।</b>
</td>
<td color="blue_bg">
<b>Sample data test में जाएगा → पता चलेगा कि code सही काम कर रहा है या नहीं।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/migrations/</u></b>
</td>
<td color="green_bg">
<b>डेटाबेस में बदलाव करने के निर्देश और उनका रिकॉर्ड रखना।</b>
</td>
<td color="green_bg">
<b>Database में कोई नया column जोड़ना या पुरानी बनावट में तय बदलाव करना।</b>
</td>
<td color="green_bg">
<b>तय बदलाव चलाया जाएगा → database की बनावट अपडेट हो जाएगी।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/tests/unit/</u></b>
</td>
<td color="blue_bg">
<b>किसी एक छोटे काम को अलग से जाँचकर देखना।</b>
</td>
<td color="blue_bg">
<b>Goal की रकम और ज़रूरी बचत का हिसाब सही आ रहा है या नहीं, यह अलग से जाँचना।</b>
</td>
<td color="blue_bg">
<b>एक छोटा input दिया जाएगा → हिसाब चलेगा → नतीजा सही है या नहीं, जाँचा जाएगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/tests/integration/</u></b>
</td>
<td color="green_bg">
<b>जाँचना कि सिस्टम के अलग-अलग हिस्से साथ मिलकर सही काम कर रहे हैं।</b>
</td>
<td color="green_bg">
<b>जाँचना कि goal सेव करने पर database में सही जानकारी जाती है और वापस सही मिलती है।</b>
</td>
<td color="green_bg">
<b>Test database में जानकारी सेव करेगा → फिर वापस निकालेगा → दोनों की जाँच होगी।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/tests/contract/</u></b>
</td>
<td color="blue_bg">
<b>जाँचना कि जानकारी भेजने और जवाब मिलने का तय तरीका सही चल रहा है।</b>
</td>
<td color="blue_bg">
<b>जाँचना कि goal भेजते समय और जवाब लेते समय तय किए गए fields और formats सही हैं।</b>
</td>
<td color="blue_bg">
<b>तय format में जानकारी भेजी जाएगी → जवाब की जाँच होगी कि सभी fields सही हैं।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/tests/end\_to\_end/</u></b>
</td>
<td color="green_bg">
<b>शुरू से अंत तक पूरी प्रक्रिया सही चल रही है या नहीं, यह जाँचना।</b>
</td>
<td color="green_bg">
<b>Investor goal की जानकारी भेजे और उसे सही जवाब मिले—पूरी प्रक्रिया को शुरू से अंत तक जाँचना।</b>
</td>
<td color="green_bg">
<b>Investor की request जाएगी → पूरा backend काम करेगा → आख़िर में मिले जवाब की जाँच होगी।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/tests/security/</u></b>
</td>
<td color="blue_bg">
<b>जाँचना कि किसी की निजी जानकारी तक गलत व्यक्ति की पहुँच न हो।</b>
</td>
<td color="blue_bg">
<b>जाँचना कि एक investor दूसरे investor का goal न देख पाए।</b>
</td>
<td color="blue_bg">
<b>दो अलग investors से कोशिश होगी → दूसरे investor की जानकारी खुलनी नहीं चाहिए।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/tests/regression/</u></b>
</td>
<td color="green_bg">
<b>बदलाव के बाद पुराने काम पहले की तरह सही चल रहे हैं या नहीं, यह जाँचना।</b>
</td>
<td color="green_bg">
<b>कोड में बदलाव के बाद पुराने goals के हिसाब पहले की तरह सही आ रहे हैं या नहीं, यह जाँचना।</b>
</td>
<td color="green_bg">
<b>पुराने test फिर चलेंगे → नए और पुराने नतीजे मिलाए जाएँगे → गलती पकड़ में आएगी।</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b><u>backend/tests/fixtures/</u></b>
</td>
<td color="blue_bg">
<b>अलग-अलग जाँच में इस्तेमाल होने वाली नमूने की जानकारी रखना।</b>
</td>
<td color="blue_bg">
<b>अलग-अलग tests में इस्तेमाल करने के लिए sample investor, goals और सही जवाब रखना।</b>
</td>
<td color="blue_bg">
<b>Sample जानकारी tests को दी जाएगी → हर test उसी से शुरू हो सकेगा।</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b><u>backend/scripts/</u></b>
</td>
<td color="green_bg">
<b>सिस्टम की देखभाल, जानकारी लाने-ले जाने और एक बार के ज़रूरी काम चलाना।</b>
</td>
<td color="green_bg">
<b>ज़रूरत पड़ने पर data import करना या backend की एक बार की सफाई/देखभाल का काम चलाना।</b>
</td>
<td color="green_bg">
<b>कमांड दी जाएगी → script चलेगी → data import या तय maintenance का काम पूरा होगा।</b>
</td>
</tr>
</table>

## 🧩 2. Main Directories — Exact Responsibilities

### 🌐 2.1 <b>app/api/</b> — HTTP Boundary

The API layer is the inbound HTTP adapter for the backend. It exposes approved product operations, validates transport payloads, resolves request-scoped dependencies and converts application outcomes into safe HTTP responses. It does not own product workflows or business decisions.

#### 🗂️ 2.1.1 API Directory Map

<quote color="blue_bg">
<p />

<b>app/api/</b><br /><b>├── routers/</b><br /><b>│   ├── investor\_profile/</b> <b>(four sibling subfeature routers)</b><br /><b>│   ├── moneywheel/</b><br /><b>│   ├── goal\_planner/</b><br /><b>│   ├── strategy\_builder/</b><br /><b>│   ├── participate\_with\_your\_finances/</b><br /><b>│   ├── multi\_goal\_planning/</b> <b>(reserved)</b><br /><b>│   ├── reports/</b><br /><b>│   ├── history/</b><br /><b>│   └── action\_plan/</b><br /><b>├── schemas/</b> <b>(request / response DTOs)</b><br /><b>├── </b>[<b>router.py</b>](http://router.py) <b>(mounts approved feature routers)</b><br /><b>├── </b>[<b>dependencies.py</b>](http://dependencies.py)<br /><b>└── exception\_</b>[<b>handlers.py</b>](http://handlers.py)\\
</quote>

#### 📋 2.1.2 File & Directory Ownership

| Directory / file | What belongs here | Explicit boundary |
| --- | --- | --- |
| routers/ | HTTP endpoints grouped by approved product feature; Investor Profile exposes four sibling subfeature router areas. | No formulas, domain decisions, direct SQL or direct Supabase calls. |
| schemas/ | Request and response DTOs, transport validation and serialization contracts. | Not canonical domain models, persistence models or physical database schemas. |
| [router.py](http://router.py) | Registration and mounting of feature routers on the API application. | No feature use-case implementation or business orchestration. |
| [dependencies.py](http://dependencies.py) | Request-scoped wiring for authenticated actor, request context and application dependencies. | Does not implement product rules or concrete persistence behavior. |
| exception\_[handlers.py](http://handlers.py) | Maps known application/domain failures to safe, stable HTTP error responses. | Must not leak secrets, internal traces or unnecessary investor financial details. |

#### 🔁 2.1.3 Request Boundary & Dependency Rules

1. Receive the HTTP request and validate its transport shape through the relevant schema.
2. Resolve the authenticated actor and request-scoped application dependencies.
3. Invoke the owning application feature use case or an approved application workflow.
4. Map the returned application result to the approved response schema and HTTP status.
5. Convert known failures through centralized exception handlers; unexpected technical failures must not expose internal details.

<b>May depend on:</b> application entry points, API schemas, security dependencies and framework-level HTTP facilities.

<b>Must not depend on:</b> concrete database clients, SQL repositories, Supabase SDK calls, domain implementation internals or duplicated business logic.

### ⚙️ 2.2 <b>app/application/</b> — Use Cases & Workflow Coordination

This layer executes product use cases and coordinates workflows across features. It owns orchestration, input/output mapping, port usage and transaction coordination; it does not own financial formulas or feature domain rules.

#### 🗂️ 2.2.1 Application Directory Map

<quote color="blue_bg">
<p />

<b>app/application/</b><br /><b>├── features/</b><br /><b>│   ├── investor\_profile/</b><br /><b>│   ├── moneywheel/</b><br /><b>│   ├── goal\_planner/</b><br /><b>│   ├── strategy\_builder/</b><br /><b>│   ├── participate\_with\_your\_finances/</b><br /><b>│   ├── multi\_goal\_planning/</b> <b>(reserved boundary)</b><br /><b>│   ├── reports/</b><br /><b>│   ├── history/</b><br /><b>│   └── action\_plan/</b><br /><b>├── workflows/</b><br /><b>│   ├── investor\_situation\_assessment/</b> <b>(Chapter 07)</b><br /><b>│   ├── budgeting\_cash\_flow\_affordability/</b> <b>(Chapter 08)</b><br /><b>│   ├── planning\_lifecycle/</b> <b>(Goal Planner → Strategy Builder)</b><br /><b>│   ├── report\_preparation/</b> <b>(authoritative feature outputs → report)</b><br /><b>│   └── plan\_acceptance/</b> <b>(Chapter 13; explicit investor acceptance)</b><br /><b>├── ports/</b><br /><b>│   ├── repositories/</b><br /><b>│   ├── identity\_</b>[<b>provider.py</b>](http://provider.py)<br /><b>│   └── unit\_of\_</b>[<b>work.py</b>](http://work.py)<br /><b>└── shared/</b><br /><b>    ├── </b>[<b>result.py</b>](http://result.py)<br /><b>    └── </b>[<b>idempotency.py</b>](http://idempotency.py)\\
</quote>

#### 📋 2.2.2 File & Directory Ownership

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Directory / file
</td>
<td color="blue_bg">
What belongs here
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
features/investor\_profile/
</td>
<td color="blue_bg">
Investor Profile use cases: capture and update investor profile inputs; coordinate Financial State, Risk Profile, Behavioural Profile and Investor Preferences & Needs operations.
</td>
<td color="blue_bg">
Does not own profile interpretation rules, risk scoring or domain validation; those remain in Investor Profile domain.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
features/moneywheel/
</td>
<td color="green_bg">
Moneywheel use cases: request the approved financial-health assessment, gather required investor facts and return the domain assessment result.
</td>
<td color="green_bg">
Does not implement financial-health formulas or protection/resilience rules.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
features/goal\_planner/
</td>
<td color="blue_bg">
Goal Planner use cases: create and manage goals, gather required inputs and invoke goal-requirement and Goal Feasibility domain capabilities.
</td>
<td color="blue_bg">
Does not implement goal taxonomy, funding calculations or feasibility rules; it coordinates the owning domain capability.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
features/strategy\_builder/
</td>
<td color="green_bg">
Strategy Builder use cases: accept approved Goal Planner output, load relevant investor context and invoke funding-path, strategy applicability, viability and comparison capabilities.
</td>
<td color="green_bg">
Does not recalculate Goal Feasibility or own cross-feature planning orchestration.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
features/participate\_with\_your\_finances/
</td>
<td color="blue_bg">
Scenario use cases: create or evaluate investor-requested scenarios and coordinate sensitivity and decision-comparison operations.
</td>
<td color="blue_bg">
Does not mutate the authoritative Strategy Builder result or turn a scenario into plan acceptance.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
features/multi\_goal\_planning/ (reserved)
</td>
<td color="green_bg">
Reserved application boundary corresponding to the approved Multi-Goal Planning domain boundary.
</td>
<td color="green_bg">
No allocation, prioritisation or optimization use cases are defined until the detailed capability design is approved.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
features/reports/
</td>
<td color="blue_bg">
Report use cases: assemble authoritative outputs from owning features into the approved report view and request rendering when needed.
</td>
<td color="blue_bg">
Does not recalculate, reinterpret or change financial or strategy decisions; rendering implementation belongs in infrastructure.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
features/history/
</td>
<td color="green_bg">
History use cases: retrieve prior saved outcomes, versions and their traceable context for the investor.
</td>
<td color="green_bg">
Does not rewrite historical results or become the owner of feature data.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
features/action\_plan/
</td>
<td color="blue_bg">
Action Plan use cases: retrieve and manage the Action Plan after the Chapter 13 acceptance workflow authorizes creation or update.
</td>
<td color="blue_bg">
Does not treat a draft, recommendation or selected strategy as investor acceptance.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
workflows/investor\_situation\_assessment/
</td>
<td color="green_bg">
Chapter 07 investor/situation assessment sequence and the required cross-feature coordination for that workflow.
</td>
<td color="green_bg">
Coordinates domain capabilities; does not own their interpretation rules.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
workflows/budgeting\_cash\_flow\_affordability/
</td>
<td color="blue_bg">
Chapter 08 budgeting, cash-flow and affordability workflow sequence.
</td>
<td color="blue_bg">
Coordinates the approved workflow; calculation logic remains with its approved domain owner.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
workflows/planning\_lifecycle/
</td>
<td color="green_bg">
Approved planning sequence and cross-feature hand-offs, including passing approved Goal Planner output to the Strategy Builder application use case.
</td>
<td color="green_bg">
Does not move Goal Planner or Strategy Builder domain logic into the workflow; feature domains do not call one another directly.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
workflows/plan\_[acceptance.py](http://acceptance.py)
</td>
<td color="blue_bg">
Chapter 13 explicit investor acceptance flow and the transaction that creates or updates the Accepted Plan / Action Plan.
</td>
<td color="blue_bg">
A proposed or selected strategy is not acceptance; creation/update requires explicit investor acceptance.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
workflows/report\_preparation/
</td>
<td color="green_bg">
Coordinates report preparation by gathering authoritative outputs from their owning feature application modules and assembling the approved report view.
</td>
<td color="green_bg">
Does not recalculate, reinterpret or change financial or strategy decisions; rendering implementation belongs in infrastructure.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
ports/repositories/
</td>
<td color="blue_bg">
Repository interfaces required by application use cases and workflows.
</td>
<td color="blue_bg">
Contains contracts only; SQL and Supabase implementations belong in infrastructure.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
ports/identity\_[provider.py](http://provider.py)
</td>
<td color="green_bg">
Identity lookup contract consumed by application logic.
</td>
<td color="green_bg">
Does not implement authentication-provider SDK calls.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
ports/unit\_of\_[work.py](http://work.py)
</td>
<td color="blue_bg">
Transaction boundary contract used to coordinate atomic persistence.
</td>
<td color="blue_bg">
Does not contain a concrete database transaction implementation.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
shared/[result.py](http://result.py)
</td>
<td color="green_bg">
Generic application result contract for successful outcomes and expected failures.
</td>
<td color="green_bg">
Does not become a feature-specific domain result or HTTP response schema.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
shared/[idempotency.py](http://idempotency.py)
</td>
<td color="blue_bg">
Generic duplicate-operation protection mechanics for application commands.
</td>
<td color="blue_bg">
Does not define business authorization or feature decision rules.
</td>
</tr>
</table>

#### 🔁 2.2.3 Workflow Coordination & Feature Hand-offs

A <b>workflow</b> is an application-layer coordinator for a business process that spans multiple use cases, features or a required transaction boundary. It controls the sequence of calls, passes approved outputs between application use cases, and coordinates persistence through ports. It is not a place for financial calculations, domain decisions or a second copy of feature logic.

Use a workflow only when coordination is genuinely cross-feature or process-level. A task contained within one feature stays in that feature's application module; it should not be moved into workflows merely because it has several steps.

<b>Approved coordination paths</b>

1. <b>Investor / situation assessment (Chapter 07):</b> coordinate the required application use cases and supporting domain capabilities for the approved assessment sequence; keep interpretation and assessment rules in their owning domain modules.
2. <b>Budgeting, cash flow & affordability (Chapter 08):</b> coordinate the budgeting workflow and validation of period-matched income, expense and savings/investment evidence. Consume Chapter 05's canonical Available Monthly Surplus calculation; do not create a separate surplus formula. Pass the supported cash-flow evidence to Goal Planner, while Chapter 06 owns affordability constraints and Chapter 10 applies the affordability comparison to each goal-funding path.
3. <b>Planning lifecycle:</b> pass the approved Goal Planner result to the Strategy Builder application use case. Strategy Builder then invokes its own domain capability. Neither feature domain calls the other directly.
4. <b>Report preparation:</b> the Reports application use case gathers authoritative outputs from their owning features for presentation. It must not recalculate or alter those outputs.
5. <b>Plan acceptance (Chapter 13):</b> pass the investor's explicit acceptance decision and selected strategy context through the acceptance workflow; create or update the Accepted Plan / Action Plan only after acceptance is confirmed.

<b>Ownership rule:</b> feature application modules own feature-specific use cases and input/output mapping. Workflows own only cross-feature sequence and transaction coordination. Domain modules own business rules and calculations. Ports define the interfaces used to load and persist data.

<b>Must not contain:</b> FastAPI request objects, concrete database clients, SQL repositories, persistence models or duplicated financial formulas.

### 📚 2.3 <b>app/domain/canonical/</b> — Canonical Business Vocabulary

This is the shared definition layer for stable business taxonomies and measurement metadata used by multiple features. It is <b>not</b> the physical PostgreSQL schema and does not own feature workflows, investor records, evaluations, scenarios or plan lifecycles.

<quote color="blue_bg">
<p />

<b>app/domain/canonical/</b><br /><b>├── goal\_</b>[<b>taxonomy.py</b>](http://taxonomy.py)<br /><b>├── financial\_</b>[<b>categories.py</b>](http://categories.py)<br /><b>└── </b>[<b>measurements.py</b>](http://measurements.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
File
</td>
<td color="blue_bg">
Exact data / definitions owned by the file
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>goal\_</b>[<b>taxonomy.py</b>](http://taxonomy.py)
</td>
<td color="blue_bg">
Exactly the ten Chapter 03 canonical goal IDs and their approved names, definitions and contextual guidance. Child Education is contextual detail, not a separate goal ID. Goal instances, priorities, requirements and feasibility belong to Goal Planner / the relevant feature workflow.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>financial\_</b>[<b>categories.py</b>](http://categories.py)
</td>
<td color="green_bg">
Chapter 03 canonical Income, Expense, Asset and Liability category IDs, names, definitions and classification guidance. The approved insurance policy-type IDs are included in this file as part of the financial-category vocabulary; do not create a separate <b>insurance\_</b>[<b>taxonomy.py</b>](http://taxonomy.py). Category IDs alone do not establish liquidity, goal availability, tax treatment or formula eligibility.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
[<b>measurements.py</b>](http://measurements.py)
</td>
<td color="blue_bg">
Chapter 05 canonical measurement IDs, names, definitions, input references, units, periods, output contracts and assumptions. This file contains measurement metadata only; formula implementations live in <b>domain/shared/calculations/</b>.
</td>
</tr>
</table>

<b>Ownership boundaries</b>

- Investor authentication and access belong to <b>app/security/</b>; identity-provider contracts belong to <b>app/application/ports/</b>. No generic investor [<b>identity.py</b>](http://identity.py) is defined in canonical.
- Investor Profile and actual Financial State records belong to <b>domain/features/investor\_profile/</b>.
- Goal Planner, Strategy Builder and Multi-Goal Planning behavior belong to their respective <b>domain/features/</b> modules.
- Constraint definitions, applicability and evaluation belong to <b>domain/shared/constraints/</b>, governed by Chapter 06.
- Scenario and decision-comparison behavior belongs to <b>domain/features/participate\_with\_your\_finances/</b>.
- Accepted Plan and Action Plan lifecycle belongs to the Chapter 13 workflow and <b>domain/features/action\_plan/</b>.
- Reports and History belong to <b>domain/features/reports/</b> and <b>domain/features/history/</b>.
- Evaluation result contracts stay with the owning feature or shared evaluation capability; they are not a universal canonical file by default.
- 00.7 governs logical data domains, persistence, physical schema, version/history mechanisms and migrations.
- Canonical code must not import API schemas, ORM rows, database clients, FastAPI or Supabase SDKs.

### 🧱 2.4 <b>app/domain/features/</b> — Feature-Level Domain Map & File Ownership

Each folder owns the domain behavior of one approved product feature. This section documents <b>domain files only</b>. API routers/schemas, application use cases/workflows, repository ports, persistence mappers/adapters and tests remain in their respective technical-layer directories; they are not placed inside <b>domain/features/</b>.

#### 🗂️ 2.4.1 Complete Domain Directory Map

Feature-wise directory trees are placed with their respective ownership sections in 2.4.2 (A, B, C). This avoids maintaining duplicate maps and keeps each tree directly beside its file responsibilities.

#### 📋 2.4.2 File-by-File Ownership Table

#### 👤 A. Investor Profile

<quote color="green_bg">
<p />

<b>app/domain/features/investor\_profile/</b><br /><b>├── financial\_state/</b><br /><b>│   ├── </b>[<b>normalization.py</b>](http://normalization.py)<br /><b>│   ├── </b>[<b>validation.py</b>](http://validation.py)<br /><b>│   └── </b>[<b>readiness.py</b>](http://readiness.py)<br /><b>├── risk\_profile/</b><br /><b>│   ├── </b>[<b>profile.py</b>](http://profile.py)<br /><b>│   └── </b>[<b>assessment.py</b>](http://assessment.py)<br /><b>├── behavioural\_profile/</b><br /><b>│   ├── </b>[<b>profile.py</b>](http://profile.py)<br /><b>│   └── </b>[<b>interpretation.py</b>](http://interpretation.py)<br /><b>└── investor\_preferences\_needs/</b><br /><b>    ├── </b>[<b>preferences.py</b>](http://preferences.py)<br /><b>    └── </b>[<b>validation.py</b>](http://validation.py)\\
</quote>

These are four sibling subfeatures. Risk Profile is not a top-level product and is not nested inside Financial State.

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature / subfeature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Financial State
</td>
<td color="blue_bg">
<b>financial\_state/</b>[<b>normalization.py</b>](http://normalization.py)
</td>
<td color="blue_bg">
Normalizes Financial State values into the approved domain representation before validation and downstream use; keeps equivalent representations consistent where the approved contract defines how to interpret them.
</td>
<td color="blue_bg">
Does not invent aliases, conversion rates, default values, missing-data fallbacks or business thresholds. Transport parsing belongs at the API/application boundary; database/schema normalization remains governed by 00.7. This is a data-normalization capability, not a Chapter 06 constraint rule.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Financial State
</td>
<td color="green_bg">
<b>financial\_state/</b>[<b>validation.py</b>](http://validation.py)
</td>
<td color="green_bg">
Domain validation of normalized investor-supplied or evidenced financial facts against the approved Financial State contract.
</td>
<td color="green_bg">
Does not define a second data schema or persistence model; Chapter 04 and 00.7 remain authoritative for data contracts.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Financial State
</td>
<td color="blue_bg">
<b>financial\_state/</b>[<b>readiness.py</b>](http://readiness.py)
</td>
<td color="blue_bg">
Decision-specific readiness assessment and the limitations caused by missing, incomplete or unsuitable inputs.
</td>
<td color="blue_bg">
No universal readiness score, freshness threshold or automatic fallback unless separately approved.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Risk Profile
</td>
<td color="green_bg">
<b>risk\_profile/</b>[<b>profile.py</b>](http://profile.py)
</td>
<td color="green_bg">
Domain representation of the approved investor risk-profile dimensions and recorded profile context.
</td>
<td color="green_bg">
Does not invent dimensions or collapse risk capacity, tolerance and willingness into one value.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Risk Profile
</td>
<td color="blue_bg">
<b>risk\_profile/</b>[<b>assessment.py</b>](http://assessment.py)
</td>
<td color="blue_bg">
Assessment behavior using only the approved risk inputs and assessment contract.
</td>
<td color="blue_bg">
No invented questionnaire, scoring weights, bands or thresholds.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Behavioural Profile
</td>
<td color="green_bg">
<b>behavioural\_profile/</b>[<b>profile.py</b>](http://profile.py)
</td>
<td color="green_bg">
Domain representation of approved behavioral context relevant to financial decisions.
</td>
<td color="green_bg">
No unsupported personality types or behavioral taxonomy.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Behavioural Profile
</td>
<td color="blue_bg">
<b>behavioural\_profile/</b>[<b>interpretation.py</b>](http://interpretation.py)
</td>
<td color="blue_bg">
Interpretation of recorded behavioral context for downstream planning decisions, within approved rules.
</td>
<td color="blue_bg">
Does not diagnose the investor or create unsupported behavioral scores.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Investor Preferences & Needs
</td>
<td color="green_bg">
<b>investor\_preferences\_needs/</b>[<b>preferences.py</b>](http://preferences.py)
</td>
<td color="green_bg">
Investor-stated preferences, needs and priorities used as planning context.
</td>
<td color="green_bg">
A preference is not proof of suitability, feasibility or acceptance.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Investor Preferences & Needs
</td>
<td color="blue_bg">
<b>investor\_preferences\_needs/</b>[<b>validation.py</b>](http://validation.py)
</td>
<td color="blue_bg">
Validation of preference/need inputs against the approved feature contract.
</td>
<td color="blue_bg">
Does not override hard constraints or authorize a transaction.
</td>
</tr>
</table>

<b>Dependencies and history ownership:</b> Investor Profile uses Chapter 03 canonical category/goal vocabulary and the Chapter 04 Financial State contract, together with approved evidence and assessment inputs. It owns investor profile and financial facts at the domain level; authentication belongs to security, canonical definitions remain in <b>domain/canonical/</b>, and physical storage remains governed by 00.7. When investor data is persisted or materially changed, its record identity, prior/current value context, provenance and applicable version references must remain traceable through History; History does not redefine the Financial State contract.

#### 🛡️ B. Moneywheel

<quote color="purple_bg">
<p />

<b>app/domain/features/moneywheel/</b><br /><b>├── </b>[<b>assessment.py</b>](http://assessment.py)<br /><b>├── </b>[<b>resilience.py</b>](http://resilience.py)<br /><b>├── </b>[<b>protection.py</b>](http://protection.py)<br /><b>├── </b>[<b>findings.py</b>](http://findings.py)<br /><b>└── </b>[<b>explanation.py</b>](http://explanation.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Moneywheel
</td>
<td color="blue_bg">
<b>moneywheel/</b>[<b>assessment.py</b>](http://assessment.py)
</td>
<td color="blue_bg">
Chapter 09 domain-level assessment orchestration: select relevant validated evidence and approved measurements, then coordinate the applicable resilience and protection assessments.
</td>
<td color="blue_bg">
Does not duplicate formulas, create another Financial State source, or produce a combined health score/pass-fail result.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Moneywheel
</td>
<td color="green_bg">
<b>moneywheel/</b>[<b>resilience.py</b>](http://resilience.py)
</td>
<td color="green_bg">
Assessment of the relevant resilience dimensions: access to money, cash-flow continuity, debt pressure, financial flexibility, and concentration/dependency; explain material interactions between them.
</td>
<td color="green_bg">
Does not invent resilience scores, severity bands, thresholds, or liquidity/accessibility classifications.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Moneywheel
</td>
<td color="blue_bg">
<b>moneywheel/</b>[<b>protection.py</b>](http://protection.py)
</td>
<td color="blue_bg">
Material adverse-event exposure, confirmed policy evidence, confirmed versus possible protection gaps, and premium affordability trade-offs.
</td>
<td color="blue_bg">
Does not infer policy validity/adequacy from sum assured or a ratio alone; insurance calculation policy and input scope remain subject to their canonical owners and Chapter 06 decision boundary.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Moneywheel
</td>
<td color="green_bg">
<b>moneywheel/</b>[<b>findings.py</b>](http://findings.py)
</td>
<td color="green_bg">
Structured assessment findings using the Chapter 09 output elements: Finding, Evidence (including date and actual/forecast/scenario status), Impact, Uncertainty, and Investor Consideration.
</td>
<td color="green_bg">
Does not add universal severity labels, unsupported conclusions, or a combined score.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Moneywheel
</td>
<td color="blue_bg">
<b>moneywheel/</b>[<b>explanation.py</b>](http://explanation.py)
</td>
<td color="blue_bg">
Domain-level explanation of findings, evidence, uncertainty, interactions, and practical trade-offs.
</td>
<td color="blue_bg">
Does not render UI/PDF, make unsupported recommendations, or change investor records.
</td>
</tr>
</table>

<b>Insurance calculation caution:</b> Chapter 09 records an existing repository formula and mixed-policy implementation, but explicitly flags the input-scope treatment for verification. Do not treat that legacy implementation as a newly approved canonical formula or adequacy standard. Chapter 05 owns measurement/calculation methods; Chapter 06 owns the insurance decision boundary; policy evidence remains sourced from Financial State.

<b>Dependencies and history ownership:</b> Moneywheel consumes validated Investor Profile / Financial State evidence, canonical measurements, shared calculations, evidence and applicable constraints. It owns Chapter 09 assessment, resilience/protection interpretation and findings. If an assessment result is saved as an investor record, its original evidence, assumptions and calculation/version context must be traceable; History must not recompute it under later rules.

#### 🎯 C. Goal Planner

<quote color="yellow_bg">
<p />

<b>app/domain/features/goal\_planner/</b><br /><b>├── </b>[<b>requirement.py</b>](http://requirement.py)<br /><b>└── </b>[<b>feasibility.py</b>](http://feasibility.py)
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Goal Planner
</td>
<td color="blue_bg">
<b>goal\_planner/</b>[<b>requirement.py</b>](http://requirement.py)
</td>
<td color="blue_bg">
Chapter 10 Goal Requirement domain contract: target amount/requirement context derived from the canonical goal and approved inputs.
</td>
<td color="blue_bg">
Goal instances are feature-owned; canonical goal identity remains in <b>domain/canonical/goal\_</b>[<b>taxonomy.py</b>](http://taxonomy.py); formulas remain in shared calculations.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Goal Planner
</td>
<td color="green_bg">
<b>goal\_planner/</b>[<b>feasibility.py</b>](http://feasibility.py)
</td>
<td color="green_bg">
Chapter 10 Goal Feasibility domain contract and supported feasibility outcome classification using resources, contribution capacity and applicable constraints.
</td>
<td color="green_bg">
Feasibility is one test; funding methods are options, not separate tests. Do not add unapproved methods or rules.
</td>
</tr>
</table>

<b>Dependencies and history ownership:</b> Goal Planner consumes canonical goal identity, Investor Profile / Financial State inputs, shared Chapter 05 calculations, cash-flow/affordability capabilities, constraints and evidence. It owns Goal Requirement and individual Goal Feasibility outputs. Each saved planning run must retain its approved input context, requirement/feasibility outputs, assumptions, evidence and relevant calculation/version references so the historical result can be understood as originally produced; History does not rerun the planner using current formulas.

#### 🧠 D. Strategy Builder

<quote color="orange_bg">
<p />

<b>app/domain/features/strategy\_builder/</b><br /><b>├── funding\_</b>[<b>paths.py</b>](http://paths.py)<br /><b>├── asset\_</b>[<b>assessment.py</b>](http://assessment.py)<br /><b>├── </b>[<b>projections.py</b>](http://projections.py)<br /><b>├── </b>[<b>financing.py</b>](http://financing.py)<br /><b>├── investment\_</b>[<b>planning.py</b>](http://planning.py)<br /><b>├── payment\_</b>[<b>withdrawal.py</b>](http://withdrawal.py)<br /><b>├── </b>[<b>monitoring.py</b>](http://monitoring.py)<br /><b>└── </b>[<b>comparison.py</b>](http://comparison.py)\\
</quote>

<p />

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Strategy Builder
</td>
<td color="blue_bg">
<b>strategy\_builder/funding\_</b>[<b>paths.py</b>](http://paths.py)
</td>
<td color="blue_bg">
The two and only top-level Goal Funding Strategy paths: Self Money and Self Money + Financing; their distinct inputs, applicability and assessment boundary.
</td>
<td color="blue_bg">
No separate canonical-strategy catalogue or extra top-level funding path. Do not select either path automatically.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Strategy Builder
</td>
<td color="green_bg">
<b>strategy\_builder/asset\_</b>[<b>assessment.py</b>](http://assessment.py)
</td>
<td color="green_bg">
Assessment of relevant assets as inputs to the approved funding-path design, including availability, liquidity/restrictions, suitability and competing commitments where evidence supports them.
</td>
<td color="green_bg">
Asset classification and actual records remain owned by Financial State; do not infer liquidity or goal availability from category alone.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Strategy Builder
</td>
<td color="blue_bg">
<b>strategy\_builder/</b>[<b>projections.py</b>](http://projections.py)
</td>
<td color="blue_bg">
Year-by-year funding projection contracts for dated contributions, asset growth, financing/repayments and goal payments.
</td>
<td color="blue_bg">
Uses Chapter 05/shared calculation outputs and approved daily/date-order conventions; no duplicated financial formulas or guaranteed-return claims.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Strategy Builder
</td>
<td color="green_bg">
<b>strategy\_builder/</b>[<b>financing.py</b>](http://financing.py)
</td>
<td color="green_bg">
Financing assessment within the approved Self Money + Financing path, including evidenced terms, cost, repayment and cash-flow effects.
</td>
<td color="green_bg">
No invented lender eligibility, borrowing terms, interest-rate assumptions or financing products.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Strategy Builder
</td>
<td color="blue_bg">
<b>strategy\_builder/investment\_</b>[<b>planning.py</b>](http://planning.py)
</td>
<td color="blue_bg">
Investment structure/allocation, techniques and product-option assessment, validation and comparison within the goal-funding design.
</td>
<td color="blue_bg">
No mandatory technique/product for every goal; no implementation or asset changes without investor approval.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Strategy Builder
</td>
<td color="green_bg">
<b>strategy\_builder/payment\_</b>[<b>withdrawal.py</b>](http://withdrawal.py)
</td>
<td color="green_bg">
Matching goal payment dates/amounts to available funds; assessment of net proceeds, costs/taxes where applicable, remaining assets, liquidity and cross-goal effects.
</td>
<td color="green_bg">
No sale, withdrawal, transfer or reallocation without explicit investor approval.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Strategy Builder
</td>
<td color="blue_bg">
<b>strategy\_builder/</b>[<b>monitoring.py</b>](http://monitoring.py)
</td>
<td color="blue_bg">
Monitoring of the goal-funding projection/assumptions, funding-gap identification and contingency-option assessment under Chapter 11.
</td>
<td color="blue_bg">
Does not own Accepted Plan adoption, Action Plan lifecycle or execution tracking; those remain Chapter 13.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Strategy Builder
</td>
<td color="green_bg">
<b>strategy\_builder/</b>[<b>comparison.py</b>](http://comparison.py)
</td>
<td color="green_bg">
Like-for-like comparison of the Self Money and Self Money + Financing paths, their supported implementation options, assumptions, constraints and trade-offs.
</td>
<td color="green_bg">
Does not accept a plan, authorize borrowing or execute a transaction.
</td>
</tr>
</table>

<b>Dependencies and history ownership:</b> Strategy Builder consumes Goal Planner's approved requirement/feasibility handoff, relevant Financial State assets and evidence, shared calculations and applicable constraints. It owns assessment of the two funding paths and their projections/comparison, not goal requirement recalculation. Each saved funding-path assessment must retain the path assessed, relevant inputs/asset decisions, assumptions, financing evidence where applicable, projection/comparison outputs and version references. A saved assessment is not investor acceptance or transaction authorization.

#### 🔄 E. Participate with Your Finances

<quote color="green_bg">
<p />

<b>app/domain/features/participate\_with\_your\_finances/</b><br /><b>├── </b>[<b>sensitivity.py</b>](http://sensitivity.py)<br /><b>├── </b>[<b>scenarios.py</b>](http://scenarios.py)<br /><b>└── decision\_</b>[<b>comparison.py</b>](http://comparison.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Participate with Your Finances
</td>
<td color="blue_bg">
<b>participate\_with\_your\_finances/</b>[<b>sensitivity.py</b>](http://sensitivity.py)
</td>
<td color="blue_bg">
Sensitivity-analysis domain behavior for changing approved input assumptions and examining resulting differences.
</td>
<td color="blue_bg">
Hypothetical changes must not mutate actual Financial State or Accepted Plan.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Participate with Your Finances
</td>
<td color="green_bg">
<b>participate\_with\_your\_finances/</b>[<b>scenarios.py</b>](http://scenarios.py)
</td>
<td color="green_bg">
Hypothetical scenario representation and scenario-domain behavior.
</td>
<td color="green_bg">
A scenario is not actual Financial State, an investor decision or plan acceptance.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Participate with Your Finances
</td>
<td color="blue_bg">
<b>participate\_with\_your\_finances/decision\_</b>[<b>comparison.py</b>](http://comparison.py)
</td>
<td color="blue_bg">
Comparison of decision alternatives using supported scenario/evaluation outputs and relevant trade-offs.
</td>
<td color="blue_bg">
Does not force a winner or silently adopt an alternative.
</td>
</tr>
</table>

<b>What-If boundary:</b> What-If is an interaction using one or more of these three capabilities, not a separate feature, calculation engine or additional file.

<b>Dependencies and ownership:</b> Participate with Your Finances consumes baseline outputs from the relevant planning features plus shared calculations, constraints, evidence and versioning. It owns sensitivity analysis, hypothetical scenarios and decision comparisons. Saved scenarios/comparisons may retain their hypothetical inputs and source-version references, but must remain distinguishable from actual investor data and accepted decisions; hypothetical changes never mutate Financial State or Accepted Plan.

#### 🧮 F. Multi-Goal Planning

Multi-Goal Planning is the domain coordination capability for assessing an investor's goals together. It consumes approved goal-level requirements, feasibility and funding outputs; it does not replace Goal Planner or Strategy Builder. The investor-facing Goal Basket is a grouping/selection interface for choosing multiple existing goals to assess together; it is not a second planning engine and does not replace this domain capability.

The following is the proposed file-level domain design recorded in this blueprint for review. It defines capability ownership, not allocation formulas, prioritisation algorithms, thresholds or automatic decisions; those require explicit approval before implementation.

<quote color="purple_bg">
<p />

<b>app/domain/features/multi\_goal\_planning/</b><br /><b>├── goal\_</b>[<b>coordination.py</b>](http://coordination.py)<br /><b>├── shared\_</b>[<b>resources.py</b>](http://resources.py)<br /><b>├── resource\_</b>[<b>allocation.py</b>](http://allocation.py)<br /><b>├── </b>[<b>prioritisation.py</b>](http://prioritisation.py)<br /><b>├── cross\_goal\_</b>[<b>impact.py</b>](http://impact.py)<br /><b>└── consolidated\_</b>[<b>plan.py</b>](http://plan.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Multi-Goal Planning
</td>
<td color="blue_bg">
<b>multi\_goal\_planning/goal\_</b>[<b>coordination.py</b>](http://coordination.py)
</td>
<td color="blue_bg">
Coordinates selected goals in one planning context and assesses their combined multi-goal feasibility using approved goal-level requirements, Goal Planner feasibility results, Strategy Builder funding assessments/projections, shared-resource availability and applicable constraints. Coordinates reassessment after proposed goal adjustments and allocation changes, then produces the refreshed combined feasibility context.
</td>
<td color="blue_bg">
Does not recalculate an individual goal's requirement or Goal Feasibility. If a proposed amount or target-date change changes an individual goal requirement, the revised requirement and individual feasibility must be recalculated by Goal Planner before the combined assessment is refreshed.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Multi-Goal Planning
</td>
<td color="green_bg">
<b>multi\_goal\_planning/shared\_</b>[<b>resources.py</b>](http://resources.py)
</td>
<td color="green_bg">
Identifies resources relevant to more than one goal, including potential shared assets, investments and contribution capacity, and exposes overlaps or possible double-allocation conflicts where supported by evidence.
</td>
<td color="green_bg">
Does not assume an asset or contribution is available to every goal, duplicate Financial State records, or decide that a resource is committed to a goal.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Multi-Goal Planning
</td>
<td color="blue_bg">
<b>multi\_goal\_planning/resource\_</b>[<b>allocation.py</b>](http://allocation.py)
</td>
<td color="blue_bg">
Represents and assesses alternative allocations of evidenced available resources and contribution capacity across selected goals, including the resulting goal-wise and combined funding positions; supports reassessment when an allocation is adjusted.
</td>
<td color="blue_bg">
Does not invent an optimisation algorithm or allocation formula, automatically assign/reassign/sell/withdraw assets, or override investor-approved commitments.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Multi-Goal Planning
</td>
<td color="green_bg">
<b>multi\_goal\_planning/</b>[<b>prioritisation.py</b>](http://prioritisation.py)
</td>
<td color="green_bg">
Assesses alternative goal priorities and sequencing using investor-stated preferences/priorities, timelines, approved feasibility/funding outputs and applicable constraints; provides priority alternatives for multi-goal reassessment.
</td>
<td color="green_bg">
Does not invent priority weights, scoring bands or a universal ranking formula; it does not silently change investor-stated priorities or force a priority order.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Multi-Goal Planning
</td>
<td color="blue_bg">
<b>multi\_goal\_planning/cross\_goal\_</b>[<b>impact.py</b>](http://impact.py)
</td>
<td color="blue_bg">
Assesses cross-goal effects of proposed adjustments to a goal's target amount, target timeline, priority or resource allocation—including how reducing one goal's amount or extending its timeline changes other goals' funding positions, resource availability and combined feasibility.
</td>
<td color="blue_bg">
Does not own or recalculate the adjusted goal's individual requirement/Goal Feasibility (Goal Planner does that); does not mutate actual Financial State or treat hypothetical adjustments as accepted decisions. Scenario mechanics remain with Participate with Your Finances.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Multi-Goal Planning
</td>
<td color="green_bg">
<b>multi\_goal\_planning/consolidated\_</b>[<b>plan.py</b>](http://plan.py)
</td>
<td color="green_bg">
Assembles the coordinated multi-goal result: combined feasibility outcome, goal-wise funding positions, shared-resource overlaps, proposed amount/timeline/priority/allocation adjustments, cross-goal impacts, shortfalls and trade-offs.
</td>
<td color="green_bg">
Does not create an Accepted Plan, authorize transactions or render reports; explicit acceptance remains governed by Chapter 13 and report rendering by the reporting layer.
</td>
</tr>
</table>

<b>Dependency and ownership boundaries:</b> Multi-Goal Planning consumes Goal Planner's goal requirements and individual feasibility results, Strategy Builder's funding-path assessments/projections, Investor Profile's Financial State and preferences/needs, and applicable shared constraints/evidence. It owns the combined multi-goal feasibility assessment and coordinates reassessment of proposed goal amount, timeline, priority and resource-allocation adjustments. When an adjustment changes an individual goal's requirement, Goal Planner recalculates that goal's requirement and individual feasibility; Multi-Goal Planning then reassesses the combined position. It must not duplicate individual calculations or mutate actual investor records. Goal Basket selects/groups existing goals; the domain capability performs the coordination. The saved consolidated result must retain the selected goal set, goal-wise and combined funding positions, shared-resource/allocation context, priorities, proposed adjustments, cross-goal impacts, shortfalls, trade-offs and relevant source-version references. History preserves that result as produced; it does not independently recalculate it.

#### 📊 G. Reports

<quote color="blue_bg">
<p />

<b>app/domain/features/reports/</b><br /><b>└── report\_</b>[<b>scope.py</b>](http://scope.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Reports
</td>
<td color="blue_bg">
<b>reports/report\_</b>[<b>scope.py</b>](http://scope.py)
</td>
<td color="blue_bg">
Defines the scope and approved content for the two report types: (1) Individual Goal Report, based on the selected goal's Goal Planner requirement/feasibility and relevant Strategy Builder funding-path assessment/projection; and (2) Goal Basket Report, based on the selected set of goals and Multi-Goal Planning's combined feasibility, shared-resource/allocation context, priorities, cross-goal impacts, shortfalls and trade-offs. Both retain relevant decision context and version references.
</td>
<td color="blue_bg">
Does not calculate or recalculate goal/multi-goal outcomes, create independent policy, change investor decisions or accept a plan; report rendering belongs to infrastructure.
</td>
</tr>
</table>

<b>Dependencies and history ownership:</b> Reports consumes authoritative Goal Planner and Strategy Builder outputs for an Individual Goal Report, and the selected goal set plus Multi-Goal Planning consolidated output for a Goal Basket Report. It owns only scope/content inclusion rules. Each generated report must be retained with its generated content, generation context and source output/version references; a historical report is not silently regenerated from current data. Rendering remains infrastructure-owned.

#### 🧾 H. History — Financial Record, Decision & Report Audit Trail

History is the cross-feature capability that preserves and retrieves historical investor records, saved planning outputs, generated reports and material decision context. It links each retained record to its owning feature and the applicable source data, evidence, assumptions and version references, so the historical result can be interpreted as it existed at the time. This is important for an RIA operating model, subject to applicable legal and regulatory recordkeeping requirements.

<quote color="blue_bg">
<p />

<b>app/domain/features/history/</b><br /><b>└── history\_</b>[<b>records.py</b>](http://records.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
History
</td>
<td color="blue_bg">
<b>history/history\_</b>[<b>records.py</b>](http://records.py)
</td>
<td color="blue_bg">
Domain-level contract for identifying, relating and interpreting historical investor-data records, saved Goal Planner runs, Strategy Builder assessments/projections, Multi-Goal Planning consolidated results, generated Individual Goal and Goal Basket Reports, and material investor decision/change records. It preserves the original context and links to relevant evidence and version references.
</td>
<td color="blue_bg">
Does not duplicate the owning feature's business logic or redefine its records; does not recalculate/overwrite historical outcomes or invent physical schema, event semantics, query filters, retention/deletion policy or immutable-storage technology. Those mechanisms remain governed by 00.7 and applicable legal/compliance requirements.
</td>
</tr>
</table>

<b>Cross-layer ownership:</b> <b>app/application/features/</b>[<b>history.py</b>](http://history.py) coordinates history retrieval use cases through repository ports; <b>app/application/ports/repositories/reports\_</b>[<b>history.py</b>](http://history.py) defines the required repository contract; <b>app/infrastructure/persistence/repositories/reports\_</b>[<b>history.py</b>](http://history.py) implements persistence access. Physical storage, version/snapshot mechanics, retention and deletion remain subject to 00.7 and applicable legal/compliance review.

#### ✅ I. Accepted Plan & Action Plan

The Accepted Plan and Action Plan are separate concepts in the system architecture. Chapter 13 owns explicit adoption and both lifecycles; the application workflow coordinates acceptance. The physical/domain contract for Accepted Plan remains open in Chapter 13, so no speculative Accepted Plan domain files are added here.

<quote color="green_bg">
<p />

<b>app/domain/features/action\_plan/</b><br /><b>├── </b>[<b>actions.py</b>](http://actions.py)<br /><b>└── </b>[<b>lifecycle.py</b>](http://lifecycle.py)\\
</quote>

Acceptance workflow ownership (application layer, not domain feature logic):

<quote color="orange_bg">
<p />

<b>app/application/workflows/</b><br /><b>└── plan\_</b>[<b>acceptance.py</b>](http://acceptance.py)\\
</quote>

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Feature
</td>
<td color="blue_bg">
File
</td>
<td color="blue_bg">
What belongs inside this file
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Accepted Plan / Action Plan
</td>
<td color="blue_bg">
<b>application/workflows/plan\_</b>[<b>acceptance.py</b>](http://acceptance.py)
</td>
<td color="blue_bg">
Application workflow that coordinates the explicit investor acceptance gate and invokes the approved Accepted Plan lifecycle contract when finalized.
</td>
<td color="blue_bg">
Does not invent acceptance choices, event semantics or persistence fields; Chapter 13's acceptance contract remains open.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Action Plan
</td>
<td color="green_bg">
<b>action\_plan/</b>[<b>actions.py</b>](http://actions.py)
</td>
<td color="green_bg">
Domain representation and invariants for actions derived from an explicitly Accepted Plan.
</td>
<td color="green_bg">
An action list is not plan acceptance or transaction authorization; do not invent amounts, deadlines or statuses.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Action Plan
</td>
<td color="blue_bg">
<b>action\_plan/</b>[<b>lifecycle.py</b>](http://lifecycle.py)
</td>
<td color="blue_bg">
Action lifecycle boundary and approved transitions only when Chapter 13 finalizes them.
</td>
<td color="blue_bg">
Chapter 13's unresolved status and lifecycle contract gaps remain open; do not treat legacy status observations as approved vocabulary.
</td>
</tr>
</table>

<b>Dependencies and history ownership:</b> The acceptance workflow consumes the explicit investor decision and the approved planning outputs/version context being adopted. Chapter 13 owns acceptance semantics; the application workflow coordinates adoption, while Action Plan domain files own action definitions and lifecycle boundaries. Once Chapter 13 finalizes the acceptance contract, the acceptance decision and resulting Accepted Plan/Action Plan version relationship must be traceable in History. A scenario, recommendation or report is not acceptance.

### 🔧 2.5 <b>app/domain/shared/</b> — Reusable Domain Capabilities

#### 🌳 Complete Directory Map

<quote color="orange_bg">
<p />

<b>app/domain/shared/</b><br /><b>├── calculations/</b><br /><b>│   ├── </b>[<b>engine.py</b>](http://engine.py)<br /><b>│   ├── </b>[<b>registry.py</b>](http://registry.py)<br /><b>│   ├── </b>[<b>result.py</b>](http://result.py)<br /><b>│   ├── </b>[<b>versions.py</b>](http://versions.py)<br /><b>│   ├── financial\_</b>[<b>position.py</b>](http://position.py)<br /><b>│   ├── financial\_</b>[<b>health.py</b>](http://health.py)<br /><b>├── constraints/</b><br /><b>│   ├── </b>[<b>catalog.py</b>](http://catalog.py)<br /><b>│   ├── </b>[<b>applicability.py</b>](http://applicability.py)<br /><b>│   ├── </b>[<b>evaluator.py</b>](http://evaluator.py)<br /><b>│   └── </b>[<b>result.py</b>](http://result.py)<br /><b>├── evidence/</b><br /><b>│   ├── </b>[<b>provenance.py</b>](http://provenance.py)<br /><b>│   └── </b>[<b>explanation.py</b>](http://explanation.py)<br /><b>├── readiness/</b><br /><b>│   └── </b>[<b>validator.py</b>](http://validator.py)<br /><b>├── versioning/</b><br /><b>│   ├── </b>[<b>references.py</b>](http://references.py)<br /><b>│   └── </b>[<b>snapshots.py</b>](http://snapshots.py)<br /><b>└── </b>[<b>value\_objects.py</b>](http://value_objects.py)\\
</quote>

The tree above is the directory-level view of every folder and file documented in the ownership table below. It is a target architecture map, not confirmation that these files already exist in the repository.

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Folder / file
</td>
<td color="blue_bg">
What belongs inside
</td>
<td color="blue_bg">
Must stay out
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
calculations/[engine.py](http://engine.py)
</td>
<td color="blue_bg">
Coordinates approved calculation execution.
</td>
<td color="blue_bg">
Feature decision policy.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
calculations/[registry.py](http://registry.py)
</td>
<td color="green_bg">
Registers canonical calculation IDs and implementations.
</td>
<td color="green_bg">
Unapproved metrics or duplicate IDs.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
calculations/[result.py](http://result.py)
</td>
<td color="blue_bg">
Standard output, units, period and limitation metadata.
</td>
<td color="blue_bg">
Constraint effects.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
calculations/[versions.py](http://versions.py)
</td>
<td color="green_bg">
Calculation method/version references.
</td>
<td color="green_bg">
Database version tables.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
calculations/financial\_[position.py](http://position.py)
</td>
<td color="blue_bg">
Chapter 05 financial-position measurement family.
</td>
<td color="blue_bg">
One-file-per-metric decomposition.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
calculations/financial\_[health.py](http://health.py)
</td>
<td color="green_bg">
Chapter 05 financial-health measurement family.
</td>
<td color="green_bg">
Moneywheel presentation.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
calculations/specialized\_[planning.py](http://planning.py)
</td>
<td color="blue_bg"></td>
<td color="blue_bg">
Unapproved return assumptions/methods.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
constraints/[catalog.py](http://catalog.py)
</td>
<td color="green_bg">
Single Chapter 06 rule catalogue representation.
</td>
<td color="green_bg">
Parallel feature rule catalogues.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
constraints/[applicability.py](http://applicability.py)
</td>
<td color="blue_bg">
Select approved rules for a decision context.
</td>
<td color="blue_bg">
Invented eligibility policy.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
constraints/[evaluator.py](http://evaluator.py)
</td>
<td color="green_bg">
Execute approved rule evaluations.
</td>
<td color="green_bg">
New thresholds, effects or formulas.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
constraints/[result.py](http://result.py)
</td>
<td color="blue_bg">
Status, evidence, missing-input, explanation and version references.
</td>
<td color="blue_bg">
Treating missing evidence as Pass.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
evidence/\{[provenance.py](http://provenance.py), [explanation.py](http://explanation.py)\}
</td>
<td color="green_bg">
Evidence source/context and explanations.
</td>
<td color="green_bg">
Invented evidence-quality scores.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
readiness/[validator.py](http://validator.py)
</td>
<td color="blue_bg">
Generic reusable validation mechanics.
</td>
<td color="blue_bg">
Duplicate Financial State readiness rules.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
versioning/\{[references.py](http://references.py), [snapshots.py](http://snapshots.py)\}
</td>
<td color="green_bg">
Generic version references and immutable input snapshots.
</td>
<td color="green_bg">
Physical retention/deletion policy.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
[value\_objects.py](http://value_objects.py)
</td>
<td color="blue_bg">
Strongly typed shared values.
</td>
<td color="blue_bg">
API DTOs or ORM models.
</td>
</tr>
</table>

### 🔌 2.6 <b>app/infrastructure/</b> — Technical Adapters

Infrastructure implements the technical details required by application ports and external providers. It connects the domain/application core to persistence, identity services, report rendering and operational instrumentation. It is an adapter layer, not an owner of financial formulas or product policy.

#### 🗂️ 2.6.1 Infrastructure Directory Map

<quote color="blue_bg">
<p />

<b>app/infrastructure/</b><br /><b>├── persistence/</b><br /><b>│   ├── </b>[<b>database.py</b>](http://database.py)<br /><b>│   ├── </b>[<b>transaction.py</b>](http://transaction.py)<br /><b>│   ├── mappers/</b><br /><b>│   └── repositories/</b><br /><b>├── providers/</b><br /><b>│   └── supabase/</b><br /><b>│       ├── </b>[<b>client.py</b>](http://client.py)<br /><b>│       └── </b>[<b>identity.py</b>](http://identity.py)<br /><b>├── reporting/</b><br /><b>│   └── pdf\_</b>[<b>renderer.py</b>](http://renderer.py)<br /><b>└── observability/</b><br /><b>    └── request\_</b>[<b>context.py</b>](http://context.py)\\
</quote>

#### 📋 2.6.2 File & Directory Ownership

| Directory / file | What belongs here | Explicit boundary |
| --- | --- | --- |
| persistence/[database.py](http://database.py) | Database connection/session setup using the PostgreSQL/Supabase access method approved by 00.7. | Does not define guessed tables, columns, indexes or schema policy. |
| persistence/[transaction.py](http://transaction.py) | Concrete transaction and unit-of-work mechanics implementing the application contract. | Does not redefine application transaction semantics or own business decisions. |
| persistence/mappers/ | Translation between canonical/domain objects and the finalized physical persistence representation. | Does not make business decisions or silently discard domain meaning. |
| persistence/repositories/ | Concrete implementations of application repository ports, including investor/record owner-scoped access. | SQL and provider details stay behind these adapters; no domain formulas. |
| providers/supabase/[client.py](http://client.py) | Server-side Supabase client configuration and construction. | No browser-side secrets or product behavior. |
| providers/supabase/[identity.py](http://identity.py) | Adapter translating the approved identity-provider interface to Supabase identity operations. | No product profile, Financial State facts or authorization policy ownership. |
| reporting/pdf\_[renderer.py](http://renderer.py) | Rendering of an already assembled and approved report payload. | No report data assembly, recalculation or change to plan decisions. |
| observability/request\_[context.py](http://context.py) | Request correlation and operational context used for diagnostics. | No secrets or unnecessary investor financial details in logs. |

#### 🔁 2.6.3 Adapter & Schema Boundaries

- Infrastructure implements interfaces defined by the application layer; application code must not import concrete infrastructure adapters.
- Persistence mapping follows the canonical/domain contracts and the finalized physical schema governed by 00.7.
- Report rendering consumes the authoritative report view assembled by the Reports application capability.
- Provider SDK calls remain server-side and isolated behind adapters.

<quote color="orange_bg">
<b>Physical schema warning</b>

Do not create guessed ORM models, table names, columns, indexes or migration tooling from this directory map. Chapter 00.7 remains authoritative for physical schema and persistence decisions.
</quote>

### 🔐 2.7 <b>app/security/</b> & <b>app/core/</b> — Access Control & Runtime Foundation

Security owns backend identity verification and access-control enforcement. Core owns technical runtime configuration and cross-cutting application mechanics. Neither area owns financial suitability, investment rules or product calculations.

#### 🗂️ 2.7.1 Security & Core Directory Map

<quote color="blue_bg">
<p />

<b>app/</b><br /><b>├── security/</b><br /><b>│   ├── </b>[<b>authentication.py</b>](http://authentication.py)<br /><b>│   ├── </b>[<b>authorization.py</b>](http://authorization.py)<br /><b>│   └── </b>[<b>policies.py</b>](http://policies.py)<br /><b>└── core/</b><br /><b>    ├── </b>[<b>settings.py</b>](http://settings.py)<br /><b>    ├── </b>[<b>exceptions.py</b>](http://exceptions.py)<br /><b>    └── </b>[<b>logging.py</b>](http://logging.py)\\
</quote>

#### 📋 2.7.2 File Ownership

| File | What belongs here | Explicit boundary |
| --- | --- | --- |
| security/[authentication.py](http://authentication.py) | Backend validation of the authenticated identity presented for a request. | Never trust frontend-supplied identity claims as proof; no product profile logic. |
| security/[authorization.py](http://authorization.py) | Investor/record ownership checks and permission enforcement before protected operations. | Does not replace repository-level owner scoping or invent product eligibility rules. |
| security/[policies.py](http://policies.py) | Reusable composition of access-control policies and permission checks. | Access control only; not financial suitability, risk scoring or Chapter 06 constraints. |
| core/[settings.py](http://settings.py) | Typed runtime configuration loaded from approved environment/configuration sources. | No committed secrets or investor-specific data. |
| core/[exceptions.py](http://exceptions.py) | Application-wide technical exception types and stable error categorization. | Domain meaning remains in domain errors; HTTP mapping remains in API handlers. |
| core/[logging.py](http://logging.py) | Safe structured logging and diagnostic conventions. | No secrets, credentials, tokens or unnecessary investor financial details. |

#### 🔁 2.7.3 Security & Runtime Rules

1. Authenticate the actor at the backend boundary before protected operations.
2. Authorize access to the specific investor-owned record; never rely solely on client-provided ownership identifiers.
3. Apply access-control policies independently from financial suitability and planning constraints.
4. Load secrets through runtime configuration; never commit or log them.
5. Return safe errors and maintain operational traceability without exposing sensitive data.

### 🧰 2.8 Root-Level Support Directories — Data, Tests & Delivery Support

Root-level support directories provide reference inputs, synthetic fixtures, schema migrations, verification suites and developer tooling. They support the application layers but do not become alternate owners of domain definitions or product behavior.

#### 🗂️ 2.8.1 Root-Level Directory & File Map

<quote color="blue_bg">
<p />

<b>backend/</b><br /><b>├── data/</b><br /><b>│   ├── reference/</b><br /><b>│   └── fixtures/</b><br /><b>├── migrations/</b><br /><b>├── tests/</b><br /><b>│   ├── unit/</b><br /><b>│   ├── integration/</b><br /><b>│   ├── contract/</b><br /><b>│   ├── end\_to\_end/</b><br /><b>│   ├── security/</b><br /><b>│   ├── regression/</b><br /><b>│   └── fixtures/</b><br /><b>├── scripts/</b><br /><b>│   ├── check\_canonical\_</b>[<b>catalog.py</b>](http://catalog.py)<br /><b>│   └── verify\_</b>[<b>environment.py</b>](http://environment.py)<br /><b>├── pyproject.toml</b><br /><b>├── requirements.txt</b> <b>(generated)</b><br /><b>├── .env.example</b><br /><b>├── Dockerfile</b><br /><b>└── </b>[<b>README.md</b>](http://README.md)\\
</quote>

#### 📋 2.8.2 Directory & File Ownership

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Directory / file
</td>
<td color="blue_bg">
What belongs here
</td>
<td color="blue_bg">
Explicit boundary
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
data/reference/
</td>
<td color="blue_bg">
Approved, non-sensitive reference data required at runtime or development time.
</td>
<td color="blue_bg">
Do not duplicate canonical IDs or taxonomies owned by domain/canonical/.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
data/fixtures/
</td>
<td color="green_bg">
Synthetic development inputs and reusable non-production examples.
</td>
<td color="green_bg">
Never store real investor data or credentials.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
migrations/
</td>
<td color="blue_bg">
Repeatable database migrations created only after 00.7 physical schema and migration-tool decisions are approved.
</td>
<td color="blue_bg">
No speculative schema or unapproved migration strategy.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
tests/unit/
</td>
<td color="green_bg">
Isolated tests for canonical contracts, domain calculations, constraints and feature behavior.
</td>
<td color="green_bg">
No live external dependencies; expected behavior must come from approved contracts.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
tests/integration/
</td>
<td color="blue_bg">
Tests of concrete persistence/provider integration boundaries.
</td>
<td color="blue_bg">
Use controlled test infrastructure and synthetic data.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
tests/contract/
</td>
<td color="green_bg">
API schema and repository-port contract tests.
</td>
<td color="green_bg">
Verify published interfaces; do not redefine business rules.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
tests/end\_to\_end/
</td>
<td color="blue_bg">
Complete investor planning journey tests across approved boundaries.
</td>
<td color="blue_bg">
Use synthetic accounts/data and approved end-to-end scenarios.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
tests/security/
</td>
<td color="green_bg">
Investor isolation, scenario isolation and plan-acceptance authorization tests.
</td>
<td color="green_bg">
Never use production investor records.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
tests/regression/
</td>
<td color="blue_bg">
Approved calculation and behavior regression cases.
</td>
<td color="blue_bg">
Expected values must trace to approved manual examples; provisional cases are not policy.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
tests/fixtures/
</td>
<td color="green_bg">
Synthetic JSON and other test-only fixtures.
</td>
<td color="green_bg">
No personal, financial or production data.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
scripts/check\_canonical\_[catalog.py](http://catalog.py)
</td>
<td color="blue_bg">
Checks consistency of canonical IDs/catalogues.
</td>
<td color="blue_bg">
Does not create or amend canonical business definitions.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
scripts/verify\_[environment.py](http://environment.py)
</td>
<td color="green_bg">
Verifies required runtime configuration without printing secret values.
</td>
<td color="green_bg">
Must not expose credentials or tokens.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
pyproject.toml
</td>
<td color="blue_bg">
Authoritative Python project and dependency configuration.
</td>
<td color="blue_bg">
requirements.txt is generated from this source, not independently maintained.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
requirements.txt
</td>
<td color="green_bg">
Generated dependency lock/export for supported deployment or tooling use.
</td>
<td color="green_bg">
Do not manually maintain a second dependency definition.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
.env.example
</td>
<td color="blue_bg">
Environment variable names and descriptions with safe placeholders only.
</td>
<td color="blue_bg">
No real secret values.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Dockerfile
</td>
<td color="green_bg">
Local/container build definition.
</td>
<td color="green_bg">
Deployment topology remains governed by 00.6 and 00.11.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
[README.md](http://README.md)
</td>
<td color="blue_bg">
Backend setup, architecture entry points and developer commands.
</td>
<td color="blue_bg">
Must describe the target blueprint accurately and not imply unverified implementation.
</td>
</tr>
</table>

#### 🧪 2.8.3 Test File Map

<quote color="blue_bg">
<p />

<b>tests/</b><br /><b>├── unit/</b><br /><b>│   ├── test\_canonical\_</b>[<b>catalog.py</b>](http://catalog.py)<br /><b>│   ├── test\_financial\_state\_</b>[<b>readiness.py</b>](http://readiness.py)<br /><b>│   ├── test\_</b>[<b>measurements.py</b>](http://measurements.py)<br /><b>│   ├── test\_</b>[<b>constraints.py</b>](http://constraints.py)<br /><b>│   ├── test\_moneywheel\_</b>[<b>assessment.py</b>](http://assessment.py)<br /><b>│   ├── test\_goal\_</b>[<b>planner.py</b>](http://planner.py)<br /><b>│   ├── test\_strategy\_</b>[<b>builder.py</b>](http://builder.py)<br /><b>│   ├── test\_scenario\_</b>[<b>isolation.py</b>](http://isolation.py)<br /><b>│   └── test\_action\_plan\_</b>[<b>lifecycle.py</b>](http://lifecycle.py)<br /><b>├── integration/</b><br /><b>│   └── test\_postgres\_</b>[<b>persistence.py</b>](http://persistence.py)<br /><b>├── contract/</b><br /><b>│   ├── test\_api\_</b>[<b>schemas.py</b>](http://schemas.py)<br /><b>│   └── test\_repository\_</b>[<b>ports.py</b>](http://ports.py)<br /><b>├── end\_to\_end/</b><br /><b>│   └── test\_investor\_planning\_</b>[<b>journey.py</b>](http://journey.py)<br /><b>├── security/</b><br /><b>│   ├── test\_investor\_</b>[<b>isolation.py</b>](http://isolation.py)<br /><b>│   ├── test\_scenario\_</b>[<b>isolation.py</b>](http://isolation.py)<br /><b>│   └── test\_plan\_acceptance\_</b>[<b>authorization.py</b>](http://authorization.py)<br /><b>├── regression/</b><br /><b>│   └── test\_approved\_calculation\_</b>[<b>cases.py</b>](http://cases.py)<br /><b>└── fixtures/</b><br /><b>    ├── financial\_state\_cases.json</b><br /><b>    └── goal\_planning\_cases.json</b>\\
</quote>

All fixture data must be synthetic. Approved expected values and rule cases must trace to the Operating Manual; tests must not turn provisional examples into approved policy.

### 🧭 2.9 Feature Ownership Quick Index

This index connects each approved product feature to its canonical vocabulary, owning domain module, application entry point and HTTP entry point. It is a navigation aid; detailed file responsibilities remain in Sections 2.2–2.5 and the relevant layer sections.

#### 📋 2.9.1 Cross-Layer Feature Ownership Matrix

| Product feature | Canonical contracts / shared inputs | Feature domain | Application entry | API entry |
| --- | --- | --- | --- | --- |
| Investor Profile | Chapter 03 financial categories and goal vocabulary; Chapter 04 Financial State contract. | domain/features/investor\_profile/ (four sibling subfeatures) | application/features/investor\_profile/ | api/routers/investor\_profile/ |
| Moneywheel | Chapter 05 measurement metadata; Financial State facts; owning feature evaluation contracts. | domain/features/moneywheel/ | application/features/moneywheel/ | api/routers/moneywheel/ |
| Goal Planner | Goal taxonomy, measurement metadata and Financial State inputs. | domain/features/goal\_planner/ | application/features/goal\_planner/ | api/routers/goal\_planner/ |
| Strategy Builder | Measurement metadata and Chapter 06 constraint contracts. | domain/features/strategy\_builder/ | application/features/strategy\_builder/ | api/routers/strategy\_builder/ |
| Participate with Your Finances | Scenario and investor-decision contracts, plus relevant evaluation outputs. | domain/features/participate\_with\_your\_finances/ | application/features/participate\_with\_your\_finances/ | api/routers/participate\_with\_your\_finances/ |
| Multi-Goal Planning | Approved Multi-Goal Planning boundary only; detailed contracts remain deferred. | domain/features/multi\_goal\_planning/ (reserved boundary) | application/features/multi\_goal\_planning/ (reserved) | api/routers/multi\_goal\_planning/ (reserved) |
| Reports | Authoritative outputs from Goal Planner and Strategy Builder; Multi-Goal Planning outputs only after its proposed domain design is approved. | domain/features/reports/ | application/features/reports/ | api/routers/reports/ |
| History | Owning feature records and version references; no duplicate feature contracts. | domain/features/history/ | application/features/history/ | api/routers/history/ |
| Accepted Plan / Action Plan | Chapter 13 acceptance decision and approved plan/action contracts; unresolved Accepted Plan details remain open. | domain/features/action\_plan/ (Action Plan); Accepted Plan contract remains governed by Chapter 13. | workflows/plan\_acceptance/ and application/features/action\_plan/ | api/routers/action\_plan/ |

#### 🔒 2.9.2 Ownership & Interpretation Rules

- Canonical vocabulary is shared; feature domain modules own feature-specific business behavior.
- Application entry points coordinate use cases; cross-feature sequencing belongs only in approved workflows.
- API entry points expose transport operations and do not own calculations, persistence or domain policy.
- Multi-Goal Planning remains a reserved boundary until its detailed design is approved.
- Reports present authoritative outputs and do not recalculate them; History preserves historical context and does not rewrite outcomes.
- Explicit investor acceptance is required before an Accepted Plan / Action Plan is created or updated.

These are proposed ownership boundaries, not claims that files already exist. Create a file only when its owning contract is ready and the existing implementation has been inspected.

## 3. Runtime flow — how these folders work together

1. The investor sends an HTTP request. <b>api/routers/</b> validates the transport payload using <b>api/schemas/</b>.
2. <b>security/</b> and API dependencies authenticate the actor and authorize access to the requested investor-owned record.
3. The router calls one <b>application/features/</b> use case or an approved <b>application/workflows/</b> coordinator.
4. The application use case loads records through <b>application/ports/repositories/</b>; infrastructure supplies the PostgreSQL/Supabase implementation.
5. Domain feature logic and shared domain capabilities execute the business behavior: canonical calculations, evidence/readiness, Chapter 06 constraints, feature assessments and lifecycle rules.
6. Application coordinates persistence through the unit-of-work boundary. Infrastructure writes records and version references to PostgreSQL.
7. The API maps the result to a response schema. Reports may pass an already-authoritative report payload to the PDF renderer.
8. Tests verify the individual domain rule, integration boundaries, end-to-end journey, security and regression behavior.

## 🔗 4. Dependency & Ownership Rules

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Component
</td>
<td color="blue_bg">
May depend on
</td>
<td color="blue_bg">
Must not depend on
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
API
</td>
<td color="blue_bg">
Application use cases, API schemas, security dependencies
</td>
<td color="blue_bg">
Domain implementation details, database client, direct SQL, formula code
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Application
</td>
<td color="green_bg">
Domain, application ports, shared application mechanics
</td>
<td color="green_bg">
FastAPI request objects, Supabase SDK, concrete SQL repositories
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Domain Canonical
</td>
<td color="blue_bg">
Other canonical types and stable value objects
</td>
<td color="blue_bg">
API schemas, ORM/database rows, HTTP, Supabase
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Domain Feature
</td>
<td color="green_bg">
Canonical model, shared calculations, shared constraints, evidence and other domain contracts through explicit interfaces
</td>
<td color="green_bg">
FastAPI, database, Supabase, report renderer
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Domain Shared Engines
</td>
<td color="blue_bg">
Canonical contracts and pure domain inputs
</td>
<td color="blue_bg">
Feature-specific duplicate formulas, HTTP, persistence
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Infrastructure
</td>
<td color="green_bg">
Application ports, canonical/domain contracts, database/provider SDKs
</td>
<td color="green_bg">
Ownership of business rules, formula definitions or investor decision policy
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Security
</td>
<td color="blue_bg">
Identity provider adapter, authorization policies, access contracts
</td>
<td color="blue_bg">
Frontend-supplied authorization claims as proof; business calculation logic
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Tests
</td>
<td color="green_bg">
Public interfaces of the layer under test and approved fixtures
</td>
<td color="green_bg">
Production investor data or unapproved thresholds/formulas
</td>
</tr>
</table>

## 🚚 5. Existing Backend Folders — Responsibility Migration Map

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Existing path
</td>
<td color="blue_bg">
Target responsibility
</td>
<td color="blue_bg">
Migration rule
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/api/</b>
</td>
<td color="blue_bg">
<b>app/api/</b>
</td>
<td color="blue_bg">
Keep endpoint behavior at the HTTP boundary; move business logic out into application/domain.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/services/</b>
</td>
<td color="green_bg">
<b>app/application/features/</b> and <b>app/application/workflows/</b>
</td>
<td color="green_bg">
Map each existing service by use-case ownership. Do not preserve a catch-all service that secretly runs every engine.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/engines/calculation/</b>
</td>
<td color="blue_bg">
<b>app/domain/shared/calculations/</b>
</td>
<td color="blue_bg">
Consolidate canonical formulas here, grouped by Chapter 05 measurement families.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/engines/rules/</b>, <b>backend/engines/constraints/</b>, <b>backend/rules/</b>
</td>
<td color="green_bg">
<b>app/domain/shared/constraints/</b>
</td>
<td color="green_bg">
One authoritative Chapter 06 rule/constraint catalogue and evaluator; remove duplicate definitions only after parity tests.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/engines/financial\_state/</b>
</td>
<td color="blue_bg">
<b>app/domain/features/investor\_profile/financial\_state/</b> plus canonical model and persistence adapter
</td>
<td color="blue_bg">
Separate financial fact model, validation/readiness, use cases and database mapping.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/engines/profile/</b>, <b>backend/engines/risk\_profiler/</b>
</td>
<td color="green_bg">
Investor Profile domain subfeatures
</td>
<td color="green_bg">
Map profile, risk, behavioural and preference code to their four approved components. Do not leave Risk Profile as a separate top-level feature.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/engines/moneywheel/</b>
</td>
<td color="blue_bg">
<b>app/domain/features/moneywheel/</b>
</td>
<td color="blue_bg">
Keep assessment/presentation logic here; move canonical formulas to shared calculations.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/engines/goal/</b>
</td>
<td color="green_bg">
<b>app/domain/features/goal\_planner/</b>
</td>
<td color="green_bg">
Goal requirement and Goal Feasibility remain in the Goal Planner feature.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/engines/investment/</b>, <b>allocation/</b>, <b>basket/</b>, <b>suitability/</b>, <b>technique/</b>
</td>
<td color="blue_bg">
Strategy Builder domain modules, after file-by-file ownership review
</td>
<td color="blue_bg">
Do not rename or merge blindly; map each function to Chapter 11 funding-path, asset assessment, projection, financing or comparison behavior. Preserve behavior with regression tests.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/engines/orchestration/</b>, <b>backend/api/</b>[<b>orchestration.py</b>](http://orchestration.py)
</td>
<td color="green_bg">
<b>app/application/workflows/</b>
</td>
<td color="green_bg">
Keep planning-lifecycle coordination in application; domain modules remain independently testable.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/engines/action\_plan/</b>
</td>
<td color="blue_bg">
<b>app/domain/features/action\_plan/</b> and application Action Plan use cases
</td>
<td color="blue_bg">
Preserve Chapter 13 acceptance boundary and action-status semantics.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/engines/summary\_report/</b>, <b>backend/report\_engine/</b>
</td>
<td color="green_bg">
<b>app/application/features/</b>[<b>reports.py</b>](http://reports.py) plus <b>app/infrastructure/reporting/</b>
</td>
<td color="green_bg">
Separate report data assembly from PDF/rendering; neither may calculate or change plan decisions.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/models/</b>
</td>
<td color="blue_bg">
<b>app/domain/canonical/</b> and <b>app/infrastructure/persistence/mappers/</b>
</td>
<td color="blue_bg">
Separate business/canonical records from physical database representations; inspect every existing model before moving it.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/schemas/</b>
</td>
<td color="green_bg">
<b>app/api/schemas/</b>
</td>
<td color="green_bg">
Keep only request/response transport schemas here.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/data/</b>
</td>
<td color="blue_bg">
<b>backend/data/reference/</b> or <b>backend/data/fixtures/</b>
</td>
<td color="blue_bg">
Distinguish approved non-sensitive reference data from synthetic test fixtures. Do not duplicate canonical catalogues.
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
<b>backend/config/</b>
</td>
<td color="green_bg">
<b>app/core/</b>[<b>settings.py</b>](http://settings.py) and deployment environment configuration
</td>
<td color="green_bg">
Keep secrets outside source control and browser code.
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
<b>backend/tests/</b>
</td>
<td color="blue_bg">
<b>backend/tests/\{unit,integration,contract,end\_to\_end,security,regression\}/</b>
</td>
<td color="blue_bg">
Preserve and classify existing tests; do not discard tests during restructuring.
</td>
</tr>
</table>

## 📖 6. Canonical Source-of-Truth Map

<table fit-page-width="true" header-row="true">
<tr color="blue_bg">
<td color="blue_bg">
Concern
</td>
<td color="blue_bg">
Authoritative source
</td>
<td color="blue_bg">
Backend implementation location
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Goal IDs and financial category IDs, including insurance policy types
</td>
<td color="blue_bg">
Chapter 03
</td>
<td color="blue_bg">
<b>domain/canonical/goal\_</b>[<b>taxonomy.py</b>](http://taxonomy.py), <b>financial\_</b>[<b>categories.py</b>](http://categories.py)
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Financial State facts, evidence, readiness and history
</td>
<td color="green_bg">
Chapter 04
</td>
<td color="green_bg">
Investor Profile Financial State domain, persistence adapters
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Measurement definitions, formulas, units, periods and assumptions
</td>
<td color="blue_bg">
Chapter 05
</td>
<td color="blue_bg">
<b>domain/canonical/</b>[<b>measurements.py</b>](http://measurements.py), <b>domain/shared/calculations/</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Constraints, thresholds, applicability and decision effects
</td>
<td color="green_bg">
Chapter 06
</td>
<td color="green_bg">
<b>domain/shared/constraints/</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Investor/situation interpretation
</td>
<td color="blue_bg">
Chapter 07
</td>
<td color="blue_bg">
<b>application/workflows/investor\_situation\_</b>[<b>assessment.py</b>](http://assessment.py) and supporting domain contracts
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Budgeting, cash flow and affordability workflow
</td>
<td color="green_bg">
Chapter 08
</td>
<td color="green_bg">
<b>application/workflows/budgeting\_cash\_flow\_</b>[<b>affordability.py</b>](http://affordability.py), Chapter 05-owned calculation family in <b>domain/shared/calculations/</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Financial health, resilience and protection
</td>
<td color="blue_bg">
Chapter 09
</td>
<td color="blue_bg">
<b>domain/features/moneywheel/</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Goal requirement and Goal Feasibility
</td>
<td color="green_bg">
Chapter 10
</td>
<td color="green_bg">
<b>domain/features/goal\_planner/</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Funding paths, strategy applicability/viability and comparison
</td>
<td color="blue_bg">
Chapter 11
</td>
<td color="blue_bg">
<b>domain/features/strategy\_builder/</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Sensitivity, scenario and decision comparison
</td>
<td color="green_bg">
Chapter 12
</td>
<td color="green_bg">
<b>domain/features/participate\_with\_your\_finances/</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Explicit acceptance, Accepted Plan and Action Plan
</td>
<td color="blue_bg">
Chapter 13
</td>
<td color="blue_bg">
<b>application/workflows/plan\_</b>[<b>acceptance.py</b>](http://acceptance.py), <b>domain/features/action\_plan/</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Logical data domains and physical schema decisions
</td>
<td color="green_bg">
00.7
</td>
<td color="green_bg">
<b>domain/canonical/</b>, <b>infrastructure/persistence/</b>, <b>migrations/</b>
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Execution, automation and version traceability
</td>
<td color="blue_bg">
00.8
</td>
<td color="blue_bg">
<b>application/workflows/</b>, shared versioning and idempotency
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Security and privacy
</td>
<td color="green_bg">
00.9
</td>
<td color="green_bg">
<b>security/</b>, API authorization, persistence policies and security tests
</td>
</tr>
<tr color="blue_bg">
<td color="blue_bg">
Test levels and acceptance evidence
</td>
<td color="blue_bg">
00.10
</td>
<td color="blue_bg">
<b>tests/</b>
</td>
</tr>
<tr color="green_bg">
<td color="green_bg">
Deployment, monitoring, backup and rollback
</td>
<td color="green_bg">
00.11
</td>
<td color="green_bg">
<b>core/</b>, observability, scripts and deployment configuration
</td>
</tr>
</table>

## 🚧 7. Critical Implementation Boundaries — Governed by the Manual

<quote color="orange_bg">
⚠️ <b>Architecture guardrail</b>

The directory map is a target blueprint—not evidence that code already exists. Sections 2.3–2.5 are the authoritative domain structure for this page: the main tree and all cross-layer indexes must mirror their canonical vocabulary, feature ownership and shared-capability boundaries. Business rules, formulas, data contracts and physical schema decisions remain governed by the Operating Manual.
</quote>

- The Canonical Data Model is a first-class domain component. Its files describe shared business concepts and contracts; they are not a guessed PostgreSQL schema.
- The physical PostgreSQL tables, columns, indexes, retention/deletion behavior and migration tool must follow the finalized 00.7 decisions. This blueprint intentionally does not fabricate them.
- Chapter 05 formulas are grouped by measurement family. Net Worth, Available Monthly Surplus and other metrics are implementations within those group files, not separate one-formula files.
- Chapter 06 is the single authority for rule identity, applicability, thresholds, effects and missing-evidence behavior. Do not keep parallel rule catalogues in feature folders.
- Multi-Goal Planning has four approved capability boundaries, but detailed design is deferred. Its README is a boundary marker, not permission to invent allocation algorithms.
- Strategy Builder consumes Goal Planner outputs. Goal Feasibility is not a separate engine or fifth strategy.
- Reports render authoritative feature outputs; they do not recalculate them. History preserves context and versions; it does not rewrite historical outcomes.
- A scenario, recommendation, selected strategy or report is not plan acceptance. Only the explicit Chapter 13 acceptance workflow can create/update an Accepted Plan.
- This is the target file-level blueprint. Before moving existing code, each current file must be mapped to an owner, behavior parity must be checked, and the relevant 00.10 tests must pass. The target layout is not a claim that these files already exist or that implementation is verified.

<page url="https://app.notion.com/p/41057e71b7b881139bc2eb448ff838bb">
Backend Redesign — Migration Plan
</page>
