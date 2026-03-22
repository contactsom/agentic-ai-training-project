import csv
import os
from cease_desist_processor.config import ARCHIVE_FILE


def archive_irrelevant(doc_name: str, received_date: str) -> str:
    file_exists = os.path.exists(ARCHIVE_FILE)
    with open(ARCHIVE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["doc_name", "received_date", "archived_at"])
        from datetime import datetime
        writer.writerow([doc_name, received_date, datetime.now().isoformat()])
    return f"Archived irrelevant document '{doc_name}' to flat file."
