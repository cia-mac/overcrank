---
workflow_step: compare_mode_shipped
agent_type: execute
token_budget: deep
last_updated: 2026-04-14
---

## Current Objective
Overcrank ships compare mode. Cross-brand side-by-side is the actual value proposition and it's now live. Next: domain + analytics + IDT insider data dump.

## Last Completed Action
Shipped de28ad4: compare mode. Each card has a + button (top-right) that adds the camera to a compare set (max 4). Floating bar shows count with Compare + Clear actions; Compare opens a side-by-side spec table (23 spec rows × up to 4 camera columns, only non-empty rows rendered, differing values subtly highlighted, per-column X to remove without closing modal). GH Pages redeployed and verified: all 6 new feature symbols present in deployed HTML.

## Open Blockers
- Custom domain purchase: financial, needs Ciamac approval.
- IDT data deepening: needs Ciamac insider materials.

## Next Actions
1. Decide overcrank domain (overcrank.app / .io / .tools).
2. IDT: Ciamac to provide insider spec sheets for 25 cams (currently 1.6 modes avg).
3. Add analytics (Plausible or Cloudflare Web Analytics).
4. Fill Weisscam dealer specs (3 cameras).
5. Shimadzu in/out decision.
6. Persist compareSet to URL hash so a compare view is shareable (not wired yet; currently compare is session-local).
7. Consider: export compare table as CSV or PNG.
8. Mobile hands-on test (compare modal horizontal scroll works but hasn't been finger-tested).

## Decisions Made
- Compare ceiling = 4 cameras. Table readability deteriorates past that and real-world comparison rarely needs more.
- Compare is a separate interaction from detail. Tap card = detail modal; tap + in top-right = compare toggle. Button stops propagation.
- Differing rows highlighted subtly (3% accent tint) rather than loud; loud would overwhelm a long spec table where most rows differ.
- Per-column X in compare header removes that camera and re-renders in place, so the user can iterate without closing/reopening.
- compareSet is NOT persisted in URL hash yet. Low-priority until someone asks to share a compare link.

## Active Branch
main (public, deployed)

## Uncommitted Changes
None. SESSION_STATE_v4.md saved as version. About to commit as part of exit.

## Fragile Areas
- Compare diff-detection uses simple string equality on rendered values. Near-equal numbers rendered identically count as "same"; off-by-one in fields like DR stops would correctly be flagged, but unit mismatches ("14.5 stops" vs "14.5") would show as diff. Acceptable.
- Compare modal max-width 1200px. At 4 cameras on a narrow viewport, horizontal scroll kicks in. Spec-label column is sticky-width 140px but doesn't pin on scroll. Cheap fix if needed: `position: sticky; left: 0` on the th.
- ESC key handler stacks: ESC closes compare first, then detail. Correct precedence.
- The `+` button uses `stopPropagation()` on click to prevent card-open. Mobile touch events are untested; if tap events bubble differently, card detail might open when user wanted to just add-to-compare.

## Context for Next Session
Live URL: https://cia-mac.github.io/overcrank/
Latest SHA: de28ad4 (feature) / about-to-commit (state).
Compare is a meaningful crossing point: tool now does the thing it's for (cross-brand side-by-side). Three shipped features stacked today:
  1. v9 cinema DB (140 high-speed + 77 cinema = 217 cams)
  2. Category filter, mount filter, min DR stops filter, codec pills
  3. Card detail modal + URL hash state + camera deep-links
  4. Compare mode (today)
Priority order for next session: domain → analytics → IDT data. Everything else is nice-to-have polish.
