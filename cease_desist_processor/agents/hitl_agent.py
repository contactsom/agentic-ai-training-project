from cease_desist_processor.state import DocumentState


def hitl_agent(state: DocumentState) -> DocumentState:
    """Presents uncertain documents to a human for review."""
    print("\n" + "=" * 60)
    print("🔍 HUMAN REVIEW REQUIRED")
    print("=" * 60)
    print(f"Document : {state['doc_name']}")
    print(f"Received : {state['received_date']}")
    print(f"Reason   : {state.get('classification_reason', 'N/A')}")
    print(f"Details  : {state.get('extracted_details', 'N/A')}")
    print("\nDocument excerpt:")
    print(state.get("raw_text", "")[:500])
    print("=" * 60)

    while True:
        decision = input("\nClassify as [c]ease / [i]rrelevant / [s]kip: ").strip().lower()
        if decision in ("c", "cease"):
            return {**state, "hitl_decision": "cease"}
        elif decision in ("i", "irrelevant"):
            return {**state, "hitl_decision": "irrelevant"}
        elif decision in ("s", "skip"):
            return {**state, "hitl_decision": None}
        print("Invalid input. Enter c, i, or s.")
