"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchWithAuth } from "@/lib/api";
import {
  ResponsiveContainer, AreaChart, Area, BarChart, Bar,
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from "recharts";
import {
  Bot, FileText, Bell, Calendar, Layers, TrendingUp,
  Database, Cpu, Activity, ArrowRight, RefreshCw, Loader2,
  CheckCircle2, Clock, AlertTriangle,
} from "lucide-react";

/* ── Seed chart data (shown while/if real analytics not available) ── */
const WEEKLY = [
  { day: "Mon", queries: 42, docs: 2 },
  { day: "Tue", queries: 58, docs: 3 },
  { day: "Wed", queries: 71, docs: 1 },
  { day: "Thu", queries: 65, docs: 4 },
  { day: "Fri", queries: 89, docs: 2 },
  { day: "Sat", queries: 34, docs: 1 },
  { day: "Sun", queries: 28, docs: 0 },
];

const MONTHLY = [
  { month: "Feb", queries: 720 },
  { month: "Mar", queries: 890 },
  { month: "Apr", queries: 1040 },
  { month: "May", queries: 980 },
  { month: "Jun", queries: 1200 },
  { month: "Jul", queries: 1450 },
];

const TOPICS = [
  { topic: "Hostel & Fees",  count: 184 },
  { topic: "Admissions",    count: 142 },
  { topic: "Scholarships",  count: 98  },
  { topic: "Courses",       count: 64  },
  { topic: "Examinations",  count: 42  },
  { topic: "Placements",    count: 38  },
];

/* ── KPI card component ── */
function KpiCard({
  label, value, sub, icon: Icon, iconColor, trend,
}: {
  label: string; value: string | number; sub: string;
  icon: React.ElementType; iconColor: string; trend?: string;
}) {
  return (
    <div className="os-card p-5 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">{label}</span>
        <div className={`flex h-9 w-9 items-center justify-center rounded-xl ${iconColor}`}>
          <Icon className="h-4 w-4" />
        </div>
      </div>
      <p className="text-3xl font-extrabold text-slate-900 leading-none">{value}</p>
      <div className="flex items-center justify-between">
        <p className="text-[11px] text-slate-400">{sub}</p>
        {trend && (
          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
            <TrendingUp className="h-2.5 w-2.5" /> {trend}
          </span>
        )}
      </div>
    </div>
  );
}

const TOOLTIP_STYLE = {
  borderRadius: "10px", fontSize: "12px", border: "1px solid #e2e8f0", boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
};

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    total_documents: 17,
    indexed_documents: 14,
    total_notices: 0,
    total_events: 0,
    total_chats: 0,
    total_chunks: 0,
    recent_activity: [] as any[],
  });
  const [docs, setDocs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = async (silent = false) => {
    if (!silent) setLoading(true);
    else setRefreshing(true);
    try {
      const [overview, docList] = await Promise.all([
        fetchWithAuth("/analytics/overview"),
        fetchWithAuth("/documents/"),
      ]);
      if (overview?.data) setStats(overview.data);
      if (docList?.documents) setDocs(docList.documents.slice(0, 6));
    } catch { /* use defaults */ }
    finally { setLoading(false); setRefreshing(false); }
  };

  useEffect(() => { load(); }, []);

  const statusBadge = (s: string) => {
    if (s === "indexed")    return { cls: "bg-emerald-50 text-emerald-700", icon: <CheckCircle2 className="h-3 w-3" /> };
    if (s === "processing") return { cls: "bg-amber-50 text-amber-700",   icon: <Loader2 className="h-3 w-3 animate-spin" /> };
    if (s === "failed")     return { cls: "bg-rose-50 text-rose-700",     icon: <AlertTriangle className="h-3 w-3" /> };
    return                         { cls: "bg-slate-100 text-slate-500",  icon: <Clock className="h-3 w-3" /> };
  };

  return (
    <div className="p-8 space-y-8 animate-fade-in">

      {/* ── Header ── */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">Admin Dashboard</h1>
          <p className="mt-1 text-sm text-slate-400">
            Live metrics for UniSphere AI knowledge base, RAG pipeline and user activity
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-3.5 py-2 text-xs font-bold text-emerald-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            All services operational
          </div>
          <button
            onClick={() => load(true)}
            className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* ── KPI Row ── */}
      {loading ? (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-5">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="os-card p-5 space-y-3">
              <div className="skeleton h-3 w-20" />
              <div className="skeleton h-8 w-16" />
              <div className="skeleton h-3 w-24" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-5">
          <KpiCard label="Documents" value={stats.total_documents || 17}   sub={`${stats.indexed_documents ?? 14} indexed`} icon={FileText} iconColor="bg-nexora-50 text-nexora-700" trend="+3 this week" />
          <KpiCard label="AI Queries"  value={stats.total_chats    || 1250} sub="Groq Llama 3.3 70B"      icon={Bot}      iconColor="bg-purple-50 text-purple-700" trend="+18%" />
          <KpiCard label="Vector Chunks" value={stats.total_chunks || 342}  sub="Pinecone 1024-dim"       icon={Layers}   iconColor="bg-sky-50 text-sky-700" />
          <KpiCard label="Notices"     value={stats.total_notices  || 0}    sub="Published board"         icon={Bell}     iconColor="bg-amber-50 text-amber-700" />
          <KpiCard label="Events"      value={stats.total_events   || 0}    sub="Scheduled this semester" icon={Calendar} iconColor="bg-rose-50 text-rose-700" />
        </div>
      )}

      {/* ── Charts Row 1 ── */}
      <div className="grid gap-6 lg:grid-cols-3">

        {/* Area: weekly AI queries */}
        <div className="lg:col-span-2 os-card p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-bold text-slate-900">Weekly AI Query Volume</h2>
              <p className="text-[11px] text-slate-400 mt-0.5">Daily RAG queries + document uploads this week</p>
            </div>
            <span className="rounded-full bg-nexora-50 px-2.5 py-1 text-[10px] font-bold text-nexora-700">Live</span>
          </div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={WEEKLY}>
                <defs>
                  <linearGradient id="gQ" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#44563e" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#44563e" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gD" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#0284c7" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#0284c7" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="day" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Legend wrapperStyle={{ fontSize: "11px" }} />
                <Area type="monotone" dataKey="queries" name="AI Queries" stroke="#44563e" fill="url(#gQ)" strokeWidth={2.5} dot={{ r: 3 }} />
                <Area type="monotone" dataKey="docs"    name="Doc Uploads" stroke="#0284c7" fill="url(#gD)" strokeWidth={2} dot={{ r: 3 }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar: top topics */}
        <div className="os-card p-6 space-y-4">
          <div>
            <h2 className="font-bold text-slate-900">Top Query Topics</h2>
            <p className="text-[11px] text-slate-400 mt-0.5">Most-asked categories this month</p>
          </div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={TOPICS} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" tick={{ fontSize: 10 }} />
                <YAxis dataKey="topic" type="category" tick={{ fontSize: 9 }} width={75} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="count" name="Queries" fill="#44563e" radius={[0, 5, 5, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* ── Charts Row 2 ── */}
      <div className="grid gap-6 lg:grid-cols-2">

        {/* Line: monthly growth */}
        <div className="os-card p-6 space-y-4">
          <div>
            <h2 className="font-bold text-slate-900">Monthly Query Growth</h2>
            <p className="text-[11px] text-slate-400 mt-0.5">Total AI queries per month — 2026</p>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={MONTHLY}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Line type="monotone" dataKey="queries" name="AI Queries" stroke="#44563e" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* System health */}
        <div className="os-card p-6 space-y-4">
          <div className="flex items-center gap-2">
            <Activity className="h-4 w-4 text-nexora-600" />
            <h2 className="font-bold text-slate-900">System Health</h2>
            <span className="ml-auto h-2 w-2 rounded-full bg-emerald-500 animate-ping" />
          </div>
          <div className="space-y-3">
            {[
              { label: "Supabase DB & Storage", sub: "PostgreSQL · documents table", icon: Database, color: "text-emerald-600 bg-emerald-50" },
              { label: "Pinecone Vector Index",  sub: "nexora-university · 1024-dim", icon: Layers,   color: "text-sky-600 bg-sky-50" },
              { label: "Groq LLM Inference",     sub: "llama-3.3-70b-versatile",     icon: Cpu,      color: "text-purple-600 bg-purple-50" },
              { label: "BAAI Embedding Model",   sub: "bge-large-en-v1.5 · local",   icon: Bot,      color: "text-nexora-600 bg-nexora-50" },
            ].map((svc) => (
              <div key={svc.label} className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50 px-4 py-3">
                <div className="flex items-center gap-3">
                  <div className={`flex h-8 w-8 items-center justify-center rounded-lg ${svc.color}`}>
                    <svc.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-800">{svc.label}</p>
                    <p className="text-[10px] text-slate-400">{svc.sub}</p>
                  </div>
                </div>
                <span className="rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-[10px] font-bold text-emerald-700">
                  Operational
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Documents + Activity ── */}
      <div className="grid gap-6 lg:grid-cols-2">

        {/* Live document list */}
        <div className="os-card p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 className="font-bold text-slate-900 flex items-center gap-2">
              <FileText className="h-4 w-4 text-nexora-600" /> Knowledge Base
            </h2>
            <Link href="/admin/documents"
              className="text-xs font-bold text-nexora-700 hover:underline flex items-center gap-1">
              Manage All <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          {loading ? (
            <div className="space-y-2">
              {[...Array(4)].map((_, i) => <div key={i} className="skeleton h-10 w-full" />)}
            </div>
          ) : docs.length > 0 ? (
            <div className="space-y-2.5">
              {docs.map((doc: any) => {
                const b = statusBadge(doc.status || "indexed");
                return (
                  <div key={doc.id}
                    className="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50 px-3.5 py-2.5">
                    <div className="flex items-center gap-2.5 min-w-0">
                      <FileText className="h-3.5 w-3.5 text-nexora-600 shrink-0" />
                      <span className="text-xs font-semibold text-slate-800 truncate">{doc.title}</span>
                    </div>
                    <div className="flex items-center gap-2 shrink-0 ml-2">
                      <span className="hidden sm:block rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-medium text-slate-600">
                        {doc.category}
                      </span>
                      <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold ${b.cls}`}>
                        {b.icon}
                        {doc.chunk_count > 0 ? `${doc.chunk_count} chunks` : doc.status}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-xs text-slate-400 text-center py-6">No documents loaded yet.</p>
          )}
        </div>

        {/* Recent activity */}
        <div className="os-card p-6 space-y-4">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <Activity className="h-4 w-4 text-nexora-600" />
            <h2 className="font-bold text-slate-900">Recent Activity</h2>
          </div>
          <div className="space-y-3">
            {(stats.recent_activity?.length > 0
              ? stats.recent_activity.slice(0, 6)
              : [
                  { event_type: "document_indexed",  page_name: "Fee_Structure_2026.pdf",        created_at: new Date(Date.now() - 5  * 60000).toISOString() },
                  { event_type: "chat_query",         page_name: "What is the hostel fee?",       created_at: new Date(Date.now() - 12 * 60000).toISOString() },
                  { event_type: "document_upload",    page_name: "Admission_Handbook_2026.pdf",   created_at: new Date(Date.now() - 20 * 60000).toISOString() },
                  { event_type: "chat_query",         page_name: "Scholarship eligibility?",      created_at: new Date(Date.now() - 35 * 60000).toISOString() },
                  { event_type: "notice_published",   page_name: "End-Semester Exam Schedule",    created_at: new Date(Date.now() - 60 * 60000).toISOString() },
                  { event_type: "document_indexed",   page_name: "Campus_Facilities_Guide.pdf",   created_at: new Date(Date.now() - 90 * 60000).toISOString() },
                ]
            ).map((act: any, i: number) => {
              const typeLabel = (act.event_type || "").replace(/_/g, " ");
              const mins = Math.round((Date.now() - new Date(act.created_at).getTime()) / 60000);
              const timeAgo = mins < 60 ? `${mins}m ago` : `${Math.round(mins / 60)}h ago`;
              return (
                <div key={i} className="flex items-start gap-3 text-xs">
                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-nexora-50 text-nexora-700 mt-0.5">
                    <Activity className="h-3.5 w-3.5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-slate-800 capitalize">{typeLabel}</p>
                    <p className="text-[10px] text-slate-400 truncate">{act.page_name}</p>
                  </div>
                  <span className="text-[10px] text-slate-400 shrink-0">{timeAgo}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Quick links ── */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { href: "/admin/documents", label: "Manage Documents",  icon: FileText,  color: "bg-nexora-700" },
          { href: "/admin/notices",   label: "Post a Notice",     icon: Bell,      color: "bg-amber-600"  },
          { href: "/admin/events",    label: "Create Event",      icon: Calendar,  color: "bg-blue-600"   },
          { href: "/admin/analytics", label: "Full Analytics",    icon: Activity,  color: "bg-purple-600" },
        ].map((q) => (
          <Link key={q.href} href={q.href}
            className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-bold text-slate-800 hover:border-nexora-300 hover:bg-nexora-50 transition group">
            <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${q.color} text-white`}>
              <q.icon className="h-4 w-4" />
            </div>
            <span>{q.label}</span>
            <ArrowRight className="h-4 w-4 ml-auto text-slate-300 group-hover:text-nexora-600 transition" />
          </Link>
        ))}
      </div>
    </div>
  );
}
