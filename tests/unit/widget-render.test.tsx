import { describe, expect, it } from 'vitest';
import { render } from '@testing-library/react';
import { createElement, type ComponentType } from 'react';
import type { WidgetProps } from '../../src/widgets/common';

// Every widget must render with default props, quickly, and expose an
// accessible name for its figure.
const mods = import.meta.glob<{ default: ComponentType<WidgetProps> }>('../../src/widgets/[A-Z]*.tsx', { eager: true });

describe('widgets render with default props', () => {
  for (const [file, mod] of Object.entries(mods)) {
    const name = file.split('/').pop()!.replace('.tsx', '');
    it(name, () => {
      const t0 = performance.now();
      const { container, unmount } = render(createElement(mod.default, { props: {} }));
      const ms = performance.now() - t0;
      expect(container.querySelector('figure')).not.toBeNull();
      expect(container.querySelector('[role="img"], [role="group"]')).not.toBeNull();
      expect(ms).toBeLessThan(3000);
      unmount();
    });
  }
});
