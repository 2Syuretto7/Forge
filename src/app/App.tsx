import { useEffect } from 'react';
import { HashRouter, Link, NavLink, Route, Routes } from 'react-router-dom';
import { MapView } from '../graph/MapView';
import { LessonPlayer } from '../lesson/LessonPlayer';
import { ExerciseWorkspace } from '../lesson/ExerciseWorkspace';
import { Dashboard } from '../home/Dashboard';
import { ReviewPage } from '../review/ReviewPage';
import { SettingsPage } from '../settings/SettingsPage';
import { WidgetGallery } from './WidgetGallery';
import { migrateRetired, useStore } from '../store/store';
import { dueReviewIds, streak, totalXp } from '../store/derive';
import { useIndex } from '../content/load';
import { Bolt, Flame } from './icons';

function useTheme() {
  const theme = useStore((s) => s.settings.theme);
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', theme);
  }, [theme]);
}

// Progress in lessons that have been retired moves to their successors once.
function useMigration() {
  const { data: idx } = useIndex();
  const loaded = useStore((s) => s.loaded);
  useEffect(() => {
    if (idx && loaded) void migrateRetired(idx);
  }, [idx, loaded]);
}

function Header() {
  const state = useStore((s) => s);
  const { data: idx } = useIndex();
  const due = idx ? dueReviewIds(state, idx).length : 0;
  const xp = totalXp(state);
  const days = streak(state);
  return (
    <header className="topbar">
      <a href="#main" className="skip">
        Skip to content
      </a>
      <Link to="/" className="brand">
        <span className="brand-mark" aria-hidden="true">
          F
        </span>
        <span className="brand-name">Forge</span>
      </Link>
      <nav className="topnav" aria-label="Main">
        <NavLink to="/" end className="navlink">
          Learn
        </NavLink>
        <NavLink to="/map" className="navlink">
          Map
        </NavLink>
        <NavLink to="/review" className="navlink" aria-label={due > 0 ? `Reviews (${due} due)` : 'Reviews'}>
          Reviews
          {due > 0 && (
            <span className="nav-count" aria-hidden="true">
              {due}
            </span>
          )}
        </NavLink>
        <NavLink to="/settings" className="navlink">
          Settings
        </NavLink>
      </nav>
      <div className="topstats">
        <span className="pill pill-streak" title="Day streak: consecutive days with any learning activity">
          <Flame />
          <span>
            {days} <span className="pill-unit">day{days === 1 ? '' : 's'}</span>
          </span>
        </span>
        <span className="pill pill-xp" title="Experience points">
          <Bolt />
          <span>{xp.toLocaleString('en-US')} XP</span>
        </span>
      </div>
    </header>
  );
}

export function App() {
  useTheme();
  useMigration();
  return (
    <HashRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/map" element={<MapView />} />
        <Route path="/lesson/:id/ex/:ex" element={<ExerciseWorkspace />} />
        <Route path="/lesson/:id/:movement?" element={<LessonPlayer />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/widgets" element={<WidgetGallery />} />
        <Route
          path="*"
          element={
            <main className="page narrow" id="main">
              <h1>Not found</h1>
              <Link to="/">Back to your dashboard</Link>
            </main>
          }
        />
      </Routes>
    </HashRouter>
  );
}
