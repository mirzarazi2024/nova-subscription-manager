import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Provider Refresh', 'value': '1 min', 'description': 'Initial APScheduler job'}, {'title': 'User Sync', 'value': 'Planned', 'description': 'Hiddify sync interval'}, {'title': 'Health', 'value': 'Planned', 'description': 'TCP/TLS/Reality checks'}, {'title': 'Backups', 'value': 'Planned', 'description': 'Database/settings backups'}];
const sections = [{'title': 'Job Control', 'body': 'Scheduler jobs are designed for HA operation with future Redis distributed locks.', 'items': ['Run history', 'Next run', 'Status', 'Payload']}, {'title': 'Production Note', 'body': 'In multi-instance deployments, shared PostgreSQL and Redis avoid code changes.'}];

export default function SchedulerPage() {
  return <PageShell title="Scheduler" description="Background jobs for user sync, provider refresh, health checks and backups." stats={stats} sections={sections} />;
}
