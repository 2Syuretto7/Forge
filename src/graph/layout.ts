// Layered layout: x by column, y by stage row. Math lessons sit in one sub-column per
// strand (docs/math-track.md) and stack down it, so a strand's chain reads top to
// bottom; lessons of the other tracks share a cell on a small two-row grid. Row
// heights follow the fullest cell. d3-force then only resolves residual overlaps.
import { forceCollide, forceSimulation, forceX, forceY, type SimulationNodeDatum } from 'd3-force';
import type { ContentIndex, LessonSummary } from '../content/types';

export const SUB_W = 128;
export const COL_W = 196;
export const MARGIN = { left: 112, top: 76 };
export const NODE_R = 23;
const STACK_DY = 64;
const PEER_DX = 100;
const PEER_DY = 74;
const MIN_ROW = 150;

export interface LaidNode extends SimulationNodeDatum {
  id: string;
  x: number;
  y: number;
}

export interface Column {
  key: string;
  label: string;
  x: number;
  strand: boolean;
}

export interface Row {
  stage: string;
  y: number;
  h: number;
}

export function layout(index: ContentIndex, labels: { track: Record<string, string>; strand: Record<string, string> }) {
  const strands = index.strands ?? [];
  const hasMath = strands.length > 0 && index.lessons.some((l) => l.track === 'math' && l.strand);
  const others = index.tracks.filter((t) => !hasMath || t !== 'math');
  const mathW = hasMath ? SUB_W * strands.length : 0;
  const columns: Column[] = [
    ...(hasMath ? strands.map((s, i) => ({ key: s, label: labels.strand[s], x: MARGIN.left + SUB_W * (i + 0.5), strand: true })) : []),
    ...others.map((t, i) => ({ key: t, label: labels.track[t], x: MARGIN.left + mathW + COL_W * (i + 0.5), strand: false })),
  ];
  const colKey = (l: LessonSummary) => (hasMath && l.track === 'math' && l.strand ? l.strand : l.track);
  const colX = (key: string) => {
    if (key === 'ALL') return MARGIN.left + mathW / 2;
    if (key === 'all') return MARGIN.left + mathW + (COL_W * others.length) / 2;
    return columns.find((c) => c.key === key)?.x ?? MARGIN.left;
  };
  const stacked = (key: string) => hasMath && (strands as string[]).concat('ALL').includes(key);

  const cells = new Map<string, string[]>();
  for (const l of index.lessons) {
    const k = `${colKey(l)}|${l.stage}`;
    cells.set(k, [...(cells.get(k) ?? []), l.id]);
  }
  const cellHeight = (key: string, n: number) => (stacked(key) ? n * STACK_DY + 44 : Math.ceil(n / 2) * PEER_DY + 76);
  const rows: Row[] = [];
  let y = MARGIN.top;
  for (const s of index.stages) {
    let h = MIN_ROW;
    for (const [k, ids] of cells) if (k.endsWith(`|${s}`)) h = Math.max(h, cellHeight(k.split('|')[0], ids.length));
    rows.push({ stage: s, y, h });
    y += h;
  }

  const target = new Map<string, { x: number; y: number }>();
  const nodes: LaidNode[] = index.lessons.map((l) => {
    const key = colKey(l);
    const row = rows.find((r) => r.stage === l.stage) ?? rows[0];
    const peers = cells.get(`${key}|${l.stage}`)!;
    const k = peers.indexOf(l.id);
    const n = peers.length;
    let cx: number;
    let cy: number;
    if (stacked(key)) {
      cx = colX(key);
      cy = row.y + row.h / 2 + (k - (n - 1) / 2) * STACK_DY - 8;
    } else {
      const perRow = n > 1 ? 2 : 1;
      const rowsN = Math.ceil(n / perRow);
      const r = Math.floor(k / perRow);
      const inRow = Math.min(perRow, n - r * perRow);
      const c = k % perRow;
      cx = colX(key) + (c - (inRow - 1) / 2) * PEER_DX;
      cy = row.y + row.h / 2 + (r - (rowsN - 1) / 2) * PEER_DY - 8;
    }
    target.set(l.id, { x: cx, y: cy });
    return { id: l.id, x: cx, y: cy };
  });
  const sim = forceSimulation(nodes)
    .force('x', forceX<LaidNode>((d) => target.get(d.id)!.x).strength(1))
    .force('y', forceY<LaidNode>((d) => target.get(d.id)!.y).strength(1))
    .force('collide', forceCollide<LaidNode>(NODE_R + 8))
    .stop();
  for (let i = 0; i < 200; i++) sim.tick();
  const width = MARGIN.left + mathW + COL_W * others.length + 16;
  const height = y + 12;
  return {
    nodes: new Map(nodes.map((n) => [n.id, { x: n.x, y: n.y }])),
    width,
    height,
    columns,
    rows,
    math: hasMath ? { x0: MARGIN.left, x1: MARGIN.left + mathW } : null,
  };
}
