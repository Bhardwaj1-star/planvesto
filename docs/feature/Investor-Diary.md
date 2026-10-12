# Investor Diary

## 1. Main kaam
- Investor ko financial notes/entries record karne dena.
- Financial decisions ka record dekhna.
- Personal financial context aur decision history ko ek review surface par rakhna.

## 2. Main views
- Diary (Open Book).
- Decision History.
- Write in Diary action/modal.

## 3. Inputs
- Investor ke saved diary entries.
- Financial decision records.
- Investor dwara likha gaya naya entry.

## 4. Process
1. Diary entries aur decision records load karo.
2. Investor Diary ya Decision History tab select kare.
3. Naya entry likhe aur save kare.
4. Save ke baad entries/decisions reload hon.

## 5. Output
- Saved diary entries.
- Decision history list.
- Nayi entry ka saved record.

## 6. Important boundaries
- Diary entry user ka note hai; use automatically verified financial fact nahi maana ja sakta.
- Decision history record se yeh apne aap prove nahi hota ki decision current Accepted Plan hai.
- Diary ko audit log, version history ya action completion ka replacement nahi samajhna.

## 7. Code evidence
- Frontend: `frontend/app/investor/diary/page.tsx`
- Diary components: `frontend/components/diary/DiaryBook`, `DecisionHistoryView`, `BackendWriteEntryModal`
- API/repository: `backend/api/diary.py`, `backend/data/diary_repository.py`

## 8. Abhi unverified
- Diary data ka complete persistence/source-of-truth path.
- Edit/delete/retention permissions.
- Financial decisions ke saath exact linkage.
- Diary entries strategy selection ya future recommendations ko influence karti hain ya nahi.
