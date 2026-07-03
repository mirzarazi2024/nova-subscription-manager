import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Level', 'value': 'INFO', 'description': 'Default structured logging'}, {'title': 'Backend', 'value': 'Loguru', 'description': 'Async-safe logging'}, {'title': 'Audit', 'value': 'Ready', 'description': 'Audit log table created'}, {'title': 'Retention', 'value': 'Config', 'description': 'Future setting'}];
const sections = [{'title': 'Application Logs', 'body': 'Backend emits structured logs through Loguru and stores operational records in the logs schema.', 'items': ['Provider refresh errors', 'Scheduler job results', 'API events', 'Security events']}, {'title': 'Audit Logs', 'body': 'Sensitive actions such as panel changes and API key operations should be tracked here.'}];

export default function LogsPage() {
  return <PageShell title="Logs" description="Central operational logs and application event stream." stats={stats} sections={sections} />;
}
