from cease_desist_processor.state import DocumentState
from cease_desist_processor.tools.pdf_loader import load_pdf_text
from datetime import date


def document_loader_agent(state: DocumentState) -> DocumentState:
    """Loads PDF and extracts raw text."""
    try:
        raw_text = load_pdf_text(state["pdf_path"])
        return {
            **state,
            "raw_text": raw_text,
            "received_date": state.get("received_date") or date.today().isoformat(),
            "error": None,
        }
    except Exception as e:
        return {**state, "raw_text": "", "error": str(e)}
