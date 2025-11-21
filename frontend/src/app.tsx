import { Toaster } from "sonner";
import { Outlet } from "react-router-dom";

export function App() {
  return (
    <main>
      <Outlet />
      <Toaster />
    </main>
  );
}
