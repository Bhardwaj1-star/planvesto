# Strategy Builder

## 1. Is feature ka kaam

Strategy Builder ka kaam hai Goal Planner se yeh samajhne ke baad ki goal ko poora karne ka kaunsa raasta financially mumkin hai, yeh decide karne mein madad dena ki **us raaste ko execute karne ke liye kaunsi financial strategy sabse munasib hai**.

Seedha sawaal:

> **Goal Planner batata hai “kya mumkin hai”; Strategy Builder batata hai “us par kaise amal karna munasib hoga”.**

Strategy Builder ko Goal Planner ka feasibility hisaab apne aap dobara nahi banana chahiye. Use goal ki situation, financial state, funding/feasibility result aur genuine restrictions ko input ke roop mein lena hai.

## 2. Strategy Builder kya dekhega

Strategy ka faisla sirf goal ke naam se nahi hona chahiye. Sirf “Education”, “Retirement” ya “Dream Home” dekhkar ek fixed strategy chunna sahi nahi hai.

Relevant cheezein hain:

- goal ki asli zaroorat aur paisa kab chahiye;
- Goal Planner ne goal ke funding gap aur feasibility ke baare mein kya nikala;
- investor ki financial situation;
- assets, karz, EMI, monthly surplus aur liquidity;
- goal kitna nazdeek hai aur capital ko kitni protection chahiye;
- kaun se sach-much zaroori restrictions hain;
- aur investor ne kaun se trade-offs accept kiye hain.

Ek hi tarah ke goal mein alag situation ke hisaab se alag strategy sahi ho sakti hai.

## 3. Strategy Builder ki chaar main strategies

Target business design mein Strategy Builder ki **chaar canonical strategies** hain:

### 1. Progressive De-risking
Jab goal abhi kuch door ho aur goal ka waqt nazdeek aane ke saath risk ko dheere-dheere kam karna madadgar ho.

Misal: Education goal ke liye abhi kai saal hain, lekin jaise-jaise payment date nazdeek aaye, paisa bachane/protect karne par zyada dhyan dena.

### 2. Capital Preservation
Jab goal ke liye chahiye capital ya uska ek zaroori hissa loss ya timing ke risk se bachana zyada important ho jaye.

Misal: Agli tuition payment nazdeek hai aur uske liye zaroori paisa risk mein nahi daalna chahiye.

### 3. Debt Reduction
Jab karz aur uski payment investor ke cash flow, goal funding ya financial stability ko materially nuksan pahuncha rahi ho, aur karz ghatane ya badalne se financial position behtar ho sakti ho.

Sirf karz maujood hone se Debt Reduction automatic choice nahi hai. Uska asar actual numbers ke saath dekhna hai.

### 4. Credit Utilisation
Jab sach mein funding ya timing ka gap ho aur borrowing zimmedari se ki ja sakti ho.

Borrowing tabhi candidate ho sakti hai jab apne available resources dekhe gaye hon, borrowing capacity ho, EMI sambhal sakein, financing cost munasib ho aur repayment ka credible raasta ho. Inmein se koi zaroori condition fail ho, to Credit Utilisation ko recommend nahi karna chahiye.

**Goal Funding in chaar strategies mein se paanchvi strategy nahi hai.** Woh Goal Planner ka kaam hai.

## 4. Strategy applicable hona aur uska kaam kar pana alag sawaal hain

Pehle yeh dekhna hai ki strategy us situation mein relevant hai bhi ya nahi. Iske baad yeh dekhna hai ki investor ke numbers aur restrictions ke andar woh sach mein kaam kar sakti hai ya nahi.

Misal: Education ke liye funding gap ho to loan ka option relevant ho sakta hai. Lekin agar EMI afford nahi ho sakti, to loan ka option practical nahi hai. Sirf option ka relevant hona kaafi nahi.

Har candidate ke liye samjhana chahiye:

- yeh strategy is situation mein kyun fit hoti hai;
- agar fit nahi hoti to kyun;
- agar fit hoti hai lekin chal nahi sakti to kya rok raha hai;
- aur selected strategy doosron se behtar kyun hai.

