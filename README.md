# REST to SQLite Data Pipeline

Extract sample product records, normalize text and numeric fields, reject malformed rows, and upsert into SQLite.

## Run locally
```bash
python pipeline.py
# Optional public API: python pipeline.py --live
pip install -r requirements.txt
python -m pytest -q
```
Offline fixture is synthetic. Live mode retrieves sample records from DummyJSON and is not verified in this publishing session. Duplicate IDs use last-record-wins semantics. This is an independent AI-assisted demonstration, not a production system or employer deliverable.
