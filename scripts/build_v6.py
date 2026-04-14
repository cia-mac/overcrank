#!/usr/bin/env python3
"""
Build overcrank_db_v6.json from v5 + expanded mode tables.

Steps:
1. Load v5 as base
2. Replace iX Cameras modes with full PDF-extracted tables (ix_cameras_v4.json)
3. Replace Photron modes where expanded data exists (photron_v2.json)
4. Write v6
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).parent.parent
V5 = ROOT / "data" / "overcrank_db_v5.json"
V6 = ROOT / "data" / "overcrank_db_v6.json"
IX_V4 = ROOT / "data" / "verified" / "ix_cameras_v4.json"
PH_V2 = ROOT / "data" / "verified" / "photron_v2.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def normalize_ix_mode(m):
    """Ensure consistent mode format."""
    return {
        "res_width": m["res_width"],
        "res_height": m["res_height"],
        "max_fps": m["max_fps"],
        "mode_type": m.get("mode_type", "standard"),
        "note": m.get("note", f"{m['res_width']}x{m['res_height']}")
    }


def main():
    db = load_json(V5)
    cameras = db["cameras"]

    # 1. Replace iX Cameras modes with full PDF tables
    ix_data = load_json(IX_V4)
    ix_lookup = {}
    for cam in ix_data["cameras"]:
        ix_lookup[cam["model"]] = cam

    ix_updated = 0
    for cam in cameras:
        if cam["brand"] == "iX Cameras" and cam["model"] in ix_lookup:
            verified = ix_lookup[cam["model"]]
            old_count = len(cam["modes"])
            cam["modes"] = [normalize_ix_mode(m) for m in verified["modes"]]
            cam["data_quality"] = "verified"
            ix_updated += 1
            print(f"  iX {cam['model']}: {old_count} -> {len(cam['modes'])} modes")

    # 2. Replace Photron modes where expanded data exists
    ph_data = load_json(PH_V2)
    ph_lookup = {}
    for cam in ph_data["cameras"]:
        model = cam.get("model_name", cam.get("model", "?"))
        ph_lookup[model] = cam

    ph_updated = 0
    for cam in cameras:
        if cam["brand"] == "Photron":
            model_key = cam["model"]
            if model_key in ph_lookup:
                verified = ph_lookup[model_key]
                v_modes = verified.get("modes", [])
                # Only replace if the verified data has more modes
                if len(v_modes) > len(cam["modes"]):
                    old_count = len(cam["modes"])
                    cam["modes"] = v_modes
                    cam["data_quality"] = "verified"
                    ph_updated += 1
                    print(f"  Photron {cam['model']}: {old_count} -> {len(cam['modes'])} modes")

    # Build output
    total_modes = sum(len(c["modes"]) for c in cameras)
    manufacturers = sorted(set(c["brand"] for c in cameras))

    output = {
        "version": 6,
        "generated": datetime.now(timezone.utc).isoformat(),
        "camera_count": len(cameras),
        "total_modes": total_modes,
        "manufacturers_included": manufacturers,
        "cameras": cameras
    }

    with open(V6, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nBuilt overcrank_db_v6.json")
    print(f"  Cameras: {len(cameras)}")
    print(f"  Modes: {total_modes} (v5 had {db['total_modes']})")
    print(f"  Manufacturers ({len(manufacturers)}): {', '.join(manufacturers)}")
    print(f"  iX Cameras updated: {ix_updated}")
    print(f"  Photron updated: {ph_updated}")

    # Summary by brand
    brand_counts = Counter(c["brand"] for c in cameras)
    print(f"\nBy brand:")
    for b in sorted(brand_counts):
        count = brand_counts[b]
        modes = sum(len(c["modes"]) for c in cameras if c["brand"] == b)
        print(f"  {b}: {count} cameras, {modes} modes")

    quality_counts = Counter(c.get("data_quality", "?") for c in cameras)
    print(f"\nData quality: {dict(quality_counts)}")


if __name__ == "__main__":
    main()
