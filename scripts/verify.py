#!/usr/bin/env python3
"""
Overcrank DB Verification Script
Fetches each camera's source_url, extracts key specs, diffs against db.
Writes data/discrepancy_log.json.

Usage:
  python3 scripts/verify.py                 # verify all
  python3 scripts/verify.py --brand IDT     # one brand
  python3 scripts/verify.py --dry-run       # print plan, don't fetch
"""

import json, re, sys, argparse
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "overcrank_db_v9.json"
LOG_PATH = ROOT / "data" / "discrepancy_log.json"

# ──────────────────────────────────────────────
# Extractors — one per manufacturer domain
# Each returns a list of dicts: {model, max_fps, res_width, res_height}
# ──────────────────────────────────────────────

def extract_idt(page_text, url):
    """IDT pages embed FAQ schema JSON with structured specs."""
    results = []
    schemas = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', page_text, re.DOTALL)
    for schema_str in schemas:
        try:
            schema = json.loads(schema_str)
        except:
            continue
        if schema.get('@type') != 'FAQPage':
            continue
        for item in schema.get('mainEntity', []):
            model_name = item.get('name', '')
            answer = item.get('acceptedAnswer', {}).get('text', '')
            # Unescape HTML entities and slashes
            answer = answer.replace('\\/', '/').replace('&amp;', '&')
            # Match fps — may be formatted with comma (e.g. "3,675 fps")
            fps_match = re.search(r'([\d,]+)\s*fps', answer, re.IGNORECASE)
            # Match resolution — "3200 x 2560" or "3200 x 2560"
            res_match = re.search(r'(\d{3,5})\s*[x×]\s*(\d{3,5})', answer)
            if fps_match and res_match:
                results.append({
                    'model': model_name,
                    'max_fps': int(fps_match.group(1).replace(',', '')),
                    'res_width': int(res_match.group(1)),
                    'res_height': int(res_match.group(2)),
                })
    return results


def extract_generic(page_text, url):
    """
    Generic: pull all res×fps pairs from visible text.
    Returns list of {res_width, res_height, max_fps} — no model names.
    """
    results = []
    # Match patterns like "1920 x 1080 @ 20,000 fps" or "1920×1080 20000fps"
    patterns = [
        r'(\d{3,5})\s*[x×\u0445]\s*(\d{3,5})\s*[@at/]*\s*([\d,\u202f]+)\s*fps',
        r'([\d,\u202f]+)\s*fps\s*@?\s*(\d{3,5})\s*[x×\u0445]\s*(\d{3,5})',
    ]
    for pat in patterns:
        for m in re.finditer(pat, page_text, re.IGNORECASE):
            g = m.groups()
            if len(g) == 3:
                try:
                    clean = lambda s: s.replace(',','').replace('\u202f','').replace('\xa0','')
                    if pat.startswith(r'(\d{3,5})'):
                        w, h, fps = int(g[0]), int(g[1]), int(clean(g[2]))
                    else:
                        fps, w, h = int(clean(g[0])), int(g[1]), int(g[2])
                    results.append({'res_width': w, 'res_height': h, 'max_fps': fps})
                except:
                    pass
    return results


def expand_k(text):
    """Expand shorthand like 8K×4K to pixel numbers."""
    K = {'8k': 8192, '6k': 6000, '4k': 4096, '3k': 3000, '2k': 2048,
         '5k': 5120, '1k': 1024, 'uhd': 3840, 'hd': 1920, 'fhd': 1920}
    def repl(m):
        a, b = m.group(1).lower(), m.group(2).lower()
        wa, ha = K.get(a), K.get(b)
        if wa and ha:
            return f"{wa} x {ha}"
        return m.group(0)
    return re.sub(r'(\d[Kk]|UHD|FHD|HD)\s*[x×\u0445]\s*(\d[Kk]|UHD|FHD|HD)', repl, text, flags=re.IGNORECASE)


def extract_idt_full(page_text, url):
    """IDT: FAQ schema first, then generic text fallback for sub-modes."""
    results = extract_idt(page_text, url)
    # Expand shorthand (8K×4K) before generic extraction
    expanded = expand_k(page_text)
    results += extract_generic(expanded, url)
    # Deduplicate
    seen = set()
    deduped = []
    for r in results:
        key = (r['res_width'], r['res_height'], r['max_fps'])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped

EXTRACTORS = {
    'idtcameras.com': extract_idt_full,
    'phantomhighspeed.com': extract_generic,
    'edgertronic.com': extract_generic,
    'freeflysystems.com': extract_generic,
    'krontech.ca': extract_generic,
    'ix-cameras.com': extract_generic,
    'photron.com': extract_generic,
}

def get_extractor(url):
    for domain, fn in EXTRACTORS.items():
        if domain in url:
            return fn
    return extract_generic


# ──────────────────────────────────────────────
# Fetch with Playwright
# ──────────────────────────────────────────────

