---
workflow_step: v4_design_mature_awaiting_domain_and_analytics
agent_type: execute
token_budget: deep
last_updated: 2026-04-22
---

## Current Objective
Overcrank v4 design is mature. Multiple audit-and-redesign rounds over 2026-04-20 → 2026-04-22 have landed a coherent instrument-panel aesthetic, preset-tile hero interaction, compact query-state filter panel, and monochrome palette. Blocker remains the original Phase-1 pair: domain + analytics picks.

## Last Completed Action
Shipped 6d87ef2 on main. Tile-button presets compressed to one row each (repeat(8, 1fr)), inputs demoted to "CUSTOM" row, Search + Clear + Refine + inlined, filter panel on query state ~280 px (was 440 px), 3-4 row results visible above fold on a 1440 × 900 viewport.

Today's design-rework commits on main:
- afd2c65 Tier 1 UX polish (amber discipline, brand collapse, empty-state hook)
- 32ddf69 Tier 2 polish (thumb variants, price normalization, legend, status chip)
- 72381d6 Tier 3 (sticky summary on scroll, contrast raise, alignment)
- a59dc14 Scale everything up (text, controls, rows breathe)
- 1221775 Total design rework (instrument-panel monochrome)
- a6969bf Refine + collapse for category/brand/text
- 6c8573d Hero-size inputs 40 px (superseded by tile-preset direction)
- 2763482 Presets become the hero, pixel inputs secondary
- fd0f6fa Preset tiles with big digits + caption
- 6d87ef2 Layout economy: one row per preset group, inline actions
- 961c8ba Bug fixes (compare modal null-fps guard, status chip dash fix, etc.)
- 82465f6 Hero-first empty state, progressive disclosure

## Open Blockers
- Domain: Ciamac pick. overcrank.dev top recommendation. "No rush" per prior direction.
- Analytics: Ciamac pick. Cloudflare Web Analytics recommended.
- Shimadzu: 0/10 for Phase 1 target. Parked.
- Thumbnail images: drop decided (kept silhouettes briefly, then pulled in total-rework). Real manufacturer images still a parked sub-project if visual identity ever wants them.

## Next Actions
1. Ciamac reviews live site at https://cia-mac.github.io/overcrank/ after GH Pages redeploy.
2. Domain pick. Once bought, wire CNAME and hand DNS records.
3. Analytics pick. Wire snippet.
4. Consider: the SPEED preset tiles wrap cleanly on wide viewports but on 1024–1280 they may still wrap. Test in that range.
5. Price filter is still deferred. price_tier is categorical, not numeric; would need data-model work.
6. Weisscam dealer specs / Phantom TMX / Photron DR stops fills — still need explicit JSON guardrail approval.
7. If domain ships, consider adding Open Graph metadata (og:image, og:title) for link previews.

## Decisions Made Today
- Monochrome direction locked. No accent color. White = emphasis + active state only. Hr-good rows marked with 2 px white left-edge; hr-tight fades to 0.58 opacity. No amber anywhere.
- Tile buttons for presets. 68 px tall, primary numeric value at 22 px bold, caption at 10 px mono. Resolution tiles show both the friendly name and the pixel dimensions so users learn the domain without a reference card.
- Rectangular shapes. radius-sm/radius/radius-lg all 0. 2–4 px on interactive elements only for hairline softness. No rounded pills.
- Rows are data-table rows. Individual card borders gone; hairline 1 px horizontal rules between rows. Thumbnail column removed entirely since the single generic silhouette carried zero info.
- Primary specs (fps + resolution) are presets first, pixel inputs second. Competitors (IDS, CineD) force pixels; overcrank does not.
- Empty-state: hero + presets + custom inputs + demo chips + stats, centered. Filters (category/brand/text) hidden entirely.
- Query-state: compact header, tiles in 8-col grid, custom inputs on one row, Search + Clear + Refine + inline, drawer collapsed by default.
- Refine drawer remains — category, brand, text-search tuck behind a Refine + toggle that's inline with Search.
- Sticky summary on scroll still active (1221775 onward).

## Active Branch
main at 6d87ef2. Pushed.
headroom-view at 0e684b2 pushed. Fully merged into main, retained for history.

## Uncommitted Changes
None other than SESSION_STATE update pending.

## Fragile Areas
- Tile wrap at narrow viewports. `grid-template-columns: repeat(8, 1fr)` forces 8 columns regardless of width. Below 1180 px the tiles may get too narrow for captions like "100K+" / "4K UHD". Add a responsive breakpoint if user reports it.
- The `.camera-card` class name is still a lie (they're rows now). Rename deferred.
- Hero subtitle wraps differently on narrower screens; may look awkward 768–1024 px range.
- The sticky-summary slide-in animation was simplified to a display toggle because the transform/opacity animation wouldn't apply in testing. Aesthetic regression acceptable; function intact.
- Cinema pill violet (#c4b5fd) neutralized on rows, but the `.row-cat.cinema` CSS rule still references it — check the detail modal doesn't rely on it.

## Context for Next Session
Live URL: https://cia-mac.github.io/overcrank/
Test query: https://cia-mac.github.io/overcrank/#w=1920&h=1080&fps=1000&cat=high_speed

Design is defensible. Any further improvements are polish or feature additions:
- Real product thumbnails (parked sub-project)
- Price filter (needs data-model change)
- Mobile responsive verification
- Inline row expand to replace detail modal

Engine, data, filter logic, URL hash, compare, detail modal, export/share, keyboard nav are all untouched across today's visual reworks. v9 DB still current (217 cams, 1889 modes, 18 brands, all verified).

To ship to a real domain:
1. Buy overcrank.dev
2. Add CNAME at apex + www pointing to cia-mac.github.io
3. Update repo Pages settings with the custom domain
4. GitHub auto-provisions HTTPS via Let's Encrypt
