#!/usr/bin/env python3
"""
Process PDF extraction data from agents into updated verified JSON files.

Creates:
- data/verified/ix_cameras_v4.json  (full mode tables from PDF datasheets)
- data/verified/photron_v2.json     (expanded mode tables for Mini AX + MH6)
"""

import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
IX_RAW = Path("/tmp/ix_cameras_performance_tables.json")
IX_V3 = ROOT / "data" / "verified" / "ix_cameras_v3.json"
IX_V4 = ROOT / "data" / "verified" / "ix_cameras_v4.json"
PH_V1 = ROOT / "data" / "verified" / "photron_v1.json"
PH_V2 = ROOT / "data" / "verified" / "photron_v2.json"


def dedup_modes(modes):
    """Keep only the highest max_fps for each unique (res_width, res_height)."""
    best = {}
    for m in modes:
        key = (m["res_width"], m["res_height"])
        if key not in best or m["max_fps"] > best[key]["max_fps"]:
            best[key] = m
    # Sort by resolution descending (largest first), then fps ascending
    result = sorted(best.values(), key=lambda m: (-m["res_width"] * m["res_height"], m["max_fps"]))
    return result


def process_ix_cameras():
    """Read raw PDF extraction, merge with v3 metadata, deduplicate modes, write v4."""
    with open(IX_RAW) as f:
        raw = json.load(f)
    with open(IX_V3) as f:
        v3 = json.load(f)

    # Build lookup from v3 for camera metadata
    v3_lookup = {}
    for cam in v3["cameras"]:
        v3_lookup[cam["model"]] = cam

    cameras = []
    model_keys = ["i-SPEED 727", "i-SPEED 721", "i-SPEED 717",
                   "i-SPEED 514", "i-SPEED 511", "i-SPEED 509",
                   "i-SPEED 203"]

    for model_key in model_keys:
        raw_cam = raw[model_key]
        v3_cam = v3_lookup.get(model_key, {})

        # Deduplicate modes
        modes = dedup_modes(raw_cam["modes"])

        # Clean up mode notes
        for m in modes:
            if m.get("note") in ("full resolution", "full HD", "max fps at full resolution",
                                  "max fps at full HD", "720p"):
                # Keep meaningful notes, clear generic ones
                if m["note"] in ("full resolution", "max fps at full resolution"):
                    m["note"] = f"{m['res_width']}x{m['res_height']} full sensor"
                elif m["note"] in ("full HD", "max fps at full HD"):
                    m["note"] = "Full HD"
                # 720p stays
            elif not m.get("note") or m["note"] == "":
                m["note"] = f"{m['res_width']}x{m['res_height']}"
            # Ensure standard fields
            if "mode_type" not in m:
                m["mode_type"] = "standard"

        cameras.append({
            "brand": "iX Cameras",
            "model": model_key,
            "series": v3_cam.get("series", raw_cam.get("series", "")),
            "sensor_size": v3_cam.get("sensor_size"),
            "crop_factor": v3_cam.get("crop_factor"),
            "bit_depth": raw_cam.get("bit_depth", v3_cam.get("bit_depth")),
            "pixel_size_um": raw_cam.get("pixel_size_um"),
            "native_resolution": raw_cam.get("sensor_resolution"),
            "price_tier": v3_cam.get("price_tier", "Purchase (Quote)"),
            "status": v3_cam.get("status", "Current"),
            "data_quality": "verified",
            "source_url": v3_cam.get("source_url", ""),
            "datasheet_url": v3_cam.get("datasheet_url", ""),
            "modes": modes
        })

    total_modes = sum(len(c["modes"]) for c in cameras)
    output = {
        "verified_date": "2026-04-13",
        "source_base_url": "https://www.ix-cameras.com",
        "notes": f"v4: Full resolution/FPS tables extracted from official iX Cameras PDF datasheets. {len(cameras)} cameras, {total_modes} modes (deduplicated to max fps per resolution). v3 had only 2 modes per camera.",
        "cameras": cameras
    }

    with open(IX_V4, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote ix_cameras_v4.json: {len(cameras)} cameras, {total_modes} modes")
    return cameras


def process_photron():
    """Update photron_v1 with expanded mode tables from PDF extraction. Write v2."""
    with open(PH_V1) as f:
        v1 = json.load(f)

    # Agent-extracted mode tables (from Photron Mini AX and MH6 PDF manuals)
    expanded_modes = {
        "FASTCAM Mini AX200": [
            {"res_width": 1024, "res_height": 1024, "max_fps": 6400, "mode_type": "standard", "note": "full frame"},
            {"res_width": 1024, "res_height": 960, "max_fps": 7200, "mode_type": "standard", "note": "1024x960"},
            {"res_width": 1024, "res_height": 848, "max_fps": 8100, "mode_type": "standard", "note": "1024x848"},
            {"res_width": 1024, "res_height": 752, "max_fps": 9000, "mode_type": "standard", "note": "1024x752"},
            {"res_width": 1024, "res_height": 672, "max_fps": 10000, "mode_type": "standard", "note": "1024x672"},
            {"res_width": 1024, "res_height": 512, "max_fps": 12500, "mode_type": "standard", "note": "1024x512"},
            {"res_width": 896, "res_height": 896, "max_fps": 8100, "mode_type": "standard", "note": "896x896"},
            {"res_width": 896, "res_height": 768, "max_fps": 10000, "mode_type": "standard", "note": "896x768"},
            {"res_width": 896, "res_height": 512, "max_fps": 14400, "mode_type": "standard", "note": "896x512"},
            {"res_width": 768, "res_height": 768, "max_fps": 10000, "mode_type": "standard", "note": "768x768"},
            {"res_width": 768, "res_height": 512, "max_fps": 15000, "mode_type": "standard", "note": "768x512"},
            {"res_width": 640, "res_height": 640, "max_fps": 15000, "mode_type": "standard", "note": "640x640"},
            {"res_width": 640, "res_height": 480, "max_fps": 20000, "mode_type": "standard", "note": "640x480"},
            {"res_width": 512, "res_height": 512, "max_fps": 22500, "mode_type": "standard", "note": "512x512"},
            {"res_width": 512, "res_height": 384, "max_fps": 30000, "mode_type": "standard", "note": "512x384"},
            {"res_width": 384, "res_height": 384, "max_fps": 36000, "mode_type": "standard", "note": "384x384"},
            {"res_width": 384, "res_height": 256, "max_fps": 54000, "mode_type": "standard", "note": "384x256"},
            {"res_width": 256, "res_height": 256, "max_fps": 67500, "mode_type": "standard", "note": "256x256"},
            {"res_width": 256, "res_height": 160, "max_fps": 100000, "mode_type": "standard", "note": "256x160"},
            {"res_width": 128, "res_height": 128, "max_fps": 160000, "mode_type": "standard", "note": "128x128"},
            {"res_width": 128, "res_height": 80, "max_fps": 216000, "mode_type": "standard", "note": "128x80"},
            {"res_width": 128, "res_height": 64, "max_fps": 240000, "mode_type": "standard", "note": "128x64"},
            {"res_width": 128, "res_height": 32, "max_fps": 360000, "mode_type": "standard", "note": "128x32"},
            {"res_width": 128, "res_height": 16, "max_fps": 540000, "mode_type": "reduced", "note": "type 540K"},
            {"res_width": 128, "res_height": 16, "max_fps": 900000, "mode_type": "reduced", "note": "type 900K"},
        ],
        "FASTCAM Mini AX100": [
            {"res_width": 1024, "res_height": 1024, "max_fps": 4000, "mode_type": "standard", "note": "full frame"},
            {"res_width": 1024, "res_height": 992, "max_fps": 4500, "mode_type": "standard", "note": "1024x992"},
            {"res_width": 1024, "res_height": 880, "max_fps": 5000, "mode_type": "standard", "note": "1024x880"},
            {"res_width": 1024, "res_height": 768, "max_fps": 5400, "mode_type": "standard", "note": "1024x768"},
            {"res_width": 1024, "res_height": 736, "max_fps": 6000, "mode_type": "standard", "note": "1024x736"},
            {"res_width": 1024, "res_height": 608, "max_fps": 7200, "mode_type": "standard", "note": "1024x608"},
            {"res_width": 1024, "res_height": 512, "max_fps": 8500, "mode_type": "standard", "note": "1024x512"},
            {"res_width": 896, "res_height": 896, "max_fps": 5400, "mode_type": "standard", "note": "896x896"},
            {"res_width": 896, "res_height": 768, "max_fps": 6000, "mode_type": "standard", "note": "896x768"},
            {"res_width": 896, "res_height": 512, "max_fps": 9000, "mode_type": "standard", "note": "896x512"},
            {"res_width": 768, "res_height": 768, "max_fps": 6800, "mode_type": "standard", "note": "768x768"},
            {"res_width": 768, "res_height": 512, "max_fps": 10000, "mode_type": "standard", "note": "768x512"},
            {"res_width": 640, "res_height": 640, "max_fps": 9000, "mode_type": "standard", "note": "640x640"},
            {"res_width": 640, "res_height": 480, "max_fps": 12500, "mode_type": "standard", "note": "640x480"},
            {"res_width": 512, "res_height": 512, "max_fps": 13600, "mode_type": "standard", "note": "512x512"},
            {"res_width": 512, "res_height": 384, "max_fps": 18000, "mode_type": "standard", "note": "512x384"},
            {"res_width": 384, "res_height": 384, "max_fps": 21600, "mode_type": "standard", "note": "384x384"},
            {"res_width": 384, "res_height": 256, "max_fps": 30000, "mode_type": "standard", "note": "384x256"},
            {"res_width": 256, "res_height": 256, "max_fps": 37500, "mode_type": "standard", "note": "256x256"},
            {"res_width": 256, "res_height": 128, "max_fps": 60000, "mode_type": "standard", "note": "256x128"},
            {"res_width": 128, "res_height": 128, "max_fps": 76500, "mode_type": "standard", "note": "128x128"},
            {"res_width": 128, "res_height": 96, "max_fps": 100000, "mode_type": "standard", "note": "128x96"},
            {"res_width": 128, "res_height": 64, "max_fps": 127500, "mode_type": "standard", "note": "128x64"},
            {"res_width": 128, "res_height": 32, "max_fps": 170000, "mode_type": "standard", "note": "128x32"},
            {"res_width": 128, "res_height": 16, "max_fps": 212500, "mode_type": "standard", "note": "128x16"},
            {"res_width": 128, "res_height": 16, "max_fps": 340000, "mode_type": "reduced", "note": "type 200K"},
            {"res_width": 128, "res_height": 16, "max_fps": 540000, "mode_type": "reduced", "note": "type 540K"},
        ],
        "FASTCAM Mini AX50": [
            {"res_width": 1024, "res_height": 1024, "max_fps": 2000, "mode_type": "standard", "note": "full frame"},
            {"res_width": 1024, "res_height": 896, "max_fps": 2500, "mode_type": "standard", "note": "1024x896"},
            {"res_width": 1024, "res_height": 736, "max_fps": 3000, "mode_type": "standard", "note": "1024x736"},
            {"res_width": 1024, "res_height": 608, "max_fps": 3600, "mode_type": "standard", "note": "1024x608"},
            {"res_width": 1024, "res_height": 560, "max_fps": 4000, "mode_type": "standard", "note": "1024x560"},
            {"res_width": 1024, "res_height": 496, "max_fps": 4500, "mode_type": "standard", "note": "1024x496"},
            {"res_width": 896, "res_height": 896, "max_fps": 2500, "mode_type": "standard", "note": "896x896"},
            {"res_width": 896, "res_height": 768, "max_fps": 3000, "mode_type": "standard", "note": "896x768"},
            {"res_width": 896, "res_height": 512, "max_fps": 4500, "mode_type": "standard", "note": "896x512"},
            {"res_width": 768, "res_height": 768, "max_fps": 3600, "mode_type": "standard", "note": "768x768"},
            {"res_width": 768, "res_height": 544, "max_fps": 5000, "mode_type": "standard", "note": "768x544"},
            {"res_width": 768, "res_height": 512, "max_fps": 5400, "mode_type": "standard", "note": "768x512"},
            {"res_width": 640, "res_height": 640, "max_fps": 4500, "mode_type": "standard", "note": "640x640"},
            {"res_width": 640, "res_height": 480, "max_fps": 6000, "mode_type": "standard", "note": "640x480"},
            {"res_width": 512, "res_height": 512, "max_fps": 6000, "mode_type": "standard", "note": "512x512"},
            {"res_width": 512, "res_height": 384, "max_fps": 9000, "mode_type": "standard", "note": "512x384"},
            {"res_width": 384, "res_height": 384, "max_fps": 10000, "mode_type": "standard", "note": "384x384"},
            {"res_width": 384, "res_height": 256, "max_fps": 13600, "mode_type": "standard", "note": "384x256"},
            {"res_width": 256, "res_height": 256, "max_fps": 37500, "mode_type": "standard", "note": "256x256"},
            {"res_width": 256, "res_height": 128, "max_fps": 60000, "mode_type": "standard", "note": "256x128"},
            {"res_width": 128, "res_height": 128, "max_fps": 45000, "mode_type": "standard", "note": "128x128"},
            {"res_width": 128, "res_height": 96, "max_fps": 60000, "mode_type": "standard", "note": "128x96"},
            {"res_width": 128, "res_height": 64, "max_fps": 76500, "mode_type": "standard", "note": "128x64"},
            {"res_width": 128, "res_height": 32, "max_fps": 127500, "mode_type": "standard", "note": "128x32"},
            {"res_width": 128, "res_height": 16, "max_fps": 170000, "mode_type": "standard", "note": "128x16"},
            {"res_width": 128, "res_height": 16, "max_fps": 340000, "mode_type": "reduced", "note": "type 200K"},
            {"res_width": 128, "res_height": 16, "max_fps": 540000, "mode_type": "reduced", "note": "type 540K"},
        ],
        "FASTCAM MH6": [
            {"res_width": 1920, "res_height": 1400, "max_fps": 750, "mode_type": "standard", "note": "full frame"},
            {"res_width": 1920, "res_height": 1080, "max_fps": 1000, "mode_type": "standard", "note": "Full HD"},
            {"res_width": 1920, "res_height": 568, "max_fps": 1600, "mode_type": "standard", "note": "1920x568"},
            {"res_width": 1920, "res_height": 376, "max_fps": 2000, "mode_type": "standard", "note": "1920x376"},
            {"res_width": 1920, "res_height": 280, "max_fps": 2640, "mode_type": "standard", "note": "1920x280"},
            {"res_width": 1920, "res_height": 224, "max_fps": 3000, "mode_type": "standard", "note": "1920x224"},
            {"res_width": 1376, "res_height": 1376, "max_fps": 750, "mode_type": "standard", "note": "1376x1376"},
            {"res_width": 1280, "res_height": 1024, "max_fps": 1000, "mode_type": "standard", "note": "1280x1024"},
            {"res_width": 1280, "res_height": 800, "max_fps": 1600, "mode_type": "standard", "note": "1280x800"},
            {"res_width": 1280, "res_height": 720, "max_fps": 1600, "mode_type": "standard", "note": "720p"},
            {"res_width": 1280, "res_height": 600, "max_fps": 2000, "mode_type": "standard", "note": "1280x600"},
            {"res_width": 1280, "res_height": 512, "max_fps": 2640, "mode_type": "standard", "note": "1280x512"},
            {"res_width": 1280, "res_height": 256, "max_fps": 4000, "mode_type": "standard", "note": "1280x256"},
            {"res_width": 1280, "res_height": 196, "max_fps": 5000, "mode_type": "standard", "note": "1280x196"},
            {"res_width": 1024, "res_height": 1024, "max_fps": 1600, "mode_type": "standard", "note": "1024x1024"},
            {"res_width": 960, "res_height": 720, "max_fps": 2000, "mode_type": "standard", "note": "960x720"},
            {"res_width": 800, "res_height": 600, "max_fps": 2640, "mode_type": "standard", "note": "800x600"},
            {"res_width": 640, "res_height": 480, "max_fps": 3000, "mode_type": "standard", "note": "640x480"},
            {"res_width": 512, "res_height": 512, "max_fps": 3000, "mode_type": "standard", "note": "512x512"},
            {"res_width": 512, "res_height": 256, "max_fps": 5000, "mode_type": "standard", "note": "512x256"},
            {"res_width": 320, "res_height": 240, "max_fps": 5000, "mode_type": "standard", "note": "320x240"},
        ],
        # MH6 LT uses the same Camera Head sensor, same modes
        "FASTCAM MH6 LT": [
            {"res_width": 1920, "res_height": 1400, "max_fps": 750, "mode_type": "standard", "note": "full frame"},
            {"res_width": 1920, "res_height": 1080, "max_fps": 1000, "mode_type": "standard", "note": "Full HD"},
            {"res_width": 1920, "res_height": 568, "max_fps": 1600, "mode_type": "standard", "note": "1920x568"},
            {"res_width": 1920, "res_height": 376, "max_fps": 2000, "mode_type": "standard", "note": "1920x376"},
            {"res_width": 1920, "res_height": 280, "max_fps": 2640, "mode_type": "standard", "note": "1920x280"},
            {"res_width": 1920, "res_height": 224, "max_fps": 3000, "mode_type": "standard", "note": "1920x224"},
            {"res_width": 1376, "res_height": 1376, "max_fps": 750, "mode_type": "standard", "note": "1376x1376"},
            {"res_width": 1280, "res_height": 1024, "max_fps": 1000, "mode_type": "standard", "note": "1280x1024"},
            {"res_width": 1280, "res_height": 800, "max_fps": 1600, "mode_type": "standard", "note": "1280x800"},
            {"res_width": 1280, "res_height": 720, "max_fps": 1600, "mode_type": "standard", "note": "720p"},
            {"res_width": 1280, "res_height": 600, "max_fps": 2000, "mode_type": "standard", "note": "1280x600"},
            {"res_width": 1280, "res_height": 512, "max_fps": 2640, "mode_type": "standard", "note": "1280x512"},
            {"res_width": 1280, "res_height": 256, "max_fps": 4000, "mode_type": "standard", "note": "1280x256"},
            {"res_width": 1280, "res_height": 196, "max_fps": 5000, "mode_type": "standard", "note": "1280x196"},
            {"res_width": 1024, "res_height": 1024, "max_fps": 1600, "mode_type": "standard", "note": "1024x1024"},
            {"res_width": 960, "res_height": 720, "max_fps": 2000, "mode_type": "standard", "note": "960x720"},
            {"res_width": 800, "res_height": 600, "max_fps": 2640, "mode_type": "standard", "note": "800x600"},
            {"res_width": 640, "res_height": 480, "max_fps": 3000, "mode_type": "standard", "note": "640x480"},
            {"res_width": 512, "res_height": 512, "max_fps": 3000, "mode_type": "standard", "note": "512x512"},
            {"res_width": 512, "res_height": 256, "max_fps": 5000, "mode_type": "standard", "note": "512x256"},
            {"res_width": 320, "res_height": 240, "max_fps": 5000, "mode_type": "standard", "note": "320x240"},
        ],
    }

    # Copy v1 cameras, replacing modes where we have expanded data
    cameras = []
    for cam in v1["cameras"]:
        model = cam.get("model_name", cam.get("model", "?"))
        cam_copy = dict(cam)
        if model in expanded_modes:
            cam_copy["modes"] = expanded_modes[model]
            cam_copy["data_quality"] = "verified"
            if "modes_note" not in cam_copy:
                cam_copy["modes_note"] = "Full resolution table extracted from official Photron PDF manual"
        cameras.append(cam_copy)

    total_modes = sum(len(c["modes"]) for c in cameras)
    output = dict(v1)
    output["cameras"] = cameras
    output["verified_date"] = "2026-04-13"
    output["notes"] = f"v2: Expanded mode tables for Mini AX200 (25 modes), Mini AX100 (27 modes), Mini AX50 (27 modes), MH6/MH6 LT (21 modes each) from official PDF manuals. Nova S and SA-Z PDFs returned 404, modes unchanged. Total: {len(cameras)} cameras, {total_modes} modes."

    with open(PH_V2, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote photron_v2.json: {len(cameras)} cameras, {total_modes} modes")
    for cam in cameras:
        model = cam.get("model_name", cam.get("model", "?"))
        n = len(cam.get("modes", []))
        marker = " *" if model in expanded_modes else ""
        print(f"  {model}: {n} modes{marker}")

    return cameras


if __name__ == "__main__":
    print("=== Processing iX Cameras PDF extractions ===")
    ix = process_ix_cameras()
    print()
    print("=== Processing Photron PDF extractions ===")
    ph = process_photron()
    print()
    print("Done. Now run scripts/build_v6.py to rebuild the database.")
