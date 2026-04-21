---
workflow_step: v1_complete_awaiting_domain_and_analytics
agent_type: execute
token_budget: deep
last_updated: 2026-04-14
---

## Current Objective
Overcrank v1 is complete. Three unblocked dev improvements just shipped (full-results CSV, keyboard nav, mobile pass). Next move requires Ciamac picks on domain + analytics. IDT work is on ice per 2026-04-14 directive.

## Last Completed Action
Shipped c3630e9: Copy MD button in compare modal. Markdown pipe-table export joins Copy Link and Copy CSV. Pipes and newlines in cell content escape correctly. Reuses compareLastSnapshot so no extra data walk. Purpose: Ciamac uses Notion as SSOT, Markdown table paste goes directly into a Notion toggle or page without import step. Prior ship same day was 1325526: full-results CSV + keyboard nav + mobile pass.

## Domain Research (2026-04-14)
WHOIS + RDAP + NS checks across candidates:
- overcrank.app: REGISTERED (parked via Namecheap). Off the table.
- overcrank.io: REGISTERED (2022 via Key-Systems). Off the table.
- overcrank.com: REGISTERED since 1996. Aftermarket.
- overcrank.tools: AVAILABLE (~$30-50/yr).
- overcrank.camera: AVAILABLE (~$45-65/yr). Thematically strongest.
- overcrank.dev: AVAILABLE (~$12-15/yr, HTTPS-preloaded). Cheapest real domain.
- overcrank.cc: AVAILABLE (~$30/yr).
- overcrank.xyz: AVAILABLE (~$10/yr).

Current recommendation: **overcrank.dev**. $12/yr, HTTPS-preloaded by registry, appropriate for a dev tool. Once purchased I wire CNAME and you add DNS records.

## Open Blockers
- Domain purchase: Ciamac decision (top pick: .dev).
- Analytics: Ciamac decision on Cloudflare Web Analytics (free, recommended) vs Plausible ($9/mo).
- IDT data: ON ICE. Do not propose until Ciamac lifts freeze.

## Next Actions
1. Ciamac picks and buys overcrank.dev (or alternate). I wire CNAME + provide DNS records.
2. Ciamac picks analytics provider. I wire the snippet.
3. NOT IDT work.
4. Weisscam dealer specs (3 cams) — needs explicit go-ahead per CLAUDE.md JSON guardrail.
5. Shimadzu in/out decision.
6. Phantom TMX / Photron DR stops column fill — needs explicit go-ahead per CLAUDE.md JSON guardrail.

## Decisions Made
- Full-results CSV export is clipboard-only (matches compare CSV pattern).
- CSV column set optimized for spreadsheet ingest: brand+model first, modes joined on semicolons in a single "All Modes" cell, source URL last.
- Keyboard "/" focuses text search (not min-width input) to match GitHub/Twitter convention.
- Keyboard "c" opens compare only if ≥2 cams selected (no-op otherwise, no error UI).
- Arrow-key nav uses linear prev/next across the DOM order of cards, not grid-aware row jumps. Simpler and works on all viewport widths.
- Mobile (≤600px) gets a real responsive pass. Detail head + compare head both stack vertically; specs grid drops to 2 cols; compare table font shrinks to 12px.
- IDT work is on ice per 2026-04-14 user directive. Removed from Next Actions.

## Active Branch
main (public, deployed)

## Uncommitted Changes
None. SESSION_STATE_v6.md saved.

## Fragile Areas
- Export CSV assumes lastResults is populated. If "Clear" is clicked lastResults is emptied and button shows "No results" banner for 1.5s. Intentional.
- Keyboard nav "c" conflicts with "c" typed in search because inp-text is a text input, but the handler skips shortcuts when target is INPUT. Should never fire while typing. If a future text field is rendered as contenteditable, that's also covered.
- Arrow-key nav calls scrollIntoView with smooth behavior. On long result lists this feels good but is a no-op for already-visible cards (block: 'nearest'). If performance matters later, drop to 'auto'.
- Mobile pass tuned for ≤600px. 601-800px range now uses the ≤800px rules (header padding only). Tablets in portrait may look a bit sparse. Fine for now.
- Sticky spec column already fragile (requires no ancestor to clip overflow-x); mobile rules don't change that.
- IDT cameras still in DB as unverified. If someone writes new overcrank features that highlight "verified" status, IDT rows will look stale. Not urgent.

## Context for Next Session
Live URL: https://cia-mac.github.io/overcrank/
Latest SHA: c3630e9.
Session produced 4 commits beyond prior rounds:
  1. 1325526 full-results CSV + keyboard nav + mobile pass
  2. 9c98222 state v6 (IDT scrubbed)
  3. c3630e9 Copy MD (Markdown table for Notion paste)
  4. (this state file commit)

Tool now does: filter, drill in, compare 2-4 side-by-side, share any view via URL, export compare as CSV/Markdown or full results as CSV, navigate by keyboard, usable on phones.

Export pattern established: all three compare exports (Link, MD, CSV) share compareLastSnapshot + clipboard. If a fourth format is needed (JSON, TSV), follow the same pattern.

Next productive round requires at least one of:
- Domain pick (.dev recommended, 2-minute purchase).
- Analytics pick (CF Web Analytics recommended).
- Explicit "fill Weisscam/Phantom/Photron public data" go-ahead to override the JSON-data guardrail.
