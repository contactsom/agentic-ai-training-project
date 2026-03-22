from typing import Optional
from typing_extensions import TypedDict


class DocumentState(TypedDict):
    # Input
    pdf_path: str
    doc_name: str
    received_date: str

    # Extracted
    raw_text: str
    extracted_details: str

    # Classification
    classification: str        # "cease" | "irrelevant" | "uncertain"
    classification_reason: str

    # HITL
    hitl_decision: Optional[str]   # "cease" | "irrelevant" | None

    # Processing status
    db_stored: bool
    archived: bool
    audit_logged: bool
    error: Optional[str]
