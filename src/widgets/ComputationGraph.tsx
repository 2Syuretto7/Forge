import { useMemo, useState } from 'react';
import { Frame, Slider, type WidgetProps, fmt } from './common';

type Op = 'input' | 'add' | 'sub' | 'mul' | 'sin' | 'square' | 'sigmoid' | 'relu' | 'exp' | 'log';
interface GNode {
  id: string;
  op: Op;
  args: string[];
  label: string;
}

const PRESETS: Record<string, { title: string; nodes: GNode[]; inputs: Record<string, number> }> = {
  default: {
    title: 'f(x, y) = (x y + sin x)^2',
    inputs: { x: 1.2, y: -0.7 },
    nodes: [
      { id: 'x', op: 'input', args: [], label: 'x' },
      { id: 'y', op: 'input', args: [], label: 'y' },
      { id: 'a', op: 'mul', args: ['x', 'y'], label: 'a = x y' },
      { id: 'b', op: 'sin', args: ['x'], label: 'b = sin x' },
      { id: 'c', op: 'add', args: ['a', 'b'], label: 'c = a + b' },
      { id: 'f', op: 'square', args: ['c'], label: 'f = c^2' },
    ],
  },
  neuron: {
    title: 'L = (sigmoid(w x + b) - t)^2',
    inputs: { w: 0.8, x: 1.5, b: -0.3, t: 1 },
    nodes: [
      { id: 'w', op: 'input', args: [], label: 'w' },
      { id: 'x', op: 'input', args: [], label: 'x' },
      { id: 'b', op: 'input', args: [], label: 'b' },
      { id: 't', op: 'input', args: [], label: 't' },
      { id: 'u', op: 'mul', args: ['w', 'x'], label: 'u = w x' },
      { id: 'z', op: 'add', args: ['u', 'b'], label: 'z = u + b' },
      { id: 's', op: 'sigmoid', args: ['z'], label: 's = sigmoid(z)' },
      { id: 'd', op: 'sub', args: ['s', 't'], label: 'd = s - t' },
      { id: 'L', op: 'square', args: ['d'], label: 'L = d^2' },
    ],
  },
  mlp: {
    title: 'L = (w2 relu(w1 x + b1) - t)^2',
    inputs: { w1: 1.1, x: 0.9, b1: -0.4, w2: -0.6, t: 0.5 },
    nodes: [
      { id: 'w1', op: 'input', args: [], label: 'w1' },
      { id: 'x', op: 'input', args: [], label: 'x' },
      { id: 'b1', op: 'input', args: [], label: 'b1' },
      { id: 'w2', op: 'input', args: [], label: 'w2' },
      { id: 't', op: 'input', args: [], label: 't' },
      { id: 'u', op: 'mul', args: ['w1', 'x'], label: 'u = w1 x' },
      { id: 'z', op: 'add', args: ['u', 'b1'], label: 'z = u + b1' },
      { id: 'h', op: 'relu', args: ['z'], label: 'h = relu(z)' },
      { id: 'y', op: 'mul', args: ['w2', 'h'], label: 'y = w2 h' },
      { id: 'd', op: 'sub', args: ['y', 't'], label: 'd = y - t' },
      { id: 'L', op: 'square', args: ['d'], label: 'L = d^2' },
    ],
  },
};

const sig = (v: number) => 1 / (1 + Math.exp(-v));

function forward(op: Op, a: number[]): number {
  switch (op) {
    case 'add':
      return a[0] + a[1];
    case 'sub':
      return a[0] - a[1];
    case 'mul':
      return a[0] * a[1];
    case 'sin':
      return Math.sin(a[0]);
    case 'square':
      return a[0] * a[0];
    case 'sigmoid':
      return sig(a[0]);
    case 'relu':
      return Math.max(0, a[0]);
    case 'exp':
      return Math.exp(a[0]);
    case 'log':
      return Math.log(a[0]);
    default:
      return NaN;
  }
}

// Local partial derivatives d(out)/d(arg_i).
function local(op: Op, a: number[]): number[] {
  switch (op) {
    case 'add':
      return [1, 1];
    case 'sub':
      return [1, -1];
    case 'mul':
      return [a[1], a[0]];
    case 'sin':
      return [Math.cos(a[0])];
    case 'square':
      return [2 * a[0]];
    case 'sigmoid':
      return [sig(a[0]) * (1 - sig(a[0]))];
    case 'relu':
      return [a[0] > 0 ? 1 : 0];
    case 'exp':
      return [Math.exp(a[0])];
    case 'log':
      return [1 / a[0]];
    default:
      return [];
  }
}

