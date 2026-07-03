import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'AzadNet', 'value': 'Ready', 'description': 'Catalog placeholder'}, {'title': 'SolVPN', 'value': 'Ready', 'description': 'Catalog placeholder'}, {'title': 'Free18', 'value': 'Ready', 'description': 'Catalog placeholder'}, {'title': 'GitHub', 'value': 'URLs', 'description': 'Raw provider sources'}];
const sections = [{'title': 'Provider Install', 'body': 'Marketplace will install provider URLs with category, priority, cache and health defaults.', 'items': ['AzadNet', 'SolVPN', 'V2RayAggregator', 'CodingBox']}, {'title': 'Extensibility', 'body': 'New marketplace entries can be added without changing merge engine internals.'}];

export default function MarketplacePage() {
  return <PageShell title="Marketplace" description="One-click provider marketplace for public and premium source catalogs." stats={stats} sections={sections} />;
}
