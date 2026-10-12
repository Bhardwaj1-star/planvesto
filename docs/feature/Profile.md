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

## 7. Code evidence
- Frontend: `frontend/app/investor/profile/page.tsx`
- Profile API: `backend/api/profile.py`
- Profile repository: `backend/data/profile_repository.py`
- Auth provider: Supabase auth usage frontend mein present hai.

## 8. Abhi unverified
- Profile fields ka complete edit/save behavior.
- Profile aur onboarding data ke beech source-of-truth rules.
- Completion score mein kaun se fields required honge, future changes ke baad.
