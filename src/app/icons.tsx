// Small inline icons (24-unit viewBox, currentColor), decorative unless labelled.
type P = { size?: number; className?: string };

function Svg({ size = 16, className, children }: P & { children: React.ReactNode }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className={className}>
      {children}
    </svg>
  );
}

export const Flame = (p: P) => (
  <Svg {...p}>
    <path d="M12 2c1 4 5 5.5 5 11a5 5 0 0 1-10 0c0-2.5 1.2-4 2.5-5.2.3 2 1.2 3 2.5 3.2C11 8 11.5 5 12 2z" fill="currentColor" stroke="none" />
  </Svg>
);
export const Bolt = (p: P) => (
  <Svg {...p}>
    <path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z" fill="currentColor" stroke="none" />
  </Svg>
);
export const Check = (p: P) => (
  <Svg {...p}>
    <path d="m5 12.5 4.5 4.5L19 7.5" />
  </Svg>
);
export const Cross = (p: P) => (
  <Svg {...p}>
    <path d="M6 6l12 12M18 6 6 18" />
  </Svg>
);
export const Lock = (p: P) => (
  <Svg {...p}>
    <rect x="5" y="11" width="14" height="10" rx="2" />
    <path d="M8 11V8a4 4 0 0 1 8 0v3" />
  </Svg>
);
export const Play = (p: P) => (
  <Svg {...p}>
    <path d="M7 4.5v15l12-7.5-12-7.5z" fill="currentColor" stroke="none" />
  </Svg>
);
export const ChevronLeft = (p: P) => (
  <Svg {...p}>
    <path d="m15 5-7 7 7 7" />
  </Svg>
);
export const ChevronRight = (p: P) => (
  <Svg {...p}>
    <path d="m9 5 7 7-7 7" />
  </Svg>
);
export const Book = (p: P) => (
  <Svg {...p}>
    <path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5z" />
    <path d="M4 19a2 2 0 0 1 2-2h13" />
  </Svg>
);
export const Code = (p: P) => (
  <Svg {...p}>
    <path d="m8 7-5 5 5 5M16 7l5 5-5 5" />
  </Svg>
);
export const Clock = (p: P) => (
  <Svg {...p}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v5l3 2" />
  </Svg>
);
export const Bulb = (p: P) => (
  <Svg {...p}>
    <path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z" />
  </Svg>
);
export const Reset = (p: P) => (
  <Svg {...p}>
    <path d="M4 4v6h6" />
    <path d="M5.5 15a7 7 0 1 0 1.6-7.4L4 10" />
  </Svg>
);
export const Menu = (p: P) => (
  <Svg {...p}>
    <path d="M4 6h16M4 12h16M4 18h16" />
  </Svg>
);
export const Cloud = (p: P) => (
  <Svg {...p}>
    <path d="M7 18a4 4 0 0 1-.6-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9H7z" />
  </Svg>
);
