import { createBrowserRouter } from "react-router-dom";
import { PublicRoute } from "../components/publicRoute";
import { LoginPage } from "../pages/login";
import { RegisterPage } from "../pages/register";
import { App } from "@/app";
import { ProtectedRoute } from "@/components/privateRoute";
import { HomePage } from "@/pages/home";
import { AuthLayout } from "@/layout/authLayout";
import { MainLayout } from "@/layout/mainLayout";

export const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      {
        element: <AuthLayout />,
        path: "/auth",
        children: [
          {
            path: "login",
            element: (
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            ),
          },
          {
            path: "register",
            element: (
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            ),
          },
        ],
      },
      {
        element: (
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        ),
        children: [
          {
            path: "/",
            element: <HomePage />,
          },
        ],
      },
    ],
  },
]);
