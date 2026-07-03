import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Rename', 'value': 'Custom', 'description': 'Node name template'}, {'title': 'Cache', 'value': 'Smart', 'description': 'Download provider once'}, {'title': 'Outputs', 'value': '5', 'description': 'Sing-box/Clash/Base64/Raw/V2Ray'}, {'title': 'Security', 'value': 'JWT', 'description': 'RBAC baseline'}];
const sections = [{'title': 'Subscription Settings', 'body': 'Configure default output format, NOVA URL prefix and node rename templates.', 'items': ['https://sub.novavpn.com/{uuid}', 'Country flags', 'Provider priority', 'Format selection']}, {'title': 'System Settings', 'body': 'Settings are designed for encrypted storage where sensitive.'}];

export default function SettingsPage() {
  return <PageShell title="Settings" description="Global NSM configuration for naming, output, cache and security behavior." stats={stats} sections={sections} />;
}
