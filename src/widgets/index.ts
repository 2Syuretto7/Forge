import { lazy, type ComponentType, type LazyExoticComponent } from 'react';
import type { WidgetProps } from './common';

// One file per widget; each is loaded on first use.
const modules = import.meta.glob<{ default: ComponentType<WidgetProps> }>('./*.tsx');

const cache = new Map<string, LazyExoticComponent<ComponentType<WidgetProps>>>();

export function getWidget(name: string) {
  const loader = modules[`./${name}.tsx`];
  if (!loader || !/^[A-Z]/.test(name)) return null;
  let c = cache.get(name);
  if (!c) {
    c = lazy(loader);
    cache.set(name, c);
  }
  return c;
}

export const widgetNames = Object.keys(modules)
  .map((k) => k.slice(2, -4))
  .filter((n) => /^[A-Z]/.test(n));