Agar koi strategy investor ki situation aur constraints mein acceptable nahi hai, to system ko zabardasti ek strategy choose nahi karni chahiye.

## 5. Strategy ke andar Variant kya hota hai

Variant us strategy ka khaas roop hai, jo batata hai ki us strategy ko kis tarah ki situation ke liye use kiya ja raha hai.

Target business tree mein variants ka set yeh hai:

| Strategy | Variant |
|---|---|
| Progressive De-risking | Goal-Date Glide Path |
| Progressive De-risking | Payment-Tranche Glide Path |
| Progressive De-risking | Recurring-Cashflow Glide Path |
| Progressive De-risking | Income-Transition Glide Path |
| Capital Preservation | Full-Goal Preservation |
| Capital Preservation | First-Payment Preservation |
| Capital Preservation | Rolling Reserve Preservation |
| Capital Preservation | Protected-Core Preservation |
| Debt Reduction | Goal-Gap Debt Reduction |
| Debt Reduction | EMI-Relief Debt Reduction |
| Debt Reduction | Residual-Gap Debt Reduction |
| Debt Reduction | Goal-Linked Debt Reduction |
| Credit Utilisation | Residual-Gap Bridge |
| Credit Utilisation | Partial-Goal Financing |
| Credit Utilisation | EMI-Cap Financing |
| Credit Utilisation | Timing-Bridge Financing |

Yeh target business tree mein defined variants hain. Is list ko current code mein poori tarah implemented hone ka proof nahi maana jayega.

## 6. Technique kya hoti hai

Technique ek aisa tareeka hai jo selected strategy aur variant ko practically kaam karne mein madad karta hai. Technique khud final solution nahi hai.

Examples:

- **Glide Path:** goal nazdeek aane ke saath risk/capital position ko dheere-dheere badalna.
- **Bucketing:** paisa ko alag-alag time ya zaroorat ke hisaab se hisson mein organize karna.
- **Cash-flow Matching:** aane wali payments ke saath paisa ya cash flow match karna.
- **Laddering:** alag-alag dates ki zarooraton ke liye maturity/payment ko alag-alag dates par rakhna.
- **Asset Earmarking:** kisi asset ya uske ek hisse ko jaan-boojhkar ek goal ke liye reserve/protect karna.
- **Goal Segmentation:** alag goals, karz aur paison ki zarooraton ko alag-alag samajhna.
- **Debt Repayment Prioritisation:** tay karna ki kaun se karz ko pehle chukana zyada munasib hai.
- **Debt Cost Optimisation:** karz ka total/effective kharch kam karne ya behtar karne ke raaste dekhna.
- **Debt Prepayment Optimisation:** extra paisa karz mein pehle dena faidemand hai ya nahi, yeh compare karna.
- **EMI Capacity Analysis:** investor kitni EMI sustainably de sakta hai, yeh dekhna.
- **Borrowing Capacity Analysis:** kitna loan zimmedari se liya ja sakta hai, yeh dekhna.
- **Financing Cost Comparison:** loan ki cost aur doosre raaston ka asar compare karna.

Har technique har situation mein zaroori nahi. Koi technique zaroori, condition ke hisaab se, optional, na-lagu, ya information ki kami ki wajah se abhi assess na ki ja sakne wali ho sakti hai.

**Technique aur Solution alag hain.** Technique ek tareeka hai; Solution investor ke actual numbers se nikla hua concrete raasta hai.

Contribution badhana ya SIP set karna Goal Planner ke funding/execution options hain; unhe sirf isliye Strategy Builder ki technique ya strategy nahi kehna chahiye.

## 7. Asset Mapping aur Asset Earmarking mein farq

- **Asset Mapping** Goal Planner mein hota hai: kaun se existing assets goal ke liye planning mein consider kiye ja rahe hain.
- **Asset Earmarking** strategy/implementation ke baad use ho sakta hai: kaun sa paisa jaan-boojhkar us goal ke liye reserve/protect kiya jayega.

Mapping se asset apne aap locked ya protected nahi hota. Earmarking se ek intentional commitment banta hai. Agar same asset ko do goals ke liye reserve karne se conflict hota hai, to system ko conflict chhupana nahi chahiye.

