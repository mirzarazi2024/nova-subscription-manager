import Link from "next/link";

const items = [
  "dashboard",
  "users",
  "providers",
  "panels",
  "subscriptions",
  "countries",
  "rules",
  "scheduler",
  "logs",
  "backup",
  "settings",
  "marketplace",
  "api-keys",
  "health",
  "analytics",
];

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-800 p-4">
      <h1 className="mb-4 text-xl font-bold">NOVA Subscription Manager</h1>
      <nav className="space-y-2">
        {items.map((item) => (
          <Link
            key={item}
            href={`/${item}`}
            className="block rounded px-3 py-2 text-sm capitalize text-slate-300 hover:bg-slate-800"
          >
            {item}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
