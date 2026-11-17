"""
Chapter 03 — Canonical Identity, Categories & Goal Taxonomy
Canonical Financial Category Taxonomy (§4.1 - §4.5)

Non-negotiable invariants:
1. Category IDs classify what kind of financial information this is.
2. They do not by themselves establish liquidity, accessibility, tax treatment, or ratio eligibility.
3. Keep flows and stocks distinct: Income/Expenses are period flows; Assets/Liabilities are dated balances.
4. Keep debt balances distinct from debt payments (EMI is an outflow; loan balance is a balance).
5. No double-counting: EMI is counted once as an expense; savings/SIPs are counted once under savings/investments.
6. Transfers between own accounts are neither Income nor Expenses.
7. Credit-card purchases are an Expense in purchase month, not again at bill payment.
8. Insurance premiums are expenses (expense_insurance); the policy itself is not an asset by default.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class FinancialGroup(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"
    LIABILITY = "liability"
    INSURANCE = "insurance"


# --- 4.1 Income Categories ---
class CanonicalIncomeCategoryId(str, Enum):
    SALARY = "income_salary"
    BUSINESS = "income_business"
    PROFESSIONAL_FREELANCE = "income_professional_freelance"
    RENTAL = "income_rental"
    INTEREST = "income_interest"
    DIVIDEND = "income_dividend"
    PENSION = "income_pension"
    OTHER = "income_other"


# --- 4.2 Expense Categories ---
class CanonicalExpenseCategoryId(str, Enum):
    HOUSING = "expense_housing"
    FOOD_GROCERIES = "expense_food_groceries"
    UTILITIES = "expense_utilities"
    TRANSPORTATION = "expense_transportation"
    EDUCATION = "expense_education"
    HEALTHCARE = "expense_healthcare"
    INSURANCE = "expense_insurance"
    DEBT_PAYMENTS = "expense_debt_payments"
    FAMILY_SUPPORT = "expense_family_support"
    TRAVEL = "expense_travel"
    ENTERTAINMENT = "expense_entertainment"
    SHOPPING = "expense_shopping"
    OTHER = "expense_other"


# --- 4.3 Asset Categories ---
class CanonicalAssetCategoryId(str, Enum):
    BANK_CASH = "asset_bank_cash"
    FIXED_DEPOSITS = "asset_fixed_deposits"
    MUTUAL_FUNDS = "asset_mutual_funds"
    STOCKS_EQUITY = "asset_stocks_equity"
    BONDS_DEBT = "asset_bonds_debt"
    EPF_PPF = "asset_epf_ppf"
    NPS = "asset_nps"
    GOLD = "asset_gold"
    REAL_ESTATE = "asset_real_estate"
    BUSINESS_OWNERSHIP = "asset_business_ownership"
    VEHICLE = "asset_vehicle"
    OTHER = "asset_other"


# --- 4.4 Liability Categories ---
class CanonicalLiabilityCategoryId(str, Enum):
    HOME_LOAN = "liability_home_loan"
    CAR_LOAN = "liability_car_loan"
    PERSONAL_LOAN = "liability_personal_loan"
    EDUCATION_LOAN = "liability_education_loan"
    BUSINESS_LOAN = "liability_business_loan"
    CREDIT_CARD = "liability_credit_card"
    OTHER = "liability_other"


# --- 4.5 Insurance Policy Types ---
class CanonicalInsurancePolicyTypeId(str, Enum):
    TERM_LIFE = "insurance_term_life"
    WHOLE_LIFE_ENDOWMENT = "insurance_whole_life_endowment"
    ULIP = "insurance_ulip"
    HEALTH = "insurance_health"
    CRITICAL_ILLNESS_ACCIDENT_DISABILITY = "insurance_critical_illness_accident_disability"
    MOTOR = "insurance_motor"
    HOME_PROPERTY = "insurance_home_property"
    TRAVEL = "insurance_travel"
    OTHER_BUSINESS_LIABILITY = "insurance_other_business_liability"


@dataclass(frozen=True)
class CategoryTaxonomyDefinition:
    id: str
    group: FinancialGroup
    display_name: str
    definition: str
    classification_guidance: str


CATEGORY_DEFINITIONS: Dict[str, CategoryTaxonomyDefinition] = {
    # Income
    CanonicalIncomeCategoryId.SALARY.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.SALARY.value,
        group=FinancialGroup.INCOME,
        display_name="Salary",
        definition="Compensation received from employment.",
        classification_guidance="Distinguish gross salary from take-home pay.",
    ),
    CanonicalIncomeCategoryId.BUSINESS.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.BUSINESS.value,
        group=FinancialGroup.INCOME,
        display_name="Business",
        definition="Income arising from operating a business.",
        classification_guidance="Distinguish business revenue from business profit; label which amount is reported.",
    ),
    CanonicalIncomeCategoryId.PROFESSIONAL_FREELANCE.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.PROFESSIONAL_FREELANCE.value,
        group=FinancialGroup.INCOME,
        display_name="Professional/Freelance",
        definition="Fees received for independent professional or freelance work.",
        classification_guidance="Distinguish total client receipts from income after work-related costs.",
    ),
    CanonicalIncomeCategoryId.RENTAL.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.RENTAL.value,
        group=FinancialGroup.INCOME,
        display_name="Rental",
        definition="Income received from renting property or other assets.",
        classification_guidance="Distinguish rent received from rental income after related costs.",
    ),
    CanonicalIncomeCategoryId.INTEREST.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.INTEREST.value,
        group=FinancialGroup.INCOME,
        display_name="Interest",
        definition="Interest earned on deposits, savings or debt instruments.",
        classification_guidance="Interest is an income flow; classify the underlying holding separately as an asset.",
    ),
    CanonicalIncomeCategoryId.DIVIDEND.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.DIVIDEND.value,
        group=FinancialGroup.INCOME,
        display_name="Dividend",
        definition="Dividend distributions received from investments.",
        classification_guidance="Dividend is the income flow; the investment itself remains an asset.",
    ),
    CanonicalIncomeCategoryId.PENSION.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.PENSION.value,
        group=FinancialGroup.INCOME,
        display_name="Pension",
        definition="Pension income received by the investor or household.",
        classification_guidance="Record the relevant period and distinguish expected payments from amounts actually received.",
    ),
    CanonicalIncomeCategoryId.OTHER.value: CategoryTaxonomyDefinition(
        id=CanonicalIncomeCategoryId.OTHER.value,
        group=FinancialGroup.INCOME,
        display_name="Other",
        definition="Income that does not fit another listed category.",
        classification_guidance="Use only when no listed category fits; do not duplicate a listed category.",
    ),

    # Expense
    CanonicalExpenseCategoryId.HOUSING.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.HOUSING.value,
        group=FinancialGroup.EXPENSE,
        display_name="Housing",
        definition="Costs of housing and residential occupancy.",
        classification_guidance="Identify the component where useful; do not count the same cost twice.",
    ),
    CanonicalExpenseCategoryId.FOOD_GROCERIES.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.FOOD_GROCERIES.value,
        group=FinancialGroup.EXPENSE,
        display_name="Food & Groceries",
        definition="Household groceries and food consumption.",
        classification_guidance="Keep the treatment of dining out consistent with the chosen category convention.",
    ),
    CanonicalExpenseCategoryId.UTILITIES.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.UTILITIES.value,
        group=FinancialGroup.EXPENSE,
        display_name="Utilities",
        definition="Household utility services.",
        classification_guidance="Classify the service charge here rather than under general shopping.",
    ),
    CanonicalExpenseCategoryId.TRANSPORTATION.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.TRANSPORTATION.value,
        group=FinancialGroup.EXPENSE,
        display_name="Transportation",
        definition="Costs of routine travel and transport.",
        classification_guidance="Use for routine commuting; trip-related holiday costs belong under Travel.",
    ),
    CanonicalExpenseCategoryId.EDUCATION.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.EDUCATION.value,
        group=FinancialGroup.EXPENSE,
        display_name="Education",
        definition="Education-related spending.",
        classification_guidance="Keep education expenses distinct from outstanding Education Loan balances.",
    ),
    CanonicalExpenseCategoryId.HEALTHCARE.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.HEALTHCARE.value,
        group=FinancialGroup.EXPENSE,
        display_name="Healthcare",
        definition="Medical and healthcare spending.",
        classification_guidance="Record insurance premiums under Insurance.",
    ),
    CanonicalExpenseCategoryId.INSURANCE.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.INSURANCE.value,
        group=FinancialGroup.EXPENSE,
        display_name="Insurance",
        definition="Premiums paid for insurance policies.",
        classification_guidance="Classify premiums here; claims received are not expenses.",
    ),
    CanonicalExpenseCategoryId.DEBT_PAYMENTS.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.DEBT_PAYMENTS.value,
        group=FinancialGroup.EXPENSE,
        display_name="Debt Payments",
        definition="Regular or planned cash payments required for loans or other outstanding liabilities.",
        classification_guidance="For cash-flow planning, count payment once as outflow. Keep loan balance separate.",
    ),
    CanonicalExpenseCategoryId.FAMILY_SUPPORT.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.FAMILY_SUPPORT.value,
        group=FinancialGroup.EXPENSE,
        display_name="Family Support",
        definition="Money spent or transferred to support family members.",
        classification_guidance="Avoid counting the same transfer again under another expense category.",
    ),
    CanonicalExpenseCategoryId.TRAVEL.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.TRAVEL.value,
        group=FinancialGroup.EXPENSE,
        display_name="Travel",
        definition="Travel-related spending, including trips and accommodation.",
        classification_guidance="Use for trips; routine commuting belongs under Transportation.",
    ),
    CanonicalExpenseCategoryId.ENTERTAINMENT.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.ENTERTAINMENT.value,
        group=FinancialGroup.EXPENSE,
        display_name="Entertainment",
        definition="Spending on leisure and entertainment.",
        classification_guidance="Use for leisure activities not better classified elsewhere.",
    ),
    CanonicalExpenseCategoryId.SHOPPING.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.SHOPPING.value,
        group=FinancialGroup.EXPENSE,
        display_name="Shopping",
        definition="Purchases of personal or household goods not better classified elsewhere.",
        classification_guidance="Prefer a more specific listed category when one fits.",
    ),
    CanonicalExpenseCategoryId.OTHER.value: CategoryTaxonomyDefinition(
        id=CanonicalExpenseCategoryId.OTHER.value,
        group=FinancialGroup.EXPENSE,
        display_name="Other",
        definition="Spending that does not fit another listed category.",
        classification_guidance="Use only when no listed category fits; do not duplicate a listed category.",
    ),

    # Asset
    CanonicalAssetCategoryId.BANK_CASH.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.BANK_CASH.value,
        group=FinancialGroup.ASSET,
        display_name="Bank / Cash",
        definition="Cash on hand and money held in bank accounts.",
        classification_guidance="Do not assume every recorded balance is immediately available for spending.",
    ),
    CanonicalAssetCategoryId.FIXED_DEPOSITS.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.FIXED_DEPOSITS.value,
        group=FinancialGroup.ASSET,
        display_name="Fixed Deposits",
        definition="Money held in fixed-term deposit products.",
        classification_guidance="Early withdrawal conditions may affect practical access to the funds.",
    ),
    CanonicalAssetCategoryId.MUTUAL_FUNDS.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.MUTUAL_FUNDS.value,
        group=FinancialGroup.ASSET,
        display_name="Mutual Funds",
        definition="Units or holdings in mutual fund schemes.",
        classification_guidance="Distinguish current value from invested cost; access conditions may vary.",
    ),
    CanonicalAssetCategoryId.STOCKS_EQUITY.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.STOCKS_EQUITY.value,
        group=FinancialGroup.ASSET,
        display_name="Stocks / Equity",
        definition="Direct equity or shareholdings.",
        classification_guidance="Distinguish current market value from invested cost.",
    ),
    CanonicalAssetCategoryId.BONDS_DEBT.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.BONDS_DEBT.value,
        group=FinancialGroup.ASSET,
        display_name="Bonds / Debt",
        definition="Bond or debt-security holdings owned by the investor.",
        classification_guidance="An owned debt instrument is an asset, not a liability owed by the investor.",
    ),
    CanonicalAssetCategoryId.EPF_PPF.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.EPF_PPF.value,
        group=FinancialGroup.ASSET,
        display_name="EPF / PPF",
        definition="Employee Provident Fund and Public Provident Fund balances.",
        classification_guidance="Withdrawal restrictions affect accessibility, not asset classification.",
    ),
    CanonicalAssetCategoryId.NPS.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.NPS.value,
        group=FinancialGroup.ASSET,
        display_name="NPS",
        definition="National Pension System holdings or balance.",
        classification_guidance="Retirement purpose and withdrawal conditions affect how and when funds may be used.",
    ),
    CanonicalAssetCategoryId.GOLD.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.GOLD.value,
        group=FinancialGroup.ASSET,
        display_name="Gold",
        definition="Gold owned as a financial or physical holding.",
        classification_guidance="Use a reasonable valuation basis; physical ownership does not mean cash is immediately available.",
    ),
    CanonicalAssetCategoryId.REAL_ESTATE.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.REAL_ESTATE.value,
        group=FinancialGroup.ASSET,
        display_name="Real Estate",
        definition="Property owned by the investor or household.",
        classification_guidance="Account for ownership share and do not presume immediate liquidity.",
    ),
    CanonicalAssetCategoryId.BUSINESS_OWNERSHIP.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.BUSINESS_OWNERSHIP.value,
        group=FinancialGroup.ASSET,
        display_name="Business Ownership",
        definition="Ownership interest in a business.",
        classification_guidance="Business revenue is not the same as the value of the ownership interest.",
    ),
    CanonicalAssetCategoryId.VEHICLE.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.VEHICLE.value,
        group=FinancialGroup.ASSET,
        display_name="Vehicle",
        definition="A vehicle owned by the investor or household.",
        classification_guidance="Ownership does not imply cash liquidity; distinguish value from related loan balance.",
    ),
    CanonicalAssetCategoryId.OTHER.value: CategoryTaxonomyDefinition(
        id=CanonicalAssetCategoryId.OTHER.value,
        group=FinancialGroup.ASSET,
        display_name="Other",
        definition="An asset that does not fit another listed category.",
        classification_guidance="Use only when no listed category fits; do not duplicate a listed category.",
    ),

    # Liability
    CanonicalLiabilityCategoryId.HOME_LOAN.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.HOME_LOAN.value,
        group=FinancialGroup.LIABILITY,
        display_name="Home Loan",
        definition="Outstanding debt secured against a home or residential property.",
        classification_guidance="Keep loan balance distinct from EMI and property value.",
    ),
    CanonicalLiabilityCategoryId.CAR_LOAN.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.CAR_LOAN.value,
        group=FinancialGroup.LIABILITY,
        display_name="Car Loan",
        definition="Outstanding borrowing used to finance a vehicle.",
        classification_guidance="Keep loan balance distinct from payment amount and vehicle value.",
    ),
    CanonicalLiabilityCategoryId.PERSONAL_LOAN.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.PERSONAL_LOAN.value,
        group=FinancialGroup.LIABILITY,
        display_name="Personal Loan",
        definition="Outstanding personal borrowing not classified under another listed loan type.",
        classification_guidance="Keep distinct loans distinguishable when assessing total liabilities.",
    ),
    CanonicalLiabilityCategoryId.EDUCATION_LOAN.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.EDUCATION_LOAN.value,
        group=FinancialGroup.LIABILITY,
        display_name="Education Loan",
        definition="Outstanding borrowing used to finance education.",
        classification_guidance="Beneficiary details do not create a separate liability category.",
    ),
    CanonicalLiabilityCategoryId.BUSINESS_LOAN.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.BUSINESS_LOAN.value,
        group=FinancialGroup.LIABILITY,
        display_name="Business Loan",
        definition="Outstanding borrowing associated with business activity.",
        classification_guidance="Do not assume a business obligation is a personal obligation without evidence.",
    ),
    CanonicalLiabilityCategoryId.CREDIT_CARD.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.CREDIT_CARD.value,
        group=FinancialGroup.LIABILITY,
        display_name="Credit Card",
        definition="Outstanding amount owed to a card issuer.",
        classification_guidance="Keep outstanding balance distinct from minimum due, statement amount and credit limit.",
    ),
    CanonicalLiabilityCategoryId.OTHER.value: CategoryTaxonomyDefinition(
        id=CanonicalLiabilityCategoryId.OTHER.value,
        group=FinancialGroup.LIABILITY,
        display_name="Other",
        definition="A liability that does not fit another listed category.",
        classification_guidance="Use only when no listed category fits; do not duplicate a listed category.",
    ),

    # Insurance
    CanonicalInsurancePolicyTypeId.TERM_LIFE.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.TERM_LIFE.value,
        group=FinancialGroup.INSURANCE,
        display_name="Term Life",
        definition="Pure protection insurance covering life risk for a defined term.",
        classification_guidance="Check cover amount and duration against dependants and liabilities.",
    ),
    CanonicalInsurancePolicyTypeId.WHOLE_LIFE_ENDOWMENT.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.WHOLE_LIFE_ENDOWMENT.value,
        group=FinancialGroup.INSURANCE,
        display_name="Whole Life / Endowment / Money-Back",
        definition="Life insurance with bundled savings or investment components.",
        classification_guidance="Separate protection from savings; do not treat non-guaranteed benefits as guaranteed assets.",
    ),
    CanonicalInsurancePolicyTypeId.ULIP.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.ULIP.value,
        group=FinancialGroup.INSURANCE,
        display_name="ULIP",
        definition="Unit Linked Insurance Plan combining life cover with market-linked investment funds.",
        classification_guidance="Keep current fund value distinct from sum assured; confirm lock-in.",
    ),
    CanonicalInsurancePolicyTypeId.HEALTH.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.HEALTH.value,
        group=FinancialGroup.INSURANCE,
        display_name="Health — Individual / Family Floater",
        definition="Indemnity health insurance covering medical expenses and hospitalization.",
        classification_guidance="Check each family member's inclusion, adequacy of sum insured, waiting periods.",
    ),
    CanonicalInsurancePolicyTypeId.CRITICAL_ILLNESS_ACCIDENT_DISABILITY.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.CRITICAL_ILLNESS_ACCIDENT_DISABILITY.value,
        group=FinancialGroup.INSURANCE,
        display_name="Critical Illness / Personal Accident / Disability",
        definition="Defined benefit coverage paying lump sum or replacement benefit upon critical illness or disability.",
        classification_guidance="Confirm trigger event; supplements rather than duplicates health cover.",
    ),
    CanonicalInsurancePolicyTypeId.MOTOR.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.MOTOR.value,
        group=FinancialGroup.INSURANCE,
        display_name="Motor — Vehicle",
        definition="Mandatory third-party and optional own-damage cover for motor vehicles.",
        classification_guidance="Check mandatory third-party cover and policy expiry.",
    ),
    CanonicalInsurancePolicyTypeId.HOME_PROPERTY.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.HOME_PROPERTY.value,
        group=FinancialGroup.INSURANCE,
        display_name="Home / Property",
        definition="Property and contents insurance against fire, disaster, theft and damage.",
        classification_guidance="Building vs contents cover; check insured risks.",
    ),
    CanonicalInsurancePolicyTypeId.TRAVEL.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.TRAVEL.value,
        group=FinancialGroup.INSURANCE,
        display_name="Travel",
        definition="Short-term trip cover for medical emergency, cancellation and travel inconvenience.",
        classification_guidance="Check destination geography, dates, and medical limits.",
    ),
    CanonicalInsurancePolicyTypeId.OTHER_BUSINESS_LIABILITY.value: CategoryTaxonomyDefinition(
        id=CanonicalInsurancePolicyTypeId.OTHER_BUSINESS_LIABILITY.value,
        group=FinancialGroup.INSURANCE,
        display_name="Other / Business / Liability",
        definition="Specialist commercial, liability or niche insurance.",
        classification_guidance="Record actual policy wording; do not force specialist cover into personal types.",
    ),
}


def get_category_definition(category_id: str) -> Optional[CategoryTaxonomyDefinition]:
    """Retrieve canonical category definition by category ID string."""
    return CATEGORY_DEFINITIONS.get(category_id)
