# Overcrank: Gemini Batch vs Verified Data — Discrepancy Report

**Report date:** 2026-04-01
**Scope:** All manufacturers in the Gemini raw batch (`data/gemini_raw/`) compared against verified JSON files (`data/verified/`) where available.

---

## Summary Table

| Manufacturer | Gemini models | Verified models | Models wrong/missing | FPS accuracy | Sensor dims | Status |
|---|---|---|---|---|---|---|
| Phantom / Vision Research | 3 (truncated) | 21 | 18 missed, 3 partial | Close for TMX | Wrong | Verified |
| Edgertronic | 4 | 5 | 1 hallucinated, 2 missed | Off 10–43% | Missing | Verified |
| Freefly Ember | 1 | 2 | 1 missed entirely | Mixed | Wrong | Verified |
| Kron Technologies | 4 | 3 | 1 duplicate, 1 wrong name | Mixed | Wrong | Verified |
| iX Cameras | 7 | 7 | 6 wrong names, 1 missed | ~3x too high | Unknown | Verified |
| Photron | 2+ (truncated) | — | Unknown | Unknown | Unknown | Needs scrape |
| Shimadzu | 5 | — | Unknown | Unknown | UNVERIFIED | Needs scrape |
| NAC | 2+ (truncated) | — | Unknown | Unknown | Unknown | Needs scrape |
| IDT | 2+ (truncated) | — | Unknown | Unknown | Unknown | Insider access |
| Weisscam | 1 | — | Unknown | Unknown | Unknown | Needs scrape |

---

## Per-Manufacturer Detail

---

### 1. Phantom / Vision Research

**Source raw:** `gemini_raw/vision_research_v1.json`
**Verified:** `verified/phantom_v1.json` (21 models)

**Model inventory:**

Gemini response was truncated after 3 models (TMX 7510, TMX 6410, TMX 5010 partial). All 21 verified models were scraped directly from phantomhighspeed.com. The original Gemini all-in-one pass (`gemini_raw_all_v1.json`) had only a single Phantom model ("V2640") which is not in the current product lineup and was likely discontinued or never correctly identified.

Series completely missed by Gemini: T-Series (5 models), KT-Series (6 models), VEO Series (5 models), C-Series (2 models).

**Sensor dimensions:**

Gemini reported `27.6 x 21.7 mm` for TMX series. Verified: `23.68 x 14.8 mm`. The Gemini dimensions are wrong on both axes (width ~17% too large, height ~47% too large). This produces a wrong crop factor.

**FPS accuracy (TMX — the 3 models Gemini had):**

| Model | Mode | Gemini fps | Verified fps | Delta |
|---|---|---|---|---|
| TMX 7510 | 1280x800 | 75,000 | 76,000 | -1.3% |
| TMX 7510 | 1280x32 | 1,750,000 | 1,750,000 | 0% |
| TMX 6410 | 1280x800 | 64,000 | 65,940 | -3% |
| TMX 6410 | 1280x32 | 1,500,000 | 1,516,000 | -1% |
| TMX 5010 | 1280x800 | 50,000 | (truncated in raw) | — |

FPS numbers for the TMX series were surprisingly close, suggesting Gemini had correct data for these three from some source. The intermediate resolutions were not provided.

Gemini listed a `1920x1080` mode for TMX 7510 marked UNVERIFIED — this mode does not exist. The TMX sensor is 1280x800 and does not support 1080p.

**Key gap:** Gemini had no data at all for the cinema-relevant T4040 (2560x1664@840fps), C980J (3840x2160@1180fps), or any VEO model.

---

### 2. Edgertronic

**Source raw:** `gemini_raw/edgertronic_v1.json`
**Verified:** `verified/edgertronic_v1.json` (5 models)

**Model inventory:**

| Gemini model | Status |
|---|---|
| SC1 | Real, but wrong specs |
| SC2+ | Real, but wrong sensor/specs |
| SC2X | Real, but wrong fps |
| SC2X+ | **Does not exist — hallucinated** |
| SC1+ | **Missed entirely** |
| SC1X | **Missed entirely** |

**Sensor dimensions:** All marked UNVERIFIED in Gemini output. Verified data has accurate dimensions for all 5 models.

**FPS accuracy:**

| Model | Mode | Gemini fps | Verified fps | Delta |
|---|---|---|---|---|
| SC1 | 1280x1024 | 700 | 494 (std) / 621 (OC) | +42% vs std |
| SC1 | 1280x720 | 1,000 | 701 | +43% |
| SC1 | 640x480 | 2,000 | 1,849 | +8% |
| SC1 | 320x240 | 5,000 | 5,712 | -12% |
| SC1 | 192x**128** | 10,000 | 192x**96**@17,791 | wrong res, -44% fps |
| SC2+ | 1920x1080 | 500 | **no such mode** | n/a — wrong sensor |
| SC2+ | 1280x720 | 1,000 | 4,456 | -78% |
| SC2X | 1920x1080 | 1,000 | 1,910 | -48% |
| SC2X | 320x240 | 10,000 | 9,024 | +11% |
| SC2X | 192x**128** | 20,000 | 1920x**96**@20,132 | wrong res, -0.7% fps |

