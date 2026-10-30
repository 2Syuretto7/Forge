import { useState } from 'react';
import { Frame, Slider, Toggle, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// Counting by a tree of choices, and the birthday problem (M08). Each level of the tree
// is one choice; the leaves are the outcomes. Without repetition each level has one
// branch fewer; if order does not matter, every set appears k! times among the leaves.

export function perm(n: number, k: number) {
  let p = 1;
  for (let i = 0; i < k; i++) p *= n - i;
  return k > n ? 0 : p;
}

export function comb(n: number, k: number) {
  if (k < 0 || k > n) return 0;
  let c = 1;
  for (let i = 1; i <= Math.min(k, n - k); i++) c = (c * (n - Math.min(k, n - k) + i)) / i;
  return Math.round(c);
}

export function pNoMatch(m: number, days = 365) {
  let p = 1;
  for (let i = 0; i < m; i++) p *= (days - i) / days;
  return Math.max(0, p);
}

const LETTERS = 'ABCDE';

export default function CountingTree({ props }: WidgetProps) {
  const [mode, setMode] = useState<'tree' | 'birthday'>(props.mode === 'birthday' ? 'birthday' : 'tree');
  const [n, setN] = useState(Number(props.n) || 3);
  const [k, setK] = useState(Number(props.k) || 2);
  const [rep, setRep] = useState(props.repeat === 'true');
  const [ordered, setOrdered] = useState(props.ordered !== 'false');
  const [m, setM] = useState(Number(props.m) || 23);

  if (mode === 'birthday') {
    const ms = Array.from({ length: 80 }, (_, i) => i + 1);
    const p = 1 - pNoMatch(m);
    return (
      <Frame
        title="The birthday problem"
        caption={
          <>
            With {m} people there are {comb(m, 2).toLocaleString('en-US')} pairs, and the chance that some pair shares a birthday is {fmt(p, 3)}. It
            passes one half at 23 people, when there are already 253 pairs.
          </>
        }
      >
        <LinePlot
          label="Chance of a shared birthday against the number of people"
          xDomain={[1, 80]}
          yDomain={[0, 1]}
          xlabel="people in the room"
          ylabel="chance of a shared birthday"
          series={[
            { label: 'exact', cls: 'series-c', points: ms.map((x) => [x, 1 - pNoMatch(x)]) },
            { label: 'one half', cls: 'series-a', dashed: true, points: [[1, 0.5], [80, 0.5]] },
          ]}
        >
          {(sx, sy) => <circle cx={sx(m)} cy={sy(p)} r={5} className="dot-b" />}
        </LinePlot>
        <div className="widget-controls">
          <Slider label="People" value={m} min={1} max={80} step={1} onChange={setM} format={(v) => String(v)} />
          <button className="btn small ghost" onClick={() => setMode('tree')}>
            Switch to the tree of choices
          </button>
        </div>
      </Frame>
    );
  }

  // Leaves of the tree, as sequences of letters.
  const kk = Math.min(k, rep ? 3 : n);
  const leaves: string[] = [];
  const grow = (prefix: string) => {
    if (prefix.length === kk) {
      leaves.push(prefix);
      return;
    }
    for (const ch of LETTERS.slice(0, n)) if (rep || !prefix.includes(ch)) grow(prefix + ch);
  };
  grow('');
  const seen = new Set<string>();
  const firstOfSet = leaves.map((s) => {
    const key = [...s].sort().join('');
    const first = !seen.has(key);
    seen.add(key);
    return first;
  });
  const count = ordered ? leaves.length : firstOfSet.filter(Boolean).length;
  const W = 440;
  const H = 230;
  const levelY = (lv: number) => 24 + (lv * (H - 60)) / Math.max(1, kk);
  const leafX = (i: number) => 14 + (i * (W - 28)) / Math.max(1, leaves.length - 1);
  // Draw the tree from its leaves: a node at level lv is the mean x of its descendants.
  const nodes = new Map<string, number[]>();
  leaves.forEach((s, i) => {
    for (let lv = 0; lv <= kk; lv++) {
      const key = s.slice(0, lv);
      nodes.set(key, [...(nodes.get(key) ?? []), leafX(i)]);
    }
  });
  const nx = (key: string) => {
    const v = nodes.get(key)!;
    return v.reduce((a, b) => a + b, 0) / v.length;
  };
  const formula = rep
    ? ordered
      ? `${n}^${kk} = ${n ** kk}`
      : `C(${n} + ${kk} - 1, ${kk}) = ${comb(n + kk - 1, kk)}`
    : ordered
      ? `${n}!/(${n}-${kk})! = ${perm(n, kk)}`
      : `${n}!/(${kk}! (${n}-${kk})!) = ${comb(n, kk)}`;
  return (
    <Frame
      title="Counting with a tree of choices"
      caption={
        <>
          {leaves.length} leaves; {ordered ? 'order matters, so each leaf is its own outcome' : 'order does not matter, so leaves holding the same letters count once'}
          : {count} outcomes ({formula}).
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Tree of choices whose leaves are the outcomes">
        {[...nodes.keys()]
          .filter((key) => key.length > 0)
          .map((key) => (
            <line key={key} x1={nx(key.slice(0, -1))} y1={levelY(key.length - 1)} x2={nx(key)} y2={levelY(key.length)} className="grid-line" />
          ))}
        {leaves.map((s, i) => (
          <g key={s} opacity={ordered || firstOfSet[i] ? 1 : 0.25}>
            <circle cx={leafX(i)} cy={levelY(kk)} r={4} className={ordered || firstOfSet[i] ? 'dot-c' : 'dot-b'} />
            {leaves.length <= 30 && (
              <text x={leafX(i)} y={levelY(kk) + 18} textAnchor="middle">
                {s}
              </text>
            )}
          </g>
        ))}
        <circle cx={nx('')} cy={levelY(0)} r={4} className="dot-a" />
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Choices (letters)" value={n} min={2} max={5} step={1} onChange={setN} format={(v) => String(v)} />
        <Slider label="Picks" value={k} min={1} max={3} step={1} onChange={setK} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Toggle label="Repetition allowed" checked={rep} onChange={setRep} />
        <Toggle label="Order matters" checked={ordered} onChange={setOrdered} />
        <button className="btn small ghost" onClick={() => setMode('birthday')}>
          Switch to the birthday problem
        </button>
      </div>
    </Frame>
  );
}
