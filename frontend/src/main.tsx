import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import { App } from "./app";
import "./index.css";
import { LoginPage } from "./pages/login-page";

createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <App>
      <Routes>
        <Route path="/login-page" element={<LoginPage />} />
      </Routes>
    </App>
  </BrowserRouter>
);