export default function ComputationGraph({ props }: WidgetProps) {
  const preset = PRESETS[props.preset ?? 'default'] ?? PRESETS.default;
  const [inputs, setInputs] = useState(preset.inputs);
  const [revealed, setRevealed] = useState(0);
  const { nodes } = preset;

  const { val, grad, order, depth } = useMemo(() => {
    const val: Record<string, number> = {};
    const depth: Record<string, number> = {};
    for (const nd of nodes) {
      if (nd.op === 'input') {
        val[nd.id] = inputs[nd.id];
        depth[nd.id] = 0;
      } else {
        val[nd.id] = forward(
          nd.op,
          nd.args.map((a) => val[a]),
        );
        depth[nd.id] = 1 + Math.max(...nd.args.map((a) => depth[a]));
      }
    }
    const grad: Record<string, number> = Object.fromEntries(nodes.map((n) => [n.id, 0]));
    const out = nodes[nodes.length - 1].id;
    grad[out] = 1;
    const order = [...nodes].reverse();
    for (const nd of order) {
      if (nd.op === 'input') continue;
      const l = local(
        nd.op,
        nd.args.map((a) => val[a]),
      );
      nd.args.forEach((a, i) => (grad[a] += grad[nd.id] * l[i]));
    }
    return { val, grad, order, depth };
  }, [nodes, inputs]);

  const maxDepth = Math.max(...Object.values(depth));
  const cols: Record<number, GNode[]> = {};
  for (const nd of nodes) (cols[depth[nd.id]] ??= []).push(nd);
  const W = 460;
  const H = 260;
  const bw = 96;
  const bh = 46;
  const pos: Record<string, { x: number; y: number }> = {};
  for (let d = 0; d <= maxDepth; d++) {
    const c = cols[d] ?? [];
    c.forEach((nd, i) => {
      pos[nd.id] = {
        x: 8 + (d * (W - bw - 16)) / Math.max(1, maxDepth),
        y: 10 + ((i + 0.5) * (H - 20)) / c.length - bh / 2,
      };
    });
  }
  const shown = new Set(order.slice(0, revealed).map((n) => n.id));
  const current = revealed > 0 ? order[revealed - 1] : null;
  const outId = nodes[nodes.length - 1].id;

  let explain = 'Forward pass: every node holds its value. Press "Backward step" to send gradients from the output back to the inputs.';
  if (current) {
    if (current.id === outId) explain = `Start: d${outId}/d${outId} = 1.`;
    else {
      const parents = nodes.filter((n) => n.args.includes(current.id));
      explain =
        `d${outId}/d${current.id} = ` +
        parents
          .map((p) => {
            const l = local(
              p.op,
              p.args.map((a) => val[a]),
            )[p.args.indexOf(current.id)];
            return `(d${outId}/d${p.id}) (d${p.id}/d${current.id}) = ${fmt(grad[p.id])} x ${fmt(l)}`;
          })
          .join(' + ') +
        ` = ${fmt(grad[current.id])}`;
    }
  }

  return (
    <Frame title={`Computation graph: ${preset.title}`} caption={<span aria-live="polite">{explain}</span>}>
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label={`Computation graph for ${preset.title}`}>
        {nodes.flatMap((nd) =>
          nd.args.map((a) => (
            <line
              key={`${a}-${nd.id}`}
              x1={pos[a].x + bw}
              y1={pos[a].y + bh / 2}
              x2={pos[nd.id].x}
              y2={pos[nd.id].y + bh / 2}
              className="edge-line"
            />
          )),
        )}
        {nodes.map((nd) => (
          <g key={nd.id} transform={`translate(${pos[nd.id].x},${pos[nd.id].y})`}>
            <rect width={bw} height={bh} rx={6} className={`node-box ${current?.id === nd.id ? 'active' : ''}`} />
            <text x={6} y={14}>
              {nd.label}
            </text>
            <text x={6} y={28} className="val">
              = {fmt(val[nd.id])}
            </text>
            {shown.has(nd.id) && (
              <text x={6} y={41} className="grad">
                grad {fmt(grad[nd.id])}
              </text>
            )}
          </g>
        ))}
      </svg>
      <div className="widget-controls">
        <button className="btn small" onClick={() => setRevealed((r) => Math.min(order.length, r + 1))} disabled={revealed >= order.length}>
          Backward step
        </button>
        <button className="btn small ghost" onClick={() => setRevealed(order.length)}>
          Show all gradients
        </button>
        <button className="btn small ghost" onClick={() => setRevealed(0)}>
          Reset
        </button>
      </div>
      <div className="widget-controls grid2">
        {Object.keys(preset.inputs).map((k) => (
          <Slider key={k} label={k} value={inputs[k]} min={-2} max={2} step={0.05} onChange={(v) => setInputs((s) => ({ ...s, [k]: v }))} />
        ))}
      </div>
    </Frame>
  );
}
