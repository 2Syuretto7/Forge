import { useEffect } from 'react';
import { HashRouter, Link, NavLink, Route, Routes } from 'react-router-dom';
import { MapView } from '../graph/MapView';
import { LessonPlayer } from '../lesson/LessonPlayer';
import { ReviewPage } from '../review/ReviewPage';
import { SettingsPage } from '../settings/SettingsPage';
import { WidgetGallery } from './WidgetGallery';
import { useIndex } from '../content/load';
import { useStore } from '../store/store';
import { dueItems, hoursDone, totalHours } from '../store/derive';

function useTheme() {
  const theme = useStore((s) => s.settings.theme);
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', theme);
  }, [theme]);
}

function Header() {
  const { data: idx } = useIndex();
  const state = useStore((s) => s);
  const due = dueItems(state).length;
  return (
    <header className="topbar">
      <a href="#main" className="skip">
        Skip to content
      </a>
      <Link to="/" className="brand">
        Forge
      </Link>
      <nav className="topnav" aria-label="Main">
        {idx && (
          <span className="hours" title="Hours of completed movements out of the whole curriculum">
            {Math.round(hoursDone(state, idx) * 10) / 10} / {totalHours(idx)} h
          </span>
        )}
        <NavLink to="/review" className="navlink">
          Reviews{due > 0 ? ` (${due} due)` : ''}
        </NavLink>
        <NavLink to="/settings" className="navlink">
          Settings
        </NavLink>
      </nav>
    </header>
  );
}

export function App() {
  useTheme();
  return (
    <HashRouter>
      <Header />
      <Routes>
        <Route path="/" element={<MapView />} />
        <Route path="/lesson/:id/:movement?" element={<LessonPlayer />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/widgets" element={<WidgetGallery />} />
        <Route
          path="*"
          element={
            <main className="page narrow" id="main">
              <h1>Not found</h1>
              <Link to="/">Back to the map</Link>
            </main>
          }
        />
      </Routes>
    </HashRouter>
  );
}