Earmarking ka matlab koi particular investment product kharidna bhi nahi hai.

## 8. Strategy Builder ka result sirf ek naam nahi hona chahiye

Strategy Builder ko decision ka reason samjhana chahiye:

1. Kaun sa goal aur kaunsi situation dekhi ja rahi hai?
2. Goal Planner ka feasibility/funding result kya hai?
3. Kaun se real restrictions lagu hain?
4. Kaun si strategies is situation mein relevant hain?
5. Kaun si strategies kyun fail hoti hain ya kyun chal nahi sakti?
6. Kaunsi strategy choose ki gayi aur kyun?
7. Kaunsa variant fit hota hai aur kyun?
8. Kaun si techniques zaroori hain, kaun si sirf condition hone par use hongi?
9. In sab ko mila kar investor ke liye actual solution kya banta hai?
10. Is raaste ke risks, faide, trade-offs aur doosre goals par asar kya hai?
11. Investor ko kya decision lena hai?

Recommendation ka reason normal bhasha mein hona chahiye, sirf code ya technical label ke roop mein nahi.

## 9. Current path aur better path

Goal feasible hone ka matlab yeh nahi ki maujooda raasta hi sabse achha hai.

Jahan meaningful alternative ho, Strategy Builder ko compare karna chahiye:

- current/appropriate raasta;
- aur ek better-path alternative.

Alternative ko bina proof “better” nahi kehna. Actual numbers ke saath dikhana chahiye ki kya badal sakta hai—jaise goal tak pahunchne ka waqt, required contribution, projected result, liquidity, risk, karz aur doosre goals par asar.

Misal: kam return wale asset ko badalne se goal jaldi poora ho sakta hai, lekin naya risk ya liquidity ka nuksan bhi ho sakta hai. Dono taraf ka asar dikhana hai. Return assumptions guaranteed nahi hain.

## 10. Ek financial plan mein kai strategies ho sakti hain

Strategy Builder ka matlab yeh nahi ki poore investor ke liye sirf ek strategy choose hogi.

Alag goals ya financial problems ke liye alag strategies ek hi plan mein saath chal sakti hain. Misal ke liye, Education ke liye ek strategy, Retirement ke liye doosri, aur mehange karz ke liye teesri.

Lekin unhe alag-alag chun lena kaafi nahi. Agar unke beech paisa ya cash flow compete karta hai, to combined plan ka impact bhi check karna hoga.

Ek decision ke liye dikhaye gaye do alternatives ka matlab yeh nahi ki poore plan mein sirf do strategies ho sakti hain.

## 11. Investor final decision leta hai

System recommendation deta hai aur trade-offs samjhata hai. Investor ko har recommendation maanane ke liye majboor nahi karna chahiye, jab tak koi sach-much hard constraint option ko rokta na ho.

Misal: 18% byaaj wala loan chukana strong recommendation ho sakta hai. Agar investor samajhne ke baad bhi loan rakhkar invest karna chahe, to system ko us choice ke extra interest cost, investment assumptions, risk, liquidity aur goal par asar samjhana chahiye—jab tak koi genuine hard constraint use rokta na ho.

Strategy change ko proposal ki tarah treat karna hai. Investor accept kare tabhi woh accepted plan ka hissa banta hai. Agar investor alternative reject kare, to purana accepted plan apne aap overwrite nahi hona chahiye.

## 12. Strategy aur execution alag cheezein hain

**Strategy:** overall approach kya hogi?

**Execution:** us approach ko kitne paison, kis timing aur kin actions ke saath lagu kiya jayega?

Investor SIP amount, lump sum, contribution timing ya existing asset use karne ka tareeka badal kar what-if dekh sakta hai. Isse zaroori nahi ki strategy bhi badle.

System ko pehle badlav ka impact dikhana hai. Agar us badlav se current strategy ab munasib nahi rehti, to strategy ko dobara evaluate karna chahiye. System ko chupke se strategy replace nahi karni.

What-if scenario aur accepted plan alag rahenge. Investor scenario accept kare tabhi accepted execution aur Action Plan update honge.

## 13. Badlav aur baar-baar re-check

Strategy ya execution mein badlav hone par poora plan har baar shuru se banana zaroori nahi.

