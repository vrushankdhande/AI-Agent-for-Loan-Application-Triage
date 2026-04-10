from langchain_groq import ChatGroq
import os
from constants import groq_api_key

os.environ["GROQ_API_KEY"] = groq_api_key

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    max_tokens=500,
)


def generate_reasoning(signals, decision):
    prompt = f"""
              You are a senior credit risk analyst at an NBFC.

              Your task is to explain a loan triage decision based on applicant financial signals.

              -----------------------------
              APPLICANT SIGNALS
              -----------------------------
              Income Ratio (actual vs declared): {signals['income_ratio']}
              EMI Ratio (EMI / income): {signals['emi_ratio']}
              Cash Withdrawal Ratio: {signals['cash_ratio']}
              Bounced Transactions: {signals['bounce_count']}
              Missing Documents: {signals['missing_docs']}
              Risk Score: {signals.get('risk_score', 'N/A')}

              -----------------------------
              SYSTEM DECISION
              -----------------------------
              {decision}

              -----------------------------
              INSTRUCTIONS
              -----------------------------
              1. Explain WHY this decision was made using the signals.
              2. Mention key financial strengths or weaknesses.
              3. Highlight any risk indicators (if present).
              4. Keep explanation concise (2–3 lines max).
              5. Be factual, no assumptions, no storytelling.

              -----------------------------
              OUTPUT FORMAT (STRICT)
              -----------------------------
              Return ONLY valid JSON:

              {{
                "reasoning": "<2-3 line explanation>",
                "key_risks": ["risk1", "risk2"],
                "summary": "<short one-line conclusion>"
              }}
              """
    print('response generated.')
    response = llm.invoke(prompt)
    return response.content