The SC2+ is a 1280x864 native sensor — Gemini assigned it 1920x1080 modes, which is incorrect. These fps values match no real mode on the SC2+.

The SC1 fps values appear inflated across the board at standard resolutions. They are closer to the overclock values but not matching those either.

Gemini's SC2X+ is a fabrication with fps values between the SC2X and SC2+, suggesting Gemini extrapolated a model that doesn't exist.

---

### 3. Freefly Ember

**Source raw:** `gemini_raw/freefly_v1.json`
**Verified:** `verified/freefly_ember_v1.json` (2 models, 35 modes total)

**Model inventory:**

Gemini had one model (S5K, 4 modes). Verified has two models: S5K (25 modes) and S2.5K (10 modes). The S2.5K was entirely absent.

**Sensor dimensions:**

Gemini reported `25.6 x 13.5 mm`. Verified: `23.04 x 18.43 mm`. Width is 11% too large; height is 27% too small. The aspect ratio is completely wrong (Gemini implies a wide landscape sensor; actual sensor is nearly square at 5:4).

**FPS accuracy (S5K modes Gemini had):**

| Gemini mode | Gemini fps | Verified mode | Verified fps | Notes |
|---|---|---|---|---|
| 5120x2048 | 600 | 5120x2048 | 858 | Same res, fps -30% |
| 4096x2160 | 800 | 4096x2160 | 809 | Near-exact (+1%) |
| 3072x1620 | 1,000 | no match | — | 1620h doesn't exist; 3072x1728@1011fps is nearest |
| 2048x1080 | 1,500 | 2048x1080 | 1,569 | Close (-4.4%) |

Gemini had 4 modes; the verified table has 25 (and 2 of the 4 Gemini modes have errors). The S5K supports resolutions up to 5120x4096 and the full table spans 5:4, 4:3, 1:1, 16:9, 2:1, and ~2.37:1 aspect ratios — none of this is reflected in the Gemini data.

---

### 4. Kron Technologies (Chronos)

**Source raw:** `gemini_raw/kron_v1.json`
**Verified:** `verified/kron_chronos_v1.json` (3 models)

**Model inventory:**

| Gemini model | Status |
|---|---|
| Chronos 1.4 | Real, partial modes, wrong sensor |
| Chronos 2.1 | **Likely duplicate of 2.1-HD** |
| Chronos 2.1-HD | Real, partial modes, wrong sensor |
| Chronos 4K10 | **Wrong name — actual model is 4K12** |

The "Chronos 2.1" and "Chronos 2.1-HD" entries have identical specs in the Gemini data. These are the same camera. Gemini may have found both the product name and a colloquial abbreviation and treated them as separate models.

The model is "Chronos 4K12" — the "12" refers to 12fps at native 4K resolution. Gemini called it "4K10" and assigned 1000fps at 4096x2160, which is wrong by two orders of magnitude (actual: 12fps at 4096x3072).

**Sensor dimensions:**

| Model | Gemini | Verified | Notes |
|---|---|---|---|
| Chronos 1.4 | 6.4×5.12mm | 8.45×6.76mm | Both dims ~24% too small |
| Chronos 2.1-HD | 8.45×4.75mm | 19.2×10.8mm | Wildly wrong — correct 1.4 width used, 2.1 height wrong |
| Chronos 4K12 | 18.8×9.9mm | (verified) | Not checked against verified data yet |

The 2.1-HD sensor dimensions appear to use the Chronos 1.4's width (8.45mm), suggesting a copy-paste error in Gemini's output.

**FPS accuracy:**

| Model | Mode | Gemini fps | Verified fps | Delta |
|---|---|---|---|---|
| 1.4 | 1280x1024 | 1,000 | 1,069 | -6.5% |
| 1.4 | 1280x720 | 1,580 | 1,519 | +4% |
| 1.4 | 640x480 | 3,390 | 4,434 | -24% |
| 1.4 | 320x240 | 12,500 | 16,682 | -25% |
| 2.1-HD | 1920x1080 | 1,000 | 1,000 | exact |
| 2.1-HD | 1280x720 | 2,160 | 1,495 | +44% |
| 2.1-HD | 640x480 | 5,000 | (not captured below 800x480) | — |
| 4K12 | 4096x2160 | 1,000 | **12** | off by 83x |

