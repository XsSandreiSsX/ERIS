export default function AuthLayout({ children, mode }) {
  const isLogin = mode === "login";

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100 px-4 py-10">
      <section className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-6 shadow-sm sm:p-8">
        <div className="mb-6">
          <p className="font-display text-xs font-semibold uppercase tracking-widest text-red-600">
            ERIS
          </p>

          <h1 className="font-display mt-3 text-3xl font-semibold text-gray-950">
            {isLogin ? "Вход" : "Регистрация"}
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            {isLogin
              ? "Войдите, чтобы открыть профиль."
              : "Создайте аккаунт, затем войдите."}
          </p>
        </div>

        {children}
      </section>
    </main>
  );
}
