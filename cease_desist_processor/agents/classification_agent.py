from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from cease_desist_processor.state import DocumentState
from cease_desist_processor.config import AWS_REGION, BEDROCK_MODEL_ID

SYSTEM_PROMPT = """You are a legal document classifier specializing in Cease & Desist requests.

Classify the document into exactly one of:
- "cease"      : A valid cease & desist / stop communication request
- "irrelevant" : Not a cease & desist request (e.g. letter of authority, general notice)
- "uncertain"  : Ambiguous, requires human review

Also extract key details (sender name, date, reason if present).

Respond in this exact format:
CLASSIFICATION: <cease|irrelevant|uncertain>
REASON: <one sentence explanation>
DETAILS: <extracted key details>
"""


def classification_agent(state: DocumentState) -> DocumentState:
    """Classifies the document using Claude via Bedrock."""
    if state.get("error") or not state.get("raw_text"):
        return {**state, "classification": "uncertain", "classification_reason": "Could not extract text", "extracted_details": ""}

    llm = ChatBedrock(model_id=BEDROCK_MODEL_ID, region_name=AWS_REGION)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Document text:\n\n{state['raw_text'][:4000]}"),
    ]
    response = llm.invoke(messages)
    content = response.content

    classification = "uncertain"
    reason = ""
    details = ""

    for line in content.splitlines():
        if line.startswith("CLASSIFICATION:"):
            val = line.split(":", 1)[1].strip().lower()
            if val in ("cease", "irrelevant", "uncertain"):
                classification = val
        elif line.startswith("REASON:"):
            reason = line.split(":", 1)[1].strip()
        elif line.startswith("DETAILS:"):
            details = line.split(":", 1)[1].strip()

    return {
        **state,
        "classification": classification,
        "classification_reason": reason,
        "extracted_details": details,
    }
