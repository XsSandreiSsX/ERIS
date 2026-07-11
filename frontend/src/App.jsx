import {
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";
import PublicOnlyRoute from "./components/PublicOnlyRoute";
import { getAccessToken } from "./utils/tokenStorage";
import AuthPage from "./pages/AuthPage";
import ProfilePage from "./pages/ProfilePage";

function RootRedirect() {
  const accessToken = getAccessToken();

  return (
    <Navigate
      to={accessToken ? "/profile" : "/login"}
      replace
    />
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<PublicOnlyRoute />}>
        <Route
          path="/login"
          element={<AuthPage />}
        />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route
          path="/profile"
          element={<ProfilePage />}
        />
      </Route>

      <Route
        path="/"
        element={<RootRedirect />}
      />

      <Route
        path="*"
        element={<RootRedirect />}
      />
    </Routes>
  );
}
