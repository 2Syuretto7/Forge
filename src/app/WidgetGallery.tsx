import { Suspense } from 'react';
import { getWidget, widgetNames } from '../widgets';

// Unlinked page (#/widgets) that renders every widget with default props,
// used for visual review and accessibility audits.
export function WidgetGallery() {
  return (
    <main className="page narrow" id="main">
      <h1>Widget gallery</h1>
      {widgetNames.map((name) => {
        const W = getWidget(name)!;
        return (
          <section key={name} aria-label={name}>
            <h2 className="small muted">{name}</h2>
            <Suspense fallback={<p className="muted">Loading</p>}>
              <W props={{}} />
            </Suspense>
          </section>
        );
      })}
    </main>
  );
}
