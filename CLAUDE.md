# Overcrank — CLAUDE.md

## Project
Cross-brand high-speed camera search tool. Input resolution + FPS, get every camera that can execute that shot. Static site, client-side filtering, JSON database.

## Stack
- Single `index.html` (vanilla JS, no framework)
- `data/overcrank_db_v4.json` loaded at runtime
- Served on port 4200 via `python3 -m http.server 4200`
- No backend, no build step

## Data Model
Each camera entry: brand, model, series, sensor_size, crop_factor, bit_depth, price_tier, price_usd, status, data_quality (verified | gemini_unverified), source_url, modes[].
Each mode: res_width, res_height, max_fps, mode_type, note.

## Data Pipeline
- Verified data lives in `data/verified/` (one JSON per manufacturer)
- Gemini-sourced raw data in `data/gemini_raw/`
- Merged database built from verified sources into `data/overcrank_db_vN.json`
- `scripts/verify.py` scrapes source URLs with Playwright and diffs against DB

## Guardrails
- Do not modify JSON data files without explicit instruction.
- Always version the database: v1, v2, v3, etc. Never overwrite.
- When adding cameras, create or update the verified JSON in `data/verified/`, then rebuild the merged DB as a new version.
- IDT specs: Ciamac has insider access. Verify directly, do not trust Gemini output for IDT.

## Phase 1 Target
10 manufacturers: Phantom, Photron, IDT, iX Cameras, Kron Technologies, Freefly, Edgertronic, NAC, Weisscam, Shimadzu (TBD).
Currently have 7 of 10. Missing: NAC, Weisscam (partial), Shimadzu (TBD).
