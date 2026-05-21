# Handling Grok/X Data Exports

Grok full data exports are usually fragmented (hundreds of small binary and JSON files under `prod-mc-asset-server/`). They rarely contain clean, readable chat history.

## Recommended workflow
1. Ask user to provide share links or manually copied conversations instead.
2. If only the full export is available, extract and inspect a few `content` files to confirm they are mostly media/PDFs.
3. Advise user that manual copy-paste or share links are more effective for memory ingestion.
4. Process any usable text in small chunks using the memory tool.