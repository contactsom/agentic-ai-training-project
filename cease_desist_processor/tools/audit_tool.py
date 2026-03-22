import logging
import os
from cease_desist_processor.config import AUDIT_LOG

os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(AUDIT_LOG),
        logging.StreamHandler(),
    ],
)
audit_logger = logging.getLogger("audit")


def log_audit(doc_name: str, classification: str, reason: str, action: str, extra: str = "") -> str:
    msg = f"DOC={doc_name} | CLASS={classification} | ACTION={action} | REASON={reason}"
    if extra:
        msg += f" | {extra}"
    audit_logger.info(msg)
    return f"Audit logged for '{doc_name}'."
