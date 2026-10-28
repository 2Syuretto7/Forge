import { useMemo, useState } from 'react';
import { Frame, Slider, Toggle, type WidgetProps, fmt } from './common';

// Byte-pair encoding on characters. With word-level pre-tokenization (as in
// GPT-2), the text is split into words that keep their leading space, and
// merges never cross a word boundary.
export const SPACE = '▁'; // the visible space marker SentencePiece uses

export function pretokenize(text: string, byWord: boolean): string[] {
  const t = text.replace(/\s+/g, ' ').trim().replace(/ /g, SPACE);
  if (!byWord) return t ? [t] : [];
  return t.match(new RegExp(`${SPACE}?[^${SPACE}]+`, 'g')) ?? [];
}

export interface BpeResult {
  merges: { pair: [string, string]; count: number }[];
  // tokens of the whole text after 0, 1, ..., merges.length merges
  steps: string[][];
}

export function bpeTrain(text: string, maxMerges: number, byWord = true): BpeResult {
  const counts = new Map<string, number>();
  for (const w of pretokenize(text, byWord)) counts.set(w, (counts.get(w) ?? 0) + 1);
  let words = [...counts.entries()].map(([w, c]) => ({ syms: [...w], c }));
  const order = pretokenize(text, byWord);
  const snapshot = () => {
    const seg = new Map<string, string[]>(words.map((w) => [w.syms.join(''), w.syms]));
    return order.flatMap((w) => seg.get(w) ?? []);
  };
  const merges: BpeResult['merges'] = [];
  const steps = [snapshot()];
  for (let m = 0; m < maxMerges; m++) {
    // Count adjacent pairs, weighted by word frequency; ties go to the pair seen first.
    const pc = new Map<string, number>();
    for (const w of words)
      for (let i = 0; i + 1 < w.syms.length; i++) {
        const k = w.syms[i] + '\u0000' + w.syms[i + 1];
        pc.set(k, (pc.get(k) ?? 0) + w.c);
      }
    let best = '';
    let bestC = 1;
    for (const [k, c] of pc) if (c > bestC) [best, bestC] = [k, c];
    if (!best) break;
    const [a, b] = best.split('\u0000') as [string, string];
    words = words.map((w) => ({ c: w.c, syms: applyMerge(w.syms, a, b) }));
    merges.push({ pair: [a, b], count: bestC });
    steps.push(snapshot());
  }
  return { merges, steps };
}

export function applyMerge(syms: string[], a: string, b: string): string[] {
  const out: string[] = [];
  for (let i = 0; i < syms.length; i++) {
    if (i + 1 < syms.length && syms[i] === a && syms[i + 1] === b) {
      out.push(a + b);
      i++;
    } else out.push(syms[i]);
  }
  return out;
}

// Encoding new text replays the learned merges in order within each word.
export function bpeEncode(text: string, merges: [string, string][], byWord = true): string[] {
  return pretokenize(text, byWord).flatMap((w) => merges.reduce((syms, [a, b]) => applyMerge(syms, a, b), [...w]));
}

const DEFAULT_TEXT =
  'low lower lowest newer newest wider widest low lower newest newest widest low lowest newer wider newest the newest lower tower is the lowest tower';

export default function TokenizerStepper({ props }: WidgetProps) {
  const [text, setText] = useState(props.text ?? DEFAULT_TEXT);
  const [byWord, setByWord] = useState(props.byword !== 'false');
  const [step, setStep] = useState(Number(props.step) || 6);
  const res = useMemo(() => bpeTrain(text.slice(0, 600), 40, byWord), [text, byWord]);
  const s = Math.min(step, res.merges.length);
  const toks = res.steps[s];
  const chars = res.steps[0].length;
  const base = new Set(res.steps[0]).size;
  return (
    <Frame
      title="Byte-pair encoding, one merge at a time"
      caption={
        <>
          After {s} merge{s === 1 ? '' : 's'}: {toks.length} tokens for {chars} characters ({fmt(chars / Math.max(toks.length, 1), 2)} characters per token); vocabulary{' '}
          {base} base symbols + {s} merges = {base + s}. Each merge replaces the most frequent adjacent pair everywhere; {SPACE} marks a space.
        </>
      }
    >
      <div className="token-row" role="group" aria-label={`Tokens after ${s} merges`}>
        {toks.slice(0, 160).map((t, i) => (
          <span key={i} className={`token tok-${i % 2}`}>
            {t}
          </span>
        ))}
        {toks.length > 160 && <span className="muted"> and {toks.length - 160} more</span>}
      </div>
      <ol className="merge-list" aria-label="Merges learned so far">
        {res.merges.slice(0, s).map((m, i) => (
          <li key={i} className={i === s - 1 ? 'latest' : undefined}>
            <code>{m.pair[0]}</code> + <code>{m.pair[1]}</code> = <code>{m.pair[0] + m.pair[1]}</code> <span className="muted">({m.count})</span>
          </li>
        ))}
      </ol>
      <div className="widget-controls grid2">
        <Slider label="Merges applied" value={s} min={0} max={res.merges.length} step={1} onChange={setStep} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Toggle label="Split into words first (merges never cross a space)" checked={byWord} onChange={setByWord} />
      </div>
      <label className="widget-text">
        Training text (first 600 characters are used)
        <textarea value={text} onChange={(e) => setText(e.target.value)} rows={3} spellCheck={false} />
      </label>
    </Frame>
  );
}
