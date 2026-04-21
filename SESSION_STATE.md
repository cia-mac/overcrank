---
workflow_step: rows_amber_fps_first_shipped_awaiting_review
agent_type: execute
token_budget: deep
last_updated: 2026-04-20
---

## Current Objective
Three design directions landed on headroom-view branch and pushed (1b5ba7f): listing rows replace card tiles, palette swapped to tungsten amber, FPS-first input order with split SPEED/RESOLUTION preset rows. Awaiting Ciamac A/B against main before promoting.

## Last Completed Action
Shipped 1b5ba7f. Three changes folded into one commit:
1. Listing rows: each row ~94 px tall (was ~400 px), 4x density. 8-col grid (thumb | HR | identity | match | sensor | bit | tier | compare). Responsive stack under 1100 px.
2. Amber palette: --accent #e8ff00 → #d9883b. All 7 hardcoded rgba(232,255,0,*) refs swept to rgba(217,136,59,*). Monochromatic headroom: amber / white / muted-gray replacing green / yellow / orange.
3. FPS-first: form reads FPS @ W × H. New SPEED preset row (60/120/240/480/1,000/5,000/10,000/100,000+) above RESOLUTION row. Preset chips auto-activate from URL hash via new syncPresetButtons().

Also moved mock_row_v1/v2/v3.html to archive/mocks/ so the repo root stays clean.

## Open Blockers
- Ciamac A/B: main (cards, neon yellow, res-first) vs headroom-view (rows, amber, fps-first). Decide merge or iterate.
- Dead CSS cleanup pending: card-header, card-identity, card-brand, card-model, card-meta, meta-item, headroom-hero, modes-chips, mode-chip, chip-*, card-modes-label, more-modes. All unused by new row render but still in the file. Non-blocking; do in a cleanup commit before merge.
- Camera thumbnail images still missing. Current SVG silhouette is a placeholder. Real images would 10x recognition. Parked sub-project.
- Domain + analytics picks — unchanged from prior session.

## Next Actions
1. Ciamac compares branches. If approved: `git checkout main && git merge --no-ff headroom-view && git push`. GH Pages updates automatically.
2. Follow-up commit: strip dead card CSS.
3. Follow-up branch: source thumbnail images for top 20 brand/cam combos.
4. Price filter (still deferred — price_tier is string not sortable number).
5. Domain + analytics picks (user said no rush).

## Decisions Made
- Neon yellow (#e8ff00) reads "tech startup," not "cinema tool." Replaced with tungsten amber (#d9883b) as the single brand accent.
- Headroom tiers go monochromatic. Only the good tier uses the accent amber. Ok = neutral white. Tight = muted gray with 0.78 opacity so the barely-passing cameras visually recede. Color is reserved for signal, not decoration.
- FPS is this tool's primary constraint, not resolution. Input order flipped. Two preset rows created with SPEED above RESOLUTION.
- Cards out, rows in. 94 px row height vs 400 px card height delivers 4x density. Comparison across rows is native.
- Thumbnail slot gets a generic SVG silhouette + brand monogram (first 4 chars uppercase) as placeholder. One silhouette used for all brands, one stroke color. Brand tints from v2 mock explicitly rejected ("colors are disgusting").
- Preset chips now auto-sync with inputs on URL hydrate. Previously they only activated on click.
- Detail modal left intact. Click-to-open-modal behavior preserved from card era. Inline row expand (as shown in v3 mock) deferred — bigger change, can follow if wanted.
- Dead card CSS retained in file. Safer than stripping in the same commit that's already large. Cleanup commit to follow.

## Active Branch
headroom-view at 1b5ba7f. Pushed. Main is still at aa0a775 (housekeeping only).

## Uncommitted Changes
None other than this SESSION_STATE update.

## Fragile Areas
- Responsive breakpoint at 1100 px. Viewports in the 1100-1400 px range may feel cramped with 8 cols. Test on a 13" MBP in Safari before merging.
- The `.camera-card` class name is now misleading (they're rows, not cards). Left as-is to avoid cascading renames through query selectors, event handlers, CSS, and serializer code. Rename in a dedicated commit.
- Dead CSS can interfere if a future commit adds new rules matching the same selectors. Flag in the cleanup commit.
- Thumbnail SVG uses stroke="#777" — hardcoded color. If --text-muted changes, the silhouette won't follow. Minor.
- The `.row-cat.cinema` still uses the violet tint (#c4b5fd). That's a second accent color. Arguably still "multiple colors" per the brand-tint rejection. Decision pending — could neutralize to match high-speed chip.
- bestMode can be undefined if a camera has zero modes. reduce() seeds with pool[0], so if pool is empty (shouldn't happen in v9 but could in Cinema-only entries without modes) it throws. Guarded elsewhere but audit if Cinema data grows.

## Context for Next Session
Live URL (main, old cards + yellow): https://cia-mac.github.io/overcrank/
Branch (rows + amber + fps-first): http://localhost:4200/ via preview server "overcrank" (port 4200)
Last SHA on branch: 1b5ba7f

Commits this session:
  1. aa0a775 Housekeeping (already on main)
  2. 927214c Headroom view
  3. 7e7ad95 State v8
  4. 1b5ba7f Listing rows + amber + fps-first

To merge headroom-view to main:
  git checkout main && git merge --no-ff headroom-view && git push origin main

To discard:
  git branch -D headroom-view && git push origin --delete headroom-view

Test query URL: http://localhost:4200/#w=1920&h=1080&fps=1000&cat=high_speed
At that query: 69 cams, 31 hr-good / 24 hr-ok / 14 hr-tight. Top card Phoenix HD at 20x.

Follow-up ideas captured:
- Strip dead card CSS in a cleanup commit
- Source thumbnail images (brand-by-brand, press kits + manufacturer sites)
- Inline row expand to replace detail modal (v3 mock showed it working)
- Price filter once price_tier is normalized to a sortable field
- Compare button polish — still 30 px circle at right edge; "Compare" pill label could help discoverability but not urgent since compare bar auto-appears on first click
