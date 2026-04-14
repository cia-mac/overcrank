#!/usr/bin/env python3
"""
Build overcrank_db_v7.json from v6 + photron_v3 expanded mode tables.

Steps:
1. Load v6 as base
2. Replace Photron modes with photron_v3.json (agent 2 expanded data)
3. Write v7
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).parent.parent
V6 = ROOT / "data" / "overcrank_db_v6.json"
V7 = ROOT / "data" / "overcrank_db_v7.json"
PH_V3 = ROOT / "data" / "verified" / "photron_v3.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def main():
    db = load_json(V6)
    cameras = db["cameras"]

    # Replace Photron modes with photron_v3 expanded data
    ph_data = load_json(PH_V3)
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
        "version": 7,
        "generated": datetime.now(timezone.utc).isoformat(),
        "camera_count": len(cameras),
        "total_modes": total_modes,
        "manufacturers_included": manufacturers,
        "cameras": cameras
    }

    with open(V7, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nBuilt overcrank_db_v7.json")
    print(f"  Cameras: {len(cameras)}")
    print(f"  Modes: {total_modes} (v6 had {db['total_modes']})")
    print(f"  Manufacturers ({len(manufacturers)}): {', '.join(manufacturers)}")
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
