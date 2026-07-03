import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Enabled Rules', 'value': '0', 'description': 'No custom rules yet'}, {'title': 'Actions', 'value': 'Reject', 'description': 'Reject / priority / rename'}, {'title': 'Latency', 'value': '>250ms', 'description': 'Example threshold'}, {'title': 'Provider', 'value': 'Score', 'description': 'Provider quality rules'}];
const sections = [{'title': 'Rule Examples', 'body': 'Create rules such as Country == RU reject, Latency > 250 reject, Reality priority +50.', 'items': ['Condition JSON', 'Action JSON', 'Ordered execution', 'Dashboard configurable']}, {'title': 'Pipeline', 'body': 'Rules run after normalization, deduplication, GeoIP and health checks.'}];

export default function RulesPage() {
  return <PageShell title="Rules" description="Configurable policy engine for rejecting, prioritizing and renaming nodes." stats={stats} sections={sections} />;
}
