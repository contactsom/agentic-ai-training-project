from cease_desist_processor.state import DocumentState
from cease_desist_processor.tools.archive_tool import archive_irrelevant


def archiving_agent(state: DocumentState) -> DocumentState:
    """Archives irrelevant documents to a flat CSV file."""
    archive_irrelevant(
        doc_name=state["doc_name"],
        received_date=state["received_date"],
    )
    return {**state, "archived": True}
