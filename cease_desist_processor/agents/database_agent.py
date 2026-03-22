from cease_desist_processor.state import DocumentState
from cease_desist_processor.tools.db_tool import store_cease_request


def database_agent(state: DocumentState) -> DocumentState:
    """Stores valid cease & desist requests in SQLite database."""
    msg = store_cease_request(
        doc_name=state["doc_name"],
        received_date=state["received_date"],
        details=state.get("extracted_details", ""),
    )
    return {**state, "db_stored": True}
