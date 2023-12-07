import React from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Authentication from "./pages/authentication/authentication";
import Dashboard from "./pages/dashboard/dashboard";
import ErrorPage from "./pages/error/error";
import { protectedLoader } from "./utils/authentication";

import "./index.css";
import Logout from "./pages/logout/logout";

const container = document.getElementById("root")!;
const root = createRoot(container);

const router = createBrowserRouter([
  {
    path: "/",
    element: <Authentication />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
    loader: protectedLoader,
  },
  {
    path: "/logout",
    element: <Logout />,
    loader: protectedLoader,
  },
]);

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
