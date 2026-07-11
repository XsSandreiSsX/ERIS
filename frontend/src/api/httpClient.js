import axios from "axios";

import {
  clearAuthStorage,
  getAccessToken,
  setAccessToken,
} from "../utils/tokenStorage";

const API_URL = import.meta.env.VITE_API_URL;
const REFRESH_URL = "/auth/refresh";
const LOGIN_URL = "/login";

const httpClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

const refreshClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

let refreshPromise = null;

function redirectToLogin() {
  clearAuthStorage();

  if (window.location.pathname !== "/login") {
    window.location.replace(LOGIN_URL);
  }
}

async function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = refreshClient
      .post(REFRESH_URL)
      .then((response) => {
        const accessToken = response.data.access_token;

        if (!accessToken) {
          throw new Error("Сервер не вернул access token.");
        }

        setAccessToken(accessToken);

        return accessToken;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }

  return refreshPromise;
}

httpClient.interceptors.request.use(
  (config) => {
    const accessToken = getAccessToken();

    if (accessToken) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },

  (error) => Promise.reject(error),
);

httpClient.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    const status = error.response?.status;
    const errorCode = error.response?.data?.error_code;

    if (!originalRequest) {
      return Promise.reject(error);
    }

    if (originalRequest.url === REFRESH_URL) {
      return Promise.reject(error);
    }

    if (
      status === 401 &&
      errorCode === "EXPIRED_TOKEN" &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const newAccessToken = await refreshAccessToken();

        originalRequest.headers.Authorization =
          `Bearer ${newAccessToken}`;

        return httpClient(originalRequest);
      } catch {
        redirectToLogin();

        return Promise.reject(error);
      }
    }

    if (
      status === 401 &&
      [
        "NOT_AUTHENTICATED",
        "INVALID_CREDENTIALS",
        "UNAUTHORIZED",
        "UNANTHORIZED",
      ].includes(errorCode)
    ) {
      redirectToLogin();
    }

    return Promise.reject(error);
  },
);

export default httpClient;
