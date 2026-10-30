import { useState } from 'react';
import { Frame, Slider, Toggle, num, type WidgetProps, fmt } from './common';

// Bayes' rule as areas (M21). A population of 1,000 people: the prevalence decides how
// many are ill, the sensitivity how many of those test positive, the specificity how
// many of the healthy test negative. The posterior is the ill share of the positives.

export function counts(N: number, prior: number, sens: number, spec: number) {
  const ill = N * prior;
  const healthy = N - ill;
  const tp = ill * sens;
  const fp = healthy * (1 - spec);
  return { ill, healthy, tp, fn: ill - tp, fp, tn: healthy - fp };
}

export function posterior(prior: number, sens: number, spec: number) {
  const tp = prior * sens;
  const fp = (1 - prior) * (1 - spec);
  return tp / (tp + fp);
}

export default function BayesGrid({ props }: WidgetProps) {
  const [prev, setPrev] = useState(num(props, 'prevalence', 1));
  const [sens, setSens] = useState(num(props, 'sensitivity', 99));
  const [spec, setSpec] = useState(num(props, 'specificity', 99));
  const [second, setSecond] = useState(props.second === 'true');
  const N = 1000;
  const p1 = posterior(prev / 1000, sens / 100, spec / 100);
  const prior = second ? p1 : prev / 1000;
  const c = counts(N, prior, sens / 100, spec / 100);
  const post = posterior(prior, sens / 100, spec / 100);
  const cols = 40;
  const rows = N / cols;
  const cell = 9;
  const W = cols * cell;
  const H = rows * cell;
  // Cells are filled in order: true positives, false negatives, false positives, true negatives.
  const tp = Math.round(c.tp);
  const fn = Math.round(c.ill) - tp;
  const fp = Math.round(c.fp);
  const kind = (k: number) => (k < tp ? 'tp' : k < tp + fn ? 'fn' : k < tp + fn + fp ? 'fp' : 'tn');
  const fill: Record<string, string> = { tp: 'var(--accent)', fn: 'var(--practice)', fp: 'var(--bad)', tn: 'var(--surface-2)' };
  return (
    <Frame
      title="Bayes' rule as areas"
      caption={
        <>
          Of 1,000 people {second ? '(already positive once) ' : ''}about {fmt(c.ill, 1)} are ill and {fmt(c.healthy, 1)} healthy. Positives: {fmt(c.tp, 1)} ill (true
          positives) and {fmt(c.fp, 1)} healthy (false positives). P(ill | positive) = {fmt(c.tp, 1)} / ({fmt(c.tp, 1)} + {fmt(c.fp, 1)}) ={' '}
          {fmt(100 * post, 1)} percent.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Grid of 1000 people coloured by illness and test result">
        {Array.from({ length: N }, (_, k) => (
          <rect key={k} x={(k % cols) * cell + 0.5} y={Math.floor(k / cols) * cell + 0.5} width={cell - 1} height={cell - 1} fill={fill[kind(k)]} />
        ))}
      </svg>
      <ul className="legend-row">
        <li>
          <svg width="12" height="12" aria-hidden="true">
            <rect width="12" height="12" fill={fill.tp} />
          </svg>
          ill, positive
        </li>
        <li>
          <svg width="12" height="12" aria-hidden="true">
            <rect width="12" height="12" fill={fill.fn} />
          </svg>
          ill, negative
        </li>
        <li>
          <svg width="12" height="12" aria-hidden="true">
            <rect width="12" height="12" fill={fill.fp} />
          </svg>
          healthy, positive
        </li>
        <li>
          <svg width="12" height="12" aria-hidden="true">
            <rect width="12" height="12" fill={fill.tn} stroke="var(--border)" />
          </svg>
          healthy, negative
        </li>
      </ul>
      <div className="widget-controls grid2">
        <Slider label="Prevalence (per 1,000)" value={prev} min={1} max={500} step={1} onChange={setPrev} format={(v) => String(v)} />
        <Slider label="Sensitivity (percent)" value={sens} min={50} max={100} step={0.5} onChange={setSens} format={(v) => v.toFixed(1)} />
        <Slider label="Specificity (percent)" value={spec} min={50} max={100} step={0.5} onChange={setSpec} format={(v) => v.toFixed(1)} />
      </div>
      <div className="widget-controls">
        <Toggle label="Test again: the first posterior becomes the prior" checked={second} onChange={setSecond} />
      </div>
    </Frame>
  );
}
