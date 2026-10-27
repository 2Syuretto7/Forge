// Browser call to the Anthropic Messages API with the learner's own key.
import { CONCEPT_CRITERIA, DESIGN_CRITERIA, DESIGN_SYSTEM_PROMPT, SYSTEM_PROMPT, userContent } from './prompt';

export const API_URL = 'https://api.anthropic.com/v1/messages';
export const MAX_TOKENS = 1200;

export interface GradeResult {
  scores: Record<string, number>;
  gaps: string[];
  followUp: string;
  total: number;
}

export type GradeOutcome = { ok: true; result: GradeResult } | { ok: false; error: string; raw?: string };

interface ApiResponse {
  content?: { type: string; text?: string }[];
  stop_reason?: string;
  error?: { message?: string };
}

function headers(apiKey: string) {
  return {
    'content-type': 'application/json',
    'x-api-key': apiKey,
    'anthropic-version': '2023-06-01',
    'anthropic-dangerous-direct-browser-access': 'true',
  };
}

async function call(apiKey: string, model: string, system: string, content: string, maxTokens: number) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: headers(apiKey),
    body: JSON.stringify({
      model,
      max_tokens: maxTokens,
      system,
      // Keep thinking short so the JSON fits in the token budget.
      output_config: { effort: 'low' },
      messages: [{ role: 'user', content }],
    }),
  });
  const body = (await res.json().catch(() => ({}))) as ApiResponse;
  if (!res.ok) throw new Error(body.error?.message ?? `HTTP ${res.status}`);
  const text = (body.content ?? [])
    .filter((b) => b.type === 'text')
    .map((b) => b.text ?? '')
    .join('');
  return { text, stop: body.stop_reason ?? '' };
}

// Pulls the first JSON object out of the reply and checks its shape.
export function parseGrade(text: string, keys: string[]): GradeResult | null {
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start < 0 || end <= start) return null;
  let obj: unknown;
  try {
    obj = JSON.parse(text.slice(start, end + 1));
  } catch {
    return null;
  }
  const o = obj as { scores?: Record<string, unknown>; gaps?: unknown; follow_up?: unknown };
  if (!o.scores || typeof o.scores !== 'object') return null;
  const scores: Record<string, number> = {};
  for (const k of keys) {
    const v = Number(o.scores[k]);
    if (!Number.isFinite(v)) return null;
    scores[k] = Math.max(0, Math.min(4, Math.round(v)));
  }
  const gaps = Array.isArray(o.gaps) ? o.gaps.map(String) : [];
  const followUp = typeof o.follow_up === 'string' ? o.follow_up : '';
  return { scores, gaps, followUp, total: Object.values(scores).reduce((a, b) => a + b, 0) };
}

export async function gradeExplanation(opts: {
  apiKey: string;
  model: string;
  rubric: 'concept' | 'design';
  lessonTitle: string;
  prompt: string;
  keyPoints: string[];
  text: string;
}): Promise<GradeOutcome> {
  const system = opts.rubric === 'design' ? DESIGN_SYSTEM_PROMPT : SYSTEM_PROMPT;
  const keys = (opts.rubric === 'design' ? DESIGN_CRITERIA : CONCEPT_CRITERIA).map((c) => c.key);
  const content = userContent(opts.lessonTitle, opts.prompt, opts.keyPoints, opts.text);
  let raw = '';
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const { text, stop } = await call(opts.apiKey, opts.model, system, content, attempt === 0 ? MAX_TOKENS : MAX_TOKENS * 3);
      raw = text;
      if (stop === 'refusal') return { ok: false, error: 'The model declined to grade this text.', raw };
      const parsed = parseGrade(text, keys);
      if (parsed) return { ok: true, result: parsed };
    } catch (e) {
      return { ok: false, error: (e as Error).message };
    }
  }
  return { ok: false, error: 'The grader did not return valid JSON twice; showing its raw reply.', raw };
}

export async function testKey(apiKey: string, model: string): Promise<{ ok: boolean; message: string }> {
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: headers(apiKey),
      body: JSON.stringify({ model, max_tokens: 64, messages: [{ role: 'user', content: 'Reply with OK.' }] }),
    });
    if (res.ok) return { ok: true, message: `Key works with ${model}.` };
    const body = (await res.json().catch(() => ({}))) as ApiResponse;
    return { ok: false, message: body.error?.message ?? `HTTP ${res.status}` };
  } catch (e) {
    return { ok: false, message: `Network error: ${(e as Error).message}` };
  }
}
