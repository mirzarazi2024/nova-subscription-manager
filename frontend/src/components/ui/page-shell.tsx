import { StatCard } from "./stat-card";

type PageShellProps = {
  title: string;
  description: string;
  stats?: Array<{ title: string; value: string; description: string }>;
  sections?: Array<{ title: string; body: string; items?: string[] }>;
};

export function PageShell({ title, description, stats = [], sections = [] }: PageShellProps) {
  return (
    <div className="space-y-6">
      <header>
        <p className="text-sm font-medium text-blue-400">NOVA Subscription Manager</p>
        <h2 className="mt-2 text-3xl font-bold tracking-tight text-white">{title}</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">{description}</p>
      </header>

      {stats.length > 0 && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          {stats.map((stat) => (
            <StatCard key={stat.title} {...stat} />
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        {sections.map((section) => (
          <section key={section.title} className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
            <h3 className="text-lg font-semibold text-white">{section.title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">{section.body}</p>
            {section.items && (
              <ul className="mt-4 space-y-2 text-sm text-slate-300">
                {section.items.map((item) => (
                  <li key={item} className="flex gap-2">
                    <span className="mt-2 h-1.5 w-1.5 rounded-full bg-blue-400" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        ))}
      </div>
    </div>
  );
}
