import { UserContext } from "@/api/context/user.context";
import { type JSX, useContext } from "react";
import { Navigate } from "react-router-dom";

export function PublicRoute({ children }: { children: JSX.Element }) {
  const { isAuth } = useContext(UserContext);
  return isAuth ? <Navigate to="/" /> : children;
}
