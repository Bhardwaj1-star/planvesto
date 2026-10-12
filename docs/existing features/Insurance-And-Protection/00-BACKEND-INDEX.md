# Insurance & Protection — Implementation Evidence & Rule Index

**Backend Route:** `backend/api/insurance.py`  
**Extractor Service:** `backend/services/pdf_policy_extractor.py`  
**Business Rules:** `backend/rules/protection.py`  
**Canonical Rule Registry:** `backend/rules/canonical.py::required-insurance-cover`  
**Frontend Route:** `frontend/app/investor/onboarding/insurance/page.tsx`, `frontend/app/protect/page.tsx`

---

## 1. Role in Financial Planning

The Protection layer answers two fundamental questions:
1. *Is the investor adequately protected against mortality risk?*
2. *Does debt burden threaten family financial solvency in the absence of primary income?*

Protection is an **independent explanatory diagnostic and hard transformation rule**; existing assets are deliberately not netted off against insurance needs to preserve a clean protection signal.

---

## 2. API Contract: Local PDF Extraction (`/api/insurance/extract-policy-pdf`)

- **Method:** `POST`
- **Payload:** `multipart/form-data`, file binary (`.pdf` or `application/x-pdf`).
- **File Constraints:** Maximum 15 MB (`HTTP 413` if exceeded).
- **Security & Privacy:** Local extraction only. No external cloud AI or OCR API is invoked.
- **Engine:** PyMuPDF (`fitz`) with automatic Tesseract OCR fallback for scanned images:
  ```python
  text = page.get_text(textpage=page.get_textpage_ocr(language="eng"))
  ```
- **Extracted Fields (Regex Patterns in `pdf_policy_extractor.py`):**
  - `policy_name`: Matches plan/product name.
  - `insurer`: Matches insurance company.
  - `policy_number`: Matches alphanumeric policy identifiers.
  - `sum_assured`: Matches life cover amount (handles ₹, Rs, INR prefixes).
  - `premium`: Installment premium amount.
  - `premium_frequency`: Monthly, Quarterly, Half-Yearly, Yearly/Annual.
  - `maturity_date`: Maturity date.
  - `maturity_value`: Expected maturity amount.
  - `current_surrender_value`: Current surrender/fund value.

---

## 3. Canonical Protection Business Rules (`rules/protection.py`)

### A. Baseline Cover Calculation Rule
$$\text{required\_cover} = (\text{annual\_income} \times 10.0) + \text{total\_liabilities}$$

- **`INCOME_REPLACEMENT_YEARS`:** Fixed benchmark of `10.0` years of gross annual income.
- **Liability Protection:** 100% of outstanding debt liabilities are added.
- **Asset Netting Policy:** Existing assets are **not** subtracted; insurance is treated as pure risk transfer.

### B. Policy Classification Vocabularies
- **Life Insurance Types:** `term insurance`, `term`, `endowment`, `whole life`, `ulip`, `money back`.
- **Health Insurance Types:** `health insurance`, `health`.

### C. MoneyWheel Diagnostic Ratio
In `backend/rules/moneywheel.py::RULES["insurance_coverage"]`:
$$\text{insurance\_coverage\_ratio} = \frac{\text{existing\_sum\_assured}}{\text{required\_cover}} \times 100$$
- **Excellent:** $\ge 100\%$ (Fully protected).
- **Healthy:** $\ge 80\%$ (Adequate buffer).
- **Attention:** $50\% - 79\%$.
- **Critical:** $< 50\%$ (Severe mortality protection deficit).
