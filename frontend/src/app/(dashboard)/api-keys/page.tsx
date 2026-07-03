import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Keys', 'value': '0', 'description': 'No keys generated'}, {'title': 'Roles', 'value': 'RBAC', 'description': 'readonly/operator/admin'}, {'title': 'Expiry', 'value': 'Config', 'description': 'Optional expiration'}, {'title': 'Hashing', 'value': 'Planned', 'description': 'Secure key storage'}];
const sections = [{'title': 'API Access', 'body': 'Use API keys for automation and external systems once middleware is enabled.', 'items': ['Scoped roles', 'Revocation', 'Audit logs', 'Expiration']}, {'title': 'Security', 'body': 'Never expose panel API keys to API clients; use NSM-issued keys only.'}];

export default function APIKeysPage() {
  return <PageShell title="API Keys" description="Machine-to-machine API access with roles, expiry and revocation." stats={stats} sections={sections} />;
}
