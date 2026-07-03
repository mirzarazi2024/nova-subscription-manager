import { StatCard } from "@/components/ui/stat-card";

export default function DashboardPage() {
  const activities = [
    "Hiddify Admin API profile configured with Hiddify-API-Key header",
    "Provider parser SDK ready for Base64, JSON and Raw URI sources",
    "Subscription preview API available at /api/v1/subscriptions/preview",
    "Prometheus metrics exposed at /metrics",
  ];

  return (
    <div className="space-y-6">
      <header className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-6">
        <p className="text-sm font-medium text-blue-400">Enterprise Control Plane</p>
        <h2 className="mt-2 text-3xl font-bold text-white">NOVA Subscription Manager</h2>
        <p className="mt-3 max-w-4xl text-sm leading-6 text-slate-400">
          NSM dynamically merges Hiddify subscriptions with unlimited external providers, removes duplicates,
          ranks nodes, and generates NOVA subscriptions through a clean API-first architecture.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Users" value="Sync Ready" description="Hiddify user sync pipeline endpoint prepared" />
        <StatCard title="Providers" value="Unlimited" description="Smart scoring and parser SDK baseline" />
        <StatCard title="Nodes" value="Dedup" description="SHA256 fingerprint duplicate detection" />
        <StatCard title="Health" value="/metrics" description="Prometheus instrumentation enabled" />
      </div>

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
          <h3 className="text-lg font-semibold">Current Sprint Capabilities</h3>
          <ul className="mt-4 space-y-3 text-sm text-slate-300">
            {activities.map((item) => (
              <li key={item} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">{item}</li>
            ))}
          </ul>
        </section>

        <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
          <h3 className="text-lg font-semibold">Next Production Milestones</h3>
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            <div>1. Real Hiddify user/domain/subscription sync jobs</div>
            <div>2. Provider node persistence and Redis smart cache</div>
            <div>3. Rule engine, health checks and output generators</div>
            <div>4. Hardened authentication, API keys and audit trail</div>
          </div>
        </section>
      </div>
    </div>
  );
}
