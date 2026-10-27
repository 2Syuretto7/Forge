// Completion codes printed by notebook autograders (Section 5.6):
// FORGE-<ID>-<first 8 hex of sha256("<ID>:<sorted passed test names>:forge")>
export async function sha256Hex(text: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function expectedCode(lessonId: string, tests: string[]): Promise<string> {
  const hex = await sha256Hex(`${lessonId}:${[...tests].sort().join(',')}:forge`);
  return `FORGE-${lessonId}-${hex.slice(0, 8)}`;
}

export async function verifyCode(lessonId: string, tests: string[], code: string): Promise<boolean> {
  const clean = code.trim().toUpperCase().replace(/^FORGE-/, 'FORGE-');
  const exp = await expectedCode(lessonId, tests);
  return clean === exp.toUpperCase();
}

export function colabUrl(lessonId: string) {
  return `https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/${lessonId}.ipynb`;
}
