#!/usr/bin/env node
/** One-shot compose via Cursor SDK (Node). Reads prompt path from argv[2]. */
import { readFileSync } from "fs";
import { Agent } from "@cursor/sdk";

const promptPath = process.argv[2];
if (!promptPath) {
  console.error("usage: node x_compose_cursor.mjs <prompt.txt>");
  process.exit(1);
}

const apiKey = process.env.CURSOR_API_KEY?.trim();
if (!apiKey) {
  console.error("CURSOR_API_KEY not set");
  process.exit(1);
}

const prompt = readFileSync(promptPath, "utf8");
const cwd = process.env.KERN_X_ROOT || process.cwd();
const modelId = process.env.X_COMPOSE_MODEL || "gemini-3.5-flash";

const result = await Agent.prompt(prompt, {
  apiKey,
  model: { id: modelId },
  local: { cwd },
});

const text = (result.result ?? "").trim();
process.stdout.write(text);
