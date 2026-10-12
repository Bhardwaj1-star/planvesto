# Profile — UI Profile vs Engine Profile

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Account and onboarding UI

`frontend/app/investor/profile/page.tsx` reads personal information, income sources, expenses, assets, liabilities and goals from the onboarding provider/store. It retrieves the email from Supabase Auth, derives initials from the display name, supports account and financial-information tabs, and signs out before navigating to `/login`.

The UI completion indicator increments for six local categories: name, income, expenses, assets, liabilities and goals. It is a simple presence count. It does not evaluate financial evidence, constraint conflicts, risk capacity, investor identity or suitability.

## Financial information section

`frontend/components/profile/FinancialInformationSection.tsx` presents financial information using onboarding state. Its saved/local state and the profile-engine result are distinct data paths unless an explicit synchronization/build action connects them.

## Engine profile

The backend Profile Engine builds structured constraints, priorities, conflicts, behavioral profile, risk profile and identity profile from Financial State and declared/observed/preference evidence. This result has a separate API and persistence lifecycle.

## Interpretation rule

Do not use “profile complete” as a synonym for “profile engine built”, “risk assessed”, “constraints validated” or “strategy suitable”. The account page's completion percentage is UI readiness only. Likewise, an existing profile-engine result does not prove its Financial State input is current; inspect snapshot ID and version provenance.
