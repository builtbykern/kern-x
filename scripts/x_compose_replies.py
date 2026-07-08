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


def _slim_candidates(candidates: list[dict], max_text: int = 200) -> list[dict]:
    """Trim tweet text to save tokens — the LLM only needs enough context to write a reply."""
    out = []
    for c in candidates:
        slim = {"h": c.get("handle", ""), "u": c.get("post_url") or c.get("url", "")}
        text = (c.get("text") or "")[:max_text]
        if text:
            slim["t"] = text
            slim["tone"] = _tone_hint(text)
        out.append(slim)
    return out


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
        "out": f'{{"replies":[{{"handle","post_url","reply_text"}}]}} max {max_replies}. English.',
    }
    resp = client.chat.completions.create(
        model=model,
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Write 1-sentence X replies for @builtbykern. Sound like a friend in a group chat, not a content creator. Follow the voice rules word for word. JSON only, no markdown.",
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


def compose_cursor(
    candidates: list[dict], voice: str, today: dict, max_replies: int, ctx: dict
) -> list[dict]:
    root = ROOT
    slim = _slim_candidates(candidates[:max_replies])
    prompt = (
        f"JSON array, max {max_replies}: handle, post_url, reply_text. 1 sentence.\n"
        f"Voice:\n{voice}\nCtx:\n{json.dumps(ctx)}\nCandidates:\n{json.dumps(slim)}"
    )
    prompt_path = root / "state" / ".compose-prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    script = root / "scripts" / "x_compose_cursor.mjs"
    env = {**os.environ, "KERN_X_ROOT": str(root), "CURSOR_API_KEY": os.environ["CURSOR_API_KEY"]}
    try:
        text = subprocess.check_output(
            ["node", str(script), str(prompt_path)],
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
    items = json.loads(text)
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
    if backend == "openai":
        items = compose_openai(candidates, voice, today, args.max, ctx)
    elif backend == "cursor":
        items = compose_cursor(candidates, voice, today, args.max, ctx)
    else:
        print("Set CURSOR_API_KEY or OPENAI_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()
