import { useEffect, useMemo, useRef, useState } from 'react';
import { Frame, Slider, Toggle, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

interface Pt {
  x: number;
  y: number;
  c: 0 | 1;
}

export function makeData(separable: boolean, seed: number): Pt[] {
  const r = rng(seed);
  const gap = separable ? 1.6 : 0.6;
  const pts: Pt[] = [];
  for (let i = 0; i < 80; i++) {
    const c = (i % 2) as 0 | 1;
    const s = c ? 1 : -1;
    pts.push({ x: s * gap + 0.55 * gauss(r), y: s * gap * 0.6 + 0.55 * gauss(r), c });
  }
  return pts;
}

const sig = (z: number) => 1 / (1 + Math.exp(-z));

export function stepGD(w: number[], pts: Pt[], lr: number, l2: number) {
  let gx = 0;
  let gy = 0;
  let gb = 0;
  let loss = 0;
  for (const p of pts) {
    const z = w[0] * p.x + w[1] * p.y + w[2];
    const pr = sig(z);
    const e = pr - p.c;
    gx += e * p.x;
    gy += e * p.y;
    gb += e;
    loss += p.c ? -Math.log(Math.max(pr, 1e-300)) : -Math.log(Math.max(1 - pr, 1e-300));
  }
  const n = pts.length;
  loss = loss / n + 0.5 * l2 * (w[0] ** 2 + w[1] ** 2);
  return {
    w: [w[0] - lr * (gx / n + l2 * w[0]), w[1] - lr * (gy / n + l2 * w[1]), w[2] - lr * (gb / n)],
    loss,
  };
}

export default function DecisionBoundary({ props }: WidgetProps) {
  const [separable, setSeparable] = useState(props.separable === 'true');
  const [lr, setLr] = useState(num(props, 'lr', 0.5));
  const [l2, setL2] = useState(num(props, 'l2', 0));
  const data = useMemo(() => makeData(separable, 7), [separable]);
  const [w, setW] = useState([0, 0, 0]);
  const [hist, setHist] = useState<[number, number][]>([]);
  const [norms, setNorms] = useState<[number, number][]>([]);
  const [playing, setPlaying] = useState(false);
  const state = useRef({ w: [0, 0, 0], it: 0 });

  const reset = () => {
    state.current = { w: [0, 0, 0], it: 0 };
    setW([0, 0, 0]);
    setHist([]);
    setNorms([]);
  };
  useEffect(reset, [separable]);

  const advance = (k: number) => {
    let { w: cw, it } = state.current;
    const h: [number, number][] = [];
    const nn: [number, number][] = [];
    for (let i = 0; i < k; i++) {
      const r = stepGD(cw, data, lr, l2);
      cw = r.w;
      it++;
      h.push([it, r.loss]);
      nn.push([it, Math.hypot(cw[0], cw[1])]);
    }
    state.current = { w: cw, it };
    setW(cw);
    setHist((a) => [...a, ...h].slice(-4000));
    setNorms((a) => [...a, ...nn].slice(-4000));
  };

  useEffect(() => {
    if (!playing) return;
    let raf = 0;
    const tick = () => {
      advance(5);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
    // advance closes over the latest lr/l2/data through re-renders
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, lr, l2, data]);

  const S = 300;
  const L = 4;
  const toPx = (v: number) => ((v + L) / (2 * L)) * S;
  const cells = 24;
  const shade = [];
  for (let i = 0; i < cells; i++)
    for (let j = 0; j < cells; j++) {
      const x = -L + ((i + 0.5) * 2 * L) / cells;
      const y = -L + ((j + 0.5) * 2 * L) / cells;
      const p = sig(w[0] * x + w[1] * y + w[2]);
      shade.push(
        <rect
          key={`${i}-${j}`}
          x={(i * S) / cells}
          y={S - ((j + 1) * S) / cells}
          width={S / cells + 0.5}
          height={S / cells + 0.5}
          fill={p > 0.5 ? 'var(--accent)' : 'var(--theory)'}
          opacity={Math.abs(p - 0.5) * 0.5}
        />,
      );
    }
  let boundary = null;
  if (Math.abs(w[1]) > 1e-9 || Math.abs(w[0]) > 1e-9) {
    const pts: [number, number][] = [];
    if (Math.abs(w[1]) > Math.abs(w[0])) for (const x of [-L, L]) pts.push([x, -(w[0] * x + w[2]) / w[1]]);
    else for (const y of [-L, L]) pts.push([-(w[1] * y + w[2]) / w[0], y]);
    boundary = <line x1={toPx(pts[0][0])} y1={S - toPx(pts[0][1])} x2={toPx(pts[1][0])} y2={S - toPx(pts[1][1])} className="series-c" />;
  }
  const last = hist[hist.length - 1];
  const maxIt = Math.max(10, state.current.it);

  return (
    <Frame
      title="Logistic regression training live"
      caption={
        <>
          Iteration {state.current.it}; loss {last ? fmt(last[1]) : 'n/a'}; weight norm {fmt(Math.hypot(w[0], w[1]))}.{' '}
          {separable && l2 === 0
            ? 'The classes are separable, so the loss keeps falling by scaling the weights up: the norm grows without bound.'
            : 'Overlapping classes or an L2 penalty give a finite optimum, and the weight norm levels off.'}
        </>
      }
    >
      <div className="widget-grid">
        <svg viewBox={`0 0 ${S} ${S}`} className="widget-svg" role="img" aria-label="Data points, predicted probabilities and the decision boundary">
          {shade}
          {boundary}
          {data.map((p, i) => (
            <circle key={i} cx={toPx(p.x)} cy={S - toPx(p.y)} r={3.5} className={`pt-${p.c}`} />
          ))}
        </svg>
        <div>
          <LinePlot
            label="Training loss over iterations"
            series={[{ points: hist, cls: 'series-a', label: 'log loss' }]}
            xDomain={[0, maxIt]}
            yDomain={[0, Math.max(0.75, ...hist.slice(0, 1).map((h) => h[1]))]}
            xlabel="iteration"
            ylabel="loss"
            height={150}
          />
          <LinePlot
            label="Weight norm over iterations"
            series={[{ points: norms, cls: 'series-c', label: 'weight norm' }]}
            xDomain={[0, maxIt]}
            yDomain={[0, Math.max(1, ...norms.map((h) => h[1])) * 1.1]}
            xlabel="iteration"
            ylabel="norm"
            height={150}
          />
        </div>
      </div>
      <div className="widget-controls">
        <button className="btn small primary" onClick={() => setPlaying((v) => !v)} aria-pressed={playing}>
          {playing ? 'Pause' : 'Train'}
        </button>
        <button className="btn small" onClick={() => advance(1)} disabled={playing}>
          One step
        </button>
        <button className="btn small ghost" onClick={reset}>
          Reset weights
        </button>
        <Toggle label="Separable classes" checked={separable} onChange={setSeparable} />
      </div>
      <div className="widget-controls grid2">
        <Slider label="Learning rate" value={lr} min={0.01} max={3} step={0.01} onChange={setLr} />
        <Slider label="L2 strength" value={l2} min={0} max={0.5} step={0.005} onChange={setL2} format={(v) => v.toFixed(3)} />
      </div>
    </Frame>
  );
}
