"use client";

import { useEffect, useState } from "react";

import { apiClient, getApiErrorMessage } from "@/lib/api/client";
import { authHeaders } from "@/lib/auth/token";

type User = {
  id: string;
  hiddify_user_id: string;
  username: string;
  email: string | null;
  role: string;
  is_active: boolean;
};

type SyncResult = {
  created: number;
  updated: number;
  disabled: number;
  total_remote: number;
};

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get<User[]>("/users", { headers: await authHeaders() });
      setUsers(response.data);
      setError("");
    } catch (err) {
      setError(`Failed to load users: ${getApiErrorMessage(err)}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const syncUsers = async () => {
    setLoading(true);
    try {
      const response = await apiClient.post<SyncResult>("/users/sync", {}, { headers: await authHeaders() });
      setSyncResult(response.data);
      await loadUsers();
      setError("");
    } catch (err) {
      setError(`Sync failed: ${getApiErrorMessage(err)}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-2xl font-semibold">Users</h2>
          <p className="text-sm text-slate-400">Real users synced from Hiddify Admin API</p>
        </div>
        <button
          onClick={syncUsers}
          disabled={loading}
          className="rounded bg-blue-600 px-4 py-2 text-sm disabled:opacity-60"
        >
          {loading ? "Syncing..." : "Sync from Hiddify"}
        </button>
      </div>

      {syncResult && (
        <div className="rounded border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-200">
          created: {syncResult.created} | updated: {syncResult.updated} | disabled: {syncResult.disabled} | total remote:
          {" "}
          {syncResult.total_remote}
        </div>
      )}

      {error && <div className="rounded border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">{error}</div>}

      <div className="overflow-x-auto rounded border border-slate-800">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-900/80 text-slate-300">
            <tr>
              <th className="px-3 py-2 text-left">Username</th>
              <th className="px-3 py-2 text-left">Hiddify ID</th>
              <th className="px-3 py-2 text-left">Email</th>
              <th className="px-3 py-2 text-left">Role</th>
              <th className="px-3 py-2 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-t border-slate-800">
                <td className="px-3 py-2">{user.username}</td>
                <td className="px-3 py-2 text-xs text-slate-400">{user.hiddify_user_id}</td>
                <td className="px-3 py-2">{user.email || "-"}</td>
                <td className="px-3 py-2">{user.role}</td>
                <td className="px-3 py-2">{user.is_active ? "active" : "disabled"}</td>
              </tr>
            ))}
            {users.length === 0 && !loading && (
              <tr>
                <td colSpan={5} className="px-3 py-4 text-center text-slate-500">
                  No users yet. Click “Sync from Hiddify”.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
