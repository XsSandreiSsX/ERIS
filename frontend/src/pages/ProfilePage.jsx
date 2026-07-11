import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getCurrentUser,
  logout,
} from "../api/authApi";
import { getApiErrorMessage } from "../api/apiError";
import ProfileCard from "../components/profile/ProfileCard";

export default function ProfilePage() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadUser() {
      try {
        const currentUser = await getCurrentUser();

        setUser(currentUser);
      } catch (error) {
        if (error.response?.status !== 401) {
          setErrorMessage(
            getApiErrorMessage(
              error,
              "Не удалось загрузить профиль.",
            ),
          );
        }
      } finally {
        setIsLoading(false);
      }
    }

    loadUser();
  }, []);

  async function handleLogout() {
    setIsLoggingOut(true);

    try {
      await logout();
    } finally {
      setIsLoggingOut(false);
      navigate("/login", {
        replace: true,
      });
    }
  }

  return (
    <main className="min-h-screen bg-gray-100 px-4 py-10">
      <section className="mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-2xl items-center">
        <div className="w-full">
          <header className="mb-6">
            <div>
              <p className="font-display text-xs font-semibold uppercase tracking-widest text-red-600">
                ERIS
              </p>

              <h1 className="font-display mt-3 text-3xl font-semibold text-gray-950">
                Профиль
              </h1>
            </div>
          </header>

          {isLoading && (
            <div className="rounded-2xl border border-gray-200 bg-white p-6 text-sm text-gray-500 shadow-sm">
              Загрузка профиля...
            </div>
          )}

          {!isLoading && errorMessage && (
            <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700">
              {errorMessage}
            </div>
          )}

          {!isLoading && user && (
            <>
              <ProfileCard user={user} />

              <button
                className="mt-4 w-full rounded-lg bg-red-600 px-4 py-2.5 font-semibold text-white transition hover:bg-red-700 disabled:bg-gray-300 disabled:text-gray-500"
                type="button"
                onClick={handleLogout}
                disabled={isLoggingOut}
              >
                {isLoggingOut ? "Выходим..." : "Выйти"}
              </button>
            </>
          )}
        </div>
      </section>
    </main>
  );
}
