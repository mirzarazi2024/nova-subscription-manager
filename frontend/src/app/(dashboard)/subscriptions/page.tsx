"use client";

import { FormEvent, useEffect, useState } from "react";

import { apiClient, getApiErrorMessage } from "@/lib/api/client";
import { authHeaders } from "@/lib/auth/token";

type User = {
  id: string;
  username: string;
  hiddify_user_id: string;
  is_active: boolean;
};

type Subscription = {
  id: string;
  user_id: string;
  uuid: string;
  source_hiddify_url: string | null;
  nova_url: string;
  format: string;
  is_active: boolean;
};

type Preview = {
  hiddify_nodes: number;
  provider_nodes: Record<string, number>;
  duplicates_removed: number;
  rules_removed: number;
  final_nodes: number;
};

export default function SubscriptionsPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [preview, setPreview] = useState<Preview | null>(null);
  const [error, setError] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [selectedUserId, setSelectedUserId] = useState<string>("");

  const loadData = async () => {
    try {
      const headers = await authHeaders();
      const [usersResponse, subscriptionsResponse] = await Promise.all([
        apiClient.get<User[]>("/users", { headers }),
        apiClient.get<Subscription[]>("/subscriptions", { headers }),
      ]);
      setUsers(usersResponse.data);
      setSubscriptions(subscriptionsResponse.data);
      if (!selectedUserId && usersResponse.data.length > 0) setSelectedUserId(usersResponse.data[0].id);
      setError("");
    } catch (err) {
      setError(`Failed to load subscriptions data: ${getApiErrorMessage(err)}`);
    }
  };

  useEffect(() => {
    void loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const syncUsers = async () => {
    try {
      await apiClient.post("/users/sync", {}, { headers: await authHeaders() });
      await loadData();
      setMessage("Users synced from Hiddify.");
    } catch (err) {
      setError(`User sync failed: ${getApiErrorMessage(err)}`);
    }
  };

  const createSubscription = async () => {
    if (!selectedUserId) {
      setError("Select a user first. If list is empty, click Sync Users.");
      return;
    }
    try {
      const response = await apiClient.post<Subscription>(
        "/subscriptions",
        { user_id: selectedUserId, format: "base64" },
        { headers: await authHeaders() },
      );
      setMessage(`NOVA subscription created: ${response.data.nova_url}`);
      await loadData();
    } catch (err) {
      setError(`Create subscription failed: ${getApiErrorMessage(err)}`);
    }
  };

  const onPreview = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const userId = String(formData.get("userId") || selectedUserId || "");
    const providerIds = String(formData.get("providerIds") || "")
      .split(",")
      .map((v) => v.trim())
      .filter(Boolean);

    try {
      const response = await apiClient.post<Preview>(
        "/subscriptions/preview",
        { user_id: userId, provider_ids: providerIds },
        { headers: await authHeaders() },
      );
      setPreview(response.data);
      setError("");
    } catch (err) {
      setError(`Preview failed: ${getApiErrorMessage(err)}`);
    }
  };

  return (
    <div className="space-y-6">
      <header>
        <h2 className="text-2xl font-semibold">Subscriptions</h2>
        <p className="text-sm text-slate-400">Create real NOVA subscription records for synced Hiddify users.</p>
      </header>

      {error && <div className="rounded border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">{error}</div>}
      {message && <div className="rounded border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-200">{message}</div>}

      <section className="rounded border border-slate-800 p-4">
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
          <h3 className="text-lg font-semibold">Create NOVA Subscription</h3>
          <button onClick={syncUsers} className="rounded bg-slate-700 px-3 py-2 text-sm">Sync Users</button>
        </div>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-[1fr_auto]">
          <select
            value={selectedUserId}
            onChange={(e) => setSelectedUserId(e.target.value)}
            className="rounded bg-slate-900 p-2"
          >
            <option value="">Select synced user</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username} — {user.hiddify_user_id}
              </option>
            ))}
          </select>
          <button onClick={createSubscription} className="rounded bg-blue-600 px-4 py-2">Create Link</button>
        </div>
      </section>

      <section className="rounded border border-slate-800 p-4">
        <h3 className="mb-3 text-lg font-semibold">Generated Links</h3>
        <div className="space-y-2">
          {subscriptions.map((subscription) => (
            <div key={subscription.id} className="rounded border border-slate-800 bg-slate-900/60 p-3 text-sm">
              <div className="font-medium text-white">{subscription.nova_url}</div>
              <div className="mt-1 text-xs text-slate-400">format: {subscription.format} | uuid: {subscription.uuid}</div>
              {subscription.source_hiddify_url && (
                <div className="mt-1 break-all text-xs text-slate-500">source: {subscription.source_hiddify_url}</div>
              )}
            </div>
          ))}
          {subscriptions.length === 0 && <div className="text-sm text-slate-500">No subscriptions yet.</div>}
        </div>
      </section>

      <section className="rounded border border-slate-800 p-4">
        <h3 className="mb-3 text-lg font-semibold">Preview Merge</h3>
        <form onSubmit={onPreview} className="space-y-3">
          <input name="userId" value={selectedUserId} onChange={(e) => setSelectedUserId(e.target.value)} placeholder="User ID" className="w-full rounded bg-slate-900 p-2" />
          <input name="providerIds" placeholder="Provider IDs (comma separated, optional)" className="w-full rounded bg-slate-900 p-2" />
          <button className="rounded bg-blue-600 px-4 py-2">Preview</button>
        </form>

        {preview && (
          <div className="mt-4 space-y-2 rounded border border-slate-800 p-4 text-sm">
            <div>Hiddify nodes: {preview.hiddify_nodes}</div>
            <div>Provider nodes: {JSON.stringify(preview.provider_nodes)}</div>
            <div>Duplicates removed: {preview.duplicates_removed}</div>
            <div>Rules removed: {preview.rules_removed}</div>
            <div>Final nodes: {preview.final_nodes}</div>
          </div>
        )}
      </section>
    </div>
  );
}
