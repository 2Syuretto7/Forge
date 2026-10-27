// Fetches compiled content. Paths are relative so the site works under any base.
import { useEffect, useState } from 'react';
import type { ContentIndex, Lesson } from './types';

const base = import.meta.env.BASE_URL;
let indexPromise: Promise<ContentIndex> | null = null;
const lessonCache = new Map<string, Promise<Lesson>>();

export function fetchIndex(): Promise<ContentIndex> {
  if (!indexPromise) {
    indexPromise = fetch(`${base}content/index.json`).then((r) => {
      if (!r.ok) throw new Error(`Could not load content index (${r.status})`);
      return r.json() as Promise<ContentIndex>;
    });
    indexPromise.catch(() => (indexPromise = null));
  }
  return indexPromise;
}

export function fetchLesson(id: string): Promise<Lesson> {
  let p = lessonCache.get(id);
  if (!p) {
    p = fetch(`${base}content/lessons/${id}.json`).then((r) => {
      if (!r.ok) throw new Error(`Lesson ${id} is not published yet`);
      return r.json() as Promise<Lesson>;
    });
    p.catch(() => lessonCache.delete(id));
    lessonCache.set(id, p);
  }
  return p;
}

type Loadable<T> = { data: T | null; error: string | null };

function useLoad<T>(key: string | null, fn: () => Promise<T>): Loadable<T> {
  const [st, setSt] = useState<Loadable<T> & { key: string | null }>({ data: null, error: null, key: null });
  useEffect(() => {
    if (key == null) return;
    let alive = true;
    fn().then(
      (data) => alive && setSt({ data, error: null, key }),
      (e: Error) => alive && setSt({ data: null, error: e.message, key }),
    );
    return () => {
      alive = false;
    };
    // fn is derived from key
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
  return st.key === key ? st : { data: null, error: null };
}

export function useIndex() {
  return useLoad('index', fetchIndex);
}

export function useLesson(id: string | undefined) {
  return useLoad(id ?? null, () => fetchLesson(id!));
}
