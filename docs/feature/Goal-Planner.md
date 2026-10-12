# Goal Planner

## 1. Main kaam
- Goal poora ho sakta hai ya nahi, check karna.
- Required amount, available resources aur funding gap dikhana.
- Goal feasible banane ke possible raaste compare karna.
- Result Strategy Builder ko dena.
- Sirf SIP calculate karna Goal Planner ka poora kaam nahi.

## 2. Inputs
- Goal, target amount aur deadline.
- Goal ke liye existing corpus.
- Income, expenses aur EMI ke baad monthly surplus.
- Existing assets aur unka possible contribution.
- Loans, interest rates, outstanding amount, EMI aur remaining tenure.
- Emergency reserve aur liquidity ki zaroorat.
- Doosre active goals aur unki funding needs.
- Goal ya financial situation mein changes.

## 3. Process
1. Goal aur requirements samjho.
2. Required amount aur timeline calculate karo.
3. Assets aur future contributions assess karo.
4. Funding gap nikalo.
5. Current situation mein feasibility check karo.
6. Gap ho to possible funding paths banao.
7. Paths ke assumptions aur projected results compare karo.
8. Cash flow, debt, liquidity aur doosre goals par impact check karo.
9. Goal feasible banane ke liye required changes dikhayo.
10. Result Strategy Builder ko do.

## 4. Goal Funding
- Goal Funding, Goal Planner ka hissa hai; Strategy Builder ki fifth strategy nahi.
- Goal Funding ka output: required money aur possible funding path.
- SIP, lump sum, step-up contribution aur combinations funding mechanisms hain.
- Koi mechanism apne aap goal feasibility prove nahi karta.

## 5. Debt vs investment
- Sirf karz hone se Debt Reduction automatic select mat karo.
- Sirf expected investment return debt interest se zyada hone se investing ko automatic best mat bolo.
- Compare karo:
  - extra money debt repayment mein lagana;
  - extra money goal ke liye invest karna;
  - EMI ya loan structure badalna.
- Interest saved, uncertain returns, goal funding, cash flow, liquidity aur risk dikhana.
- Return assumptions guarantee nahi hain.
- Money Wheel measurements dikhata hai; akela final decision nahi karta.
- DTI ya interest rate ko automatic “karz chukao” rule mat banao.
- Weighted Debt Rate aur Investment–Debt Spread candidate measurements hain; final formula/code status verified nahi.

## 6. Multiple goals
- Har goal alag feasible ho, phir bhi combined plan infeasible ho sakta hai.
- Available money, goal funding needs aur resource competition check karo.
- Ek goal ko zyada paisa dene ka doosre goals par impact dikhana.
- Whole-plan impact check tab karo jab decision multiple goals ya accepted plan ko materially affect kare.
- Har individual-goal decision mein bina wajah poora plan dobara calculate mat karo.

## 7. Asset Mapping vs Asset Earmarking
- **Asset Mapping:** asset ko planning ke liye goal se associate karna; asset automatically sold, locked ya committed nahi hota.
- **Asset Earmarking:** asset ya uske hisse ko jaan-boojhkar goal ke liye reserve/protect karna.
- Dono alag decisions hain; mapped aur earmarked amount alag ho sakte hain.
- Same asset ko competing goals ke liye fully earmark karne ka conflict chhupana nahi.
- Mapping feasibility ka input hai, guarantee nahi.
- Goal cancel hone par underlying asset Financial State se delete nahi hota.
- Existing earmarking release karne ka decision alag se check karo.

## 8. Goal change/cancellation
- Amount, date, horizon ya corpus badle to affected funding aur feasibility dobara calculate karo.
- Har change par poora plan ya strategy automatically replace mat karo.
- Goal cancel ho to planning requirement update karo; asset ko Financial State mein rehne do.
- Asset ko remap, unallocated ya doosre use ke liye consider karo.
- Earmarked asset ki protection release karne ka impact alag se check karo.

## 9. Existing plan mein naya goal
- Naye goal ko pehle separate what-if scenario mein assess karo.
- Naye goal ki funding need aur existing goals par impact dikhana.
- Monthly surplus, assets, liquidity aur debt par impact check karo.
- Investor ke accept karne se pehle existing Accepted Plan overwrite mat karo.
- Accept hone par multi-goal feasibility aur affected decisions re-check karo.

## 10. Financial situation change
- Income, expenses, assets, debt ya surplus change ka impact assess karo.
- Chhota change ho aur current path suitable ho to full rebuild zaroori nahi.
- Material change ho to affected goal aur decisions re-check karo.
- Completed actions history mein rahen; active/future actions zaroorat par revise hon.
- Materiality thresholds abhi final nahi.

## 11. Output
- Goal, target amount aur timeline.
- Available resources aur funding gap.
- Feasibility: feasible, infeasible, ya information missing.
- Compared funding paths, assumptions aur projected results.
- Debt, cash flow, liquidity aur other-goal impact.
- Goal feasible banane ke liye required changes.
- Investor ke decision points.
- Strategy Builder ko dene wala feasibility/funding result.
- Koi acceptable path na ho to clearly batao; forced recommendation mat do.

## 12. Strategy Builder ke saath boundary
- **Goal Planner:** kya mumkin hai aur goal feasible banane ke liye kya chahiye?
- **Strategy Builder:** feasible path ko execute karne ke liye kaunsi strategy munasib hai?
- Strategy Builder feasibility calculation ko independently dobara na banaye.
- Strategy, variant aur technique select karna Strategy Builder ka kaam hai.
- Action Plan investor ke accepted path ke actions dikhata hai.

## 13. Abhi unverified
- Exact feasibility formulas.
- Multiple goals mein resources allocate karne ke rules.
- Material change ki threshold.
- Goal cancellation ke baad exact asset remapping behaviour.
- Weighted Debt Rate aur Investment–Debt Spread ka final formula/code status.
- Scenario save, compare aur accept karne ka implementation.
- Yeh document business intent hai, code implementation ka proof nahi.

## 14. Source documents
- `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` — Goal Funding, debt-vs-investment aur Money Wheel.
- `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md` — multiple goals.
- `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md` — financial changes.
- `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md` — goal change/cancellation.
- `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md` — new goal scenario.
- `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md` — mapping vs earmarking.
- `strategy-decision-tree.md` and `FULL_AUDIT_REPORT.md` — decision boundaries and audit findings.
