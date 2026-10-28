import { useState } from "react";
import { Frame, Select, Slider, Toggle, type WidgetProps, fmt } from "./common";

export interface FloatSpec {
  label: string;
  exp: number; // exponent bits
  man: number; // stored mantissa (fraction) bits
  bias: number;
  hasInf: boolean; // false for fp8 E4M3, whose all-ones exponent still holds finite values
  max: number; // largest finite value
}

const ieeeMax = (exp: number, man: number) =>
  (2 - 2 ** -man) * 2 ** (2 ** exp - 2 - (2 ** (exp - 1) - 1));

export const FORMATS = {
  fp32: {
    label: "fp32",
    exp: 8,
    man: 23,
    bias: 127,
    hasInf: true,
    max: ieeeMax(8, 23),
  },
  bf16: {
    label: "bf16",
    exp: 8,
    man: 7,
    bias: 127,
    hasInf: true,
    max: ieeeMax(8, 7),
  },
  fp16: {
    label: "fp16",
    exp: 5,
    man: 10,
    bias: 15,
    hasInf: true,
    max: ieeeMax(5, 10),
  },
  e5m2: {
    label: "fp8 E5M2",
    exp: 5,
    man: 2,
    bias: 15,
    hasInf: true,
    max: ieeeMax(5, 2),
  },
  e4m3: { label: "fp8 E4M3", exp: 4, man: 3, bias: 7, hasInf: false, max: 448 },
} satisfies Record<string, FloatSpec>;
export type FormatId = keyof typeof FORMATS;

export const minNormal = (f: FloatSpec) => 2 ** (1 - f.bias);
export const minSubnormal = (f: FloatSpec) => 2 ** (1 - f.bias - f.man);
export const epsilon = (f: FloatSpec) => 2 ** -f.man; // gap between 1 and the next value

// floor(log2(a)) for a > 0, exact even when Math.log2 rounds across a power of two.
function ilog2(a: number) {
  let e = Math.floor(Math.log2(a));
  if (2 ** e > a) e -= 1;
  if (2 ** (e + 1) <= a) e += 1;
  return e;
}

// Spacing between neighbouring representable values near |x|.
export function ulp(x: number, f: FloatSpec) {
  const a = Math.abs(x);
  const e = a === 0 ? 1 - f.bias : Math.max(ilog2(a), 1 - f.bias);
  return 2 ** (e - f.man);
}

// Round a float64 to the nearest value of format f, ties to even. Overflow
// gives infinity, or saturates at the largest finite value for formats
// without infinity (as PyTorch's float8_e4m3fn cast does).
export function roundTo(x: number, f: FloatSpec): number {
  if (!Number.isFinite(x))
    return f.hasInf || Number.isNaN(x) ? x : Math.sign(x) * f.max;
  if (x === 0) return x;
  const a = Math.abs(x);
  const u = ulp(a, f);
  const q = a / u; // exact: u is a power of two
  const fl = Math.floor(q);
  const frac = q - fl;
  const r = frac > 0.5 || (frac === 0.5 && fl % 2 === 1) ? fl + 1 : fl;
  const v = r * u;
  if (v > f.max) return Math.sign(x) * (f.hasInf ? Infinity : f.max);
  return Math.sign(x) * v;
}

export interface Encoded {
  sign: number;
  expField: number;
  manField: number;
  kind: "zero" | "subnormal" | "normal" | "inf" | "nan";
}

export function encode(x: number, f: FloatSpec): Encoded {
  const v = roundTo(x, f);
  const sign = v < 0 || Object.is(v, -0) ? 1 : 0;
  const allOnes = 2 ** f.exp - 1;
  if (Number.isNaN(v))
    return {
      sign: 0,
      expField: allOnes,
      manField: 2 ** f.man - 1,
      kind: "nan",
    };
  if (!Number.isFinite(v))
    return { sign, expField: allOnes, manField: 0, kind: "inf" };
  const a = Math.abs(v);
  if (a === 0) return { sign, expField: 0, manField: 0, kind: "zero" };
  const e = ilog2(a);
  if (e < 1 - f.bias)
    return {
      sign,
      expField: 0,
      manField: a / minSubnormal(f),
      kind: "subnormal",
    };
  return {
    sign,
    expField: e + f.bias,
    manField: (a / 2 ** e - 1) * 2 ** f.man,
    kind: "normal",
  };
}

const bits = (v: number, n: number) => v.toString(2).padStart(n, "0");

