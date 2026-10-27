import { useRef, useState } from 'react';
import { DEFAULT_MODEL, exportProgress, importProgress, resetProgress, saveSetting, useStore, type Settings } from '../store/store';
import { testKey } from '../grader/client';

export function SettingsPage() {
  const settings = useStore((s) => s.settings);
  const [key, setKey] = useState(settings.apiKey);
  const [showKey, setShowKey] = useState(false);
  const [model, setModel] = useState(settings.modelId);
  const [keyMsg, setKeyMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [testing, setTesting] = useState(false);
  const [dataMsg, setDataMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [confirm, setConfirm] = useState('');
  const fileRef = useRef<HTMLInputElement>(null);

  const saveKey = async () => {
    await saveSetting('apiKey', key.trim());
    await saveSetting('modelId', model.trim() || DEFAULT_MODEL);
    setKeyMsg({ ok: true, text: 'Saved in this browser only.' });
  };

  const doTest = async () => {
    setTesting(true);
    const r = await testKey(key.trim(), model.trim() || DEFAULT_MODEL);
    setTesting(false);
    setKeyMsg({ ok: r.ok, text: r.message });
  };

  const doExport = async () => {
    const data = await exportProgress();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `forge-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    setDataMsg({ ok: true, text: 'Progress exported.' });
  };

  const doImport = async (file: File) => {
    try {
      const data = JSON.parse(await file.text());
      await importProgress(data);
      setDataMsg({ ok: true, text: 'Progress imported. Everything on this device now matches the file.' });
    } catch (e) {
      setDataMsg({ ok: false, text: `Import failed: ${(e as Error).message}` });
    }
  };

  return (
    <main className="page narrow" id="main">
      <h1>Settings</h1>

      <section className="card" aria-labelledby="set-ai">
        <h2 id="set-ai">AI feedback</h2>
        <p className="muted">
          Your Anthropic API key is stored only in this browser (IndexedDB) and sent only to api.anthropic.com when you ask for feedback on an
          explanation.
        </p>
        <label className="field">
          API key
          <span className="row">
            <input
              type={showKey ? 'text' : 'password'}
              value={key}
              onChange={(e) => setKey(e.target.value)}
              autoComplete="off"
              spellCheck={false}
              placeholder="sk-ant-..."
            />
            <button className="btn small ghost" onClick={() => setShowKey((v) => !v)} aria-pressed={showKey}>
              {showKey ? 'Hide' : 'Show'}
            </button>
          </span>
        </label>
        <label className="field">
          Model ID
          <input value={model} onChange={(e) => setModel(e.target.value)} spellCheck={false} />
        </label>
        <div className="row">
          <button className="btn primary" onClick={() => void saveKey()}>
            Save
          </button>
          <button className="btn" onClick={() => void doTest()} disabled={!key.trim() || testing}>
            {testing ? 'Testing' : 'Test key'}
          </button>
        </div>
        {keyMsg && (
          <p className={keyMsg.ok ? 'reveal good' : 'reveal bad'} role="status">
            {keyMsg.text}
          </p>
        )}
      </section>

      <section className="card" aria-labelledby="set-theme">
        <h2 id="set-theme">Theme</h2>
        <div className="row" role="radiogroup" aria-labelledby="set-theme">
          {(['system', 'light', 'dark'] as Settings['theme'][]).map((t) => (
            <label key={t} className="radio">
              <input type="radio" name="theme" checked={settings.theme === t} onChange={() => void saveSetting('theme', t)} />{' '}
              {t === 'system' ? 'Follow system' : t === 'light' ? 'Light' : 'Dark'}
            </label>
          ))}
        </div>
      </section>

      <section className="card" aria-labelledby="set-data">
        <h2 id="set-data">Your progress</h2>
        <p className="muted">Progress lives in this browser. Export it to back it up or move it to another device.</p>
        <div className="row">
          <button className="btn" onClick={() => void doExport()}>
            Export progress JSON
          </button>
          <button className="btn" onClick={() => fileRef.current?.click()}>
            Import progress JSON
          </button>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            className="sr-only"
            aria-label="Choose a progress file to import"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) void doImport(f);
              e.target.value = '';
            }}
          />
        </div>
        {dataMsg && (
          <p className={dataMsg.ok ? 'reveal good' : 'reveal bad'} role="status">
            {dataMsg.text}
          </p>
        )}
        <h3>Reset</h3>
        <p className="muted">Deletes all progress, predictions, explanations and reviews. Your key and theme stay. Type RESET to confirm.</p>
        <div className="row">
          <label className="sr-only" htmlFor="reset-confirm">
            Type RESET to confirm
          </label>
          <input id="reset-confirm" value={confirm} onChange={(e) => setConfirm(e.target.value)} placeholder="RESET" />
          <button
            className="btn danger"
            disabled={confirm !== 'RESET'}
            onClick={() =>
              void resetProgress().then(() => {
                setConfirm('');
                setDataMsg({ ok: true, text: 'Progress reset.' });
              })
            }
          >
            Reset progress
          </button>
        </div>
      </section>
    </main>
  );
}
