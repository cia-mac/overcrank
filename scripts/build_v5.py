#!/usr/bin/env python3
"""
Build overcrank_db_v5.json from v4 + all verified sources + manifest updates.

Steps:
1. Load v4 as base
2. Apply field_updates from manifest (sensor_size, bit_depth, etc.)
3. Apply mode_additions from manifest (Helios 8K new modes)
4. Replace Weisscam cameras with verified data
5. Add NAC cameras from verified data
6. Update Photron cameras with verified corrections
7. Upgrade data_quality for Photron from gemini_unverified -> verified
8. Write v5
"""

import json
import math
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
V4 = ROOT / "data" / "overcrank_db_v4.json"
V5 = ROOT / "data" / "overcrank_db_v5.json"
MANIFEST = ROOT / "data" / "v5_update_manifest.json"
NAC_FILE = ROOT / "data" / "verified" / "nac_v1.json"
WEISSCAM_FILE = ROOT / "data" / "verified" / "weisscam_v1.json"
PHOTRON_FILE = ROOT / "data" / "verified" / "photron_v1.json"

def load_json(path):
    with open(path) as f:
        return json.load(f)

def normalize_nac(nac_data):
    """Convert NAC verified format to DB format."""
    cameras = nac_data if isinstance(nac_data, list) else nac_data.get("cameras", [])
    result = []
    for cam in cameras:
        modes = []
        for m in cam.get("modes", cam.get("resolution_fps_modes", [])):
            if m.get("res_width") and m.get("res_height"):
                modes.append({
                    "res_width": m["res_width"],
                    "res_height": m["res_height"],
                    "max_fps": m["max_fps"],
                    "mode_type": m.get("mode_type", "standard"),
                    "note": m.get("note", m.get("notes", f"{m['res_width']}x{m['res_height']}"))
                })
        # Sensor size normalization
        sensor = cam.get("sensor_size")
        if not sensor and cam.get("sensor_size_mm"):
            sensor = cam["sensor_size_mm"].replace(" ", "") + "mm"

        result.append({
            "brand": cam.get("brand", "NAC"),
            "model": cam.get("model", cam.get("model_name", "?")),
            "series": cam.get("series", ""),
            "sensor_size": sensor,
            "crop_factor": cam.get("crop_factor"),
            "bit_depth": cam.get("bit_depth"),
            "price_tier": cam.get("price_tier", "Purchase (Quote)"),
            "price_usd": cam.get("price_usd"),
            "status": cam.get("status", "Current"),
            "data_quality": cam.get("data_quality", "verified"),
            "source_url": cam.get("source_url", ""),
            "modes": modes
        })
    return result

def normalize_weisscam(ws_data):
    """Convert Weisscam verified format to DB format."""
    cameras = ws_data.get("cameras", [])
    result = []
    for cam in cameras:
        modes = []
        for m in cam.get("modes", []):
            modes.append({
                "res_width": m["res_width"],
                "res_height": m["res_height"],
                "max_fps": m["max_fps"],
                "mode_type": m.get("mode_type", "standard"),
                "note": m.get("note", f"{m['res_width']}x{m['res_height']}")
            })
        result.append({
            "brand": cam.get("brand", "Weisscam"),
            "model": cam["model"],
            "series": cam.get("series", ""),
            "sensor_size": cam.get("sensor_size"),
            "crop_factor": cam.get("crop_factor"),
            "bit_depth": cam.get("bit_depth"),
            "price_tier": cam.get("price_tier"),
            "price_usd": cam.get("price_usd"),
            "status": cam.get("status", "Current"),
            "data_quality": "verified",
            "source_url": cam.get("source_url", ""),
            "modes": modes
        })
    return result

