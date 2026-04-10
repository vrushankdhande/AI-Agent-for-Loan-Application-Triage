from signals import extract_signals
from decision_maker import decide_from_signals
from model_response import generate_reasoning
from show_output import build_output
import json
import random


def generate_application(app_id):
    employment_type = random.choice(["salaried", "self-employed"])

    # -------------------------
    # Base Income Setup
    # -------------------------
    declared_income = random.randint(20000, 100000)

    case_type = random.choice([
        "clean",          # easy approve
        "income_mismatch",
        "high_emi",
        "high_cash",
        "bounces",
        "conflict",       # IMPORTANT
        "missing_docs"
    ])

    # -------------------------
    # Bank Behaviour Simulation
    # -------------------------
    if case_type == "clean":
        avg_credit = int(declared_income * random.uniform(0.9, 1.05))
        emi = int(declared_income * random.uniform(0.1, 0.3))
        cash = int(declared_income * random.uniform(0.1, 0.3))
        bounces = 0
        salary_consistency = "consistent"

    elif case_type == "income_mismatch":
        avg_credit = int(declared_income * random.uniform(0.4, 0.7))
        emi = int(declared_income * random.uniform(0.2, 0.4))
        cash = int(declared_income * random.uniform(0.2, 0.4))
        bounces = random.randint(0, 2)
        salary_consistency = "irregular"

    elif case_type == "high_emi":
        avg_credit = int(declared_income * random.uniform(0.8, 1.0))
        emi = int(declared_income * random.uniform(0.5, 0.8))
        cash = int(declared_income * random.uniform(0.2, 0.4))
        bounces = random.randint(1, 3)
        salary_consistency = "consistent"

    elif case_type == "high_cash":
        avg_credit = int(declared_income * random.uniform(0.8, 1.0))
        emi = int(declared_income * random.uniform(0.2, 0.4))
        cash = int(declared_income * random.uniform(0.6, 0.9))
        bounces = random.randint(0, 2)
        salary_consistency = "consistent"

    elif case_type == "bounces":
        avg_credit = int(declared_income * random.uniform(0.7, 1.0))
        emi = int(declared_income * random.uniform(0.3, 0.6))
        cash = int(declared_income * random.uniform(0.2, 0.4))
        bounces = random.randint(3, 6)
        salary_consistency = "irregular"

    elif case_type == "conflict":
        # High income BUT suspicious behaviour
        avg_credit = int(declared_income * random.uniform(0.9, 1.1))
        emi = int(declared_income * random.uniform(0.4, 0.6))
        cash = int(declared_income * random.uniform(0.5, 0.8))
        bounces = random.randint(2, 4)
        salary_consistency = "irregular"

    elif case_type == "missing_docs":
        avg_credit = int(declared_income * random.uniform(0.8, 1.0))
        emi = int(declared_income * random.uniform(0.2, 0.4))
        cash = int(declared_income * random.uniform(0.2, 0.4))
        bounces = random.randint(0, 2)
        salary_consistency = "consistent"

    # -------------------------
    # Documents
    # -------------------------
    if case_type == "missing_docs":
        bank_doc = random.choice(["missing", "present"])
        kyc_doc = random.choice(["missing", "present"])
    else:
        bank_doc = "present"
        kyc_doc = "present"

    salary_doc = "present" if employment_type == "salaried" else "na"

    # -------------------------
    # Salary Detection Logic
    # -------------------------
    salary_detected = (
        employment_type == "salaried" and
        salary_consistency == "consistent"
    )

    # -------------------------
    # Loan Amount (REALISTIC)
    # -------------------------
    loan_amount = int(declared_income * random.uniform(5, 15))

    # -------------------------
    # Final Application
    # -------------------------
    return {
        "id": f"APP{str(app_id).zfill(3)}",
        "case_type": case_type,  # 🔥 for evaluation/debug

        "employment_type": employment_type,
        "declared_income": declared_income,
        "loan_amount": loan_amount,
        "loan_purpose": random.choice(
            ["personal", "business", "car", "medical", "education"]
        ),

        "bank_statement_summary": {
            "avg_monthly_credit": avg_credit,
            "salary_detected": salary_detected,
            "salary_consistency": salary_consistency,
            "cash_withdrawals": cash,
            "emi_obligations": emi,
            "bounced_transactions": bounces
        },

        "documents": {
            "bank_statement": bank_doc,
            "salary_slip": salary_doc,
            "kyc": kyc_doc
        }
    }


def generate_dataset(n=50):
    return [generate_application(i+1) for i in range(n)]


# Generate dataset
data = generate_dataset(50)

# # Save
# with open("loan_applications.json", "w") as f:
#     json.dump(data, f, indent=2)

# print("✅ Realistic dataset generated")

print('The Random Id are from APP001 to APP050. Please enter any one of them to process the application.')
target_id = input("Enter Application ID to process (e.g., APP001): ").strip().upper()

index = next((i for i, item in enumerate(data) if item['id'] == target_id), None)

signals = extract_signals(data[index])
decision = decide_from_signals(signals)
reasoning_text=generate_reasoning(signals, decision)
output_main=build_output(signals, decision, reasoning_text)

print(output_main)

print('The Script Ends Here.')