import { UserContext } from "@/api/context/user.context";
import { useContext, type JSX } from "react";
import { Navigate } from "react-router-dom";

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isAuth } = useContext(UserContext);
  return isAuth ? children : <Navigate to="/auth/login" />;
}
