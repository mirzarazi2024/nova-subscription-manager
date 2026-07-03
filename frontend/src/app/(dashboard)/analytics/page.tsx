import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Users', 'value': '0', 'description': 'Sync pending'}, {'title': 'Providers', 'value': '0', 'description': 'Configured providers'}, {'title': 'Countries', 'value': '0', 'description': 'GeoIP pending'}, {'title': 'Traffic', 'value': 'N/A', 'description': 'Panel sync pending'}];
const sections = [{'title': 'Charts', 'body': 'Chart.js is available for dashboard visualizations once live data endpoints are populated.', 'items': ['Top providers', 'Top countries', 'Protocol distribution', 'Last updates']}, {'title': 'Data Sources', 'body': 'Analytics will aggregate Hiddify sync, provider ingestion and health engine results.'}];

export default function AnalyticsPage() {
  return <PageShell title="Analytics" description="Operational analytics for users, providers, countries, protocols and traffic." stats={stats} sections={sections} />;
}
