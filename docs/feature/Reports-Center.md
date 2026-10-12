# Reports Center

## 1. Main kaam
- Financial plan aur selected goals/strategies ke reports generate/download karna.
- Ek goal ya multiple goals ke liye report scope choose karne dena.
- Investor ko plan aur strategy decisions ka shareable record dena.

## 2. Report options visible in code
- Complete Financial Plan.
- Goal/Strategy report PDF.
- Basket report PDF.
- Summary report PDF.
- Goal-specific report availability selected goal aur strategy version par depend kar sakti hai.

## 3. Inputs
- Defined goals.
- Selected goal.
- Selected strategy version.
- Planning basket/goal selection.
- Report type.

## 4. Process
1. Goals aur available saved baskets load karo.
2. Investor report type aur relevant goal/basket choose kare.
3. Required selected strategy version resolve karo.
4. Relevant report generation/download function call karo.
5. Missing required data ho to report availability/error explain karo.

## 5. Output
- Downloadable PDF report, selected report option ke hisaab se.
- Complete plan, goal/strategy, basket ya summary scope.

## 6. Important boundaries
- Report ek snapshot/presentation hai; khud strategy execute ya Accepted Plan update nahi karta.
- Report available hone ka matlab har underlying calculation business-approved hai, aisa nahi.
- Report mein assumptions, missing inputs aur version/scope clear rehne chahiye.

## 7. Code evidence
- Frontend: `frontend/app/investor/reports/page.tsx`
- Report functions: `frontend/lib/api/strategy`
- Backend report APIs: `backend/api/summary_report.py`, `backend/api/basket_report.py`

## 8. Abhi unverified
- Har report ke PDF contents aur calculations.
- Report snapshot version/time stamp.
- Saved basket persistence: current page local storage key `planvesto:planning-baskets` use karti hai.
- PDF generation errors/availability ke all cases.
