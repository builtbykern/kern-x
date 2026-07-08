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


def referral_urls(cfg: dict | None = None) -> dict[str, str]:
    """Allowed affiliate URLs for reply compose (from config)."""
    c = cfg or load_config()
    return {
        "cursor": str(c.get("cursor_referral_url") or "").strip(),
        "framer": str(c.get("framer_referral_url") or "").strip(),
    }


def cursor_referral_url(cfg: dict | None = None) -> str:
    return referral_urls(cfg)["cursor"]


def text_has_referral_link(text: str) -> bool:
    t = (text or "").lower()
    return any(
        m in t
        for m in (
            "cursor.com/referral",
            "framer.link/builtbykern",
            "framer.link/",
        )
    )


def referral_markers_in_text(text: str, cfg: dict | None = None) -> list[str]:
    """Return which referral types appear in text (for logging/caps)."""
    t = (text or "").lower()
    found: list[str] = []
    if "cursor.com/referral" in t or "whbu5crp1xkf" in t:
        found.append("cursor")
    if "framer.link" in t:
        found.append("framer")
    return found
