"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

import { apiClient, getApiErrorMessage } from "@/lib/api/client";
import { authHeaders } from "@/lib/auth/token";

type PanelType = "hiddify" | "marzban" | "3x-ui" | "xray";

type Panel = {
  name: string;
  panel_type: PanelType;
  base_url: string;
  api_key_masked: string;
  enabled: boolean;
  verify_ssl: boolean;
  api_header_name: string;
  api_prefix: string;
  proxy_path: string;
  test_endpoint: string;
};

type TestResult = {
  success: boolean;
  message: string;
  status_code: number | null;
};

type AutoDetectResult = {
  success: boolean;
  detected_header_name: string;
  detected_prefix: string;
  detected_test_endpoint: string | null;
  working_endpoints: string[];
  message: string;
};

const defaultsByType: Record<PanelType, { api_header_name: string; api_prefix: string; test_endpoint: string }> = {
  hiddify: { api_header_name: "Hiddify-API-Key", api_prefix: "", test_endpoint: "/api/v2/admin/user/" },
  marzban: { api_header_name: "Authorization", api_prefix: "Bearer", test_endpoint: "/api/system" },
  "3x-ui": { api_header_name: "Authorization", api_prefix: "Bearer", test_endpoint: "/panel/api/inbounds/list" },
  xray: { api_header_name: "Authorization", api_prefix: "Bearer", test_endpoint: "/api/health" },
};

