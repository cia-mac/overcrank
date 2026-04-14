#!/usr/bin/env python3
"""
Build overcrank_db_v9.json: v8 base + 77 cinema cameras from 8 agent scrapers.

Pipeline:
1. Load v8 as base (140 high-speed cameras)
2. Load each agent JSON from /tmp/cinema_agents/
3. Normalize to overcrank schema (add mode_type, compute crop_factor)
4. Preserve cinema-extended fields (codecs, DR stops, sensor_format, mount, ND, media)
5. Write to data/verified/cinema_v1.json
6. Merge into overcrank_db_v9.json
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).parent.parent
V8 = ROOT / "data" / "overcrank_db_v8.json"
V9 = ROOT / "data" / "overcrank_db_v9.json"
CINEMA_V1 = ROOT / "data" / "verified" / "cinema_v1.json"
AGENT_DIR = Path("/tmp/cinema_agents")

# Source of truth for sensor format -> crop factor (relative to full-frame 36x24mm diagonal=43.27mm)
# FF = 1.0, S35 ~= 1.5, APS-C ~= 1.5, MFT ~= 2.0, 1-inch ~= 2.7, 65mm ~= 0.75, VV = 0.9 (ish)
FORMAT_CROP = {
    "Full Frame": 1.0,
    "FF": 1.0,
    "LF": 1.0,
    "65mm": 0.75,
    "VV": 0.9,
    "Super 35": 1.5,
    "S35": 1.5,
    "APS-C": 1.5,
    "APSC": 1.5,
    "Micro Four Thirds": 2.0,
    "MFT": 2.0,
    "M43": 2.0,
    "Super 16": 2.7,
    "1-inch": 2.7,
}


def norm_crop(sensor_format, sensor_size=None):
    if sensor_format in FORMAT_CROP:
        return FORMAT_CROP[sensor_format]
    # Derive from width if known format string
    if sensor_size:
        try:
            w = float(sensor_size.split("x")[0])
            return round(36.0 / w, 2)
        except Exception:
            pass
    return None


def normalize_mode(mode):
    """Map agent mode -> overcrank mode schema."""
    out = {
        "res_width": mode.get("res_width"),
        "res_height": mode.get("res_height"),
        "max_fps": mode.get("max_fps"),
        "mode_type": mode.get("mode_type", "standard"),
        "note": mode.get("note", ""),
    }
    if mode.get("codec"):
        out["codec"] = mode["codec"]
    return out


def dedupe_modes(modes):
    """Keep highest max_fps per (res_width, res_height, codec)."""
    best = {}
    for m in modes:
        key = (m.get("res_width"), m.get("res_height"), m.get("codec"))
        existing = best.get(key)
        if existing is None or (m.get("max_fps") or 0) > (existing.get("max_fps") or 0):
            best[key] = m
    # Sort by max_fps desc for display
    return sorted(best.values(), key=lambda x: (-(x.get("max_fps") or 0), -(x.get("res_width") or 0)))


def normalize_camera(c):
    """Map agent camera -> overcrank schema with cinema extension."""
    out = {
        "brand": c.get("brand"),
        "model": c.get("model"),
        "series": c.get("series"),
        "sensor_format": c.get("sensor_format"),
        "sensor_size": c.get("sensor_size"),
        "crop_factor": norm_crop(c.get("sensor_format"), c.get("sensor_size")),
        "native_resolution": c.get("native_resolution"),
        "max_resolution_recording": c.get("max_resolution_recording"),
        "dynamic_range_stops": c.get("dynamic_range_stops"),
        "base_iso": c.get("base_iso"),
        "dual_native_iso": c.get("dual_native_iso"),
        "bit_depth": c.get("bit_depth"),
        "codecs": c.get("codecs"),
        "lens_mount_native": c.get("lens_mount_native"),
        "other_mounts": c.get("other_mounts"),
        "nd_filter": c.get("nd_filter"),
        "media": c.get("media"),
        "max_shutter_angle": c.get("max_shutter_angle"),
        "price_tier": c.get("price_tier"),
        "price_usd": c.get("price_usd"),
        "status": c.get("status"),
        "data_quality": "verified",
        "source_url": c.get("source_url"),
        "category": "cinema",
        "modes": dedupe_modes([normalize_mode(m) for m in c.get("modes", [])]),
    }
    if c.get("hybrid_note"):
        out["hybrid_note"] = c["hybrid_note"]
    # Strip None fields
    return {k: v for k, v in out.items() if v is not None}


def main():
    # Load v8
    with open(V8) as f:
        db = json.load(f)
    existing_cams = db["cameras"]

    # Tag existing high-speed cameras
    for c in existing_cams:
        c.setdefault("category", "high_speed")

    # Load agent outputs
    agents = ["arri", "red", "sony", "blackmagic", "canon", "panasonic", "zcam_dji", "kinefinity"]
    cinema_cams = []
    for agent in agents:
        path = AGENT_DIR / f"{agent}.json"
        if not path.exists():
            print(f"  Missing {agent}.json")
            continue
        with open(path) as f:
            raw = json.load(f)
        for c in raw:
            cinema_cams.append(normalize_camera(c))
        print(f"  {agent}: {len(raw)} cameras")

    # Write cinema_v1 unified file
    CINEMA_V1.parent.mkdir(parents=True, exist_ok=True)
    with open(CINEMA_V1, "w") as f:
        json.dump(cinema_cams, f, indent=2)
    print(f"\nWrote {CINEMA_V1}")

    # Dedupe: make sure no (brand, model) collisions with existing
    existing_keys = {(c["brand"], c["model"]) for c in existing_cams}
    new_cams = []
    dupes = 0
    for c in cinema_cams:
        if (c["brand"], c["model"]) in existing_keys:
            dupes += 1
            continue
        new_cams.append(c)
    if dupes:
        print(f"  Skipped {dupes} duplicate (brand,model) pairs")

    all_cams = existing_cams + new_cams

    total_modes = sum(len(c["modes"]) for c in all_cams)
    manufacturers = sorted(set(c["brand"] for c in all_cams))

    output = {
        "version": 9,
        "generated": datetime.now(timezone.utc).isoformat(),
        "camera_count": len(all_cams),
        "total_modes": total_modes,
        "manufacturers_included": manufacturers,
        "cameras": all_cams,
    }

    with open(V9, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nBuilt overcrank_db_v9.json")
    print(f"  Cameras: {len(all_cams)} (v8 had {len(existing_cams)})")
    print(f"  Cinema added: {len(new_cams)}")
    print(f"  Modes: {total_modes} (v8 had {db['total_modes']})")
    print(f"  Manufacturers ({len(manufacturers)}): {', '.join(manufacturers)}")

    brand_counts = Counter(c["brand"] for c in all_cams)
    print(f"\nBy brand:")
    for b in sorted(brand_counts):
        count = brand_counts[b]
        modes = sum(len(c["modes"]) for c in all_cams if c["brand"] == b)
        cat = next((c.get("category", "?") for c in all_cams if c["brand"] == b), "?")
        print(f"  {b}: {count} cameras, {modes} modes [{cat}]")

    cat_counts = Counter(c.get("category", "?") for c in all_cams)
    print(f"\nBy category: {dict(cat_counts)}")


if __name__ == "__main__":
    main()
