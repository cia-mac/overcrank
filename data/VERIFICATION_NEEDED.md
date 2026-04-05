# VERIFICATION_NEEDED.md
*Overcrank project — Gemini data collection audit*
*Generated: 2026-03-31*

---

## Session Notes

Gemini relay (gemini-2.5-flash, free tier) hit the 20 requests/day quota limit during collection.
5 of 10 manufacturers returned truncated or markdown-formatted responses that could not be parsed as JSON.
5 manufacturers returned clean, parseable JSON arrays.
The rate limit resets daily. Re-run collection tomorrow or upgrade the API key to remove the cap.

---

## Collection Status

| Manufacturer | Status | Cameras Collected | Action Needed |
|---|---|---|---|
| Vision Research (Phantom) | TRUNCATED | 0 | Re-query when quota resets + verify via Chrome tools |
| Photron | TRUNCATED | 0 | Re-query when quota resets + verify via Chrome tools |
| Kron Technologies (Chronos) | OK | 4 | Verify against manufacturer spec sheet |
| Freefly | OK | 1 | Verify against manufacturer spec sheet |
| Edgertronic | OK | 4 | Verify against manufacturer spec sheet |
| Shimadzu | TRUNCATED | 0 | Re-query when quota resets + verify via Chrome tools |
| NAC Image Technology | TRUNCATED | 0 | Re-query when quota resets + verify via Chrome tools |
| Weisscam | OK | 1 | Verify against manufacturer spec sheet |
| IDT Integrated Design Tools | TRUNCATED | 0 | Re-query when quota resets + verify via Chrome tools |
| iX Cameras | OK | 7 | Verify against manufacturer spec sheet |

---

## UNVERIFIED Fields by Manufacturer

### Vision Research (Phantom)
No parseable data collected. Full re-query needed.

### Photron
No parseable data collected. Full re-query needed.

### Kron Technologies (Chronos)
No UNVERIFIED fields found in collected data.

### Freefly
**Ember S5K:**
  - `resolution_fps_modes[0].crop_factor`
  - `resolution_fps_modes[0].note`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[1].note`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[2].note`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[3].note`

### Edgertronic
**Edgertronic SC1:**
  - `sensor_size_mm`
  - `bit_depth`
  - `resolution_fps_modes[0].crop_factor`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**Edgertronic SC2+:**
  - `sensor_size_mm`
  - `bit_depth`
  - `resolution_fps_modes[0].crop_factor`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
  - `resolution_fps_modes[5].crop_factor`
**Edgertronic SC2X:**
  - `sensor_size_mm`
  - `bit_depth`
  - `resolution_fps_modes[0].crop_factor`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
  - `resolution_fps_modes[5].crop_factor`
**Edgertronic SC2X+:**
  - `sensor_size_mm`
  - `bit_depth`
  - `resolution_fps_modes[0].crop_factor`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
  - `resolution_fps_modes[5].crop_factor`

### Shimadzu
No parseable data collected. Full re-query needed.

### NAC Image Technology
No parseable data collected. Full re-query needed.

### Weisscam
**HS-2 MKII:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`

### IDT Integrated Design Tools
No parseable data collected. Full re-query needed.

### iX Cameras
**i-SPEED 716:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**i-SPEED 720:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**i-SPEED 721:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**i-SPEED 722:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**i-SPEED 507:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**i-SPEED 510:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`
**i-SPEED 513:**
  - `price_tier`
  - `resolution_fps_modes[1].crop_factor`
  - `resolution_fps_modes[2].crop_factor`
  - `resolution_fps_modes[3].crop_factor`
  - `resolution_fps_modes[4].crop_factor`

---

## Incomplete Mode Tables

Cameras where the mode table is likely incomplete based on known lineup depth:

**Vision Research (Phantom):** TRUNCATED. Known lineup includes TMX 7510, TMX 5010, v2640, v2012, VEO 4K 990, VEO 640S, Flex4K, Miro series, C-series. Only partial data for 2 models captured before truncation.

**Photron:** TRUNCATED. Known lineup includes SA-Z, SA-X2, NOVA S12/S20, Mini AX200. Only partial data captured.

**Kron Technologies (Chronos):** 4 models captured (1.4, 2.1-HD, 4K12, Q12). Likely complete for current lineup.

**Freefly:** Only 1 model (Ember S5K) captured. Ember S2.5K may also exist. Mode table appears minimal — verify full resolution table.

**Edgertronic:** 4 models captured (SC1, SC2, SC2+, SC2X). Verify completeness of mode tables per model.

**Shimadzu:** TRUNCATED in markdown. Known lineup includes HPV-X2, HPV-4. No usable JSON extracted.

**NAC Image Technology:** TRUNCATED. Known lineup includes MEMRECAM HX series, GX series. Only partial data captured.

**Weisscam:** 1 model (HS-2) captured. Very limited mode table. Weisscam specs are notoriously hard to find publicly.

**IDT Integrated Design Tools:** TRUNCATED. Ciamac has direct access — verify all specs manually. Do not trust any Gemini data for IDT.

**iX Cameras:** 7 models captured. Likely most complete dataset in this collection. Verify mode tables against iX official spec sheets.

---

## Missing Price Tier

- Weisscam: HS-2 MKII
- iX Cameras: i-SPEED 716
- iX Cameras: i-SPEED 720
- iX Cameras: i-SPEED 721
- iX Cameras: i-SPEED 722
- iX Cameras: i-SPEED 507
- iX Cameras: i-SPEED 510
- iX Cameras: i-SPEED 513

---

## IDT — Verify Directly

Gemini returned truncated data for IDT. Ciamac has insider access. Do not use Gemini output for IDT.
Verify these manually:

- Full current IDT camera lineup (model names)
- Complete resolution/FPS table for each model
- Sensor size in mm for each model
- Crop factor at each resolution mode
- Current vs discontinued status
- Price tier (Purchase / Rental / Both)

---

## Next Steps

1. Wait for Gemini free tier quota reset (daily), then re-run truncated manufacturers: Phantom, Photron, Shimadzu, NAC, IDT
2. Use Claude Chrome tools to navigate manufacturer spec pages and fill gaps regardless of Gemini quota
3. Ciamac to verify all IDT specs directly
4. Cross-reference all Gemini output against source PDFs before loading into production database
5. Priority order: Phantom (most complex lineup), Photron, iX Cameras (verify), Chronos (verify), IDT (manual)