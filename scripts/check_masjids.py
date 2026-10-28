#!/usr/bin/env python3
"""Checks masjids.json before the Sujuda app can download it.

The app applies the same rules (MasjidDirectoryService.validate) and ignores
a list that breaks them, keeping its last good copy - this check makes the
problem visible on GitHub straight away instead.

Usage: python3 scripts/check_masjids.py masjids.json
"""
import json
import re
import sys

URL_FIELDS = ("website", "prayerTimeSourceUrl", "prayerTimesUrl", "prayerTimeApiUrl")


def check(data):
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("masjids"), list):
        return ['The file must be an object with a "masjids" list.']
    if not data["masjids"]:
        return ['The "masjids" list is empty.']
    seen = set()
    for i, m in enumerate(data["masjids"], 1):
        where = f'Entry {i} ({m.get("id", "no id") if isinstance(m, dict) else "?"})'
        if not isinstance(m, dict):
            errors.append(f"{where}: must be an object.")
            continue
        mid = m.get("id")
        if not isinstance(mid, str) or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", mid):
            errors.append(f'{where}: "id" must be lowercase letters, digits and dashes, e.g. "masjid-al-jannah".')
        elif mid in seen:
            errors.append(f'{where}: "id" is used twice.')
        seen.add(mid)
        if not isinstance(m.get("name"), str) or not m["name"].strip():
            errors.append(f'{where}: "name" is missing.')
        lat, lon = m.get("latitude"), m.get("longitude")
        if not isinstance(lat, (int, float)) or isinstance(lat, bool) or not -90 <= lat <= 90:
            errors.append(f'{where}: "latitude" must be a number between -90 and 90.')
        if not isinstance(lon, (int, float)) or isinstance(lon, bool) or not -180 <= lon <= 180:
            errors.append(f'{where}: "longitude" must be a number between -180 and 180.')
        for field in URL_FIELDS:
            v = m.get(field)
            if v is not None and (not isinstance(v, str) or not re.match(r"https?://[^\s/]+\.[^\s]+$", v)):
                errors.append(f'{where}: "{field}" must be a full link starting with https:// (or null).')
        for field in ("verified", "coordinatesApproximate"):
            if field in m and not isinstance(m[field], bool):
                errors.append(f'{where}: "{field}" must be true or false.')
        if m.get("prayerTimesSelector") and not m.get("prayerTimeSourceUrl"):
            errors.append(f'{where}: "prayerTimesSelector" needs "prayerTimeSourceUrl" (the page it is on).')
    return errors


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "masjids.json"
    try:
        data = json.load(open(path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"::error file={path},line={e.lineno}::Not valid JSON: {e.msg} (line {e.lineno}, column {e.colno}). "
              "Check for a missing comma or quote.")
        sys.exit(1)
    problems = check(data)
    for p in problems:
        print(f"::error file={path}::{p}")
    if problems:
        sys.exit(1)
    print(f"OK: {len(data['masjids'])} masjids.")
