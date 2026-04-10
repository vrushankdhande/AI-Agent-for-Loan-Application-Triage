import json

def build_output(signals, decision_output, llm_response):
    try:
        reasoning_json = json.loads(llm_response)
    except:
        reasoning_json = {
            "reasoning": llm_response,
            "key_risks": [],
            "summary": "LLM output parsing failed"
        }

    decision = decision_output.get("decision", "REVIEW")
    base_confidence = decision_output.get("confidence", 0.6)

    risk_score = signals.get("risk_score", 5)

    if decision == "APPROVE":
        confidence = max(0.7, 1 - (risk_score * 0.05))
    elif decision == "REJECT":
        confidence = min(0.95, 0.7 + (risk_score * 0.05))
    else:
        confidence = max(0.5, 0.75 - (risk_score * 0.03))

    confidence = round(confidence, 2)


    key_signals = {
        "income_ratio": signals["income_ratio"],
        "emi_ratio": signals["emi_ratio"],
        "cash_ratio": signals["cash_ratio"],
        "bounce_count": signals["bounce_count"],
        "risk_score": risk_score
    }


    flags = []

    if signals["income_ratio"] < 0.75:
        flags.append("Declared income higher than bank credits")

    if signals["emi_ratio"] > 0.5:
        flags.append("High EMI burden")

    if signals["cash_ratio"] > 0.6:
        flags.append("High cash withdrawals")

    if signals["bounce_count"] >= 2:
        flags.append("Payment reliability issues")

    if signals["missing_docs"]:
        flags.append("Missing required documents")

    # Merge LLM risks (avoid duplicates)
    flags = list(set(flags + reasoning_json.get("key_risks", [])))

    # -------------------------
    # Recommended Action
    # -------------------------
    if decision == "APPROVE":
        action = "Auto-approve and disburse loan"
    elif decision == "REJECT":
        action = "Reject application with reason codes"
    else:
        action = "Manual credit analyst review required"

    # -------------------------
    # Final Output
    # -------------------------

    print('output generated please check.')
    return {
        "decision": decision,
        "confidence": confidence,
        "key_signals": key_signals,
        "flags": flags,
        "reasoning": reasoning_json.get("reasoning", ""),
        "summary": reasoning_json.get("summary", ""),
        "recommended_action": action
    }