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
const modelId = process.env.X_COMPOSE_MODEL || "default";

let result;
try {
  result = await Agent.prompt(prompt, {
    apiKey,
    model: { id: modelId },
    // LaunchAgent / headless hosts often lack Cursor sandbox support
    local: { cwd, sandboxOptions: { enabled: false } },
  });
} catch (err) {
  console.error(String(err?.stack || err));
  process.exit(1);
}

const text = (result.result ?? "").trim();
if (!text) {
  console.error("cursor compose empty result:", JSON.stringify(result).slice(0, 500));
  process.exit(1);
}
// Strip accidental markdown fences so Python json.loads succeeds
let out = text;
if (out.startsWith("```")) {
  out = out.split("\n").slice(1).join("\n").replace(/```\s*$/, "").trim();
}
process.stdout.write(out);
