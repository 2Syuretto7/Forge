import { useState } from 'react';
import { Frame, Select, type WidgetProps } from './common';

// Two propositional formulas side by side: every row of the truth table, and whether the
// formulas agree on all of them (logically equivalent) or differ somewhere (M03).

type V = Record<'p' | 'q' | 'r', boolean>;
const imp = (a: boolean, b: boolean) => !a || b;

export interface Pair {
  label: string;
  vars: ('p' | 'q' | 'r')[];
  a: [string, (v: V) => boolean];
  b: [string, (v: V) => boolean];
}

export const PAIRS: Record<string, Pair> = {
  contrapositive: {
    label: 'An implication and its contrapositive',
    vars: ['p', 'q'],
    a: ['p implies q', (v) => imp(v.p, v.q)],
    b: ['not q implies not p', (v) => imp(!v.q, !v.p)],
  },
  converse: {
    label: 'An implication and its converse',
    vars: ['p', 'q'],
    a: ['p implies q', (v) => imp(v.p, v.q)],
    b: ['q implies p', (v) => imp(v.q, v.p)],
  },
  orform: {
    label: 'Implication as an or',
    vars: ['p', 'q'],
    a: ['p implies q', (v) => imp(v.p, v.q)],
    b: ['(not p) or q', (v) => !v.p || v.q],
  },
  demorgan: {
    label: 'De Morgan',
    vars: ['p', 'q'],
    a: ['not (p and q)', (v) => !(v.p && v.q)],
    b: ['(not p) or (not q)', (v) => !v.p || !v.q],
  },
  wrongDemorgan: {
    label: 'A tempting mistake',
    vars: ['p', 'q'],
    a: ['not (p and q)', (v) => !(v.p && v.q)],
    b: ['(not p) and (not q)', (v) => !v.p && !v.q],
  },
  distribute: {
    label: 'And distributes over or',
    vars: ['p', 'q', 'r'],
    a: ['p and (q or r)', (v) => v.p && (v.q || v.r)],
    b: ['(p and q) or (p and r)', (v) => (v.p && v.q) || (v.p && v.r)],
  },
};

export function rows(pair: Pair) {
  const n = pair.vars.length;
  const out: { v: V; a: boolean; b: boolean }[] = [];
  for (let m = 0; m < 2 ** n; m++) {
    const v: V = { p: false, q: false, r: false };
    pair.vars.forEach((name, i) => (v[name] = ((m >> (n - 1 - i)) & 1) === 0));
    out.push({ v, a: pair.a[1](v), b: pair.b[1](v) });
  }
  return out;
}

export function equivalent(pair: Pair) {
  return rows(pair).every((r) => r.a === r.b);
}

const T = (b: boolean) => (b ? 'T' : 'F');

export default function TruthTable({ props }: WidgetProps) {
  const [key, setKey] = useState(props.pair && PAIRS[props.pair] ? props.pair : 'contrapositive');
  const pair = PAIRS[key];
  const rs = rows(pair);
  const diff = rs.filter((r) => r.a !== r.b).length;
  return (
    <Frame
      title="Truth tables: when are two statements the same?"
      caption={
        diff === 0
          ? `The two columns agree on all ${rs.length} rows: the formulas are logically equivalent.`
          : `The columns differ on ${diff} of ${rs.length} rows (highlighted): the formulas are not equivalent, and each highlighted row is a counterexample.`
      }
    >
      <div role="group" aria-label="Truth table">
        <table className="widget-table truth">
          <thead>
            <tr>
              {pair.vars.map((v) => (
                <th key={v}>{v}</th>
              ))}
              <th>{pair.a[0]}</th>
              <th>{pair.b[0]}</th>
            </tr>
          </thead>
          <tbody>
            {rs.map((r, i) => (
              <tr key={i} className={r.a !== r.b ? 'differs' : undefined}>
                {pair.vars.map((v) => (
                  <td key={v}>{T(r.v[v])}</td>
                ))}
                <td>{T(r.a)}</td>
                <td>{T(r.b)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="widget-controls">
        <Select
          label="Compare"
          value={key}
          options={Object.entries(PAIRS).map(([k, p]) => ({ value: k, label: p.label }))}
          onChange={setKey}
        />
      </div>
    </Frame>
  );
}