def normalize_photron(ph_data):
    """Convert Photron verified format to DB format. Returns dict keyed by model_name."""
    cameras = ph_data.get("cameras", [])
    result = {}
    for cam in cameras:
        model = cam.get("model_name", cam.get("model", "?"))

        # Normalize sensor size
        sensor = cam.get("sensor_size")
        if not sensor and cam.get("sensor_size_mm"):
            raw = cam["sensor_size_mm"].replace(" ", "")
            if not raw.endswith("mm"):
                raw += "mm"
            # Convert "20.48x20.48mm" format
            raw = raw.replace(" x ", "x").replace("×", "x")
            sensor = raw

        # Normalize bit depth
        bit_depth = cam.get("bit_depth")
        if isinstance(bit_depth, str):
            # Handle "12-bit", "10 / 12-bit", etc. Take the max value.
            clean = bit_depth.replace("-bit", "").replace("bit", "").strip()
            if "/" in clean:
                parts = [int(p.strip()) for p in clean.split("/")]
                bit_depth = max(parts)
            else:
                bit_depth = int(clean)

        modes = []
        for m in cam.get("modes", []):
            if m.get("res_width") and m.get("res_height"):
                modes.append({
                    "res_width": m["res_width"],
                    "res_height": m["res_height"],
                    "max_fps": m["max_fps"],
                    "mode_type": m.get("mode_type", "standard"),
                    "note": m.get("note", f"{m['res_width']}x{m['res_height']}")
                })

        result[model] = {
            "sensor_size": sensor,
            "bit_depth": bit_depth,
            "data_quality": "verified",
            "modes": modes,
            "status": cam.get("status", "Current"),
        }
    return result

def main():
    db = load_json(V4)
    manifest = load_json(MANIFEST)
    cameras = db["cameras"]

    # 1. Apply field updates from manifest
    for update in manifest.get("field_updates", []):
        brand = update["brand"]
        model = update["model"]
        for cam in cameras:
            if cam["brand"] == brand and cam["model"] == model:
                for k, v in update["set"].items():
                    cam[k] = v
                break

    # 2. Apply mode additions (Helios 8K)
    for addition in manifest.get("mode_additions", []):
        brand = addition["brand"]
        model = addition["model"]
        for cam in cameras:
            if cam["brand"] == brand and cam["model"] == model:
                existing = {(m["res_width"], m["res_height"], m["max_fps"]) for m in cam["modes"]}
                for new_mode in addition["add_modes"]:
                    key = (new_mode["res_width"], new_mode["res_height"], new_mode["max_fps"])
                    if key not in existing:
                        cam["modes"].append(new_mode)
                break

    # 3. Replace Weisscam cameras
    ws_data = load_json(WEISSCAM_FILE)
    ws_cameras = normalize_weisscam(ws_data)
    cameras = [c for c in cameras if c["brand"] != "Weisscam"]
    cameras.extend(ws_cameras)

    # 4. Add NAC cameras
    nac_data = load_json(NAC_FILE)
    nac_cameras = normalize_nac(nac_data)
    cameras.extend(nac_cameras)

    # 5. Update Photron with verified data
    ph_data = load_json(PHOTRON_FILE)
    ph_verified = normalize_photron(ph_data)
    for cam in cameras:
        if cam["brand"] == "Photron":
            model_key = cam["model"]
            if model_key in ph_verified:
                verified = ph_verified[model_key]
                if verified.get("sensor_size"):
                    cam["sensor_size"] = verified["sensor_size"]
                if verified.get("bit_depth"):
                    cam["bit_depth"] = verified["bit_depth"]
                cam["data_quality"] = "verified"
                # Use verified modes if they have more or equal
                if len(verified["modes"]) >= len(cam["modes"]):
                    cam["modes"] = verified["modes"]

    # Build output
    total_modes = sum(len(c["modes"]) for c in cameras)
    manufacturers = sorted(set(c["brand"] for c in cameras))

    output = {
        "version": 5,
        "generated": datetime.now(timezone.utc).isoformat(),
        "camera_count": len(cameras),
        "total_modes": total_modes,
        "manufacturers_included": manufacturers,
        "cameras": cameras
    }

    with open(V5, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Built overcrank_db_v5.json")
    print(f"  Cameras: {len(cameras)}")
    print(f"  Modes: {total_modes}")
    print(f"  Manufacturers ({len(manufacturers)}): {', '.join(manufacturers)}")

    # Summary by brand
    from collections import Counter
    brand_counts = Counter(c["brand"] for c in cameras)
    quality_counts = Counter(c.get("data_quality", "?") for c in cameras)
    missing_bits = [c["model"] for c in cameras if not c.get("bit_depth")]
    missing_sensor = [c["model"] for c in cameras if not c.get("sensor_size")]

    print(f"\nBy brand:")
    for b in sorted(brand_counts):
        count = brand_counts[b]
        modes = sum(len(c["modes"]) for c in cameras if c["brand"] == b)
        print(f"  {b}: {count} cameras, {modes} modes")

    print(f"\nData quality: {dict(quality_counts)}")
    if missing_bits:
        print(f"Still missing bit_depth: {missing_bits}")
    if missing_sensor:
        print(f"Still missing sensor_size: {missing_sensor}")

if __name__ == "__main__":
    main()
