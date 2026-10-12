# Profile

## 1. Main kaam
- Investor account aur personal/financial information ka control center.
- Account details aur financial information ko alag tabs mein dikhana.
- Onboarding se judi information aur profile completion ka summary dikhana.
- Investor ko sign out karne dena.

## 2. Main views
- Account.
- Financial Information.
- Profile completion summary.

## 3. Inputs
- Authenticated user/account.
- Personal information.
- Income sources, expenses, assets, liabilities aur goals.
- Onboarding store ka data.

## 4. Process
1. Authenticated user details load karo.
2. Personal/financial information se completion summary calculate karo.
3. Investor Account ya Financial Information tab dekhe.
4. Financial information section se related data review kare.
5. Sign out action par session end karke login page par le jao.

## 5. Output
- Account identity details.
- Financial information view.
- Profile completion percentage.
- Sign-out action.

## 6. Important boundaries
- Profile completion percentage sirf listed data sections ki completion ka indicator hai; financial plan ki quality ya goal feasibility ka score nahi.
- Profile mein information dikhna uske mathematically validated hone ka proof nahi.
- Profile aur Financial State ke exact synchronization rules verify karne honge.

## 7. Real-Life Decision Case relationships
- **Cases 5–6:** changes to income, expenses, assets, liabilities, or goal intent may affect financial calculations. Profile data display/save and downstream revalidation are separate steps.
- **Cases 7–11:** a financial input change may affect one goal, multiple goals, or the accepted implementation. Revalidation should be targeted to material effects; the whole plan should not be assumed to rebuild for every edit.
- Profile completion is not an adoption signal. Saving profile data must not silently convert a proposal into an Accepted Plan or overwrite an investor-adopted plan without an explicit workflow.

## 8. Code evidence
- Frontend: `frontend/app/investor/profile/page.tsx`
- Profile API: `backend/api/profile.py`
- Profile repository: `backend/data/profile_repository.py`
- Auth provider: Supabase auth usage frontend mein present hai.

## 9. Abhi unverified
- Profile fields ka complete edit/save behavior.
- Profile aur onboarding data ke beech source-of-truth rules.
- Completion score mein kaun se fields required honge, future changes ke baad.
- Which profile edits emit a financial-state change event and how downstream goal/strategy revalidation is triggered.
