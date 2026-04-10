
### new main code


def extract_signals(app):

    print('signals function working.')
    bs = app["bank_statement_summary"]
    docs = app["documents"]


    avg_credit = max(bs.get("avg_monthly_credit", 0), 1)
    declared_income = max(app.get("declared_income", 1), 1)

    income_ratio = avg_credit / declared_income
    cash_ratio = bs.get("cash_withdrawals", 0) / avg_credit
    emi_ratio = bs.get("emi_obligations", 0) / avg_credit
    net_income = avg_credit - bs.get("emi_obligations", 0)

    bounce_count = bs.get("bounced_transactions", 0)

    missing_docs = any(v == "missing" for v in docs.values())
    risk_score = 0


    # Income
    if income_ratio < 0.5:
        risk_score += 3
    elif income_ratio < 0.7:
        risk_score += 2

    # EMI
    if emi_ratio > 0.6:
        risk_score += 3
    elif emi_ratio > 0.4:
        risk_score += 2

    # Cash
    if cash_ratio > 0.6:
        risk_score += 1

    # Bounces
    if bounce_count >= 4:
        risk_score += 3
    elif bounce_count >= 2:
        risk_score += 2

    # Documents
    if missing_docs:
        risk_score += 3

    
    print('signals function worked.')
    return {
        "income_ratio": round(income_ratio, 2),
        "cash_ratio": round(cash_ratio, 2),
        "emi_ratio": round(emi_ratio, 2),
        "bounce_count": bounce_count,
        "net_income": net_income,
        "missing_docs": missing_docs,
        "risk_score": risk_score
    }