import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  login,
  register,
} from "../api/authApi";
import { getApiErrorMessage } from "../api/apiError";
import { AUTH_PASSWORD_MIN_LENGTH } from "../auth/config";
import AuthField from "../components/auth/AuthField";
import AuthLayout from "../components/auth/AuthLayout";

const initialForm = {
  email: "",
  password: "",
  confirmPassword: "",
};

export default function AuthPage() {
  const navigate = useNavigate();

  const [mode, setMode] = useState("login");
  const [form, setForm] = useState(initialForm);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const isLogin = mode === "login";

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  }

  function switchMode() {
    setMode((currentMode) =>
      currentMode === "login" ? "register" : "login",
    );
    setForm(initialForm);
    setErrorMessage("");
    setSuccessMessage("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!isLogin && form.password !== form.confirmPassword) {
      setErrorMessage("Пароли не совпадают.");
      return;
    }

    if (form.password.length < AUTH_PASSWORD_MIN_LENGTH) {
      setErrorMessage(
        `Пароль должен быть не короче ${AUTH_PASSWORD_MIN_LENGTH} символов.`,
      );
      return;
    }

    setIsLoading(true);

    try {
      if (isLogin) {
        await login({
          email: form.email,
          password: form.password,
        });

        setForm(initialForm);
        navigate("/profile", {
          replace: true,
        });
        return;
      }

      await register({
        email: form.email,
        password: form.password,
      });

      setMode("login");
      setForm({
        ...initialForm,
        email: form.email,
      });
      setSuccessMessage("Аккаунт создан. Войдите в систему.");
    } catch (error) {
      setErrorMessage(
        getApiErrorMessage(error),
      );
    } finally {
      setIsLoading(false);
      setForm((currentForm) => ({
        ...currentForm,
        password: "",
        confirmPassword: "",
      }));
    }
  }

  return (
    <AuthLayout mode={mode}>
      <div className="mb-5 grid grid-cols-2 rounded-lg bg-gray-100 p-1 text-sm font-medium">
        <button
          className={`rounded-md px-3 py-2 transition ${
            isLogin
              ? "bg-white text-gray-950 shadow-sm"
              : "text-gray-500 hover:text-gray-900"
          }`}
          type="button"
          onClick={() => {
            if (!isLogin) {
              switchMode();
            }
          }}
        >
          Login
        </button>

        <button
          className={`rounded-md px-3 py-2 transition ${
            !isLogin
              ? "bg-white text-gray-950 shadow-sm"
              : "text-gray-500 hover:text-gray-900"
          }`}
          type="button"
          onClick={() => {
            if (isLogin) {
              switchMode();
            }
          }}
        >
          Register
        </button>
      </div>

      <form
        className="space-y-4"
        onSubmit={handleSubmit}
      >
        <AuthField
          autoComplete="email"
          label="Email"
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          placeholder="user@example.com"
        />

        <AuthField
          autoComplete={isLogin ? "current-password" : "new-password"}
          label="Password"
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          minLength={AUTH_PASSWORD_MIN_LENGTH}
          placeholder="password"
        />

        {!isLogin && (
          <AuthField
            autoComplete="new-password"
            label="Confirm password"
            name="confirmPassword"
            type="password"
            value={form.confirmPassword}
            onChange={handleChange}
            minLength={AUTH_PASSWORD_MIN_LENGTH}
            placeholder="password"
          />
        )}

        {errorMessage && (
          <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2.5 text-sm text-red-700">
            {errorMessage}
          </p>
        )}

        {successMessage && (
          <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2.5 text-sm text-red-700">
            {successMessage}
          </p>
        )}

        <button
          className="w-full rounded-lg bg-red-600 px-4 py-2.5 font-semibold text-white transition hover:bg-red-700 disabled:bg-gray-300 disabled:text-gray-500"
          type="submit"
          disabled={isLoading}
        >
          {isLoading
            ? isLogin
              ? "Входим..."
              : "Создаем аккаунт..."
            : isLogin
              ? "Войти"
              : "Создать аккаунт"}
        </button>
      </form>
    </AuthLayout>
  );
}
