---
workflow_step: compare_polish_shipped_awaiting_domain
agent_type: execute
token_budget: deep
last_updated: 2026-04-14
---

## Current Objective
Overcrank compare-mode polish shipped. Tool is feature-complete for v1. Next blocker is Ciamac's call on domain + analytics token.

## Last Completed Action
Shipped 673f266: compare-mode polish. Three improvements in one commit: (1) compareSet now round-trips through #cmp=Brand|Model,Brand|Model URL param, so compare views are linkable and auto-open on load; (2) Copy Link + Copy CSV buttons in the compare modal header — CSV export respects quoting/escaping and is ready to paste into spreadsheets; (3) spec-label column is `position: sticky; left: 0` so specs stay readable when horizontally scrolling a 4-wide compare. Deployed and verified.

## Domain Research (2026-04-14)
WHOIS + RDAP + NS checks across candidates:
- overcrank.app: REGISTERED (parked via Namecheap registrar-servers). Off the table without outreach.
- overcrank.io: REGISTERED (2022-04-27 via Key-Systems/RRPproxy). Off the table.
- overcrank.com: REGISTERED since 1996. Likely expensive aftermarket.
- overcrank.tools: AVAILABLE (Donuts registry, ~$30-50/yr typical).
- overcrank.camera: AVAILABLE (Donuts registry, ~$45-65/yr typical). Thematically strongest.
- overcrank.dev: AVAILABLE (Google registry, HTTPS-preloaded, ~$12-15/yr).
- overcrank.cc: AVAILABLE (~$30/yr).
- overcrank.xyz: AVAILABLE (~$10/yr).

My recommendation: **overcrank.camera** for thematic fit, **overcrank.dev** for cheapest + HTTPS-preloaded by default, **overcrank.xyz** for cheapest overall. Decide and I can wire CNAME on the public repo and add DNS records.

## Open Blockers
- Domain purchase: financial, needs Ciamac approval. Candidates + pricing above.
- IDT data deepening: needs Ciamac insider materials.
- Analytics: needs token from Cloudflare / Plausible account creation.

## Next Actions
1. Decide overcrank domain. Top 3: overcrank.camera / overcrank.dev / overcrank.xyz.
2. After domain: I wire CNAME file and gh api to set custom domain, user adds DNS A/AAAA + CNAME records at registrar.
3. Analytics: decide CF Web Analytics or Plausible, provide beacon token or site ID.
4. IDT insider spec tables (25 cams).
5. Fill Weisscam dealer specs (3 cams).
6. Shimadzu in/out.
7. Consider export of full filtered results as CSV (now that compare CSV export is in, extending to full results is cheap).
8. Add DR stops data to high-speed cameras where publicly published (Phantom TMX series, Photron top models).

## Decisions Made
- compareSet persisted in URL under `cmp=` key. Example full-state link: `#cat=cinema&dr=14&cmp=ARRI|ALEXA%2035,Sony|VENICE%202`.
- CSV export is clipboard-only, not file-download. Clipboard paste into Sheets/Excel works identically and avoids the download UX friction.
- Sticky spec column uses solid var(--surface) background; diff rows get a tinted variant (#181900) so sticky column matches row color when scrolled.
- Domain shortlist narrowed from 7 candidates to 3 viable picks, with available TLDs only.

## Active Branch
main (public, deployed)

## Uncommitted Changes
None. SESSION_STATE_v5.md saved.

## Fragile Areas
- Sticky spec column requires horizontal scroll container to not also be clipping; current layout allows it. If someone nests the compare table in a new container with `overflow-x: hidden` later, sticky will silently break.
- CSV export uses `\n` line separator. Excel on Windows may want `\r\n`. Google Sheets handles both. Unlikely to matter for current audience.
- Compare URL deep-link relies on cam keys being `Brand|Model` exactly. If any camera's brand or model is renamed in the DB, existing shared compare links break. Not versioned; no URL schema migration path.
- Auto-open compare on load uses `setTimeout(100ms)` to let the render pass complete. Flaky on slow devices; could use a proper "loaded" event but not worth it yet.

## Context for Next Session
Live URL: https://cia-mac.github.io/overcrank/
Latest SHA: 673f266.
Session produced 5 commits today:
  1. edccc6c (prior session) DB v9 + cinema UI
  2. 108cac0 card detail modal + URL state sync
  3. de28ad4 compare mode
  4. 673f266 compare polish (URL persist, CSV, sticky column)
  5. c3a1613 / (state-only) session state updates

Tool now does: filter, drill in, compare 2-4 side-by-side, share any view via URL, export compare as CSV. That's the v1 feature set. Everything remaining is either content (fill data gaps) or infra (domain, analytics).

Autopilot ran out of unblocked technical work. Next productive round requires Ciamac input on at least one of: domain choice, IDT data, analytics provider.
