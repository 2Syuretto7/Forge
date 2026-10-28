/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_COLAB_BRANCH?: string;
}
declare module '*.py?raw' {
  const src: string;
  export default src;
}
