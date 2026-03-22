import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
PDF_DIR = os.getenv("PDF_DIR", "data/pdfs")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/output")

DB_PATH = os.path.join(OUTPUT_DIR, "cease_desist.db")
ARCHIVE_FILE = os.path.join(OUTPUT_DIR, "irrelevant_archive.csv")
AUDIT_LOG = os.path.join(OUTPUT_DIR, "audit.log")
