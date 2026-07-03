"use client";

import { useEffect, useState } from "react";

import { apiClient } from "@/lib/api/client";

type Provider = {
  id: string;
  name: string;
  status: string;
  scoring_total: number;
};

export default function ProvidersPage() {
  const [providers, setProviders] = useState<Provider[]>([]);

  useEffect(() => {
    apiClient
      .get<Provider[]>("/providers", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token") || ""}` },
      })
      .then((res) => setProviders(res.data))
      .catch(() => setProviders([]));
  }, []);

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">Providers</h2>
      <div className="rounded border border-slate-800">
        {providers.map((provider) => (
          <div key={provider.id} className="flex items-center justify-between border-b border-slate-800 p-3 last:border-b-0">
            <span>{provider.name}</span>
            <span className="text-sm text-slate-400">{provider.status} / score {provider.scoring_total.toFixed(2)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