const PRESETS: { label: string; value: number }[] = [
  { label: "0.1", value: 0.1 },
  { label: "1/3", value: 1 / 3 },
  { label: "pi", value: Math.PI },
  { label: "1 + 2^-11", value: 1 + 2 ** -11 },
  { label: "1000", value: 1000 },
  { label: "65504 (fp16 max)", value: 65504 },
  { label: "70000", value: 70000 },
  { label: "1e-5", value: 1e-5 },
  { label: "1e-8", value: 1e-8 },
  { label: "3e38", value: 3e38 },
];

export default function FloatFormats({ props }: WidgetProps) {
  const [logA, setLogA] = useState(
    Math.log10(Math.abs(Number(props.value) || 0.1)),
  );
  const [neg, setNeg] = useState(false);
  const [preset, setPreset] = useState("");
  const x = (neg ? -1 : 1) * (preset ? Number(preset) : 10 ** logA);
  return (
    <Frame
      title="Floating-point formats: the same number in fp32, bf16, fp16 and fp8"
      caption={
        <>
          A value is (-1)^sign times 1.mantissa times 2^(exponent - bias); an
          all-zero exponent field holds subnormals, 0.mantissa times 2^(1 -
          bias). Exponent bits set the range, mantissa bits the precision: bf16
          keeps fp32&apos;s range with far less precision, fp16 the reverse.
        </>
      }
    >
      <div
        className="widget-stats"
        role="group"
        aria-label="Value being encoded"
      >
        <span>x = {x.toPrecision(10)}</span>
      </div>
      <div className="table-scroll">
        <table className="widget-table">
          <thead>
            <tr>
              <th>format</th>
              <th>sign | exponent | mantissa</th>
              <th>stored value</th>
              <th>relative error</th>
            </tr>
          </thead>
          <tbody>
            {(Object.keys(FORMATS) as FormatId[]).map((id) => {
              const f = FORMATS[id];
              const enc = encode(x, f);
              const v = roundTo(x, f);
              const rel = Number.isFinite(v)
                ? Math.abs(v - x) / Math.abs(x)
                : NaN;
              return (
                <tr key={id}>
                  <td>{f.label}</td>
                  <td className="bitfield">
                    <span className="bit-s">{enc.sign}</span>{" "}
                    <span className="bit-e">{bits(enc.expField, f.exp)}</span>{" "}
                    <span className="bit-m">
                      {f.man > 10
                        ? bits(enc.manField, f.man).slice(0, 10) + "..."
                        : bits(enc.manField, f.man)}
                    </span>
                  </td>
                  <td>
                    {Number.isFinite(v)
                      ? v.toPrecision(8)
                      : `${v > 0 ? "+" : "-"}inf (overflow)`}
                    {!f.hasInf && Math.abs(x) > f.max ? " (saturated)" : ""}
                  </td>
                  <td>
                    {Number.isFinite(rel)
                      ? rel === 0
                        ? "exact"
                        : rel.toExponential(2)
                      : "-"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="table-scroll">
        <table className="widget-table">
          <thead>
            <tr>
              <th>format</th>
              <th>bits (e, m)</th>
              <th>max</th>
              <th>min normal</th>
              <th>min subnormal</th>
              <th>epsilon</th>
            </tr>
          </thead>
          <tbody>
            {(Object.keys(FORMATS) as FormatId[]).map((id) => {
              const f = FORMATS[id];
              return (
                <tr key={id}>
                  <td>{f.label}</td>
                  <td>
                    {1 + f.exp + f.man} ({f.exp}, {f.man})
                  </td>
                  <td>{fmt(f.max, 0)}</td>
                  <td>{minNormal(f).toExponential(2)}</td>
                  <td>{minSubnormal(f).toExponential(2)}</td>
                  <td>{epsilon(f).toExponential(2)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="widget-controls grid2">
        <Slider
          label="log10 |x|"
          value={logA}
          min={-10}
          max={39}
          step={0.01}
          onChange={(v) => {
            setPreset("");
            setLogA(v);
          }}
        />
        <Select
          label="Preset"
          value={preset}
          options={[
            { value: "", label: "use the slider" },
            ...PRESETS.map((p) => ({ value: String(p.value), label: p.label })),
          ]}
          onChange={setPreset}
        />
      </div>
      <div className="widget-controls">
        <Toggle label="Negative" checked={neg} onChange={setNeg} />
      </div>
    </Frame>
  );
}
