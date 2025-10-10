import type { ReactNode } from "react";

interface AppProps {
  children: ReactNode;
}

export function App({ children }: AppProps) {
  return <main className="flex h-screen w-full p-16">{children}</main>;
}
