import { PageShell } from "@/components/ui/page-shell";

const stats = [{'title': 'Total Users', 'value': '0', 'description': 'Awaiting first Hiddify sync'}, {'title': 'Active', 'value': '0', 'description': 'Enabled NOVA subscriptions'}, {'title': 'Deleted', 'value': '0', 'description': 'Soft-deleted source users'}, {'title': 'Sync', 'value': '1 min', 'description': 'Scheduler target interval'}];
const sections = [{'title': 'User Synchronization', 'body': 'This module will detect new, updated and deleted users from Hiddify without touching its database.', 'items': ['REST API only', 'Per-user NOVA subscription UUID', 'Audit-friendly sync state']}, {'title': 'Operational Notes', 'body': 'Use Panels > Auto Detect first, then enable scheduler sync once the Hiddify Admin API test succeeds.'}];

export default function UsersPage() {
  return <PageShell title="Users" description="Hiddify users synchronized into NSM and mapped to NOVA subscription UUIDs." stats={stats} sections={sections} />;
}
