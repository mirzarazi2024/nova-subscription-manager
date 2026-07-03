import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Countries', 'value': '0', 'description': 'Detected from providers'}, {'title': 'Flags', 'value': 'Auto', 'description': 'Emoji flags generated'}, {'title': 'GeoIP', 'value': 'Ready', 'description': 'GeoIP2 integration shell'}, {'title': 'Timezone', 'value': 'Auto', 'description': 'Per-node metadata'}];
const sections = [{'title': 'Country Detection', 'body': 'NSM will enrich nodes from IP, hostname and SNI using GeoIP and fallback heuristics.', 'items': ['Country code', 'City', 'Flag', 'Continent', 'Timezone']}, {'title': 'Filtering', 'body': 'Country metadata feeds the rule engine for reject/priority/rename decisions.'}];

export default function CountriesPage() {
  return <PageShell title="Countries" description="GeoIP country, flag, city, continent and timezone enrichment for every normalized node." stats={stats} sections={sections} />;
}
