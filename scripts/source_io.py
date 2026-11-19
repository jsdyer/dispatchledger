"""Fetch publisher resources and replace a complete, validated edition atomically."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "web/data/edition.json"


def fetch(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (CoolCode public data refresh)"})
    with urlopen(request, timeout=100) as response:
        return response.read()


def publish(edition):
    edition["count"] = sum(len(rows) for rows in edition["districts"].values())
    edition["retrieved"] = datetime.now(timezone.utc).date().isoformat()
    output = EDITION.with_suffix(".tmp")
    output.write_text(json.dumps(edition, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    output.replace(EDITION)
