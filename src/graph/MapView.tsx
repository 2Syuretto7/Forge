import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { select } from 'd3-selection';
import { zoom, zoomIdentity, type ZoomBehavior } from 'd3-zoom';
import { useIndex } from '../content/load';
import type { ContentIndex, Edge, EdgeType, LessonSummary } from '../content/types';
import { useStore, type State } from '../store/store';
import { closure, lessonPercent, missingPrereqs, nodeState, theoryShare, type NodeState } from '../store/derive';
import { layout, NODE_R } from './layout';
import { STAGE_LABEL, STATE_LABEL, STRAND_SHORT, TRACK_LABEL, stageNumber, trackLabel } from './labels';
import styles from './Map.module.css';

const EDGE_LABEL: Record<EdgeType, string> = {
  vertical: 'Prerequisite',
  horizontal: 'Same stage, cross-track',
  long_range: 'Long-range',
};

function useNarrow(px = 640) {
  const [narrow, setNarrow] = useState(() => window.matchMedia(`(max-width: ${px}px)`).matches);
  useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${px}px)`);
    const on = () => setNarrow(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, [px]);
  return narrow;
}

function Tooltip({ l, st, idx, state }: { l: LessonSummary; st: NodeState; idx: ContentIndex; state: State }) {
  const name = (id: string) => `${id} ${idx.lessons.find((x) => x.id === id)?.title ?? ''}`;
  const close = st === 'complete' ? closure(state, idx, l.id) : null;
  const feynman = st === 'locked' ? missingPrereqs(state, idx, l).filter((m) => m.reason === 'feynman') : [];
  return (
    <div className={styles.tip} role="tooltip">
      <div className={styles.tipTitle}>
        {l.id}. {l.title}
      </div>
      <div className="muted">
        {trackLabel(l)}. {STATE_LABEL[st]}
        {close && (close.closed ? '; closed by its one-week review check' : '; closes after its one-week review check')}
      </div>
      {feynman.length > 0 && <div>Waiting on a passed Feynman explanation in {feynman.map((m) => m.id).join(', ')}.</div>}
      {l.hours > 0 && (
        <div>
          {l.hours} h; theory {Math.round(theoryShare(l) * 100)}% / practice {100 - Math.round(theoryShare(l) * 100)}%
          {l.gpu ? '; uses Colab' : '; runs in the browser'}
        </div>
      )}
      <div>
        <strong>Prerequisites:</strong> {l.prereqs.length ? l.prereqs.map(name).join('; ') : 'none'}
      </div>
      <div>
        <strong>Unlocks:</strong> {l.unlocks.length ? l.unlocks.map(name).join('; ') : 'none'}
      </div>
    </div>
  );
}

export function shortTitle(t: string, max = 22) {
  const head = t.split(/[:;,]/)[0];
  return head.length > max ? head.slice(0, max - 1).replace(/\s+\S*$/, '') + '...' : head;
}

function edgePath(a: { x: number; y: number }, b: { x: number; y: number }, e: Edge) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len = Math.hypot(dx, dy) || 1;
  const ux = dx / len;
  const uy = dy / len;
  const pad = NODE_R + 4;
  const x1 = a.x + ux * pad;
  const y1 = a.y + uy * pad;
  const x2 = b.x - ux * (pad + 2);
  const y2 = b.y - uy * (pad + 2);
  if (e.type === 'vertical') return `M${x1},${y1} L${x2},${y2}`;
  // Curve cross-links so they do not hide prerequisite arrows.
  const bend = e.type === 'long_range' ? 0.22 : 0.12;
  const mx = (x1 + x2) / 2 - uy * len * bend;
  const my = (y1 + y2) / 2 + ux * len * bend;
  return `M${x1},${y1} Q${mx},${my} ${x2},${y2}`;
}

function GraphSvg({ idx, state }: { idx: ContentIndex; state: State }) {
  const { nodes, width, height, columns, rows, math } = useMemo(() => layout(idx, { track: TRACK_LABEL, strand: STRAND_SHORT }), [idx]);
  const [show, setShow] = useState<Record<EdgeType, boolean>>({ vertical: true, horizontal: true, long_range: true });
  const [hover, setHover] = useState<string | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const gRef = useRef<SVGGElement>(null);
  const zoomRef = useRef<ZoomBehavior<SVGSVGElement, unknown> | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const svg = select(svgRef.current!);
    const z = zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.4, 3])
      // The map is taller than the window: the wheel scrolls the page, and zooms with Ctrl or Cmd.
      .filter((ev: Event) => (ev.type === 'wheel' ? (ev as WheelEvent).ctrlKey || (ev as WheelEvent).metaKey : !(ev as MouseEvent).button))
      .on('zoom', (ev) => {
        gRef.current?.setAttribute('transform', ev.transform.toString());
      });
    svg.call(z);
    zoomRef.current = z;
    return () => {
      svg.on('.zoom', null);
    };
  }, []);

  const zoomBy = (k: number) => zoomRef.current && select(svgRef.current!).call(zoomRef.current.scaleBy, k);
  const reset = () => zoomRef.current && select(svgRef.current!).call(zoomRef.current.transform, zoomIdentity);

  const hovered = hover ? idx.lessons.find((l) => l.id === hover) : null;
  const related = hover ? new Set(idx.edges.filter((e) => e.from === hover || e.to === hover).flatMap((e) => [e.from, e.to])) : null;

  return (
    <div className={styles.graphWrap}>
      <div className={styles.toolbar} role="group" aria-label="Map controls">
        {(['vertical', 'horizontal', 'long_range'] as EdgeType[]).map((t) => (
          <label key={t} className={`${styles.toggle} ${styles['t_' + t]}`}>
            <input type="checkbox" checked={show[t]} onChange={(e) => setShow((s) => ({ ...s, [t]: e.target.checked }))} />
            <svg width="34" height="12" aria-hidden="true">
              <line x1="2" y1="6" x2="32" y2="6" className={styles['e_' + t]} />
            </svg>
            {EDGE_LABEL[t]}
          </label>
        ))}
        <span className={styles.zoomBtns}>
          <button className="btn small ghost" onClick={() => zoomBy(1.25)} aria-label="Zoom in">
            +
          </button>
          <button className="btn small ghost" onClick={() => zoomBy(0.8)} aria-label="Zoom out">
            -
          </button>
          <button className="btn small ghost" onClick={reset}>
            Reset view
          </button>
        </span>
      </div>
      <svg
        ref={svgRef}
        className={styles.svg}
        viewBox={`0 0 ${width} ${height}`}
        role="group"
        aria-label={`Curriculum map: ${idx.lessons.length} lessons by track, strand and stage`}
      >
        <defs>
          {(['vertical', 'horizontal', 'long_range'] as EdgeType[]).map((t) => (
            <marker key={t} id={`arrow-${t}`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M0,0 L10,5 L0,10 z" className={styles['m_' + t]} />
            </marker>
          ))}
        </defs>
        <g ref={gRef}>
          {math && (
            <g>
              <text x={(math.x0 + math.x1) / 2} y={24} className={styles.colLabel} textAnchor="middle">
                {TRACK_LABEL.math}
              </text>
              <line x1={math.x0 + 8} x2={math.x1 - 8} y1={32} y2={32} className={styles.mathRule} />
            </g>
          )}
          {columns.map((c) => (
            <text key={c.key} x={c.x} y={c.strand ? 52 : 24} className={c.strand ? styles.strandLabel : styles.colLabel} textAnchor="middle">
              {c.label}
            </text>
          ))}
          {rows.map((r, i) => (
            <g key={r.stage}>
              <rect x={6} y={r.y + 2} width={width - 12} height={r.h - 4} rx={10} className={i % 2 ? styles.bandA : styles.bandB} />
              <text x={16} y={r.y + r.h / 2 - 4} className={styles.rowLabel}>
                Stage {stageNumber(idx.stages, r.stage)}
              </text>
              <text x={16} y={r.y + r.h / 2 + 12} className={styles.rowName}>
                {STAGE_LABEL[r.stage]}
              </text>
            </g>
          ))}
          {idx.edges
            .filter((e) => show[e.type])
            .map((e) => {
              const a = nodes.get(e.from)!;
              const b = nodes.get(e.to)!;
              const dim = related && !(e.from === hover || e.to === hover);
              return (
                <path
                  key={`${e.from}-${e.to}-${e.type}`}
                  d={edgePath(a, b, e)}
                  className={`${styles['e_' + e.type]} ${dim ? styles.dim : ''}`}
                  markerEnd={`url(#arrow-${e.type})`}
                  markerStart={e.type === 'horizontal' ? `url(#arrow-${e.type})` : undefined}
                  fill="none"
                >
                  <title>
                    {e.from} to {e.to}: {EDGE_LABEL[e.type]}
                    {e.note ? `. ${e.note}` : ''}
                  </title>
                </path>
              );
            })}
          {idx.lessons.map((l) => {
            const p = nodes.get(l.id)!;
            const st = nodeState(state, idx, l);
            const pct = lessonPercent(state, l);
            const circ = 2 * Math.PI * (NODE_R + 5);
            const dim = related && !related.has(l.id);
            return (
              <g
                key={l.id}
                transform={`translate(${p.x},${p.y})`}
                className={`${styles.node} ${styles['s_' + st]} ${dim ? styles.dim : ''}`}
                tabIndex={0}
                role="link"
                aria-label={`${l.id} ${l.title}. ${STATE_LABEL[st]}${st === 'in_progress' ? `, ${Math.round(pct * 100)} percent` : ''}`}
                onMouseEnter={() => setHover(l.id)}
                onMouseLeave={() => setHover(null)}
                onFocus={() => setHover(l.id)}
                onBlur={() => setHover(null)}
                onClick={() => st !== 'unpublished' && navigate(`/lesson/${l.id}`)}
                onKeyDown={(e) => {
                  if ((e.key === 'Enter' || e.key === ' ') && st !== 'unpublished') {
                    e.preventDefault();
                    navigate(`/lesson/${l.id}`);
                  }
                }}
              >
                <circle r={NODE_R} className={styles.disc} />
                {st === 'in_progress' && (
                  <circle
                    r={NODE_R + 5}
                    className={styles.ring}
                    strokeDasharray={`${circ * pct} ${circ}`}
                    transform="rotate(-90)"
                    fill="none"
                  />
                )}
                <text className={styles.nodeId} textAnchor="middle" dy="0.35em">
                  {l.id}
                </text>
                <text className={styles.nodeTitle} textAnchor="middle" y={NODE_R + 15}>
                  {shortTitle(l.title, l.track === 'math' ? 19 : 22)}
                </text>
              </g>
            );
          })}
        </g>
      </svg>
      {hovered && <Tooltip l={hovered} st={nodeState(state, idx, hovered)} idx={idx} state={state} />}
      <ul className={styles.legend} aria-label="Node states">
        {(['available', 'in_progress', 'complete', 'locked'] as NodeState[]).map((s) => (
          <li key={s}>
            <svg width="16" height="16" aria-hidden="true">
              <circle cx="8" cy="8" r="7" className={`${styles.legendDot} ${styles['s_' + s]}`} />
            </svg>
            {STATE_LABEL[s]}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ListMode({ idx, state }: { idx: ContentIndex; state: State }) {
  return (
    <div className={styles.list}>
      {idx.stages.map((s) => (
        <section key={s} aria-labelledby={`stage-${s}`}>
          <h2 id={`stage-${s}`} className={styles.stageHead}>
            Stage {stageNumber(idx.stages, s)}: {STAGE_LABEL[s]}
          </h2>
          <ul className={styles.lessonList}>
            {idx.lessons
              .filter((l) => l.stage === s)
              .map((l) => {
                const st = nodeState(state, idx, l);
                const out = idx.edges.filter((e) => e.from === l.id);
                const inn = idx.edges.filter((e) => e.to === l.id);
                return (
                  <li key={l.id} className={`${styles.listItem} ${styles['s_' + st]}`}>
                    <div className={styles.listHead}>
                      {st === 'unpublished' ? (
                        <span className={styles.listTitle}>
                          {l.id}. {l.title}
                        </span>
                      ) : (
                        <Link to={`/lesson/${l.id}`} className={styles.listTitle}>
                          {l.id}. {l.title}
                        </Link>
                      )}
                      <span className="muted small">
                        {trackLabel(l)}
                        {l.hours ? `, ${l.hours} h` : ''}. {STATE_LABEL[st]}
                        {st === 'in_progress' ? ` (${Math.round(lessonPercent(state, l) * 100)}%)` : ''}
                      </span>
                    </div>
                    <ul className="chips">
                      {inn.map((e) => (
                        <li key={'i' + e.from} className={`chip ${e.type}`}>
                          from {e.from}
                          {e.type !== 'vertical' ? ` (${EDGE_LABEL[e.type].toLowerCase()})` : ''}
                        </li>
                      ))}
                      {out.map((e) => (
                        <li key={'o' + e.to} className={`chip ${e.type}`}>
                          to {e.to}
                          {e.type !== 'vertical' ? ` (${EDGE_LABEL[e.type].toLowerCase()})` : ''}
                        </li>
                      ))}
                    </ul>
                  </li>
                );
              })}
          </ul>
        </section>
      ))}
    </div>
  );
}

export function MapView() {
  const { data: idx, error } = useIndex();
  const state = useStore((s) => s);
  const narrow = useNarrow();
  useEffect(() => {
    document.title = 'Forge';
  }, []);
  if (error)
    return (
      <main className="page" id="main">
        <p className="reveal bad">{error}</p>
      </main>
    );
  if (!idx)
    return (
      <main className="page" id="main">
        <p className="muted">Loading map</p>
      </main>
    );
  return (
    <main className={styles.map} id="main">
      <h1 className="sr-only">Curriculum map</h1>
      {narrow ? <ListMode idx={idx} state={state} /> : <GraphSvg idx={idx} state={state} />}
    </main>
  );
}