Pehle pata karo:

- kya badla;
- kaun sa goal ya strategy seedhe affect hua;
- aur kaun se doosre goals ya strategies par material asar ho sakta hai.

Sirf affected hisson ko dobara check karna kaafi ho sakta hai. Agar badlav poore plan ko affect karta hai, to broader check hoga.

Investor baar-baar what-if kar sakta hai: execution badle, impact dekhe, zaroorat ho to strategy dobara dekhe, phir naya execution test kare. Sirf wahi raasta active plan banega jise investor accept kare.

## 14. Jab koi strategy acceptable na ho

“No acceptable strategy” ek valid result hai, system ki galti nahi.

System ko sirf recommendation dene ke liye zabardasti strategy nahi chunni chahiye. Use samjhana chahiye ki kaun si condition raasta rok rahi hai aur goal ko mumkin banane ke liye kya badalna pad sakta hai.

Investor chahe to apna raasta khud design kar sakta hai. Is mode mein investor approach aur numbers batata hai; system usko samajhne layak banata hai, calculation karta hai, risk/trade-offs samjhata hai aur restrictions check karta hai. System investor ki jagah decision nahi leta.

Investor-designed raasta bhi actual financial impact, hard constraints aur whole-plan impact ke check se guzrega. Accept hone se pehle woh active plan nahi banega.

## 15. Strategy Builder ke baad kya hota hai

Target business flow ka simple roop:

**Goal Planner ka result**
→ **Restrictions check**
→ **Kaun si strategies fit hoti hain**
→ **Kya woh sach mein kaam kar sakti hain**
→ **Strategy chunna**
→ **Variant chunna**
→ **Zaroori techniques**
→ **Har technique ka use kaise hoga**
→ **Architecture: sab parts ko ek plan mein jodna**
→ **Solution: investor ke numbers se nikla actual raasta**
→ **Stress/resilience check**
→ **Recommendation aur uska reason**
→ **Investor accept / reject / modify**
→ **Accepted Plan**
→ **Action Plan**
→ **Execution**

Yeh target business flow hai; isse yeh claim nahi hota ki current code isi order mein chal raha hai.

## 16. Abhi kya final/verified nahi hai

Real-Life Decision Cases target business direction batate hain. Woh apne aap prove nahi karte ki sab behavior current code mein implemented hai.

Abhi in baaton ko bina alag validation ke implemented/frozen nahi kehna chahiye:

- har strategy/variant ka exact selection rule;
- technique ke required/conditional hone ke exact rules;
- har calculation aur comparison ka formula;
- strategy ke beech conflict solve karne ka tareeka;
- stress/resilience test ki exact limits;
- strategy ya execution change ka material impact threshold;
- what-if scenarios ko save/compare/accept karne ka exact flow;
- investor ke accept kiye gaye plan aur Action Plan ka code-level behavior.

Target model mein chaar strategies hain, lekin current code aur purane documents mein purani naming ya alag structure ho sakta hai. Use bina verify kiye target design ke barabar nahi maanna.

## 17. Is document ke liye dekhe gaye source documents

- `strategy-decision-tree.md` — target strategies, variants, techniques aur decision ka flow.
- `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` — Goal Funding ko Strategy Builder se alag rakhna.
- `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md` — multi-goal impact aur Action Plan ka role.
- `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md` — current path aur better path ka comparison.
- `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md` — financial situation badalne par targeted re-check.
- `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md` — goal change aur feasibility dobara calculate karna.
- `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md` — naya goal pehle scenario, phir investor decision.
- `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md` — investor choice aur ek plan mein multiple strategies.
- `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md` — strategy badle bina execution what-if.
- `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md` — execution ke badlav se strategy dobara check karna.
- `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md` — baar-baar what-if aur revalidation.
- `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md` — no acceptable path aur investor ka apna raasta.
- `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md` — asset mapping aur earmarking ka farq.
- `FULL_AUDIT_REPORT.md` — purane documents mein conflicting definitions aur target/current code ko alag rakhna.

Yeh document business decisions ko normal bhasha mein register karta hai. Yeh current code ki audit file nahi hai aur implementation complete hone ka daawa nahi karta.
