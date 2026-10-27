import { describe, expect, it } from 'vitest';
import { parseGrade } from '../../src/grader/client';
import { SYSTEM_PROMPT } from '../../src/grader/prompt';

const keys = ['correctness', 'completeness', 'plainness', 'mechanism', 'example'];

describe('grader response parsing', () => {
  it('reads JSON even with surrounding text', () => {
    const r = parseGrade(
      'Here you go: {"scores":{"correctness":4,"completeness":3,"plainness":2,"mechanism":3,"example":4},"gaps":["no example"],"follow_up":"Why?"} done',
      keys,
    );
    expect(r?.total).toBe(16);
    expect(r?.gaps).toEqual(['no example']);
    expect(r?.followUp).toBe('Why?');
  });
  it('clamps scores and rejects missing criteria', () => {
    expect(parseGrade('{"scores":{"correctness":9,"completeness":3,"plainness":2,"mechanism":3,"example":-1}}', keys)?.scores.correctness).toBe(4);
    expect(parseGrade('{"scores":{"correctness":4}}', keys)).toBeNull();
    expect(parseGrade('not json', keys)).toBeNull();
  });
  it('keeps the plan system prompt verbatim', () => {
    expect(SYSTEM_PROMPT).toContain('Return only JSON: {"scores":{"correctness":n,"completeness":n,"plainness":n,"mechanism":n,"example":n}');
    expect(SYSTEM_PROMPT.startsWith("You grade a learner's plain-language explanation")).toBe(true);
  });
});

describe('grader client', () => {
  it('sends the plan request shape and retries once on unparseable output', async () => {
    const { gradeExplanation, MAX_TOKENS } = await import('../../src/grader/client');
    const calls: { url: string; init: RequestInit }[] = [];
    const replies = [
      { content: [{ type: 'text', text: 'I think it is good.' }], stop_reason: 'end_turn' },
      {
        content: [
          { type: 'thinking', thinking: '' },
          { type: 'text', text: '{"scores":{"correctness":3,"completeness":3,"plainness":4,"mechanism":2,"example":3},"gaps":["g"],"follow_up":"q?"}' },
        ],
        stop_reason: 'end_turn',
      },
    ];
    const orig = globalThis.fetch;
    globalThis.fetch = (async (url: string, init: RequestInit) => {
      calls.push({ url, init });
      return new Response(JSON.stringify(replies[calls.length - 1]), { status: 200 });
    }) as typeof fetch;
    try {
      const out = await gradeExplanation({
        apiKey: 'sk-test',
        model: 'claude-sonnet-5-5',
        rubric: 'concept',
        lessonTitle: 'L01',
        prompt: 'Explain SVD',
        keyPoints: ['a', 'b'],
        text: 'my words',
      });
      expect(out.ok).toBe(true);
      if (out.ok) expect(out.result.total).toBe(15);
      expect(calls).toHaveLength(2);
      const h = calls[0].init.headers as Record<string, string>;
      expect(calls[0].url).toBe('https://api.anthropic.com/v1/messages');
      expect(h['x-api-key']).toBe('sk-test');
      expect(h['anthropic-dangerous-direct-browser-access']).toBe('true');
      expect(h['anthropic-version']).toBe('2023-06-01');
      const body = JSON.parse(calls[0].init.body as string);
      expect(body.max_tokens).toBe(MAX_TOKENS);
      expect(MAX_TOKENS).toBe(1200);
      expect(body.model).toBe('claude-sonnet-5-5');
      expect(body.system).toContain('Feynman');
      expect(body.messages[0].content).toContain("Learner's text");
      expect(body).not.toHaveProperty('temperature');
    } finally {
      globalThis.fetch = orig;
    }
  });

  it('reports raw text after two unparseable replies and surfaces API errors', async () => {
    const { gradeExplanation } = await import('../../src/grader/client');
    const orig = globalThis.fetch;
    let n = 0;
    globalThis.fetch = (async () => {
      n++;
      return new Response(JSON.stringify({ content: [{ type: 'text', text: 'not json' }] }), { status: 200 });
    }) as typeof fetch;
    const args = { apiKey: 'k', model: 'm', rubric: 'concept' as const, lessonTitle: 't', prompt: 'p', keyPoints: ['a'], text: 'x' };
    try {
      const out = await gradeExplanation(args);
      expect(out.ok).toBe(false);
      if (!out.ok) expect(out.raw).toBe('not json');
      expect(n).toBe(2);
      globalThis.fetch = (async () => new Response(JSON.stringify({ error: { message: 'invalid x-api-key' } }), { status: 401 })) as typeof fetch;
      const bad = await gradeExplanation(args);
      expect(bad.ok).toBe(false);
      if (!bad.ok) expect(bad.error).toContain('invalid x-api-key');
    } finally {
      globalThis.fetch = orig;
    }
  });
});
