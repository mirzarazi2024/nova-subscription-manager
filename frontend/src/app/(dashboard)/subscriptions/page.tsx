"use client";

import { FormEvent, useState } from "react";

import { apiClient } from "@/lib/api/client";

type Preview = {
  hiddify_nodes: number;
  provider_nodes: Record<string, number>;
  duplicates_removed: number;
  rules_removed: number;
  final_nodes: number;
};

export default function SubscriptionsPage() {
  const [preview, setPreview] = useState<Preview | null>(null);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const userId = String(formData.get("userId") || "");
    const providerIds = String(formData.get("providerIds") || "")
      .split(",")
      .map((v) => v.trim())
      .filter(Boolean);

    const response = await apiClient.post<Preview>(
      "/subscriptions/preview",
      { user_id: userId, provider_ids: providerIds },
      { headers: { Authorization: `Bearer ${localStorage.getItem("token") || ""}` } },
    );
    setPreview(response.data);
  };

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">Subscription Preview</h2>
      <form onSubmit={onSubmit} className="mb-6 space-y-3 rounded border border-slate-800 p-4">
        <input name="userId" placeholder="User ID" className="w-full rounded bg-slate-900 p-2" />
        <input name="providerIds" placeholder="Provider IDs (comma separated)" className="w-full rounded bg-slate-900 p-2" />
        <button className="rounded bg-blue-600 px-4 py-2">Preview</button>
      </form>

      {preview && (
        <div className="space-y-2 rounded border border-slate-800 p-4 text-sm">
          <div>Hiddify nodes: {preview.hiddify_nodes}</div>
          <div>Provider nodes: {JSON.stringify(preview.provider_nodes)}</div>
          <div>Duplicates removed: {preview.duplicates_removed}</div>
          <div>Rules removed: {preview.rules_removed}</div>
          <div>Final nodes: {preview.final_nodes}</div>
        </div>
      )}
    </div>
  );
}
