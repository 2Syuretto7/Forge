import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { loadGraph } from '../../scripts/lib/content';
import { bannedIn, graphErrors } from '../../scripts/validate_content';
import { judgePrediction } from '../../src/lesson/blocks/Predict';

describe('curriculum graph', () => {
  const g = loadGraph();
  it('has 24 lessons and satisfies the graph rules', () => {
    expect(g.lessons).toHaveLength(24);
    expect(graphErrors(g)).toEqual([]);
  });
  it('contains every edge listed in Section 10', () => {
    const vertical =
      'L01-L05, L01-L09, L01-L13, L02-L04, L02-L05, L02-L06, L03-L07, L03-L08, L04-L06, L04-L14, L05-L06, L05-L07, L06-L15, L07-L08, L07-L09, L07-L13, L08-L11, L09-L10, L09-L15, L10-L13, L11-L12, L11-L17, L11-L18, L13-L12, L13-L14, L13-L20, L13-L22, L13-L23, L14-L15, L14-L16, L15-L18, L15-L19, L16-L19, L17-L18, L17-L22, L18-L19, L19-L20, L20-L21, L21-L23, L12-L22, L19-L24, L20-L24, L21-L24, L22-L24, L23-L24';
    const horizontal = 'L03-L04, L08-L09, L11-L13, L16-L15, L17-L14';
    const longRange = 'L01-L20, L04-L21, L02-L23, L09-L19, L05-L13';
    const has = (pair: string, type: string) => {
      const [from, to] = pair.split('-');
      return g.edges.some((e) => e.from === from && e.to === to && e.type === type);
    };
    for (const p of vertical.split(', ')) expect(has(p, 'vertical'), p).toBe(true);
    for (const p of horizontal.split(', ')) expect(has(p, 'horizontal'), p).toBe(true);
    for (const p of longRange.split(', ')) expect(has(p, 'long_range'), p).toBe(true);
  });
});

describe('banned content', () => {
  it('detects banned words and emoji', () => {
    expect(bannedIn('a TODO here')).toContain('TODO');
    expect(bannedIn('Lorem ipsum')).toContain('lorem');
    expect(bannedIn('nice \u{1F600}')).toContain('emoji');
    expect(bannedIn('x → y and ≈')).toEqual([]);
  });
  it('the app source has no emoji', () => {
    const walk = (d: string): string[] =>
      fs.readdirSync(d).flatMap((f) => (fs.statSync(path.join(d, f)).isDirectory() ? walk(path.join(d, f)) : [path.join(d, f)]));
    for (const f of walk(path.resolve('src'))) expect(bannedIn(fs.readFileSync(f, 'utf8')).filter((h) => h === 'emoji'), f).toEqual([]);
  });
});

describe('prediction judging', () => {
  it('judges each kind', () => {
    expect(judgePrediction({ kind: 'choice', answer: 'b', tol: 0 }, 'b')).toBe(true);
    expect(judgePrediction({ kind: 'numeric', answer: '100', tol: 0 }, '104')).toBe(true);
    expect(judgePrediction({ kind: 'numeric', answer: '100', tol: 0 }, '110')).toBe(false);
    expect(judgePrediction({ kind: 'sketch', answer: '0,0.5,1', tol: 0.15 }, '0.1,0.5,0.9')).toBe(true);
    expect(judgePrediction({ kind: 'sketch', answer: '0,0.5,1', tol: 0.15 }, '1,0.5,0')).toBe(false);
  });
});
