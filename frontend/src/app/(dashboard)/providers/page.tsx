"use client";

import { useEffect, useState } from "react";

import { apiClient, getApiErrorMessage } from "@/lib/api/client";
import { authHeaders } from "@/lib/auth/token";

type Provider = {
  id: string;
  name: string;
  status: string;
  scoring_total: number;
};

export default function ProvidersPage() {
  const [providers, setProviders] = useState<Provider[]>([]);

  useEffect(() => {
    const loadProviders = async () => {
      try {
        const response = await apiClient.get<Provider[]>("/providers", {
          headers: await authHeaders(),
        });
        setProviders(response.data);
      } catch (err) {
        console.error(getApiErrorMessage(err));
        setProviders([]);
      }
    };

    void loadProviders();
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
