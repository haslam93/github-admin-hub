#!/usr/bin/env python3
"""Weekly changelog watcher.

Fetches the GitHub Blog changelog RSS feeds, filters entries relevant to
enterprise administration (cost centers, billing, budgets, Copilot seats,
enterprise teams, premium requests, admin settings), merges them into
data/changelog.json, and regenerates the changelog section of README.md.

Stdlib only - no dependencies required.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "changelog.json"
README = ROOT / "README.md"

FEEDS = [
    "https://github.blog/changelog/feed/",
    "https://github.blog/changelog/label/copilot/feed/",
    "https://github.blog/changelog/label/enterprise/feed/",
]

KEYWORDS = [
    "cost center", "cost centers", "billing", "budget", "budgets",
    "premium request", "premium requests", "ai credit", "included usage",
    "usage cap", "copilot seat", "copilot license", "copilot business",
    "copilot enterprise", "enterprise team", "enterprise teams",
    "enterprise account", "enterprise owner", "billing manager",
    "organization role", "org role", "seat assignment", "metered",
    "usage report", "spending limit", "agent hq", "copilot policy",
    "copilot policies", "enterprise managed user", "emu",
]

MARK_START = "<!-- CHANGELOG:START -->"
MARK_END = "<!-- CHANGELOG:END -->"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "admin-hub-changelog-watcher"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def parse_feed(xml_text: str) -> list[dict]:
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = strip_html(item.findtext("description") or "")
        pub = (item.findtext("pubDate") or "").strip()
        try:
            date = parsedate_to_datetime(pub).astimezone(timezone.utc).date().isoformat()
        except Exception:
            date = ""
        cats = [c.text.strip() for c in item.findall("category") if c.text]
        items.append({
            "title": title,
            "url": link,
            "date": date,
            "summary": desc[:400],
            "labels": cats,
        })
    return items


def is_relevant(entry: dict) -> bool:
    haystack = " ".join([entry["title"], entry["summary"], " ".join(entry["labels"])]).lower()
    return any(kw in haystack for kw in KEYWORDS)


def main() -> int:
    existing = {"updated": "", "entries": []}
    if DATA_FILE.exists():
        existing = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    by_url = {e["url"]: e for e in existing.get("entries", [])}
    new_count = 0

    for feed in FEEDS:
        try:
            xml_text = fetch(feed)
        except Exception as exc:  # noqa: BLE001
            print(f"WARN: could not fetch {feed}: {exc}", file=sys.stderr)
            continue
        for entry in parse_feed(xml_text):
            if not entry["url"] or not is_relevant(entry):
                continue
            if entry["url"] not in by_url:
                new_count += 1
            by_url[entry["url"]] = entry

    entries = sorted(by_url.values(), key=lambda e: e["date"], reverse=True)
    payload = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entries": entries,
    }
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"changelog.json: {len(entries)} entries ({new_count} new)")

    # Regenerate README changelog section
    if README.exists():
        readme = README.read_text(encoding="utf-8")
        if MARK_START in readme and MARK_END in readme:
            lines = ["", f"_Last checked: {payload['updated']} (auto-updated weekly)_", ""]
            for e in entries[:20]:
                labels = f" `{'` `'.join(e['labels'][:3])}`" if e["labels"] else ""
                lines.append(f"- **{e['date']}** — [{e['title']}]({e['url']}){labels}")
            block = MARK_START + "\n" + "\n".join(lines) + "\n" + MARK_END
            readme = re.sub(
                re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
                block.replace("\\", "\\\\"),
                readme,
                flags=re.DOTALL,
            )
            README.write_text(readme, encoding="utf-8")
            print("README.md changelog section updated")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
