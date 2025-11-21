import { Outlet } from "react-router";

export function AuthLayout() {
  return (
    <main className="flex h-screen w-full">
      <Outlet />
    </main>
  );
}
