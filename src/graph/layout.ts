// Layered layout: x by track column, y by stage row. Lessons sharing a cell sit
// on a small two-row grid; d3-force then only resolves residual overlaps.
import { forceCollide, forceSimulation, forceX, forceY, type SimulationNodeDatum } from 'd3-force';
import type { ContentIndex } from '../content/types';

export const COL_W = 230;
export const ROW_H = 170;
export const MARGIN = { left: 120, top: 64 };
export const NODE_R = 25;
const PEER_DX = 112;
const PEER_DY = 74;

export interface LaidNode extends SimulationNodeDatum {
  id: string;
  x: number;
  y: number;
}

export function layout(index: ContentIndex) {
  const colOf = (track: string) => (track === 'all' ? (index.tracks.length - 1) / 2 : index.tracks.indexOf(track as never));
  const cells = new Map<string, string[]>();
  for (const l of index.lessons) {
    const k = `${l.track}|${l.stage}`;
    cells.set(k, [...(cells.get(k) ?? []), l.id]);
  }
  const target = new Map<string, { x: number; y: number }>();
  const nodes: LaidNode[] = index.lessons.map((l) => {
    const col = colOf(l.track);
    const row = index.stages.indexOf(l.stage);
    const peers = cells.get(`${l.track}|${l.stage}`)!;
    const k = peers.indexOf(l.id);
    const n = peers.length;
    const perRow = n > 1 ? 2 : 1;
    const rows = Math.ceil(n / perRow);
    const r = Math.floor(k / perRow);
    const inRow = Math.min(perRow, n - r * perRow);
    const c = k % perRow;
    const cx = MARGIN.left + COL_W * (col + 0.5) + (c - (inRow - 1) / 2) * PEER_DX;
    const cy = MARGIN.top + ROW_H * (row + 0.5) + (r - (rows - 1) / 2) * PEER_DY - 8;
    target.set(l.id, { x: cx, y: cy });
    return { id: l.id, x: cx, y: cy };
  });
  const sim = forceSimulation(nodes)
    .force('x', forceX<LaidNode>((d) => target.get(d.id)!.x).strength(1))
    .force('y', forceY<LaidNode>((d) => target.get(d.id)!.y).strength(1))
    .force('collide', forceCollide<LaidNode>(NODE_R + 10))
    .stop();
  for (let i = 0; i < 200; i++) sim.tick();
  const width = MARGIN.left + COL_W * index.tracks.length + 16;
  const height = MARGIN.top + ROW_H * index.stages.length + 12;
  return { nodes: new Map(nodes.map((n) => [n.id, { x: n.x, y: n.y }])), width, height };
}
