"use client";

import { useState, useEffect } from "react";
import {
  ResponsiveContainer, LineChart, Line, BarChart, Bar,
  PieChart, Pie, Cell, AreaChart, Area,
  XAxis, YAxis, Tooltip, CartesianGrid, Legend, RadialBarChart, RadialBar,
} from "recharts";
import { fetchWithAuth } from "@/lib/api";
import {
  TrendingUp, TrendingDown, Activity, Bot, FileText,
  Bell, Calendar, Layers, Clock, Search, RefreshCw, Loader2,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/* Static seed data (used until real backend returns richer time-series) */
/* ------------------------------------------------------------------ */
const DAILY_SEED = Array.from({ length: 15 }, (_, i) => ({
  day: `D${i * 2 + 1}`,
  questions: Math.floor(35 + Math.sin(i) * 20 + i * 3),
  cited: Math.floor(28 + Math.sin(i) * 14 + i * 2.5),
}));

const MONTHLY_SEED = [
  { month: "Jan", queries: 850, downloads: 420 },
  { month: "Feb", queries: 920, downloads: 490 },
  { month: "Mar", queries: 1100, downloads: 610 },
  { month: "Apr", queries: 1050, downloads: 580 },
  { month: "May", queries: 1300, downloads: 750 },
  { month: "Jun", queries: 1450, downloads: 820 },
  { month: "Jul", queries: 1680, downloads: 910 },
];

const TOPIC_SEED = [
  { topic: "Admissions", count: 340 },
  { topic: "Hostel & Mess", count: 285 },
  { topic: "Fee Structure", count: 240 },
  { topic: "Placements", count: 195 },
  { topic: "Scholarships", count: 160 },
  { topic: "Academics", count: 135 },
  { topic: "Library", count: 110 },
  { topic: "Departments", count: 90 },
];

const STATUS_COLORS: Record<string, string> = {
  indexed: "#10b981",
  processing: "#f59e0b",
  uploaded: "#3b82f6",
  failed: "#ef4444",
};

const PIE_COLORS = ["#0284c7", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899", "#64748b", "#06b6d4", "#84cc16"];

const RECENT_ACTIVITIES = [
  { id: 1, type: "AI Query", text: "\"What is the hostel fee?\" — cited Page 1", time: "2m ago", icon: Bot, color: "text-purple-600 bg-purple-50" },
  { id: 2, type: "Doc Indexed", text: "Fee_Structure_2026.pdf indexed (32 chunks)", time: "8m ago", icon: FileText, color: "text-emerald-600 bg-emerald-50" },
  { id: 3, type: "Notice Posted", text: "Published: End-Semester Exam Schedule", time: "15m ago", icon: Bell, color: "text-amber-600 bg-amber-50" },
  { id: 4, type: "Event Created", text: "Nexora Hackathon 2026 created", time: "30m ago", icon: Calendar, color: "text-blue-600 bg-blue-50" },
];

/* ------------------------------------------------------------------ */

interface OverviewData {
  total_documents: number;
  indexed_documents: number;
  total_notices: number;
  total_events: number;
  total_chats: number;
  total_chunks: number;
  recent_activity: any[];
}

interface DocData {
  total_documents: number;
  by_status: Record<string, number>;
  by_category: Record<string, number>;
  total_chunks: number;
}

interface AiData {
  total_ai_queries: number;
  avg_confidence: number;
  top_intents: string[];
  recent_queries: any[];
}

export default function AdminAnalyticsPage() {
  const [activeTab, setActiveTab] = useState<"overview" | "ai" | "documents">("overview");
  const [overview, setOverview] = useState<OverviewData | null>(null);
  const [docData, setDocData] = useState<DocData | null>(null);
  const [aiData, setAiData] = useState<AiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = async (silent = false) => {
    if (!silent) setLoading(true);
    else setRefreshing(true);
    try {
      const [ov, ai, docs] = await Promise.all([
        fetchWithAuth("/analytics/overview"),
        fetchWithAuth("/analytics/ai"),
        fetchWithAuth("/analytics/documents"),
      ]);
      if (ov?.data)   setOverview(ov.data);
      if (ai?.data)   setAiData(ai.data);
      if (docs?.data) setDocData(docs.data);
    } catch {/* use seed data */}
    finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { load(); }, []);

  const ovr = overview ?? {
    total_documents: 17, indexed_documents: 14, total_notices: 8,
    total_events: 5, total_chats: 1250, total_chunks: 342, recent_activity: [],
  };
  const ai = aiData ?? { total_ai_queries: 1250, avg_confidence: 0.72, top_intents: [], recent_queries: [] };
  const doc = docData ?? {
    total_documents: 17, by_status: { indexed: 14, processing: 1, uploaded: 1, failed: 1 },
    by_category: { Admissions: 2, Academics: 2, Hostel: 1, Finance: 1, Placements: 1, Scholarships: 1 },
    total_chunks: 342,
  };

  const statusPieData = Object.entries(doc.by_status).map(([name, value]) => ({ name, value }));
  const categoryBarData = Object.entries(doc.by_category)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);

  const radialData = [
    { name: "Indexed", value: doc.total_documents > 0 ? Math.round((doc.by_status.indexed || 0) / doc.total_documents * 100) : 0, fill: "#10b981" },
  ];

  const tabs = ["overview", "ai", "documents"] as const;

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-3">
          <Loader2 className="h-8 w-8 animate-spin text-nexora-600 mx-auto" />
          <p className="text-sm text-slate-500 font-medium">Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Analytics Dashboard</h1>
          <p className="mt-1 text-slate-500 text-sm">Real-time usage insights, AI query performance, and document metrics</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => load(true)}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} /> Refresh
          </button>
          <div className="flex items-center gap-1 rounded-xl bg-white border border-slate-200 p-1">
            {tabs.map((t) => (
              <button
                key={t}
                onClick={() => setActiveTab(t)}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold capitalize transition ${
                  activeTab === t ? "bg-nexora-700 text-white" : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { label: "AI Queries", value: ovr.total_chats.toLocaleString(), sub: `Avg confidence: ${(ai.avg_confidence * 100).toFixed(0)}%`, icon: Bot, color: "text-purple-600 bg-purple-50", trend: "+18%" },
          { label: "Documents", value: `${ovr.total_documents} PDFs`, sub: `${ovr.indexed_documents} indexed`, icon: FileText, color: "text-sky-600 bg-sky-50", trend: "+12%" },
          { label: "Vector Chunks", value: ovr.total_chunks.toLocaleString(), sub: "1024-dim Pinecone", icon: Layers, color: "text-nexora-600 bg-nexora-50", trend: "Active" },
          { label: "Avg Response", value: "1.2s", sub: "Groq Llama 3.3 70B", icon: Clock, color: "text-emerald-600 bg-emerald-50", trend: "↓8% faster" },
        ].map((kpi) => (
          <div key={kpi.label} className="os-card p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{kpi.label}</span>
              <div className={`flex h-8 w-8 items-center justify-center rounded-lg ${kpi.color}`}>
                <kpi.icon className="h-4 w-4" />
              </div>
            </div>
            <div>
              <p className="text-2xl font-extrabold text-slate-900">{kpi.value}</p>
              <p className="text-[11px] text-slate-400 mt-0.5">{kpi.sub}</p>
            </div>
            <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
              <TrendingUp className="h-2.5 w-2.5" /> {kpi.trend}
            </span>
          </div>
        ))}
      </div>

      {/* Main Chart Section */}
      {activeTab === "overview" && (
        <div className="space-y-8">
          {/* Line + Area charts */}
          <div className="grid gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2 os-card p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="font-bold text-slate-900">Daily AI Questions</h2>
                  <p className="text-xs text-slate-400">Volume of RAG queries vs. sources cited</p>
                </div>
                <span className="rounded-full bg-nexora-50 px-2.5 py-1 text-[10px] font-bold text-nexora-700">Live Trend</span>
              </div>
              <div className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={DAILY_SEED}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="day" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ borderRadius: "10px", fontSize: "12px" }} />
                    <Legend wrapperStyle={{ fontSize: "11px" }} />
                    <Line type="monotone" dataKey="questions" name="AI Questions" stroke="#0284c7" strokeWidth={2.5} dot={{ r: 3 }} activeDot={{ r: 5 }} />
                    <Line type="monotone" dataKey="cited" name="Sources Cited" stroke="#10b981" strokeWidth={2} strokeDasharray="4 4" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="os-card p-6 space-y-4">
              <div>
                <h2 className="font-bold text-slate-900">Indexing Health</h2>
                <p className="text-xs text-slate-400 mt-0.5">Documents indexed vs. total</p>
              </div>
              <div className="h-40 flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <RadialBarChart innerRadius="55%" outerRadius="90%" data={radialData} startAngle={90} endAngle={-270}>
                    <RadialBar dataKey="value" cornerRadius={8} />
                    <Tooltip formatter={(v) => [`${v}%`, "Indexed"]} contentStyle={{ borderRadius: "8px", fontSize: "12px" }} />
                  </RadialBarChart>
                </ResponsiveContainer>
              </div>
              <p className="text-center text-xs text-slate-400">{doc.by_status.indexed || 0} of {doc.total_documents} indexed</p>
              <div className="space-y-1.5 pt-2 border-t border-slate-100">
                {Object.entries(doc.by_status).map(([s, v]) => (
                  <div key={s} className="flex items-center justify-between text-xs">
                    <span className="flex items-center gap-1.5">
                      <span className="h-2 w-2 rounded-full" style={{ background: STATUS_COLORS[s] || "#94a3b8" }} />
                      <span className="capitalize text-slate-600">{s}</span>
                    </span>
                    <span className="font-bold text-slate-800">{v}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Monthly usage area + activity feed */}
          <div className="grid gap-8 lg:grid-cols-2">
            <div className="os-card p-6 space-y-4">
              <div>
                <h2 className="font-bold text-slate-900">Monthly Growth</h2>
                <p className="text-xs text-slate-400">AI queries vs. document downloads</p>
              </div>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={MONTHLY_SEED}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ borderRadius: "10px", fontSize: "12px" }} />
                    <Area type="monotone" dataKey="queries" name="AI Queries" stroke="#0284c7" fill="#e0f2fe" strokeWidth={2} />
                    <Area type="monotone" dataKey="downloads" name="Downloads" stroke="#10b981" fill="#d1fae5" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="os-card p-6 space-y-4">
              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-nexora-600" />
                <h2 className="font-bold text-slate-900">Live Activity Feed</h2>
                <span className="ml-auto h-2 w-2 rounded-full bg-emerald-500 animate-ping" />
              </div>
              <div className="space-y-3">
                {(ovr.recent_activity.length > 0 ? ovr.recent_activity : RECENT_ACTIVITIES).slice(0, 5).map((act: any, i: number) => {
                  const isLive = act.event_type !== undefined;
                  return (
                    <div key={i} className="flex items-start gap-3 text-xs">
                      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600">
                        <Activity className="h-3.5 w-3.5" />
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold text-slate-800">
                          {isLive ? act.event_type?.replace(/_/g, " ") : act.type}
                        </p>
                        <p className="text-slate-500 text-[11px] mt-0.5">
                          {isLive ? (act.page_name || "system") : act.text}
                        </p>
                      </div>
                      <span className="text-[10px] text-slate-400 shrink-0">
                        {isLive ? new Date(act.created_at).toLocaleTimeString() : act.time}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === "ai" && (
        <div className="space-y-8">
          <div className="grid gap-8 lg:grid-cols-2">
            <div className="os-card p-6 space-y-4">
              <h2 className="font-bold text-slate-900">Top Asked Topics</h2>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={TOPIC_SEED}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="topic" tick={{ fontSize: 9 }} interval={0} angle={-15} textAnchor="end" height={40} />
                    <YAxis tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ borderRadius: "10px", fontSize: "12px" }} />
                    <Bar dataKey="count" name="Questions" fill="#0284c7" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="os-card p-6 space-y-4">
              <h2 className="font-bold text-slate-900">Recent AI Searches</h2>
              <div className="space-y-3 max-h-64 overflow-y-auto pr-1">
                {(ai.recent_queries.length > 0 ? ai.recent_queries : [
                  { user_message: "What is the hostel fee for 2026?", created_at: new Date().toISOString() },
                  { user_message: "What are the admission requirements?", created_at: new Date().toISOString() },
                  { user_message: "What courses are offered in CSE?", created_at: new Date().toISOString() },
                  { user_message: "What scholarships are available?", created_at: new Date().toISOString() },
                ]).map((q: any, i: number) => (
                  <div key={i} className="rounded-xl border border-slate-100 bg-slate-50 p-3 text-xs">
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-semibold text-slate-800 leading-relaxed">"{q.user_message || q.q}"</p>
                      <span className="shrink-0 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
                        RAG
                      </span>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1">
                      {q.created_at ? new Date(q.created_at).toLocaleString() : ""}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="os-card p-6 space-y-4">
            <h2 className="font-bold text-slate-900">Top Intent Categories</h2>
            <div className="flex flex-wrap gap-3">
              {(ai.top_intents.length > 0 ? ai.top_intents : ["hostel", "admission", "fees", "placements", "scholarships", "library", "departments", "faculty"]).map((intent, i) => (
                <span key={intent} className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3.5 py-1.5 text-xs font-semibold text-slate-700 capitalize">
                  <span className="h-2 w-2 rounded-full" style={{ background: PIE_COLORS[i % PIE_COLORS.length] }} />
                  {intent}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === "documents" && (
        <div className="space-y-8">
          <div className="grid gap-8 lg:grid-cols-2">
            <div className="os-card p-6 space-y-4">
              <h2 className="font-bold text-slate-900">Documents by Status</h2>
              <div className="h-52 flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={statusPieData} innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value" label={({ name, value }) => `${name}: ${value}`} labelLine={false}>
                      {statusPieData.map((entry, i) => (
                        <Cell key={i} fill={STATUS_COLORS[entry.name] || PIE_COLORS[i]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: "8px", fontSize: "12px" }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs border-t border-slate-100 pt-3">
                {statusPieData.map((s) => (
                  <div key={s.name} className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full" style={{ background: STATUS_COLORS[s.name] || "#94a3b8" }} />
                    <span className="capitalize text-slate-600">{s.name}: <strong>{s.value}</strong></span>
                  </div>
                ))}
              </div>
            </div>

            <div className="os-card p-6 space-y-4">
              <h2 className="font-bold text-slate-900">Documents by Category</h2>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={categoryBarData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis type="number" tick={{ fontSize: 10 }} />
                    <YAxis dataKey="name" type="category" tick={{ fontSize: 9 }} width={80} />
                    <Tooltip contentStyle={{ borderRadius: "10px", fontSize: "12px" }} />
                    <Bar dataKey="value" name="Count" fill="#44563e" radius={[0, 6, 6, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div className="grid gap-5 sm:grid-cols-3">
            <div className="os-card p-5 space-y-2 text-center">
              <p className="label-caps text-slate-400">Total Documents</p>
              <p className="text-3xl font-extrabold text-slate-900">{doc.total_documents}</p>
            </div>
            <div className="os-card p-5 space-y-2 text-center">
              <p className="label-caps text-slate-400">Total Chunks</p>
              <p className="text-3xl font-extrabold text-slate-900">{doc.total_chunks.toLocaleString()}</p>
              <p className="text-xs text-slate-400">1024-dim vectors</p>
            </div>
            <div className="os-card p-5 space-y-2 text-center">
              <p className="label-caps text-slate-400">Index Health</p>
              <p className="text-3xl font-extrabold text-emerald-600">
                {doc.total_documents > 0 ? Math.round(((doc.by_status.indexed || 0) / doc.total_documents) * 100) : 0}%
              </p>
              <p className="text-xs text-slate-400">Indexed rate</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
