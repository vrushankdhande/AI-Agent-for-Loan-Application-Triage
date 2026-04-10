def decide_from_signals(signals):

    print('decision code working.')
    income_ratio = signals["income_ratio"]
    emi_ratio = signals["emi_ratio"]
    bounce_count = signals["bounce_count"]
    missing_docs = signals["missing_docs"]
    cash_ratio = signals.get("cash_ratio", 0)
    risk_score = signals.get("risk_score", 0)

    decision = "REVIEW"  # default
    reasons = []

    # -------------------------
    # HARD RULES
    # -------------------------
    if missing_docs:
        decision = "REJECT"
        reasons.append("Missing required documents")

    elif income_ratio < 0.5:
        decision = "REJECT"
        reasons.append("Severe income mismatch")

    elif bounce_count >= 4:
        decision = "REJECT"
        reasons.append("Frequent payment bounces")

    # -------------------------
    # REVIEW CONDITIONS
    # -------------------------
    elif emi_ratio > 0.6:
        decision = "REVIEW"
        reasons.append("High EMI burden")

    elif income_ratio < 0.7:
        decision = "REVIEW"
        reasons.append("Income inconsistency")

    elif bounce_count >= 2:
        decision = "REVIEW"
        reasons.append("Some payment bounces")

    elif income_ratio > 0.9 and emi_ratio > 0.4:
        decision = "REVIEW"
        reasons.append("High income but high EMI burden")

    elif income_ratio > 0.9 and cash_ratio > 0.5:
        decision = "REVIEW"
        reasons.append("High income but suspicious cash activity")

    # -------------------------
    # APPROVE
    # -------------------------
    elif (
        income_ratio >= 0.9 and
        emi_ratio < 0.3 and
        bounce_count == 0 and
        cash_ratio < 0.4
    ):
        decision = "APPROVE"
        reasons.append("Strong financial profile")

    # -------------------------
    # FINAL STRUCTURED OUTPUT
    # -------------------------
    print('decision code worked.')
    return {
        "decision": decision,
        "confidence": round(max(0.5, 1 - (risk_score * 0.1)), 2),
        "reasons": reasons
    }