The 4K12 fps error is severe. The camera is designed for high-resolution science work at modest frame rates (12fps at 4K), not high fps. Gemini appears to have extrapolated based on the "4K" branding rather than reading the actual spec.

Gemini provided only 5 modes per camera. Verified has 22 modes for the 1.4 and 23 for the 2.1-HD (the lower resolutions being the most interesting for high-speed work).

---

### 5. iX Cameras

**Source raw:** `gemini_raw/ix_cameras_v1.json`
**Verified:** `verified/ix_cameras_v1.json` (7 models)

**Model inventory:**

| Gemini model | Status |
|---|---|
| i-SPEED 716 | **Does not exist** |
| i-SPEED 720 | **Does not exist** |
| i-SPEED 721 | Real model name |
| i-SPEED 722 | **Does not exist** |
| i-SPEED 507 | **Does not exist** |
| i-SPEED 510 | **Does not exist** |
| i-SPEED 513 | **Does not exist** |

Verified current lineup: i-SPEED 717, 721, 727 (7-Series); i-SPEED 509, 511, 514 (5-Series); i-SPEED 203 (2-Series).

Only "i-SPEED 721" is a real model name. All other Gemini model names are fabricated. The pattern (7xx, 5xx with sequential numbering) suggests Gemini invented a regular numbering scheme based on partial information, likely confusing the discontinued i-SPEED 3 series or IDT model naming conventions.

The i-SPEED 203 (2-Series, $quote, 1280x864 sensor) was missed entirely.

**Native resolution:** Gemini said 2048x1536. Verified: 2072x1536. The width is off by 24 pixels.

**Sensor dimensions:** Gemini stated "20.48x15.36mm" for all models. This is not published on the iX Cameras website and could not be verified. The sensor dimensions for i-SPEED 5 and 7 series are only in PDF datasheets. The i-SPEED 203 is the only model with a published pixel size (13.7µm), giving 17.54x11.83mm — notably different from Gemini's figure.

**Bit depth:** Gemini stated "12-bit" for all models. Not published on website. Cannot be verified without PDF datasheets.

**FPS accuracy:**

Gemini fps values are approximately 3x higher than verified values for the 7-Series:

| Model | Mode | Gemini fps | Verified fps | Ratio |
|---|---|---|---|---|
| i-SPEED 716 (closest: 717) | full res | 16,000 | 5,315 | 3.0x too high |
| i-SPEED 721 | 1920x1080 | 26,000 | 9,944 | 2.6x too high |
| i-SPEED 721 | full res | 21,000 | 6,642 | 3.2x too high |
| i-SPEED 722 (closest: 727) | full res | 22,000 | 8,512 | 2.6x too high |

These fps values are consistent with the discontinued i-SPEED 3 series (which topped ~150,000fps at reduced res) or possibly with the IDT OS-series naming confusion. The Gemini data is not usable for the iX lineup.

---

### 6. Photron

**Source raw:** `gemini_raw/photron_v1.json` (truncated after 2 models)
**Verified:** None yet

Gemini showed FASTCAM Nova S16 and S12 with sensor size 20.48×20.48mm and 12-bit depth. The response was cut off mid-JSON. The real Photron lineup is substantially larger (Nova series plus SA, Mini, and other lines). This data cannot be used until re-queried and verified.

**Priority:** Medium. Photron cameras are widely used in scientific and ballistics work but less common in cinema contexts.

---

### 7. Shimadzu

**Source raw:** `gemini_raw/shimadzu_v1.json`
**Verified:** None yet

Shimadzu HyperVision cameras are an unusual category: burst-mode imagers that capture a fixed number of frames at ultra-high speeds (up to 20,000,000 fps). They are not continuous-recording cameras in the conventional sense.

Models: HPV-1 (discontinued), HPV-2 (discontinued), HPV-X (unclear), HPV-X2, HPV-X3. All sensor sizes marked UNVERIFIED. Resolutions are small (312x260 to 628x480).

**Priority:** Low for cinematography applications. These are scientific instruments, not usable for the kind of high-speed video work Overcrank targets.

---

### 8. NAC Image Technology

**Source raw:** `gemini_raw/nac_v1.json` (truncated after 2 models)
**Verified:** None yet

MEMRECAM ACS-1 (2048x2048@10,000fps) and HX-7s (truncated). All data unverified. Response was cut off. NAC is a Japanese manufacturer with a substantial lineup. Needs full re-query.

**Priority:** Medium.

---

### 9. IDT (Integrated Design Tools)

**Source raw:** `gemini_raw/idt_v1.json` (truncated after 2 models)
**Verified:** None yet

Gemini showed OS8 (2048x1536@10,000fps) and OS7 (2048x1536@7,000fps). Response was cut off. Sensor size "20.48x15.36mm" is identical to the iX Cameras raw data — Gemini may have conflated these two brands (both UK-based, similar sensor formats).

