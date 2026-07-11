export function getApiErrorMessage(
  error,
  fallbackMessage = "Не удалось выполнить запрос.",
) {
  const data = error.response?.data;

  if (!data) {
    return error.message ?? fallbackMessage;
  }

  if (
    data.error_code === "validation_error" &&
    typeof data.detail === "string"
  ) {
    return data.detail;
  }

  if (typeof data.detail === "string") {
    return data.detail;
  }

  if (typeof data.detail?.msg === "string") {
    return data.detail.msg;
  }

  if (Array.isArray(data.detail)) {
    const firstMessage = data.detail.find(
      (item) => typeof item?.msg === "string",
    )?.msg;

    if (firstMessage) {
      return firstMessage;
    }
  }

  return error.message ?? fallbackMessage;
}
