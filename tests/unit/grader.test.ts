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