def fetch_page(url):
    """Returns (page_text, final_url, error). Uses Playwright headless Chromium."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, url, "playwright not installed"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            text = page.content()
            final_url = page.url
            browser.close()
            return text, final_url, None
    except Exception as e:
        return None, url, str(e)


# ──────────────────────────────────────────────
# Comparison logic
# ──────────────────────────────────────────────

def compare_camera(camera, extracted, final_url):
    """
    Compare a DB camera entry against what was found on the page.
    Returns list of issue dicts.
    """
    issues = []
    brand  = camera['brand']
    model  = camera['model']

    # Skip modes that aren't in the manufacturer's main spec table
    SKIP_TYPES = {'sample_footage', 'speed_booster', 'min_res'}

    for mode in camera.get('modes', []):
        if mode.get('mode_type') in SKIP_TYPES:
            continue
        w   = mode['res_width']
        h   = mode['res_height']
        fps = mode['max_fps']

        # Look for this exact fps value anywhere in extracted data
        fps_found = any(abs(e['max_fps'] - fps) / max(fps, 1) < 0.05  # 5% tolerance
                        for e in extracted)

        # Look for this resolution anywhere in extracted data
        res_found = any(e['res_width'] == w and e['res_height'] == h
                        for e in extracted)

        if not fps_found and not res_found:
            issues.append({
                'severity': 'warning',
                'type': 'mode_not_found',
                'brand': brand,
                'model': model,
                'expected': f"{w}×{h} @ {fps:,} fps",
                'detail': 'Neither resolution nor fps found on page',
                'source_url': final_url,
            })
        elif not fps_found:
            issues.append({
                'severity': 'warning',
                'type': 'fps_not_found',
                'brand': brand,
                'model': model,
                'expected': f"{fps:,} fps",
                'detail': f'Resolution {w}×{h} found but fps {fps:,} not present on page',
                'source_url': final_url,
            })

    return issues


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--brand', help='Only verify this brand')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    with open(DB_PATH) as f:
        db = json.load(f)

    cameras = [c for c in db['cameras'] if c.get('data_quality') == 'verified']
    if args.brand:
        cameras = [c for c in cameras if c['brand'].lower() == args.brand.lower()]

    # Group cameras by source_url to avoid re-fetching same page
    by_url = defaultdict(list)
    for cam in cameras:
        url = cam.get('source_url') or cam.get('source_base_url')
        if url:
            by_url[url].append(cam)

    print(f"Verifying {len(cameras)} cameras across {len(by_url)} unique URLs")
    print()

    if args.dry_run:
        for url, cams in by_url.items():
            print(f"  {url}")
            for c in cams:
                print(f"    {c['brand']} {c['model']}")
        return

    all_issues = []
    url_results = {}  # url -> {status, extracted_count, final_url}

    for url, cams in by_url.items():
        print(f"Fetching: {url}")
        page_text, final_url, error = fetch_page(url)

        if error or not page_text:
            print(f"  ERROR: {error}")
            for cam in cams:
                all_issues.append({
                    'severity': 'error',
                    'type': 'fetch_failed',
                    'brand': cam['brand'],
                    'model': cam['model'],
                    'detail': error or 'Empty response',
                    'source_url': url,
                })
            url_results[url] = {'status': 'error', 'error': error}
            continue

        # Detect redirect to different domain
        if final_url != url:
            print(f"  Redirected to: {final_url}")

        extractor = get_extractor(final_url)
        extracted = extractor(page_text, final_url)
        print(f"  Extracted {len(extracted)} spec entries  ({extractor.__name__})")

        url_results[url] = {
            'status': 'ok',
            'final_url': final_url,
            'extracted_count': len(extracted),
        }

        for cam in cams:
            issues = compare_camera(cam, extracted, final_url)
            if issues:
                for iss in issues:
                    print(f"  ⚠  {cam['brand']} {cam['model']}: {iss['type']} — {iss['detail']}")
            else:
                print(f"  ✓  {cam['brand']} {cam['model']}")
            all_issues.extend(issues)

        print()

    # Write log
    log = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'db_version': db.get('version'),
        'cameras_checked': len(cameras),
        'urls_checked': len(by_url),
        'issues_found': len(all_issues),
        'summary': {
            'errors': sum(1 for i in all_issues if i['severity'] == 'error'),
            'warnings': sum(1 for i in all_issues if i['severity'] == 'warning'),
            'ok': len(cameras) - len({(i['brand'], i['model']) for i in all_issues}),
        },
        'issues': all_issues,
        'url_results': url_results,
    }

    with open(LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)

    print(f"{'='*50}")
    print(f"  Cameras checked : {len(cameras)}")
    print(f"  Issues found    : {len(all_issues)}")
    print(f"  Errors          : {log['summary']['errors']}")
    print(f"  Warnings        : {log['summary']['warnings']}")
    print(f"  Log written to  : {LOG_PATH.relative_to(ROOT)}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
