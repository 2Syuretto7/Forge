// Small dense linear algebra for widgets (float64, row-major number[][]).
export function solve(A: number[][], b: number[]): number[] {
  const n = A.length;
  const M = A.map((r, i) => [...r, b[i]]);
  for (let k = 0; k < n; k++) {
    let p = k;
    for (let i = k + 1; i < n; i++) if (Math.abs(M[i][k]) > Math.abs(M[p][k])) p = i;
    [M[k], M[p]] = [M[p], M[k]];
    const piv = M[k][k] || 1e-300;
    for (let i = k + 1; i < n; i++) {
      const f = M[i][k] / piv;
      if (f === 0) continue;
      for (let j = k; j <= n; j++) M[i][j] -= f * M[k][j];
    }
  }
  const x = Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    let s = M[i][n];
    for (let j = i + 1; j < n; j++) s -= M[i][j] * x[j];
    x[i] = s / (M[i][i] || 1e-300);
  }
  return x;
}

// Ridge regression with the kernel trick when features outnumber samples, so
// that lambda -> 0 gives the minimum-norm interpolating solution.
export function ridge(Phi: number[][], y: number[], lambda: number): number[] {
  const n = Phi.length;
  const p = Phi[0].length;
  if (p <= n) {
    const G = Array.from({ length: p }, (_, i) => Array.from({ length: p }, (_, j) => (i === j ? lambda : 0)));
    const r = Array(p).fill(0);
    for (let s = 0; s < n; s++)
      for (let i = 0; i < p; i++) {
        r[i] += Phi[s][i] * y[s];
        for (let j = 0; j < p; j++) G[i][j] += Phi[s][i] * Phi[s][j];
      }
    return solve(G, r);
  }
  const K = Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => {
      let s = i === j ? lambda : 0;
      for (let k = 0; k < p; k++) s += Phi[i][k] * Phi[j][k];
      return s;
    }),
  );
  const a = solve(K, y);
  const w = Array(p).fill(0);
  for (let s = 0; s < n; s++) for (let k = 0; k < p; k++) w[k] += Phi[s][k] * a[s];
  return w;
}
