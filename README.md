# 🧠 AI Agent for Loan Application Triage
**CoVector AI Take-Home Assignment | Vrushank Dhande**

---

## 🚀 Overview
This project implements an **AI-driven loan triage agent** that processes loan applications end-to-end and routes them into one of three decisions:

- ✅ **APPROVE** – Eligible for auto-disbursal
- ⚠️ **REVIEW** – Requires human analyst intervention
- ❌ **REJECT** – High-risk or policy violation

The system is designed to **automate routine cases** while **surfacing non-routine or risky applications with clear reasoning and flags**, enabling faster decision-making by credit analysts.

---

## 🏗️ System Design

### 🔹 Inputs
Each application includes:
- Declared income
- Loan amount
- Employment type
- Loan purpose
- Documents:
  - Bank statement (6 months)
  - Salary slip / ITR
  - KYC (Aadhaar/PAN)

---

### 🔹 Signals Used (and Why)

| Signal | Description | Why it Matters |
|------|------------|----------------|
| **Income Ratio** | Declared income vs actual bank credits | Detects income inflation or fraud |
| **EMI Ratio** | EMI obligations / monthly income | Measures repayment capacity |
| **Cash Withdrawal Ratio** | Cash withdrawals / total credits | High values may indicate risky behavior |
| **Bounce Count** | Number of failed transactions | Indicates repayment reliability |
| **Salary Consistency** | Regular vs irregular credits | Stability of income |
| **Missing Documents** | Missing or incomplete uploads | Data reliability risk |

👉 These signals were chosen because they directly impact **creditworthiness, fraud detection, and repayment behavior**, rather than just raw extraction.

---

## ⚖️ Decision Logic & Thresholds

The routing logic is rule-based with contextual overrides.

### ❌ REJECT Conditions
- Income Ratio < **0.5** → Significant mismatch (fraud risk)
- EMI Ratio > **0.7** → Unsustainable debt load
- Bounce Count ≥ **4** → Poor repayment behavior
- Critical documents missing

---

### ⚠️ REVIEW Conditions
- Income Ratio between **0.5 – 0.75**
- EMI Ratio between **0.5 – 0.7**
- High cash withdrawal ratio (> 0.6)
- Irregular salary credits
- Conflicting signals (see below)

---

### ✅ APPROVE Conditions
- Income Ratio ≥ **0.9**
- EMI Ratio < **0.5**
- Stable salary credits
- Low cash withdrawals
- No transaction bounces

---

### 📌 Why These Thresholds?
- **EMI > 60–70%** → Financial stress in real-world lending
- **Income mismatch < 50%** → Strong fraud indicator
- **Frequent bounces** → Direct signal of repayment failure
- **High cash usage** → Reduced traceability, risk signal

These thresholds are inspired by **common NBFC credit heuristics** and simplified for this prototype.

---

## 🔄 Handling Conflicting Signals

Real-world applications often contain mixed indicators.

### Example:
- High income ratio ✅
- But high cash withdrawals ❌

### Strategy:
- Such cases are routed to **REVIEW**
- Explicit reasoning is generated:
  - *"Strong income but suspicious transaction behavior"*

👉 This ensures the system does **not over-trust a single strong signal**.

---

## ❓ Handling Ambiguity

Borderline cases (e.g., moderate income + moderate EMI burden) are:

➡️ Routed to **REVIEW**
➡️ Tagged with **"borderline profile"** reasoning

This avoids false approvals while minimizing unnecessary rejections.

---

## 📄 Handling Missing / Inconsistent Documents

| Scenario | Behavior |
|--------|---------|
| Missing critical docs | REJECT |
| Partially missing docs | REVIEW |
| Income inconsistency | REVIEW |
| Illegible / unreliable data | REVIEW |

👉 Not all missing data leads to rejection — the agent escalates when uncertainty exists.

---

## 🤖 Role of LLM in the Agent

The LLM is used for:
- Generating **human-readable reasoning**
- Explaining **key risk factors**
- Structuring output for analysts

For borderline cases, the LLM can also assist in:
- Context-aware decision refinement

---

## 📦 Output Format

The agent produces structured output:

```json
{
  "decision": "REVIEW",
  "confidence": 0.78,
  "key_signals": {
    "income_ratio": 0.75,
    "emi_ratio": 0.45,
    "salary_consistency": "irregular"
  },
  "flags": [
    "High EMI ratio",
    "Income mismatch"
  ],
  "summary": "Moderate risk; requires further review."
}
```

👉 This allows a credit analyst to **act immediately without re-reading documents**.

---

## 🔁 Reversed Design Decision (Important)

### ❌ Initial Approach:
All applications with missing documents were **automatically rejected**.

### ⚠️ Problem Observed:
During testing, this led to:
- False negatives (good applicants rejected)
- Overly strict filtering

### ✅ Final Approach:
- Missing documents → **REVIEW instead of REJECT** (unless critical)

### 💡 Insight:
In real-world systems, **uncertainty should escalate, not eliminate applicants**.

---

## 🧪 Example Scenarios

### Case 1: Ideal Applicant
- Stable salary
- Low EMI
- Clean transactions
➡️ **APPROVE**

### Case 2: Conflict Case
- High income
- High cash withdrawals
➡️ **REVIEW**

### Case 3: High Risk
- Low income match
- High EMI
- Multiple bounces
➡️ **REJECT**

---

## ⚙️ Tech Stack
- Python
- Rule-based decision engine
- LLM (Groq API) for reasoning

---

## 📌 Future Improvements
- Real bank statement parsing (PDF/CSV)
- Fraud pattern detection (round-tripping)
- Learning-based decision models
- Risk scoring instead of hard thresholds

---

## 🙌 Conclusion

This agent demonstrates how AI can:
- Automate routine credit decisions
- Highlight risky applications with context
- Reduce analyst workload significantly

The focus is not just automation — but **making decisions explainable and actionable**.

---

- **Author:** Vrushank Dhande
- **reference:** https://www.bajajfinserv.in/investments/what-is-ratio-analysis?
