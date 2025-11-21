import { Outlet } from "react-router";

export function MainLayout() {
  return (
    <main className="flex h-screen w-full">
      <Outlet />
    </main>
  );
}
