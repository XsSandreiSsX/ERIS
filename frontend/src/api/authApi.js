import httpClient from "./httpClient";
import {
  clearAuthStorage,
  setAccessToken,
} from "../utils/tokenStorage";

export const AUTH_ENDPOINTS = {
  register: "/auth/register",
  login: "/auth/login",
  refresh: "/auth/refresh",
  logout: "/auth/logout",
  me: "/auth/me",
};

export async function login(credentials) {
  const response = await httpClient.post(
    AUTH_ENDPOINTS.login,
    credentials,
  );

  const accessToken = response.data.access_token;

  if (!accessToken) {
    throw new Error("Сервер не вернул access token.");
  }

  setAccessToken(accessToken);

  return response.data;
}

export async function register(credentials) {
  const response = await httpClient.post(
    AUTH_ENDPOINTS.register,
    credentials,
  );

  return response.data;
}

export async function refresh() {
  const response = await httpClient.post(AUTH_ENDPOINTS.refresh);

  return response.data;
}

export async function logout() {
  try {
    await httpClient.post(AUTH_ENDPOINTS.logout);
  } finally {
    clearAuthStorage();
  }
}

export async function getCurrentUser() {
  const response = await httpClient.get(AUTH_ENDPOINTS.me);

  return response.data;
}
