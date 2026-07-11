export default function AuthField({
  autoComplete,
  label,
  minLength,
  name,
  onChange,
  placeholder,
  type,
  value,
}) {
  return (
    <label
      className="block"
      htmlFor={name}
    >
      <span className="mb-1.5 block text-sm font-medium text-gray-700">
        {label}
      </span>

      <input
        className="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-gray-950 outline-none transition placeholder:text-gray-400 focus:border-red-600 focus:ring-2 focus:ring-red-100 disabled:bg-gray-100"
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        minLength={minLength}
        placeholder={placeholder}
        required
      />
    </label>
  );
}
