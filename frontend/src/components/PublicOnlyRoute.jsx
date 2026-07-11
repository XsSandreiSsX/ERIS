import {
  Navigate,
  Outlet,
} from "react-router-dom";

import { getAccessToken } from "../utils/tokenStorage";

export default function PublicOnlyRoute() {
  const accessToken = getAccessToken();

  if (accessToken) {
    return (
      <Navigate
        to="/profile"
        replace
      />
    );
  }

  return <Outlet />;
}
