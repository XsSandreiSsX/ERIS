const ACCESS_TOKEN_KEY = "eris_access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setAccessToken(token) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function removeAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export function removeRefreshTokenCookie() {
  if (typeof document === "undefined") {
    return;
  }

  const expires = "expires=Thu, 01 Jan 1970 00:00:00 GMT";
  const sameSite = "SameSite=Lax";

  document.cookie = `${REFRESH_TOKEN_KEY}=; ${expires}; path=/; ${sameSite}`;
  document.cookie = `${REFRESH_TOKEN_KEY}=; ${expires}; path=/auth; ${sameSite}`;
  document.cookie = `${REFRESH_TOKEN_KEY}=; ${expires}; path=/auth/refresh; ${sameSite}`;
}

export function clearAuthStorage() {
  removeAccessToken();
  removeRefreshTokenCookie();
}