IDT product family: Galileo, Phoenix, XSM, CCM (CrashCam Mini), Stereo Galileo. The OS nomenclature does not match IDT's current naming. Gemini likely pulled legacy data.

**Special note:** Ciamac has insider access to IDT specs as their Creative Director. Verify directly rather than scraping.

---

### 10. Weisscam

**Source raw:** `gemini_raw/weisscam_v1.json`
**Verified:** None yet

Single model: HS-2 MKII. Sensor 23.76x13.37mm, 12-bit. Key modes: 2048x1152@1500fps, 2048x1080@2000fps, 1920x1080@2000fps. Gemini shows only 3 modes.

Weisscam is a German cinema camera manufacturer — the HS-2 is their high-speed offering. Small model count, niche market.

**Priority:** Low. Small lineup, low query volume likely.

---

## Cross-Cutting Findings

### Sensor dimensions

Gemini's sensor dimension data was wrong or unverified for every manufacturer it attempted to quantify. The errors range from ~10% (Freefly width) to ~47% (Freefly height) to completely fabricated (Edgertronic — all UNVERIFIED). Sensor dimensions must always come from datasheets or verified product pages, never from Gemini's training data.

### FPS accuracy pattern

Two patterns emerge:

1. Close but consistently low: Gemini had roughly correct fps for well-documented models like Phantom TMX, Chronos 1.4 at standard res, Freefly S5K at common modes. Errors are typically -5 to -15%.

2. Wrong by 2-4x: For brands with less web documentation (iX Cameras) or for reduced-resolution modes where Gemini had to extrapolate (Chronos lower modes, Edgertronic reduced modes), errors reach 2-4x.

### Truncation problem

Four of ten manufacturer raw files were truncated (Photron, Shimadzu partial, NAC, IDT). These are unusable in current form. A re-query with a narrower prompt targeting one manufacturer at a time should resolve this.

### Hallucinated models

Confirmed hallucinations:
- Edgertronic SC2X+ (fully fabricated model with plausible-looking specs)
- Phantom V2640 (appears in `gemini_raw_all_v1.json`, not in current lineup)

Probable hallucinations (wrong names, adjacent to real models):
- iX Cameras: i-SPEED 716, 720, 722, 507, 510, 513 — all six model names fabricated

### What Gemini got right

- Bit depth for Chronos (12-bit), Phantom TMX (12-bit), Freefly (10-bit) — matches verified
- Price tier category (Purchase vs Rental) — all correct directionally
- Availability status — mostly correct where not truncated
- Top-of-line fps for flagship modes on documented models — within 5% for Phantom TMX
- The overall structure of the market (which brands exist, which series exist) — mostly correct despite model-level errors

---

## Action Items

| Item | Priority | Notes |
|---|---|---|
| Re-query Photron (full lineup) | High | Truncated; Nova series alone has 6+ models |
| Re-query NAC (full lineup) | High | Truncated |
| Verify IDT directly | High | Insider access available; Gemini data unusable |
| Re-query iX Cameras for PDF datasheet sensor data | Medium | Website doesn't publish pixel pitch for 5/7 series |
| Pull Chronos 2.1-HD lower-resolution modes from PDF | Medium | PDF: `https://www.krontech.ca/wp-content/uploads/2023/02/Frame-Rates-Chronos-2.1.pdf` |
| Verify Phantom VEO 1310 sensor dimensions | Low | Truncated before sensor specs on product page |
| Verify Phantom C-Series sensor dimensions and bit depth | Low | Not stated on product pages |
| Verify Weisscam HS-2 MKII | Low | Single model; small market |
| Decide on Shimadzu inclusion | Low | Burst-mode cameras may be out of scope for cinematography tool |

---

## Data Confidence Summary

| File | Confidence | Modes complete? |
|---|---|---|
| `verified/phantom_v1.json` | High | Partial (common presets only; full calculator table not scraped) |
| `verified/edgertronic_v1.json` | High | Complete (all published modes) |
| `verified/freefly_ember_v1.json` | High | Complete (25+10 modes; 3 null-width entries flagged) |
| `verified/kron_chronos_v1.json` | High (1.4), Medium (2.1-HD), High (4K12) | 1.4 complete; 2.1-HD missing lower modes |
| `verified/ix_cameras_v1.json` | Medium | Only 2 fps points per model (full tables in PDFs only) |
| `gemini_raw/photron_v1.json` | Do not use | Truncated |
| `gemini_raw/shimadzu_v1.json` | Do not use | Wrong model statuses; wrong category |
| `gemini_raw/nac_v1.json` | Do not use | Truncated |
| `gemini_raw/idt_v1.json` | Do not use | Truncated; wrong naming scheme |
| `gemini_raw/weisscam_v1.json` | Low — unverified | Only 3 modes; no verification |
