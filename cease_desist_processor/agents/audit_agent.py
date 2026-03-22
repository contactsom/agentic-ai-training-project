from cease_desist_processor.state import DocumentState
from cease_desist_processor.tools.audit_tool import log_audit


def audit_agent(state: DocumentState) -> DocumentState:
    """Logs the full processing decision to the audit trail."""
    final_class = state.get("hitl_decision") or state["classification"]

    if state.get("db_stored"):
        action = "STORED_IN_DB"
    elif state.get("archived"):
        action = "ARCHIVED_TO_FILE"
    else:
        action = "PENDING_HITL"

    log_audit(
        doc_name=state["doc_name"],
        classification=final_class,
        reason=state.get("classification_reason", ""),
        action=action,
        extra=f"HITL={state.get('hitl_decision', 'N/A')}",
    )
    return {**state, "audit_logged": True}