export default function PanelsPage() {
  const [panels, setPanels] = useState<Panel[]>([]);
  const [error, setError] = useState<string>("");
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [autoDetectResult, setAutoDetectResult] = useState<AutoDetectResult | null>(null);
  const [panelTypeForForm, setPanelTypeForForm] = useState<PanelType>("hiddify");
  const [panelTypeForTest, setPanelTypeForTest] = useState<PanelType>("hiddify");

  const formDefaults = useMemo(() => defaultsByType[panelTypeForForm], [panelTypeForForm]);
  const testDefaults = useMemo(() => defaultsByType[panelTypeForTest], [panelTypeForTest]);

  const loadPanels = async () => {
    try {
      const res = await apiClient.get<Panel[]>("/panels", {
        headers: await authHeaders(),
      });
      setPanels(res.data);
      setError("");
    } catch (err) {
      setError(`Failed to load panels: ${getApiErrorMessage(err)}`);
    }
  };

  useEffect(() => {
    void loadPanels();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onCreate = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const fd = new FormData(event.currentTarget);
    try {
      await apiClient.post(
        "/panels",
        {
          name: String(fd.get("name") || ""),
          panel_type: String(fd.get("panel_type") || "hiddify"),
          base_url: String(fd.get("base_url") || ""),
          api_key: String(fd.get("api_key") || ""),
          enabled: fd.get("enabled") === "on",
          verify_ssl: fd.get("verify_ssl") === "on",
          api_header_name: String(fd.get("api_header_name") || ""),
          api_prefix: String(fd.get("api_prefix") || ""),
          proxy_path: String(fd.get("proxy_path") || ""),
          test_endpoint: String(fd.get("test_endpoint") || ""),
        },
        { headers: await authHeaders() },
      );
      event.currentTarget.reset();
      setPanelTypeForForm("hiddify");
      await loadPanels();
    } catch (err) {
      setError(`Failed to create panel: ${getApiErrorMessage(err)}`);
    }
  };

  const onDelete = async (name: string) => {
    try {
      await apiClient.delete(`/panels/${name}`, {
        headers: await authHeaders(),
      });
      await loadPanels();
    } catch (err) {
      setError(`Failed to delete panel: ${getApiErrorMessage(err)}`);
    }
  };

  const onTestConnection = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const fd = new FormData(event.currentTarget);
    setTestResult(null);
    try {
      const response = await apiClient.post<TestResult>(
        "/panels/test-connection",
        {
          panel_type: String(fd.get("panel_type") || "hiddify"),
          base_url: String(fd.get("base_url") || ""),
          api_key: String(fd.get("api_key") || ""),
          verify_ssl: fd.get("verify_ssl") === "on",
          api_header_name: String(fd.get("api_header_name") || ""),
          api_prefix: String(fd.get("api_prefix") || ""),
          proxy_path: String(fd.get("proxy_path") || ""),
          test_endpoint: String(fd.get("test_endpoint") || ""),
        },
        { headers: await authHeaders() },
      );
      setTestResult(response.data);
      setError("");
    } catch (err) {
      setError(`Connection test failed: ${getApiErrorMessage(err)}`);
    }
  };

  const onAutoDetect = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const fd = new FormData(event.currentTarget);
    setAutoDetectResult(null);
    try {
      const response = await apiClient.post<AutoDetectResult>(
        "/panels/auto-detect",
        {
          panel_type: String(fd.get("panel_type") || "hiddify"),
          base_url: String(fd.get("base_url") || ""),
          api_key: String(fd.get("api_key") || ""),
          verify_ssl: fd.get("verify_ssl") === "on",
          proxy_path: String(fd.get("proxy_path") || ""),
        },
        { headers: await authHeaders() },
      );
      setAutoDetectResult(response.data);
      setError("");
    } catch (err) {
      setError(`Auto-detect failed: ${getApiErrorMessage(err)}`);
    }
  };

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold">Panels</h2>
      <p className="mb-4 text-sm text-slate-400">پنل‌ها قابل انتخاب هستند و هدر/API هر پنل قابل تنظیم است.</p>
      <div className="mb-6 rounded border border-blue-500/30 bg-blue-500/10 p-4 text-sm text-blue-100">
        برای Hiddify مقدار <b>Proxy Path for Admins</b> را در proxy_path بزن، نه Proxy Path for Clients. Header باید <code>Hiddify-API-Key</code> و prefix خالی باشد.
      </div>

      <form onSubmit={onCreate} className="mb-6 grid grid-cols-1 gap-3 rounded border border-slate-800 p-4 md:grid-cols-2">
        <input name="name" placeholder="Panel name" className="rounded bg-slate-900 p-2" required />
        <select name="panel_type" className="rounded bg-slate-900 p-2" value={panelTypeForForm} onChange={(e) => setPanelTypeForForm(e.target.value as PanelType)}>
          <option value="hiddify">hiddify</option>
          <option value="marzban">marzban</option>
          <option value="3x-ui">3x-ui</option>
          <option value="xray">xray</option>
        </select>
        <input name="base_url" placeholder="https://panel.example.com" className="rounded bg-slate-900 p-2" required />
        <input name="api_key" placeholder="API Key" className="rounded bg-slate-900 p-2" required />
        <input name="api_header_name" defaultValue={formDefaults.api_header_name} className="rounded bg-slate-900 p-2" placeholder="Header name" />
        <input name="api_prefix" defaultValue={formDefaults.api_prefix} className="rounded bg-slate-900 p-2" placeholder="Header prefix (optional)" />
        <input name="proxy_path" placeholder="proxy path (optional, e.g. admin)" className="rounded bg-slate-900 p-2" />
        <input name="test_endpoint" defaultValue={formDefaults.test_endpoint} className="rounded bg-slate-900 p-2" placeholder="test endpoint" />
        <label className="flex items-center gap-2 text-sm"><input name="enabled" type="checkbox" defaultChecked /> Enabled</label>
        <label className="flex items-center gap-2 text-sm"><input name="verify_ssl" type="checkbox" defaultChecked /> Verify SSL</label>
        <button className="rounded bg-blue-600 px-4 py-2 md:col-span-2">Add Panel</button>
      </form>

      <form onSubmit={onTestConnection} className="mb-6 grid grid-cols-1 gap-3 rounded border border-slate-800 p-4 md:grid-cols-2">
        <h3 className="md:col-span-2 text-lg font-semibold">Test Connection</h3>
        <select name="panel_type" className="rounded bg-slate-900 p-2" value={panelTypeForTest} onChange={(e) => setPanelTypeForTest(e.target.value as PanelType)}>
          <option value="hiddify">hiddify</option>
          <option value="marzban">marzban</option>
          <option value="3x-ui">3x-ui</option>
          <option value="xray">xray</option>
        </select>
        <input name="base_url" placeholder="https://panel.example.com" className="rounded bg-slate-900 p-2" required />
        <input name="api_key" placeholder="API Key" className="rounded bg-slate-900 p-2" required />
        <input name="api_header_name" defaultValue={testDefaults.api_header_name} className="rounded bg-slate-900 p-2" placeholder="Header name" />
        <input name="api_prefix" defaultValue={testDefaults.api_prefix} className="rounded bg-slate-900 p-2" placeholder="Header prefix" />
        <input name="proxy_path" placeholder="proxy path (optional)" className="rounded bg-slate-900 p-2" />
        <input name="test_endpoint" defaultValue={testDefaults.test_endpoint} className="rounded bg-slate-900 p-2" placeholder="test endpoint" />
        <label className="flex items-center gap-2 text-sm"><input name="verify_ssl" type="checkbox" defaultChecked /> Verify SSL</label>
        <button className="rounded bg-emerald-600 px-4 py-2 md:col-span-2">Test Connection</button>
      </form>

      <form onSubmit={onAutoDetect} className="mb-6 grid grid-cols-1 gap-3 rounded border border-slate-800 p-4 md:grid-cols-2">
        <h3 className="md:col-span-2 text-lg font-semibold">Auto Detect (Header + Endpoint)</h3>
        <select name="panel_type" className="rounded bg-slate-900 p-2" defaultValue="hiddify">
          <option value="hiddify">hiddify</option>
          <option value="marzban">marzban</option>
          <option value="3x-ui">3x-ui</option>
          <option value="xray">xray</option>
        </select>
        <input name="base_url" placeholder="https://panel.example.com" className="rounded bg-slate-900 p-2" required />
        <input name="api_key" placeholder="API Key" className="rounded bg-slate-900 p-2" required />
        <input name="proxy_path" placeholder="proxy path (optional)" className="rounded bg-slate-900 p-2" />
        <label className="flex items-center gap-2 text-sm"><input name="verify_ssl" type="checkbox" defaultChecked /> Verify SSL</label>
        <button className="rounded bg-violet-600 px-4 py-2 md:col-span-2">Auto Detect</button>
      </form>

      {autoDetectResult && (
        <div className={`mb-4 rounded border p-3 text-sm ${autoDetectResult.success ? "border-violet-500/30 bg-violet-500/10 text-violet-200" : "border-amber-500/30 bg-amber-500/10 text-amber-200"}`}>
          <div>{autoDetectResult.message}</div>
          <div className="text-xs opacity-90">header: {autoDetectResult.detected_header_name}</div>
          <div className="text-xs opacity-90">prefix: {autoDetectResult.detected_prefix || "(none)"}</div>
          <div className="text-xs opacity-90">test endpoint: {autoDetectResult.detected_test_endpoint || "-"}</div>
          <div className="text-xs opacity-90">working: {autoDetectResult.working_endpoints.join(", ") || "-"}</div>
        </div>
      )}

      {testResult && (
        <div className={`mb-4 rounded border p-3 text-sm ${testResult.success ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-200" : "border-amber-500/30 bg-amber-500/10 text-amber-200"}`}>
          <div>{testResult.message}</div>
          <div className="text-xs opacity-80">status: {String(testResult.status_code)}</div>
        </div>
      )}

      {error && <div className="mb-3 rounded border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">{error}</div>}

      <div className="space-y-2 rounded border border-slate-800 p-3">
        {panels.map((panel) => (
          <div key={panel.name} className="rounded border border-slate-800 p-3">
            <div className="flex items-center justify-between">
              <div className="font-semibold">{panel.name}</div>
              <button onClick={() => onDelete(panel.name)} className="rounded bg-red-600 px-3 py-1 text-sm">Delete</button>
            </div>
            <div className="mt-1 text-xs text-slate-400">
              {panel.panel_type} • {panel.base_url} • key: {panel.api_key_masked}
            </div>
            <div className="mt-1 text-xs text-slate-500">
              header: {panel.api_header_name} | prefix: {panel.api_prefix || "(none)"} | proxy_path: {panel.proxy_path || "(none)"} | test: {panel.test_endpoint}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
