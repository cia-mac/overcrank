#!/usr/bin/env python3
"""
Add missing camera models to verified JSON files, then rebuild DB as v8.

Adds:
- Phantom v-series UHS (6 cameras)
- Phantom VEO/T/Miro/S-series (variable, from agent results)
- iX Cameras 2-series and 7-series additions (variable)
- Photron Orion S40, Mini Nova S20, Pharsighted E9 (variable)
- Kron Chronos Q12

This script hardcodes the scraped data from manufacturer websites.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).parent.parent
V7 = ROOT / "data" / "overcrank_db_v7.json"
V8 = ROOT / "data" / "overcrank_db_v8.json"
PHANTOM_V1 = ROOT / "data" / "verified" / "phantom_v1.json"
PHANTOM_V2 = ROOT / "data" / "verified" / "phantom_v2.json"
IX_V4 = ROOT / "data" / "verified" / "ix_cameras_v4.json"
IX_V5 = ROOT / "data" / "verified" / "ix_cameras_v5.json"
PHOTRON_V3 = ROOT / "data" / "verified" / "photron_v3.json"
PHOTRON_V4 = ROOT / "data" / "verified" / "photron_v4.json"
KRON_V1 = ROOT / "data" / "verified" / "kron_chronos_v1.json"
KRON_V2 = ROOT / "data" / "verified" / "kron_chronos_v2.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Wrote {path.name}")


def make_mode(w, h, fps, mode_type="standard", note=None):
    m = {
        "res_width": w,
        "res_height": h,
        "max_fps": fps,
        "mode_type": mode_type,
        "note": note or f"{w}x{h}"
    }
    return m


# ============================================================
# PHANTOM V-SERIES UHS (from official datasheets)
# ============================================================

PHANTOM_V_SERIES = [
    {
        "brand": "Phantom",
        "series": "v-Series UHS",
        "model": "Phantom v2640",
        "sensor_type": "BSI CMOS",
        "native_resolution": "2048x1952",
        "pixel_size_um": 13.5,
        "sensor_size": "27.6x26.3mm",
        "crop_factor": 1.32,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/ultrahighspeed/v2640",
        "modes": [
            make_mode(2048, 1952, 6600, "standard", "Full sensor HS"),
            make_mode(2048, 1600, 8020, "standard", "2048x1600 HS"),
            make_mode(2048, 1440, 8880, "standard", "2048x1440 HS"),
            make_mode(1920, 1080, 12510, "standard", "Full HD HS"),
            make_mode(1792, 976, 14740, "standard", "1792x976 HS"),
            make_mode(1280, 720, 19695, "standard", "720p HS"),
            make_mode(1024, 976, 25030, "binned", "1024x976 HS Binned"),
            make_mode(896, 720, 37360, "binned", "896x720 HS Binned"),
            make_mode(640, 480, 53290, "binned", "640x480 HS Binned"),
            make_mode(256, 320, 74460, "binned", "256x320 HS Binned"),
            make_mode(256, 64, 204270, "binned", "256x64 HS Binned"),
            make_mode(896, 16, 303460, "binned", "896x16 HS Binned"),
            make_mode(1792, 8, 303460, "standard", "1792x8 HS max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "v-Series UHS",
        "model": "Phantom v1840",
        "sensor_type": "BSI CMOS",
        "native_resolution": "2048x1952",
        "pixel_size_um": 13.5,
        "sensor_size": "27.6x26.3mm",
        "crop_factor": 1.32,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/ultrahighspeed/v1840",
        "modes": [
            make_mode(2048, 1952, 4510, "standard", "Full sensor HS"),
            make_mode(2048, 1600, 5490, "standard", "2048x1600 HS"),
            make_mode(2048, 1440, 6080, "standard", "2048x1440 HS"),
            make_mode(1920, 1080, 8570, "standard", "Full HD HS"),
            make_mode(1792, 976, 10110, "standard", "1792x976 HS"),
            make_mode(1280, 720, 13540, "standard", "720p HS"),
            make_mode(1024, 976, 17240, "binned", "1024x976 HS Binned"),
            make_mode(896, 720, 25850, "binned", "896x720 HS Binned"),
            make_mode(640, 480, 37100, "binned", "640x480 HS Binned"),
            make_mode(256, 320, 52260, "binned", "256x320 HS Binned"),
            make_mode(256, 64, 150840, "binned", "256x64 HS Binned"),
            make_mode(896, 16, 225000, "binned", "896x16 HS Binned"),
            make_mode(1792, 8, 225000, "standard", "1792x8 HS max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "v-Series UHS",
        "model": "Phantom v2512",
        "sensor_type": "CMOS",
        "native_resolution": "1280x800",
        "pixel_size_um": 28,
        "sensor_size": "35.8x22.4mm",
        "crop_factor": 1.0,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/ultrahighspeed/v2512",
        "modes": [
            make_mode(1280, 800, 25700, "standard", "Full sensor"),
            make_mode(1280, 720, 28500, "standard", "720p"),
            make_mode(1024, 800, 30500, "standard", "1024x800"),
            make_mode(1024, 512, 47400, "standard", "1024x512"),
            make_mode(896, 800, 33700, "standard", "896x800"),
            make_mode(768, 768, 39100, "standard", "768x768"),
            make_mode(640, 480, 70100, "standard", "640x480"),
            make_mode(512, 512, 75600, "standard", "512x512"),
            make_mode(512, 384, 99800, "standard", "512x384"),
            make_mode(384, 256, 171650, "standard", "384x256"),
            make_mode(256, 256, 206300, "standard", "256x256"),
            make_mode(256, 128, 380100, "standard", "256x128"),
            make_mode(128, 64, 663250, "standard", "128x64"),
            make_mode(128, 32, 677000, "standard", "128x32"),
            make_mode(128, 16, 663280, "standard", "128x16"),
            make_mode(256, 32, 1000000, "standard_fast", "256x32 FAST option"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "v-Series UHS",
        "model": "Phantom v2012",
        "sensor_type": "CMOS",
        "native_resolution": "1280x800",
        "pixel_size_um": 28,
        "sensor_size": "35.8x22.4mm",
        "crop_factor": 1.0,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/ultrahighspeed/v2012",
        "modes": [
            make_mode(1280, 800, 22600, "standard", "Full sensor"),
            make_mode(1280, 720, 25100, "standard", "720p"),
            make_mode(1024, 800, 26900, "standard", "1024x800"),
            make_mode(1024, 512, 41800, "standard", "1024x512"),
            make_mode(896, 800, 29800, "standard", "896x800"),
            make_mode(768, 768, 34750, "standard", "768x768"),
            make_mode(640, 480, 62500, "standard", "640x480"),
            make_mode(512, 512, 67800, "standard", "512x512"),
            make_mode(512, 384, 89550, "standard", "512x384"),
            make_mode(384, 256, 115100, "standard", "384x256"),
            make_mode(256, 256, 188500, "standard", "256x256"),
            make_mode(256, 128, 347800, "standard", "256x128"),
            make_mode(128, 64, 651150, "standard", "128x64"),
            make_mode(128, 32, 666000, "standard", "128x32"),
            make_mode(384, 16, 1000000, "standard_fast", "384x16 FAST option"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "v-Series UHS",
        "model": "Phantom v1612",
        "sensor_type": "CMOS",
        "native_resolution": "1280x800",
        "pixel_size_um": 28,
        "sensor_size": "35.8x22.4mm",
        "crop_factor": 1.0,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/ultrahighspeed/v1612",
        "modes": [
            make_mode(1280, 800, 16600, "standard", "Full sensor"),
            make_mode(1280, 720, 18400, "standard", "720p"),
            make_mode(1024, 800, 19700, "standard", "1024x800"),
            make_mode(1024, 512, 30700, "standard", "1024x512"),
            make_mode(896, 800, 21800, "standard", "896x800"),
            make_mode(768, 768, 25300, "standard", "768x768"),
            make_mode(640, 480, 45500, "standard", "640x480"),
            make_mode(512, 512, 49100, "standard", "512x512"),
            make_mode(512, 384, 65000, "standard", "512x384"),
            make_mode(384, 256, 112300, "standard", "384x256"),
            make_mode(256, 256, 135400, "standard", "256x256"),
            make_mode(256, 128, 253000, "standard", "256x128"),
            make_mode(128, 64, 538400, "standard", "128x64"),
            make_mode(128, 32, 626850, "standard", "128x32"),
            make_mode(128, 16, 647000, "standard", "128x16"),
            make_mode(128, 16, 1000000, "standard_fast", "128x16 FAST option"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "v-Series UHS",
        "model": "Phantom v1212",
        "sensor_type": "CMOS",
        "native_resolution": "1280x800",
        "pixel_size_um": 28,
        "sensor_size": "35.8x22.4mm",
        "crop_factor": 1.0,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/ultrahighspeed/v1212",
        "modes": [
            make_mode(1280, 800, 12600, "standard", "Full sensor"),
            make_mode(1280, 720, 14000, "standard", "720p"),
            make_mode(1024, 800, 15000, "standard", "1024x800"),
            make_mode(1024, 512, 23400, "standard", "1024x512"),
            make_mode(896, 800, 16600, "standard", "896x800"),
            make_mode(768, 768, 19300, "standard", "768x768"),
            make_mode(640, 480, 34700, "standard", "640x480"),
            make_mode(512, 512, 37500, "standard", "512x512"),
            make_mode(512, 384, 49600, "standard", "512x384"),
            make_mode(384, 256, 85700, "standard", "384x256"),
            make_mode(256, 256, 103500, "standard", "256x256"),
            make_mode(256, 128, 193900, "standard", "256x128"),
            make_mode(128, 64, 415500, "standard", "128x64"),
            make_mode(128, 32, 551700, "standard", "128x32"),
            make_mode(128, 16, 571000, "standard", "128x16"),
            make_mode(128, 16, 820500, "standard_fast", "128x16 FAST option"),
        ]
    },
]


# ============================================================
# PHANTOM VEO / T / MIRO / S SERIES
# (Will be populated when agent 2 returns)
# ============================================================

PHANTOM_OTHER = [
    {
        "brand": "Phantom",
        "series": "VEO",
        "model": "Phantom VEO 410",
        "sensor_size": "25.6x16mm",
        "crop_factor": 1.43,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/veo/veo410",
        "modes": [
            make_mode(1280, 800, 5200, "standard", "Full sensor"),
            make_mode(1280, 720, 5800, "standard", "720p"),
            make_mode(640, 480, 15900, "standard", "640x480"),
            make_mode(256, 256, 57500, "standard", "256x256"),
            make_mode(64, 8, 650000, "standard", "64x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "VEO",
        "model": "Phantom VEO 710",
        "sensor_size": "25.6x16mm",
        "crop_factor": 1.43,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/veo/veo710",
        "modes": [
            make_mode(1280, 800, 7500, "standard", "Full sensor"),
            make_mode(1280, 720, 8300, "standard", "720p"),
            make_mode(1024, 720, 10100, "standard", "1024x720"),
            make_mode(768, 480, 19200, "standard", "768x480"),
            make_mode(640, 480, 22300, "standard", "640x480"),
            make_mode(512, 512, 24800, "standard", "512x512"),
            make_mode(512, 320, 39400, "standard", "512x320"),
            make_mode(256, 256, 77600, "standard", "256x256"),
            make_mode(256, 160, 120500, "standard", "256x160"),
            make_mode(128, 128, 204000, "standard", "128x128"),
            make_mode(128, 64, 360000, "standard", "128x64"),
            make_mode(128, 32, 580000, "standard", "128x32"),
            make_mode(64, 8, 690000, "standard", "64x8"),
            make_mode(64, 8, 1000000, "standard_fast", "64x8 FAST option"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "VEO",
        "model": "Phantom VEO4K-PL",
        "sensor_size": "27.6x15.6mm",
        "crop_factor": 1.32,
        "bit_depth": 12,
        "price_tier": "Rental / Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/veo/veo4kpl",
        "modes": [
            make_mode(4096, 2304, 938, "standard", "4K full sensor"),
            make_mode(4096, 2160, 1000, "standard", "4K UHD"),
            make_mode(4096, 2048, 1050, "standard", "4K DCI"),
            make_mode(4096, 1152, 1850, "standard", "4K anamorphic"),
            make_mode(4096, 1080, 1970, "standard", "4K x 1080"),
            make_mode(4096, 720, 2930, "standard", "4K x 720"),
            make_mode(4096, 360, 5660, "standard", "4K x 360"),
            make_mode(4096, 8, 64300, "standard", "4096x8 max fps"),
            make_mode(2048, 2048, 1050, "standard", "2K square"),
            make_mode(2048, 1152, 1850, "standard", "2K x 1152"),
            make_mode(2048, 1080, 1970, "standard", "Full HD"),
            make_mode(2048, 240, 8220, "standard", "2048x240"),
            make_mode(2048, 8, 64300, "standard", "2048x8"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "T-Series",
        "model": "Phantom T1340",
        "sensor_size": "27.6x26.3mm",
        "crop_factor": 1.32,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/tseries/t1340",
        "modes": [
            make_mode(2048, 1952, 3270, "standard", "Full sensor"),
            make_mode(2048, 1440, 4390, "standard", "2048x1440"),
            make_mode(2048, 1256, 5010, "standard", "2048x1256"),
            make_mode(1920, 1080, 6160, "standard", "Full HD"),
            make_mode(1280, 720, 13050, "standard", "720p"),
            make_mode(1024, 976, 9900, "standard", "1024x976"),
            make_mode(1024, 976, 12130, "binned", "1024x976 Binned"),
            make_mode(768, 608, 15160, "standard", "768x608"),
            make_mode(768, 608, 23360, "binned", "768x608 Binned"),
            make_mode(640, 480, 18600, "standard", "640x480"),
            make_mode(640, 480, 32350, "binned", "640x480 Binned"),
            make_mode(640, 352, 24050, "standard", "640x352"),
            make_mode(640, 352, 40300, "binned", "640x352 Binned"),
            make_mode(640, 272, 29450, "standard", "640x272"),
            make_mode(640, 272, 47610, "binned", "640x272 Binned"),
            make_mode(640, 128, 49400, "standard", "640x128"),
            make_mode(640, 128, 70700, "binned", "640x128 Binned"),
            make_mode(640, 16, 104470, "standard", "640x16"),
            make_mode(640, 16, 113510, "binned", "640x16 Binned max fps"),
            make_mode(2048, 8, 107900, "standard", "2048x8"),
            make_mode(640, 8, 113510, "standard", "640x8"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro C321",
        "sensor_size": "19.2x10.8mm",
        "crop_factor": 1.9,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/mirocnn/miroc321",
        "modes": [
            make_mode(1920, 1080, 1480, "standard", "Full HD"),
            make_mode(1920, 800, 1990, "standard", "1920x800"),
            make_mode(1280, 1024, 1560, "standard", "1280x1024"),
            make_mode(1280, 512, 3090, "standard", "1280x512"),
            make_mode(640, 480, 3290, "standard", "640x480"),
            make_mode(640, 128, 11765, "standard", "640x128"),
            make_mode(640, 64, 22070, "standard", "640x64"),
            make_mode(640, 8, 94510, "standard", "640x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro C321 Air",
        "sensor_size": "19.2x10.8mm",
        "crop_factor": 1.9,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/mirocnn",
        "modes": [
            make_mode(1920, 1080, 1480, "standard", "Full HD"),
            make_mode(1920, 800, 1990, "standard", "1920x800"),
            make_mode(1280, 1024, 1560, "standard", "1280x1024"),
            make_mode(1280, 512, 3090, "standard", "1280x512"),
            make_mode(640, 480, 3290, "standard", "640x480"),
            make_mode(640, 128, 11765, "standard", "640x128"),
            make_mode(640, 64, 22070, "standard", "640x64"),
            make_mode(640, 8, 94510, "standard", "640x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro C211",
        "sensor_size": "7.16x5.73mm",
        "crop_factor": 5.03,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/mirocnn/miroc211",
        "modes": [
            make_mode(1280, 1024, 1800, "standard", "Full sensor"),
            make_mode(1280, 800, 2290, "standard", "1280x800"),
            make_mode(1280, 720, 2540, "standard", "720p"),
            make_mode(768, 768, 2380, "standard", "768x768"),
            make_mode(768, 576, 3150, "standard", "768x576"),
            make_mode(640, 480, 3760, "standard", "640x480"),
            make_mode(512, 512, 3530, "standard", "512x512"),
            make_mode(512, 384, 4650, "standard", "512x384"),
            make_mode(384, 288, 6100, "standard", "384x288"),
            make_mode(256, 256, 6810, "standard", "256x256"),
            make_mode(128, 64, 22380, "standard", "128x64"),
            make_mode(64, 8, 67140, "standard", "64x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro C210",
        "sensor_size": "7.16x5.73mm",
        "crop_factor": 5.03,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/mirocnn/miroc210",
        "modes": [
            make_mode(1280, 1024, 1800, "standard", "Full sensor"),
            make_mode(1280, 720, 2540, "standard", "720p"),
            make_mode(768, 768, 2385, "standard", "768x768"),
            make_mode(640, 480, 3760, "standard", "640x480"),
            make_mode(512, 512, 3530, "standard", "512x512"),
            make_mode(256, 256, 6811, "standard", "256x256"),
            make_mode(128, 128, 12700, "standard", "128x128"),
            make_mode(64, 8, 67140, "standard", "64x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro N5",
        "sensor_size": "3.6x2.8mm",
        "crop_factor": 10.0,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/mirocnn",
        "modes": [
            make_mode(768, 600, 560, "standard", "Full sensor"),
            make_mode(640, 480, 810, "standard", "640x480"),
            make_mode(512, 512, 930, "standard", "512x512"),
            make_mode(512, 472, 1000, "standard", "512x472"),
            make_mode(480, 480, 1040, "standard", "480x480"),
            make_mode(256, 256, 2325, "standard", "256x256"),
            make_mode(256, 128, 3565, "standard", "256x128"),
            make_mode(128, 64, 4865, "standard", "128x64"),
            make_mode(128, 32, 9000, "standard", "128x32 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro 321S",
        "sensor_size": "19.2x12mm",
        "crop_factor": 1.9,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/miromidsize/miro321s",
        "modes": [
            make_mode(1920, 1200, 1380, "standard", "Full sensor"),
            make_mode(1920, 1080, 1530, "standard", "Full HD"),
            make_mode(1280, 800, 2940, "standard", "1280x800"),
            make_mode(1280, 720, 3200, "standard", "720p"),
            make_mode(640, 480, 8300, "standard", "640x480"),
            make_mode(512, 512, 9200, "standard", "512x512"),
            make_mode(256, 256, 26400, "standard", "256x256"),
            make_mode(128, 128, 62000, "standard", "128x128"),
            make_mode(128, 8, 240000, "standard", "128x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "Miro",
        "model": "Phantom Miro R311",
        "sensor_size": "25.6x16mm",
        "crop_factor": 1.43,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/miromidsize/miror311",
        "modes": [
            make_mode(1280, 800, 3260, "standard", "Full sensor"),
            make_mode(1280, 720, 3630, "standard", "720p"),
            make_mode(640, 480, 10100, "standard", "640x480"),
            make_mode(512, 512, 11500, "standard", "512x512"),
            make_mode(256, 256, 39700, "standard", "256x256"),
            make_mode(128, 128, 120700, "standard", "128x128"),
            make_mode(128, 8, 650000, "standard", "128x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "S-Series",
        "model": "Phantom S991",
        "sensor_size": "27.6x15.5mm",
        "crop_factor": 1.32,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/machinevision/s991",
        "modes": [
            make_mode(4096, 2304, 937, "standard", "4K full sensor"),
            make_mode(3072, 2000, 1070, "standard", "3072x2000"),
            make_mode(2048, 1600, 1340, "standard", "2048x1600"),
            make_mode(1280, 800, 2630, "standard", "1280x800"),
            make_mode(1024, 512, 4030, "standard", "1024x512"),
            make_mode(1024, 128, 13840, "standard", "1024x128"),
            make_mode(1920, 64, 23270, "standard", "1920x64"),
            make_mode(2560, 32, 35280, "standard", "2560x32"),
            make_mode(2048, 16, 47550, "standard", "2048x16"),
            make_mode(128, 4, 72910, "standard", "128x4 rolling shutter max"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "S-Series",
        "model": "Phantom S710",
        "sensor_size": "25.6x16mm",
        "crop_factor": 1.43,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/machinevision/s710",
        "modes": [
            make_mode(1280, 800, 7270, "standard", "Full sensor"),
            make_mode(1024, 768, 9250, "standard", "1024x768"),
            make_mode(768, 640, 13980, "standard", "768x640"),
            make_mode(512, 512, 23480, "standard", "512x512"),
            make_mode(256, 320, 57430, "standard", "256x320"),
            make_mode(128, 32, 310800, "standard", "128x32"),
            make_mode(128, 16, 641480, "standard", "128x16 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "S-Series",
        "model": "Phantom S711",
        "sensor_size": "25.6x16mm",
        "crop_factor": 1.43,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/machinevision/s711",
        "modes": [
            make_mode(1280, 800, 7360, "standard", "Full sensor"),
            make_mode(1024, 720, 9850, "standard", "1024x720"),
            make_mode(1024, 768, 9260, "standard", "1024x768"),
            make_mode(768, 640, 13940, "standard", "768x640"),
            make_mode(512, 512, 23240, "standard", "512x512"),
            make_mode(256, 320, 53240, "standard", "256x320"),
            make_mode(256, 256, 63610, "standard", "256x256"),
            make_mode(128, 128, 129520, "standard", "128x128"),
            make_mode(128, 32, 220060, "standard", "128x32"),
            make_mode(128, 16, 249080, "standard", "128x16 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "S-Series",
        "model": "Phantom S641",
        "sensor_size": "25.6x16mm",
        "crop_factor": 1.43,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/machinevision/s641",
        "modes": [
            make_mode(2560, 1600, 1490, "standard", "Full sensor"),
            make_mode(1920, 1600, 1900, "standard", "1920x1600"),
            make_mode(1280, 1600, 2610, "standard", "1280x1600"),
            make_mode(1280, 800, 5180, "standard", "1280x800"),
            make_mode(1024, 720, 6740, "standard", "1024x720"),
            make_mode(640, 680, 9620, "standard", "640x680"),
            make_mode(512, 512, 14280, "standard", "512x512"),
            make_mode(256, 256, 36080, "standard", "256x256"),
            make_mode(128, 128, 74460, "standard", "128x128"),
            make_mode(128, 16, 202890, "standard", "128x16"),
            make_mode(128, 8, 231400, "standard", "128x8 max fps"),
        ]
    },
    {
        "brand": "Phantom",
        "series": "S-Series",
        "model": "Phantom S210",
        "sensor_size": "7.16x5.73mm",
        "crop_factor": 5.03,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.phantomhighspeed.com/products/cameras/machinevision/s210",
        "modes": [
            make_mode(1280, 1024, 1730, "standard", "Full sensor"),
            make_mode(1280, 720, 2440, "standard", "720p"),
            make_mode(1280, 576, 3030, "standard", "1280x576"),
            make_mode(1280, 480, 3610, "standard", "1280x480"),
            make_mode(1280, 256, 6545, "standard", "1280x256"),
            make_mode(1280, 128, 12210, "standard", "1280x128"),
            make_mode(1280, 8, 64550, "standard", "1280x8 max fps"),
        ]
    },
]


# ============================================================
# IX CAMERAS ADDITIONS
# (Will be populated when agent 3 returns)
# ============================================================

IX_NEW = [
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 210",
        "series": "i-SPEED 2",
        "sensor_size": "17.9x14.3mm",
        "crop_factor": 2.0,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-2-series/",
        "modes": [
            make_mode(1280, 1024, 500, "standard", "Full sensor"),
            make_mode(1280, 720, 700, "standard", "720p"),
            make_mode(1280, 512, 1000, "standard", "1280x512"),
            make_mode(800, 600, 1250, "standard", "800x600"),
            make_mode(640, 480, 1850, "standard", "640x480"),
            make_mode(512, 512, 2000, "standard", "512x512"),
            make_mode(320, 240, 5650, "standard", "320x240"),
            make_mode(128, 100, 18500, "standard", "128x100"),
            make_mode(128, 10, 79500, "standard", "128x10 max fps"),
        ]
    },
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 211",
        "series": "i-SPEED 2",
        "sensor_size": "17.9x14.3mm",
        "crop_factor": 2.0,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-2-series/",
        "modes": [
            make_mode(1280, 1024, 500, "standard", "Full sensor"),
            make_mode(1280, 720, 700, "standard", "720p"),
            make_mode(1280, 512, 1000, "standard", "1280x512"),
            make_mode(800, 600, 1250, "standard", "800x600"),
            make_mode(640, 480, 1850, "standard", "640x480"),
            make_mode(512, 512, 2000, "standard", "512x512"),
            make_mode(320, 240, 5650, "standard", "320x240"),
            make_mode(128, 100, 18500, "standard", "128x100"),
            make_mode(128, 10, 79500, "standard", "128x10 max fps"),
        ]
    },
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 220",
        "series": "i-SPEED 2",
        "sensor_size": "12.8x12.8mm",
        "crop_factor": 2.85,
        "bit_depth": 8,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-2-series/",
        "modes": [
            make_mode(1600, 1600, 600, "standard", "Full sensor"),
            make_mode(1600, 900, 1000, "standard", "1600x900"),
            make_mode(1280, 1024, 1150, "standard", "1280x1024"),
            make_mode(1024, 1024, 1400, "standard", "1024x1024"),
            make_mode(1280, 720, 1640, "standard", "720p"),
            make_mode(800, 600, 2850, "standard", "800x600"),
            make_mode(640, 480, 4450, "standard", "640x480"),
            make_mode(512, 512, 5000, "standard", "512x512"),
            make_mode(320, 240, 14750, "standard", "320x240"),
            make_mode(128, 128, 43500, "standard", "128x128"),
            make_mode(128, 10, 204100, "standard", "128x10 max fps"),
        ]
    },
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 221",
        "series": "i-SPEED 2",
        "sensor_size": "12.8x12.8mm",
        "crop_factor": 2.85,
        "bit_depth": 8,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-2-series/",
        "modes": [
            make_mode(1600, 1600, 600, "standard", "Full sensor"),
            make_mode(1600, 900, 1000, "standard", "1600x900"),
            make_mode(1280, 1024, 1150, "standard", "1280x1024"),
            make_mode(1024, 1024, 1400, "standard", "1024x1024"),
            make_mode(1280, 720, 1640, "standard", "720p"),
            make_mode(800, 600, 2850, "standard", "800x600"),
            make_mode(640, 480, 4450, "standard", "640x480"),
            make_mode(512, 512, 5000, "standard", "512x512"),
            make_mode(320, 240, 14750, "standard", "320x240"),
            make_mode(128, 128, 43500, "standard", "128x128"),
            make_mode(128, 10, 204100, "standard", "128x10 max fps"),
        ]
    },
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 230",
        "series": "i-SPEED 2",
        "sensor_size": "17.5x11.8mm",
        "crop_factor": 2.07,
        "bit_depth": 10,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-2-series/",
        "modes": [
            make_mode(1280, 864, 2500, "standard", "Full sensor"),
            make_mode(1280, 768, 2813, "standard", "1280x768"),
            make_mode(1280, 720, 3000, "standard", "720p"),
            make_mode(1280, 512, 4219, "standard", "1280x512"),
            make_mode(1280, 480, 4501, "standard", "1280x480"),
            make_mode(1280, 240, 9002, "standard", "1280x240"),
            make_mode(1280, 128, 16879, "standard", "1280x128"),
            make_mode(1280, 64, 33758, "standard", "1280x64"),
            make_mode(1280, 32, 67516, "standard", "1280x32"),
            make_mode(1280, 24, 90022, "standard", "1280x24"),
            make_mode(1280, 12, 180044, "standard", "1280x12"),
            make_mode(1280, 8, 225000, "standard", "1280x8 max fps"),
        ]
    },
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 713",
        "series": "i-SPEED 7",
        "sensor_size": "27.6x20.7mm",
        "crop_factor": 1.24,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-7-series/",
        "modes": [
            make_mode(2048, 1536, 4260, "standard", "Full sensor"),
            make_mode(1904, 1416, 5000, "standard", "1904x1416"),
            make_mode(1920, 1080, 6380, "standard", "Full HD"),
            make_mode(1568, 1134, 7500, "standard", "1568x1134"),
            make_mode(1344, 984, 10000, "standard", "1344x984"),
            make_mode(1064, 798, 15000, "standard", "1064x798"),
            make_mode(952, 672, 20000, "standard", "952x672"),
            make_mode(728, 546, 30000, "standard", "728x546"),
            make_mode(560, 420, 50000, "standard", "560x420"),
            make_mode(560, 198, 100000, "standard", "560x198"),
            make_mode(560, 84, 200000, "standard", "560x84"),
            make_mode(560, 18, 500000, "standard", "560x18"),
            make_mode(280, 24, 750000, "standard", "280x24"),
            make_mode(280, 18, 1000000, "standard", "280x18 max fps"),
        ]
    },
    {
        "brand": "iX Cameras",
        "model": "i-SPEED 720",
        "series": "i-SPEED 7",
        "sensor_size": "27.6x20.7mm",
        "crop_factor": 1.24,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://www.ix-cameras.com/i-speed-7-series/",
        "modes": [
            make_mode(2048, 1536, 6642, "standard", "Full sensor"),
            make_mode(1960, 1428, 7500, "standard", "1960x1428"),
            make_mode(1920, 1080, 9942, "standard", "Full HD"),
            make_mode(1680, 1242, 10000, "standard", "1680x1242"),
            make_mode(1344, 1008, 15000, "standard", "1344x1008"),
            make_mode(1176, 864, 20000, "standard", "1176x864"),
            make_mode(952, 696, 30000, "standard", "952x696"),
            make_mode(840, 462, 50000, "standard", "840x462"),
            make_mode(840, 216, 100000, "standard", "840x216"),
            make_mode(840, 96, 200000, "standard", "840x96"),
            make_mode(896, 24, 500000, "standard", "896x24"),
            make_mode(448, 36, 750000, "standard", "448x36"),
            make_mode(448, 24, 1000000, "standard", "448x24 max fps"),
        ]
    },
]


# ============================================================
# PHOTRON ADDITIONS
# (Will be populated when agent 4 returns)
# ============================================================

PHOTRON_NEW = [
    {
        "brand": "Photron",
        "model_name": "FASTCAM Orion S40",
        "series": "Orion",
        "sensor_size": "20.48x16.38mm",
        "crop_factor": 1.78,
        "bit_depth": 12,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://photron.com/fastcam-orion-s40/",
        "modes": [
            make_mode(1280, 1024, 31250, "standard", "Full sensor"),
            make_mode(1024, 1024, 37500, "standard", "1024x1024"),
            make_mode(1280, 640, 48000, "standard", "1280x640"),
            make_mode(1280, 512, 56250, "standard", "1280x512"),
            make_mode(896, 384, 100000, "standard", "896x384"),
            make_mode(896, 32, 312500, "standard", "896x32 max fps"),
        ]
    },
    {
        "brand": "Photron",
        "model_name": "Pharsighted E9-150S",
        "series": "Pharsighted E9",
        "sensor_size": "33.28x24.96mm",
        "crop_factor": 1.09,
        "bit_depth": 9,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://photron.com/pharsighted-e9/",
        "modes": [
            make_mode(640, 480, 489000, "standard", "Full sensor"),
            make_mode(640, 384, 601000, "standard", "640x384"),
            make_mode(640, 320, 710000, "standard", "640x320"),
            make_mode(640, 240, 918000, "standard", "640x240"),
            make_mode(640, 160, 1299000, "standard", "640x160"),
            make_mode(640, 128, 1557000, "standard", "640x128"),
            make_mode(640, 64, 2582000, "standard", "640x64"),
            make_mode(640, 48, 2720000, "standard", "640x48"),
            make_mode(640, 32, 2720000, "standard", "640x32"),
            make_mode(640, 16, 2720000, "standard", "640x16 max fps"),
        ]
    },
    {
        "brand": "Photron",
        "model_name": "Pharsighted E9-100S",
        "series": "Pharsighted E9",
        "sensor_size": "33.28x24.96mm",
        "crop_factor": 1.09,
        "bit_depth": 9,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://photron.com/pharsighted-e9/",
        "modes": [
            make_mode(640, 480, 326000, "standard", "Full sensor"),
            make_mode(640, 448, 349000, "standard", "640x448"),
            make_mode(640, 416, 375000, "standard", "640x416"),
            make_mode(640, 384, 404000, "standard", "640x384"),
            make_mode(640, 352, 439000, "standard", "640x352"),
            make_mode(640, 320, 481000, "standard", "640x320"),
            make_mode(640, 288, 531000, "standard", "640x288"),
            make_mode(640, 256, 593000, "standard", "640x256"),
            make_mode(640, 240, 629000, "standard", "640x240"),
            make_mode(640, 224, 671000, "standard", "640x224"),
            make_mode(640, 192, 772000, "standard", "640x192"),
            make_mode(640, 160, 910000, "standard", "640x160"),
            make_mode(640, 128, 1108000, "standard", "640x128"),
            make_mode(640, 96, 1416000, "standard", "640x96"),
            make_mode(640, 64, 1961000, "standard", "640x64"),
            make_mode(640, 48, 2428000, "standard", "640x48"),
            make_mode(640, 32, 2720000, "standard", "640x32"),
            make_mode(640, 16, 2720000, "standard", "640x16 max fps"),
        ]
    },
    {
        "brand": "Photron",
        "model_name": "Pharsighted E9-80S",
        "series": "Pharsighted E9",
        "sensor_size": "33.28x24.96mm",
        "crop_factor": 1.09,
        "bit_depth": 9,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://photron.com/pharsighted-e9/",
        "modes": [
            make_mode(640, 480, 272000, "standard", "Full sensor"),
            make_mode(640, 448, 290000, "standard", "640x448"),
            make_mode(640, 416, 311000, "standard", "640x416"),
            make_mode(640, 384, 336000, "standard", "640x384"),
            make_mode(640, 352, 365000, "standard", "640x352"),
            make_mode(640, 320, 400000, "standard", "640x320"),
            make_mode(640, 288, 441000, "standard", "640x288"),
            make_mode(640, 256, 492000, "standard", "640x256"),
            make_mode(640, 240, 523000, "standard", "640x240"),
            make_mode(640, 224, 557000, "standard", "640x224"),
            make_mode(640, 192, 641000, "standard", "640x192"),
            make_mode(640, 160, 755000, "standard", "640x160"),
            make_mode(640, 128, 918000, "standard", "640x128"),
            make_mode(640, 96, 1172000, "standard", "640x96"),
            make_mode(640, 64, 1619000, "standard", "640x64"),
            make_mode(640, 48, 2000000, "standard", "640x48"),
            make_mode(640, 32, 2457000, "standard", "640x32"),
            make_mode(640, 16, 2457000, "standard", "640x16 max fps"),
        ]
    },
    {
        "brand": "Photron",
        "model_name": "Pharsighted E9-50S",
        "series": "Pharsighted E9",
        "sensor_size": "33.28x24.96mm",
        "crop_factor": 1.09,
        "bit_depth": 9,
        "price_tier": "Purchase (Quote)",
        "status": "Current",
        "data_quality": "verified",
        "source_url": "https://photron.com/pharsighted-e9/",
        "modes": [
            make_mode(640, 480, 164000, "standard", "Full sensor"),
            make_mode(640, 384, 203000, "standard", "640x384"),
            make_mode(640, 320, 242000, "standard", "640x320"),
            make_mode(640, 240, 318000, "standard", "640x240"),
            make_mode(640, 160, 462000, "standard", "640x160"),
            make_mode(640, 128, 565000, "standard", "640x128"),
            make_mode(640, 64, 1014000, "standard", "640x64"),
            make_mode(640, 48, 1267000, "standard", "640x48"),
            make_mode(640, 32, 1685000, "standard", "640x32"),
            make_mode(640, 16, 1980000, "standard", "640x16 max fps"),
        ]
    },
]

# Expanded modes for existing FASTCAM Nova S20 (currently has 2 modes, should have 7)
NOVA_S20_EXPANDED_MODES = [
    make_mode(1024, 1024, 18750, "standard", "Full sensor 10-bit"),
    make_mode(1024, 1024, 16500, "standard", "Full sensor 12-bit"),
    make_mode(1024, 966, 20000, "standard", "1024x966 10-bit"),
    make_mode(1024, 768, 25000, "standard", "1024x768 10-bit"),
    make_mode(512, 512, 62500, "standard", "512x512 10-bit"),
    make_mode(384, 256, 137500, "standard", "384x256 12-bit"),
    make_mode(128, 16, 1100000, "standard", "128x16 max fps"),
]


# ============================================================
# KRON Q12
# (Will be populated when agent 4 returns)
# ============================================================

KRON_NEW = [
    {
        "brand": "Kron Technologies",
        "model": "Chronos Q12",
        "sensor_size_mm": "18.4 x 18.1",
        "sensor_format": "Super35",
        "crop_factor": 1.6,
        "bit_depth": "12",
        "price_tier": "Purchase",
        "price_usd": 19995,
        "status": "Pre-order",
        "source_url": "https://www.krontech.ca/chronos-q12",
        "notes": "Pre-order. Same 11.8 GP/s throughput as 4K12. Sensor caps at 2048x2016.",
        "resolution_fps_modes": [
            {"width": 2048, "height": 2016, "max_fps": 2782, "note": "Max resolution 8-bit"},
            {"width": 1920, "height": 1080, "max_fps": 4900, "note": "HD 8-bit"},
            {"width": 1280, "height": 1024, "max_fps": 3856, "note": "1280x1024 8-bit"},
            {"width": 1280, "height": 720, "max_fps": 5153, "note": "720p 8-bit"},
            {"width": 1280, "height": 96, "max_fps": 20414, "note": "1280x96 8-bit"},
            {"width": 768, "height": 576, "max_fps": 6338, "note": "768x576 8-bit"},
            {"width": 512, "height": 480, "max_fps": 7352, "note": "512x480 8-bit"},
            {"width": 384, "height": 256, "max_fps": 11730, "note": "384x256 8-bit"},
            {"width": 384, "height": 96, "max_fps": 20414, "note": "384x96 8-bit"},
            {"width": 256, "height": 160, "max_fps": 15750, "note": "256x160 8-bit"},
            {"width": 128, "height": 32, "max_fps": 29002, "note": "Min resolution / max fps 8-bit"},
        ]
    },
]


def build_phantom_v2():
    """Create phantom_v2.json with all new Phantom models added."""
    ph = load_json(PHANTOM_V1)
    existing_models = {c["model"] for c in ph["cameras"]}

    added = 0
    for cam in PHANTOM_V_SERIES + PHANTOM_OTHER:
        if cam["model"] not in existing_models:
            ph["cameras"].append(cam)
            existing_models.add(cam["model"])
            added += 1
            print(f"  + Phantom {cam['model']}: {len(cam['modes'])} modes")

    ph["notes"] = ph.get("notes", "") + " v2: Added v-series UHS, VEO, T, Miro, S-series models."
    save_json(PHANTOM_V2, ph)
    return added


def build_ix_v5():
    """Create ix_cameras_v5.json with new models added."""
    ix = load_json(IX_V4)
    existing_models = {c["model"] for c in ix["cameras"]}

    added = 0
    for cam in IX_NEW:
        if cam["model"] not in existing_models:
            ix["cameras"].append(cam)
            existing_models.add(cam["model"])
            added += 1
            print(f"  + iX {cam['model']}: {len(cam['modes'])} modes")

    if added:
        ix["notes"] = ix.get("notes", "") + f" v5: Added {added} new models."
        save_json(IX_V5, ix)
    return added


def build_photron_v4():
    """Create photron_v4.json with new models added."""
    ph = load_json(PHOTRON_V3)
    existing_models = {c.get("model_name", c.get("model", "")) for c in ph["cameras"]}

    added = 0
    for cam in PHOTRON_NEW:
        name = cam.get("model_name", cam.get("model", ""))
        if name not in existing_models:
            ph["cameras"].append(cam)
            existing_models.add(name)
            added += 1
            print(f"  + Photron {name}: {len(cam['modes'])} modes")

    if added:
        save_json(PHOTRON_V4, ph)
    return added


def build_kron_v2():
    """Create kron_chronos_v2.json with Q12 added."""
    kron = load_json(KRON_V1)
    existing_models = {c["model"] for c in kron}

    added = 0
    for cam in KRON_NEW:
        if cam["model"] not in existing_models:
            kron.append(cam)
            added += 1
            print(f"  + Kron {cam['model']}: {len(cam.get('resolution_fps_modes', cam.get('modes', [])))} modes")

    if added:
        save_json(KRON_V2, kron)
    return added


def build_v8():
    """Build overcrank_db_v8.json from v7 + all new verified data."""
    db = load_json(V7)
    cameras = db["cameras"]
    existing_models = {c["model"] for c in cameras}

    # Expand Nova S20 modes
    for cam in cameras:
        if cam["model"] == "FASTCAM Nova S20" and len(cam["modes"]) < len(NOVA_S20_EXPANDED_MODES):
            old = len(cam["modes"])
            cam["modes"] = NOVA_S20_EXPANDED_MODES
            print(f"  FASTCAM Nova S20: {old} -> {len(cam['modes'])} modes")

    # Add new Phantom cameras
    for cam in PHANTOM_V_SERIES + PHANTOM_OTHER:
        if cam["model"] not in existing_models:
            # Normalize to DB format
            entry = {
                "brand": cam["brand"],
                "model": cam["model"],
                "series": cam.get("series", ""),
                "sensor_size": cam.get("sensor_size", ""),
                "crop_factor": cam.get("crop_factor"),
                "bit_depth": cam.get("bit_depth"),
                "price_tier": cam.get("price_tier", "Purchase (Quote)"),
                "price_usd": cam.get("price_usd"),
                "status": cam.get("status", "Current"),
                "data_quality": "verified",
                "source_url": cam.get("source_url", ""),
                "modes": cam["modes"]
            }
            cameras.append(entry)
            existing_models.add(cam["model"])

    # Add new iX cameras
    for cam in IX_NEW:
        if cam["model"] not in existing_models:
            entry = {
                "brand": cam["brand"],
                "model": cam["model"],
                "series": cam.get("series", ""),
                "sensor_size": cam.get("sensor_size", ""),
                "crop_factor": cam.get("crop_factor"),
                "bit_depth": cam.get("bit_depth"),
                "price_tier": cam.get("price_tier", "Purchase (Quote)"),
                "price_usd": cam.get("price_usd"),
                "status": cam.get("status", "Current"),
                "data_quality": "verified",
                "source_url": cam.get("source_url", ""),
                "modes": cam["modes"]
            }
            cameras.append(entry)
            existing_models.add(cam["model"])

    # Add new Photron cameras
    for cam in PHOTRON_NEW:
        name = cam.get("model_name", cam.get("model", ""))
        if name not in existing_models:
            entry = {
                "brand": cam.get("brand", "Photron"),
                "model": name,
                "series": cam.get("series", ""),
                "sensor_size": cam.get("sensor_size", ""),
                "crop_factor": cam.get("crop_factor"),
                "bit_depth": cam.get("bit_depth"),
                "price_tier": cam.get("price_tier", "Purchase (Quote)"),
                "price_usd": cam.get("price_usd"),
                "status": cam.get("status", "Current"),
                "data_quality": "verified",
                "source_url": cam.get("source_url", ""),
                "modes": cam["modes"]
            }
            cameras.append(entry)
            existing_models.add(name)

    # Add new Kron cameras
    for cam in KRON_NEW:
        if cam["model"] not in existing_models:
            # Kron uses resolution_fps_modes format, convert to modes
            modes = []
            for m in cam.get("resolution_fps_modes", cam.get("modes", [])):
                modes.append(make_mode(
                    m.get("width", m.get("res_width")),
                    m.get("height", m.get("res_height")),
                    m.get("max_fps"),
                    "standard",
                    m.get("note", f"{m.get('width', m.get('res_width'))}x{m.get('height', m.get('res_height'))}")
                ))
            entry = {
                "brand": cam["brand"],
                "model": cam["model"],
                "series": cam.get("series", ""),
                "sensor_size": cam.get("sensor_size", cam.get("sensor_size_mm", "")),
                "crop_factor": cam.get("crop_factor"),
                "bit_depth": cam.get("bit_depth"),
                "price_tier": cam.get("price_tier", "Purchase"),
                "price_usd": cam.get("price_usd"),
                "status": cam.get("status", "Current"),
                "data_quality": "verified",
                "source_url": cam.get("source_url", ""),
                "modes": modes
            }
            cameras.append(entry)
            existing_models.add(cam["model"])

    # Build output
    total_modes = sum(len(c["modes"]) for c in cameras)
    manufacturers = sorted(set(c["brand"] for c in cameras))

    output = {
        "version": 8,
        "generated": datetime.now(timezone.utc).isoformat(),
        "camera_count": len(cameras),
        "total_modes": total_modes,
        "manufacturers_included": manufacturers,
        "cameras": cameras
    }

    save_json(V8, output)

    print(f"\nBuilt overcrank_db_v8.json")
    print(f"  Cameras: {len(cameras)} (v7 had {db['camera_count']})")
    print(f"  Modes: {total_modes} (v7 had {db['total_modes']})")
    print(f"  Manufacturers ({len(manufacturers)}): {', '.join(manufacturers)}")

    brand_counts = Counter(c["brand"] for c in cameras)
    print(f"\nBy brand:")
    for b in sorted(brand_counts):
        count = brand_counts[b]
        modes = sum(len(c["modes"]) for c in cameras if c["brand"] == b)
        print(f"  {b}: {count} cameras, {modes} modes")

    quality_counts = Counter(c.get("data_quality", "?") for c in cameras)
    print(f"\nData quality: {dict(quality_counts)}")


if __name__ == "__main__":
    print("Adding missing camera models...\n")

    print("Phantom v-series UHS:")
    ph_added = build_phantom_v2()
    print(f"  Total added: {ph_added}\n")

    if IX_NEW:
        print("iX Cameras:")
        ix_added = build_ix_v5()
        print(f"  Total added: {ix_added}\n")

    if PHOTRON_NEW:
        print("Photron:")
        ph_added = build_photron_v4()
        print(f"  Total added: {ph_added}\n")

    if KRON_NEW:
        print("Kron Technologies:")
        kr_added = build_kron_v2()
        print(f"  Total added: {kr_added}\n")

    print("\nBuilding v8 database...")
    build_v8()
