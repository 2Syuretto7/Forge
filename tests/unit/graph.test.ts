import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { loadGraph } from '../../scripts/lib/content';
import { bannedIn, graphErrors } from '../../scripts/validate_content';
import { judgePrediction } from '../../src/lesson/blocks/Predict';

describe('curriculum graph', () => {
  const g = loadGraph();
  it('has the 38 math-track lessons and satisfies the graph rules', () => {
    expect(g.lessons.filter((l) => /^M\d\d$/.test(l.id))).toHaveLength(38);
    expect(g.stages[0]).toBe('prelude');
    expect(graphErrors(g)).toEqual([]);
  });
  it('contains every math-track edge of docs/math-track.md: 74 vertical, 27 horizontal, 19 long-range', () => {
    const vertical =
      'M01-M02, M02-M03, M02-M04, M02-M11, M03-M05, M03-M08, M04-M05, M04-M06, M04-M07, M04-M09, M05-M06, M05-M08, M05-M15, M06-M15, M06-M26, M06-M27, M07-M09, M08-M21, M09-M10, M10-M11, M10-M18, M11-M12, M12-L05, M12-M13, M13-M14, M13-M23, M13-M28, M13-M32, M14-M33, M14-M34, M15-M16, M15-M17, M15-M26, M16-M18, M16-M25, M17-M20, M17-M22, M18-M19, M18-M20, M18-M28, M19-L07, M19-L08, M20-M23, M21-M22, M22-M23, M22-M24, M22-M27, M22-M32, M23-M37, M24-M25, M24-M29, M24-M31, M25-L05, M25-L06, M25-M31, M25-M35, M26-M33, M27-L06, M27-L14, M27-M30, M27-M36, M28-L09, M28-M29, M28-M30, M29-M35, M29-M36, M30-M38, M31-M34, M32-M37, M33-M38, M34-M38, M35-M38, M36-M38, M37-M38';
    const horizontal =
      'M30-L05, M31-L06, M29-L09, M34-L10, M33-L11, M34-L13, M35-L15, M36-L21, M38-L24, M01-M06, M01-M08, M06-M07, M11-M26, M12-M22, M12-M25, M13-M18, M14-M23, M15-M24, M17-M24, M19-M26, M19-M27, M21-M27, M24-M26, M25-M27, M25-M28, M29-M32, M33-M34';
    const longRange =
      'M01-M35, M02-M12, M03-M31, M04-L07, M05-M29, M07-L13, M08-M31, M09-M34, M10-L13, M13-M29, M13-M32, M14-L20, M16-M29, M20-M37, M24-M36, M25-L23, M26-L17, M27-L21, M30-L21';
    expect(vertical.split(', ')).toHaveLength(74);
    expect(horizontal.split(', ')).toHaveLength(27);
    expect(longRange.split(', ')).toHaveLength(19);
    const has = (pair: string, type: string) => {
      const [from, to] = pair.split('-');
      return g.edges.some((e) => e.from === from && e.to === to && e.type === type);
    };
    for (const p of vertical.split(', ')) expect(has(p, 'vertical'), p).toBe(true);
    for (const p of horizontal.split(', ')) expect(has(p, 'horizontal'), p).toBe(true);
    for (const p of longRange.split(', ')) expect(has(p, 'long_range'), p).toBe(true);
  });
  it('keeps the edges between the other tracks', () => {
    const vertical =
      'L05-L06, L05-L07, L06-L15, L07-L08, L07-L09, L07-L13, L08-L11, L09-L10, L09-L15, L10-L13, L11-L12, L11-L17, L11-L18, L13-L12, L13-L14, L13-L20, L13-L22, L13-L23, L14-L15, L14-L16, L15-L18, L15-L19, L16-L19, L17-L18, L17-L22, L18-L19, L19-L20, L20-L21, L21-L23, L12-L22, L19-L24, L20-L24, L21-L24, L22-L24, L23-L24';
    for (const p of vertical.split(', ')) {
      const [from, to] = p.split('-');
      expect(g.edges.some((e) => e.from === from && e.to === to && e.type === 'vertical'), p).toBe(true);
    }
  });
  it('rejects a horizontal edge inside one strand and a long-range edge inside one stage', () => {
    const bad = {
      ...g,
      edges: [...g.edges, { from: 'M09', to: 'M11', type: 'horizontal' as const }, { from: 'M02', to: 'M06', type: 'long_range' as const }],
    };
    const errs = graphErrors(bad);
    expect(errs).toContain('horizontal edge M09->M11 stays within one track and strand');
    expect(errs).toContain('long-range edge M02->M06 stays within one stage');
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
