const dateFormatter = new Intl.DateTimeFormat("ru-RU", {
  dateStyle: "medium",
  timeStyle: "short",
});

export default function ProfileCard({ user }) {
  const createdAt = dateFormatter.format(new Date(user.created_at));

  return (
    <article className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 border-b border-gray-100 pb-5 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm text-gray-500">
            Пользователь
          </p>

          <h2 className="mt-1 break-all text-xl font-semibold text-gray-950 sm:text-2xl">
            {user.email}
          </h2>
        </div>

        <div className="flex w-fit shrink-0 items-center gap-2 rounded-full bg-red-50 px-3 py-1.5 text-sm font-medium text-red-700">
          <span className="h-2 w-2 rounded-full bg-red-600" />
          Онлайн
        </div>
      </div>

      <dl className="mt-5 space-y-4">
        <div>
          <dt className="text-sm text-gray-500">
            ID
          </dt>
          <dd className="mt-1 font-medium text-gray-950">
            {user.id}
          </dd>
        </div>

        <div>
          <dt className="text-sm text-gray-500">
            Email
          </dt>
          <dd className="mt-1 break-all font-medium text-gray-950">
            {user.email}
          </dd>
        </div>

        <div>
          <dt className="text-sm text-gray-500">
            Создан
          </dt>
          <dd className="mt-1 font-medium text-gray-950">
            {createdAt}
          </dd>
        </div>
      </dl>
    </article>
  );
}
