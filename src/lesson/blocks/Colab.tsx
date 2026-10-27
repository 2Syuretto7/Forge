import { useState } from 'react';
import type { Block } from '../../content/types';
import { colabUrl, verifyCode } from '../colab';
import { saveColab, useStore } from '../../store/store';

type C = Extract<Block, { t: 'colab' }>;

export function Colab({ b }: { b: C }) {
  const rec = useStore((s) => s.colab[b.notebook]);
  const [code, setCode] = useState('');
  const [msg, setMsg] = useState('');
  const submit = async () => {
    const ok = await verifyCode(b.notebook, b.tests, code);
    if (ok) {
      await saveColab({ lessonId: b.notebook, code: code.trim(), verifiedAt: Date.now() });
      setMsg('');
    } else {
      setMsg('That code does not match a run where every autograder test passed. Re-run the last cell and copy the line exactly.');
    }
  };
  return (
    <div className="card colab">
      <div className="card-kicker">GPU notebook</div>
      <p>
        Open the notebook in Google Colab, choose <em>Runtime, Change runtime type, T4 GPU</em>, then run all cells. The final cell prints a
        completion code.
      </p>
      <a className="btn primary" href={colabUrl(b.notebook)} target="_blank" rel="noreferrer">
        Open in Colab
      </a>
      {rec ? (
        <p className="reveal good" role="status">
          Verified: <code>{rec.code}</code>
        </p>
      ) : (
        <div className="colab-code">
          <label>
            Completion code{' '}
            <input value={code} onChange={(e) => setCode(e.target.value)} placeholder={`FORGE-${b.notebook}-xxxxxxxx`} spellCheck={false} />
          </label>
          <button className="btn" onClick={() => void submit()} disabled={!code.trim()}>
            Verify
          </button>
          {msg && (
            <p className="reveal bad" role="alert">
              {msg}
            </p>
          )}
        </div>
      )}
      <p className="muted small">Expected autograder tests: {b.tests.join(', ')}</p>
    </div>
  );
}
