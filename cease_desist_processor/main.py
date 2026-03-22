import os
import glob
from datetime import date

from cease_desist_processor.config import PDF_DIR, OUTPUT_DIR
from cease_desist_processor.graph import build_graph

os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_all_pdfs():
    graph = build_graph()
    pdf_files = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))

    if not pdf_files:
        print(f"No PDF files found in {PDF_DIR}")
        return

    print(f"\nFound {len(pdf_files)} PDF(s) to process.\n")

    results = {"cease": [], "irrelevant": [], "uncertain": [], "error": []}

    for pdf_path in pdf_files:
        doc_name = os.path.basename(pdf_path)
        print(f"\n{'─' * 50}")
        print(f"Processing: {doc_name}")

        initial_state: dict = {
            "pdf_path": pdf_path,
            "doc_name": doc_name,
            "received_date": date.today().isoformat(),
            "raw_text": "",
            "extracted_details": "",
            "classification": "",
            "classification_reason": "",
            "hitl_decision": None,
            "db_stored": False,
            "archived": False,
            "audit_logged": False,
            "error": None,
        }

        try:
            final_state = graph.invoke(initial_state)
            classification = final_state.get("hitl_decision") or final_state.get("classification", "error")
            results[classification].append(doc_name)
            print(f"✅ Done — {doc_name} → {classification.upper()}")
        except Exception as e:
            results["error"].append(doc_name)
            print(f"❌ Error processing {doc_name}: {e}")

    print(f"\n{'=' * 50}")
    print("PROCESSING SUMMARY")
    print(f"{'=' * 50}")
    print(f"  Cease      : {len(results['cease'])}  → {results['cease']}")
    print(f"  Irrelevant : {len(results['irrelevant'])}  → {results['irrelevant']}")
    print(f"  Uncertain  : {len(results['uncertain'])}  → {results['uncertain']}")
    print(f"  Errors     : {len(results['error'])}  → {results['error']}")
    print(f"\nOutputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    process_all_pdfs()
