// Renders HTML compiled at build time from our own markdown (trusted).
export function Html({ html, inline }: { html: string; inline?: boolean }) {
  return inline ? (
    <span className="prose-inline" dangerouslySetInnerHTML={{ __html: html }} />
  ) : (
    <div className="prose" dangerouslySetInnerHTML={{ __html: html }} />
  );
}
