#!/usr/bin/env python3
"""Compose 1-3 English replies from candidates + voice (OPENAI_API_KEY or CURSOR_API_KEY)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_referral_urls() -> dict[str, str]:
    sys.path.insert(0, str(ROOT / "scripts"))
    from _config import referral_urls

    return referral_urls()


_NEG_HINTS = (
    "slow week", "zero dollar", "no sales", "didn't sell", "rejected", "rejection",
    "behind on", "struggling", "burnout", "hard week", "silence", "nerve-wracking",
    "hardest", "slump", "lost ", "failed", "not selling",
)


def _tone_hint(text: str) -> str:
    lower = (text or "").lower()
    if any(h in lower for h in _NEG_HINTS):
        return "empathy"
    return "neutral"


def compose_context(today: dict) -> dict:
    slim = {k: v for k, v in today.items() if k in ("component", "link", "theme")} if today else {}
    refs = {k: v for k, v in load_referral_urls().items() if v}
    return {"today": slim, "refs": refs, "ref_max": 1}


def _slim_candidates(candidates: list[dict], max_text: int = 280) -> list[dict]:
    """Trim tweet text to save tokens — keep enough for one concrete detail."""
    out = []
    for c in candidates:
        slim = {"h": c.get("handle", ""), "u": c.get("post_url") or c.get("url", "")}
        text = (c.get("text") or "")[:max_text]
        if text:
            slim["t"] = text
            slim["tone"] = _tone_hint(text)
        out.append(slim)
    return out


def _recent_reply_texts(limit: int = 12) -> list[str]:
    """Last reply lines — avoid repeating the same robot cadence."""
    path = ROOT / "logs" / "replies.json"
    support = (
        Path.home()
        / "Library"
        / "Application Support"
        / "builtbykern-kern-x"
        / "runtime"
        / "logs"
        / "replies.json"
    )
    for p in (support, path):
        if not p.is_file():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        out: list[str] = []
        for e in reversed(data.get("entries") or []):
            if e.get("is_followup"):
                continue
            t = (e.get("reply_text") or "").strip()
            if t:
                out.append(t)
            if len(out) >= limit:
                break
        return out
    return []


def _compose_instructions(max_replies: int) -> str:
    return (
        f"Write up to {max_replies} replies for @builtbykern. "
        "Each reply_text: ONE short lowercase sentence. Cool mood only — never critical or pedantic. "
        "Plain > clever. React like a chill friend who skimmed the post. "
        "Never dunk, lecture, judge quality, or sound smarter than the author. "
        "Never restate or paraphrase their tweet — react, don't summarize. "
        "Never label-speak (product name + category). Never 'X as a Y' captions. "
        "Never try-hard specifics (rankings, caption meta, scraped-sounding numbers). "
        "No twin structure across replies in this batch. "
        "Do not echo recent_replies phrasing. "
        'JSON only: {"replies":[{"handle","post_url","reply_text"}]}'
    )


def compose_openai(
    candidates: list[dict], voice: str, today: dict, max_replies: int, ctx: dict
) -> list[dict]:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("X_COMPOSE_MODEL", "gpt-4o-mini")
    slim = _slim_candidates(candidates[:max_replies])
    payload = {
        "c": slim,
        "ctx": ctx,
        "v": voice,
        "recent_replies": _recent_reply_texts(),
        "out": _compose_instructions(max_replies),
    }
    resp = client.chat.completions.create(
        model=model,
        temperature=0.55,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You write plain, chill X replies — cool mood only, never critical or pedantic. "
                    "Follow voice rules exactly. Simple friendly reactions. JSON only, no markdown."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(payload),
            },
        ],
    )
    raw = resp.choices[0].message.content or "{}"
    data = json.loads(raw)
    items = data.get("replies") or data.get("items") or data
    if isinstance(items, dict):
        items = items.get("replies", [])
    if not isinstance(items, list):
        raise ValueError("unexpected compose shape")
    out = []
    for item in items[:max_replies]:
        out.append(
            {
                "handle": item["handle"],
                "post_url": item["post_url"],
                "reply_text": item["reply_text"].strip(),
            }
        )
    return out


def resolve_node_bin() -> str:
    """Find node even under launchd (minimal PATH)."""
    candidates = [
        os.environ.get("NODE_BIN", "").strip(),
        "node",
        str(Path.home() / ".local" / "bin" / "node"),
        "/opt/homebrew/bin/node",
        "/usr/local/bin/node",
    ]
    for c in candidates:
        if not c:
            continue
        if c == "node":
            from shutil import which

            found = which("node")
            if found:
                return found
            continue
        if Path(c).is_file() and os.access(c, os.X_OK):
            return c
    raise FileNotFoundError("node binary not found")


def compose_cursor(
    candidates: list[dict], voice: str, today: dict, max_replies: int, ctx: dict
) -> list[dict]:
    root = ROOT
    slim = _slim_candidates(candidates[:max_replies])
    recent = _recent_reply_texts()
    prompt = (
        f"{_compose_instructions(max_replies)}\n"
        "Return a JSON array of objects (not wrapped), fields: handle, post_url, reply_text.\n"
        f"Voice:\n{voice}\n"
        f"Ctx:\n{json.dumps(ctx)}\n"
        f"Avoid repeating these recent_replies (same cadence/phrases):\n{json.dumps(recent)}\n"
        f"Candidates:\n{json.dumps(slim)}"
    )
    prompt_path = root / "state" / ".compose-prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    script = root / "scripts" / "x_compose_cursor.mjs"
    env = {**os.environ, "KERN_X_ROOT": str(root), "CURSOR_API_KEY": os.environ["CURSOR_API_KEY"]}
    # Ensure node deps resolve when cwd is Application Support mirror
    node_path = env.get("PATH", "")
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin not in node_path.split(":"):
        env["PATH"] = f"{local_bin}:{node_path}" if node_path else local_bin
    try:
        node = resolve_node_bin()
        text = subprocess.check_output(
            [node, str(script), str(prompt_path)],
            cwd=root,
            env=env,
            text=True,
            timeout=300,
        ).strip()
    except FileNotFoundError as e:
        raise SystemExit("node not found — install Node.js for CURSOR_API_KEY compose") from e
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"cursor compose failed: {e.stderr or e}") from e
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    if not text:
        raise ValueError("cursor compose returned empty stdout")
    try:
        items = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"cursor compose invalid JSON: {text[:200]!r}") from e
    if not isinstance(items, list):
        # Some models wrap as {"replies":[...]}
        if isinstance(items, dict) and isinstance(items.get("replies"), list):
            items = items["replies"]
        else:
            raise ValueError(f"cursor compose expected list, got {type(items).__name__}")
    return items[:max_replies]


def _is_cursor_key(value: str) -> bool:
    v = value.strip().lower()
    return v.startswith("cursor_") or v.startswith("crsr_")


def resolve_compose_backend() -> str | None:
    openai_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    cursor_key = (os.environ.get("CURSOR_API_KEY") or "").strip()
    if cursor_key:
        return "cursor"
    if openai_key and _is_cursor_key(openai_key):
        os.environ["CURSOR_API_KEY"] = openai_key
        return "cursor"
    if openai_key:
        return "openai"
    return None


def main() -> None:
    from x_playwright import load_dotenv

    load_dotenv()

    p = argparse.ArgumentParser()
    p.add_argument("--candidates", required=True, help="JSON file path")
    p.add_argument("--voice-file", required=True)
    p.add_argument("--today-json", default="{}")
    p.add_argument("--max", type=int, default=3)
    args = p.parse_args()

    candidates = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    voice = Path(args.voice_file).read_text(encoding="utf-8").strip()
    today = json.loads(args.today_json)
    ctx = compose_context(today)

    backend = resolve_compose_backend()
    items: list[dict] = []
    if backend == "openai":
        items = compose_openai(candidates, voice, today, args.max, ctx)
    elif backend == "cursor":
        try:
            items = compose_cursor(candidates, voice, today, args.max, ctx)
            if not isinstance(items, list) or not items:
                raise ValueError("cursor compose returned empty")
        except Exception as e:
            # Fall back to OpenAI when Cursor SDK returns empty/invalid JSON
            openai_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
            if openai_key and not _is_cursor_key(openai_key):
                print(f"cursor compose failed ({e}); falling back to openai", file=sys.stderr)
                items = compose_openai(candidates, voice, today, args.max, ctx)
            else:
                raise
    else:
        print("Set CURSOR_API_KEY or OPENAI_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()
