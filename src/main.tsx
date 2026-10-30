import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import 'katex/dist/katex.min.css';
import './app/global.css';
import { App } from './app/App';
import { loadStore, startCurriculum } from './store/store';
import { setResetNotice } from './home/Dashboard';

const root = createRoot(document.getElementById('root')!);
loadStore()
  .then(startCurriculum)
  .then((wasReset) => setResetNotice(wasReset))
  .catch((e) => console.warn('Progress storage unavailable; continuing without it.', e))
  .finally(() =>
    root.render(
      <StrictMode>
        <App />
      </StrictMode>,
    ),
  );
