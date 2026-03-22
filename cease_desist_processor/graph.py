from langgraph.graph import StateGraph, END

from cease_desist_processor.state import DocumentState
from cease_desist_processor.agents.loader_agent import document_loader_agent
from cease_desist_processor.agents.classification_agent import classification_agent
from cease_desist_processor.agents.database_agent import database_agent
from cease_desist_processor.agents.archiving_agent import archiving_agent
from cease_desist_processor.agents.hitl_agent import hitl_agent
from cease_desist_processor.agents.audit_agent import audit_agent


def route_classification(state: DocumentState) -> str:
    """Routes to the correct agent based on classification."""
    classification = state.get("classification", "uncertain")
    if classification == "cease":
        return "database"
    elif classification == "irrelevant":
        return "archive"
    else:
        return "hitl"


def route_hitl(state: DocumentState) -> str:
    """Routes after human review decision."""
    decision = state.get("hitl_decision")
    if decision == "cease":
        return "database"
    elif decision == "irrelevant":
        return "archive"
    else:
        return "audit"  # skipped — go straight to audit


def build_graph() -> StateGraph:
    graph = StateGraph(DocumentState)

    graph.add_node("loader", document_loader_agent)
    graph.add_node("classifier", classification_agent)
    graph.add_node("database", database_agent)
    graph.add_node("archive", archiving_agent)
    graph.add_node("hitl", hitl_agent)
    graph.add_node("audit", audit_agent)

    graph.set_entry_point("loader")
    graph.add_edge("loader", "classifier")

    graph.add_conditional_edges(
        "classifier",
        route_classification,
        {"database": "database", "archive": "archive", "hitl": "hitl"},
    )

    graph.add_conditional_edges(
        "hitl",
        route_hitl,
        {"database": "database", "archive": "archive", "audit": "audit"},
    )

    graph.add_edge("database", "audit")
    graph.add_edge("archive", "audit")
    graph.add_edge("audit", END)

    return graph.compile()
