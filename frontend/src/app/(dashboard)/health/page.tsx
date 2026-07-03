import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Healthy Nodes', 'value': '0', 'description': 'Awaiting provider ingestion'}, {'title': 'Dead Nodes', 'value': '0', 'description': 'Health engine planned'}, {'title': 'Latency', 'value': 'N/A', 'description': 'TCP/TLS checks planned'}, {'title': 'Metrics', 'value': 'Live', 'description': '/metrics endpoint'}];
const sections = [{'title': 'Health Engine', 'body': 'Background checks will validate TCP, TLS, Reality, ping latency and packet loss.', 'items': ['Auto-disable dead nodes', 'Provider health score', 'Latency ranking', 'Packet loss']}, {'title': 'System Health', 'body': 'FastAPI /health and Prometheus /metrics are available now.'}];

export default function HealthPage() {
  return <PageShell title="Health" description="Node and system health overview for providers and merged subscriptions." stats={stats} sections={sections} />;
}
