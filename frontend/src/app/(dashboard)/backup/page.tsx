import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Database', 'value': 'Planned', 'description': 'PostgreSQL dumps'}, {'title': 'Settings', 'value': 'Planned', 'description': 'Encrypted configuration'}, {'title': 'Providers', 'value': 'Planned', 'description': 'Provider catalog'}, {'title': 'Rules', 'value': 'Planned', 'description': 'Policy exports'}];
const sections = [{'title': 'Backup Scope', 'body': 'Backups will include database state, provider definitions, settings and rule engine configuration.', 'items': ['Checksum', 'Storage URL', 'Backup type', 'Status']}, {'title': 'Restore', 'body': 'Restore workflows will be added after persistence pipelines mature.'}];

export default function BackupPage() {
  return <PageShell title="Backup" description="Automatic backup management for database, settings, providers and rules." stats={stats} sections={sections} />;
}
