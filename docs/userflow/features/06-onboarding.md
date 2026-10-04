# Onboarding

## 1. Purpose

Onboarding is the **starting point of the financial planning system**.

Its job is to collect the user's important financial information once, in an organized way, so the rest of Planvesto can build a reliable picture of the user's financial life.

Onboarding is **not the financial plan itself**. It provides the information on which the financial plan is built.

---

## 2. Complete User Flow

The user should move through onboarding in this order:

```text
User
  ↓
Personal Information
  ↓
Family / Dependents
  ↓
Income
  ↓
Expenses
  ↓
Assets
  ↓
Liabilities
  ↓
Insurance
  ↓
Goals
  ↓
Complete Financial Picture
  ↓
Financial Health & Measures
  ↓
Goal Planner / MoneyWheel / Strategy
```

This is the core onboarding flow and should remain understandable to a normal user.

---

## 3. What We Need to Understand About the User

Onboarding must collect the information needed to answer four basic questions:

### A. Who is the user?

- Personal information
- Family and dependents

### B. How does money come in and go out?

- Income
- Expenses

### C. What does the user own and owe?

- Assets
- Liabilities

### D. What protection does the user have and what does the user want to achieve?

- Insurance
- Financial goals

These together form the user's **starting financial picture**.

---

## 4. Insurance Is a Core Part of Onboarding

Insurance is not an optional side feature.

It is part of understanding the user's financial position because insurance can provide:

- financial protection;
- health protection;
- life protection;
- an existing financial commitment through premiums;
- and, in some policies, a financial value or maturity value.

Therefore **Insurance must be a dedicated onboarding step**.

### Correct position

```text
Assets
  ↓
Liabilities
  ↓
Insurance
  ↓
Goals
```

The system already has Insurance functionality. The problem is that it is not currently included in the guided onboarding journey.

**System decision:** integrate the existing Insurance functionality into onboarding rather than creating another Insurance system.

---

## 5. What Each Step Means

| Step | What we are collecting | Why it matters |
|---|---|---|
| Personal Information | Basic identity and personal circumstances | Establishes the user's planning context |
| Family / Dependents | People financially connected to the user | Determines who the financial plan needs to consider |
| Income | Sources and amount of income | Establishes earning capacity |
| Expenses | Regular and important spending | Establishes cost of living and available surplus |
| Assets | Things the user owns financially | Establishes existing wealth/resources |
| Liabilities | Loans and other obligations | Establishes debt burden |
| Insurance | Life, health and other policies | Establishes protection and insurance-related financial commitments |
| Goals | What the user wants to achieve | Defines what the financial plan needs to accomplish |

---

## 6. Important Business Rules

These are the decisions that the rest of the system must be built around.

### 6.1 Onboarding captures facts; it does not make the plan

The user tells the system what is true about their financial life.

The system should then use those facts to calculate financial health, evaluate goals and build strategies.

Onboarding should not independently decide:

- whether a goal is financially feasible;
- which strategy is best;
- how much the user should invest;
- or what the user's financial health score is.

Those decisions belong to the downstream planning system.

### 6.2 The user's financial information must connect

The information collected in onboarding cannot remain as isolated forms.

It must come together into one financial picture:

```text
Personal
+ Family
+ Income
+ Expenses
+ Assets
+ Liabilities
+ Insurance
+ Goals
        ↓
Complete Financial Picture
```

This combined picture is the foundation for everything that follows.

### 6.3 Insurance must affect the financial picture correctly

Insurance should not be treated as only a document or checklist.

Where applicable:

- premiums are part of the user's financial commitments;
- policy value can represent an existing financial asset;
- protection information can be used for insurance/protection analysis.

The system must use the existing Insurance rules consistently.

### 6.4 Goals are intentions, not conclusions

When a user says:

> "I want to retire at 55."

or

> "I want financial freedom through passive income."

that is the user's **goal**, not the system's conclusion that the goal is achievable.

The Goal Planner must later determine:

- what the goal will cost;
- whether current resources are sufficient;
- what funding is required;
- and what strategy may be appropriate.

### 6.5 Different goals must remain conceptually separate

Onboarding may collect different kinds of goals, but the planning system must preserve their meaning.

For example:

- **Retirement** is not the same as **Financial Independence**.
- Financial Independence / Financial Freedom is associated with the user's ability to sustain life through sufficient independent/passive income.
- A beneficiary or circumstance such as "child" does not automatically create a new goal category.

The goal itself must remain clear; additional circumstances can be captured as supporting information.

---

## 7. What Onboarding Must Produce

At the end of onboarding, the system should have a reliable answer to:

> **"What does this person's financial life look like today, and what are they trying to achieve?"**

That means the system should know:

- who the user is;
- who depends on them;
- how much they earn;
- how much they spend;
- what they own;
- what they owe;
- what protection they have;
- and what they want to achieve.

This becomes the **single starting point for financial planning**.

---

## 8. What Happens After Onboarding

Onboarding hands the collected information to the rest of the system.

```text
Onboarding
    ↓
Complete Financial Picture
    ↓
Financial Health & Measures
    ↓
Goal Planning
    ↓
MoneyWheel
    ↓
Strategy Building
```

Each stage should use the same underlying financial picture.

The system must not create different versions of the user's financial reality for different features.

---

## 9. Core System Principles

These principles are more important than the individual screens.

1. **One user → one coherent financial picture.**
2. **Onboarding collects facts; downstream systems analyse and plan.**
3. **Insurance is a first-class part of financial planning.**
4. **Assets, liabilities, insurance, income and expenses must connect to the same financial picture.**
5. **Goals describe what the user wants; the system later determines feasibility and strategy.**
6. **Goal meaning must remain canonical and consistent throughout the system.**
7. **The same financial reality must be used by Financial Health, Goal Planner, MoneyWheel and Strategy Builder.**
8. **Existing domain logic should be reused rather than creating duplicate systems.**

---

## 10. Current Correction

### Problem

Insurance already exists in Planvesto, but the guided onboarding journey does not currently include it.

### Required correction

Add Insurance as a dedicated onboarding step:

```text
Liabilities
    ↓
Insurance
    ↓
Goals
```

The correction should integrate the existing Insurance functionality and make its information part of the same financial picture used by the rest of the system.

---

## 11. Final Business-Level Contract

```text
USER
  ↓
UNDERSTAND THE USER
  ↓
UNDERSTAND THEIR MONEY
  ↓
UNDERSTAND THEIR PROTECTION
  ↓
UNDERSTAND THEIR GOALS
  ↓
BUILD ONE COMPLETE FINANCIAL PICTURE
  ↓
ANALYSE
  ↓
PLAN
  ↓
BUILD STRATEGIES
```

**This document defines the business-level purpose and flow of Onboarding. Detailed implementation decisions belong to the code and supporting technical documentation.**
