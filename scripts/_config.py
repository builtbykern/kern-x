"""Load kern-x config (default + optional local.json)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
STATE_DIR = ROOT / "state"
LOGS_DIR = ROOT / "logs"


def load_config() -> dict:
    cfg: dict = {}
    default_path = CONFIG_DIR / "default.json"
    if default_path.is_file():
        cfg.update(json.loads(default_path.read_text(encoding="utf-8")))
    local_path = CONFIG_DIR / "local.json"
    if local_path.is_file():
        cfg.update(json.loads(local_path.read_text(encoding="utf-8")))
    listings = cfg.get("listings_dir", "")
    if listings:
        p = Path(listings)
        if not p.is_absolute():
            p = (ROOT / p).resolve()
        cfg["listings_dir"] = str(p)
    return cfg
