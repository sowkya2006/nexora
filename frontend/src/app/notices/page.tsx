"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { notices as staticNotices } from "@/lib/data";
import { Bell, Calendar, Tag, ArrowRight, Loader2, AlertCircle } from "lucide-react";

interface NoticeItem {
  id: string;
  title: string;
  description: string;
  category: string;
  date: string;
  status: string;
  attachment_url?: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  Academic: "bg-blue-50 text-blue-700",
  Examination: "bg-amber-50 text-amber-700",
  Events: "bg-purple-50 text-purple-700",
  Administration: "bg-slate-100 text-slate-700",
};

export default function NoticesPage() {
  const [notices, setNotices] = useState<NoticeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("All");

  useEffect(() => {
    const fetchNotices = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
        const res = await fetch(`${API_URL}/notices/?status=published`);
        if (res.ok) {
          const data = await res.json();
          if (data?.notices?.length > 0) {
            setNotices(data.notices.map((n: any) => ({
              id: n.id,
              title: n.title,
              description: n.description || "",
              category: n.category || "Academic",
              date: n.published_at ? n.published_at.split("T")[0] : (n.created_at?.split("T")[0] || ""),
              status: n.status || "published",
              attachment_url: n.attachment_url,
            })));
            return;
          }
        }
      } catch { /* fall through */ }
      setNotices(staticNotices.map((n) => ({
        id: n.id, title: n.title, description: n.description,
        category: n.category, date: n.date, status: n.status,
        attachment_url: n.attachmentUrl,
      })));
    };
    fetchNotices().finally(() => setLoading(false));
  }, []);

  const categories = ["All", ...Array.from(new Set(notices.map((n) => n.category)))];
  const filtered = filter === "All" ? notices : notices.filter((n) => n.category === filter);

  return (
    <>
      <PageHero
        title="Official Notices & Announcements"
        description="Stay updated with university circulars, academic notices, and official announcements."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Notices" }]}
      />
      <Section>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Latest Announcements</h2>
            <p className="text-xs text-slate-400 mt-0.5">Live from the university notice board</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button key={cat} onClick={() => setFilter(cat)}
                className={`rounded-full px-3 py-1.5 text-xs font-semibold border transition ${
                  filter === cat
                    ? "bg-nexora-700 text-white border-nexora-700"
                    : "bg-white text-slate-600 border-slate-200 hover:border-nexora-400"
                }`}>
                {cat}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="h-6 w-6 animate-spin text-nexora-600 mr-2" />
            <span className="text-sm text-slate-400">Loading notices…</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center">
            <Bell className="h-8 w-8 text-slate-300 mx-auto mb-2" />
            <p className="text-slate-600 font-medium">No notices in this category.</p>
          </div>
        ) : (
          <div className="space-y-4 mb-12">
            {filtered.map((n) => (
              <div key={n.id} className="storybook-card p-5 flex flex-col sm:flex-row sm:items-center gap-4 justify-between">
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${CATEGORY_COLORS[n.category] || "bg-slate-100 text-slate-700"}`}>
                      <Tag className="h-3 w-3" /> {n.category}
                    </span>
                    {n.date && (
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <Calendar className="h-3 w-3" /> {n.date}
                      </span>
                    )}
                  </div>
                  <h3 className="font-bold text-slate-900 text-base">{n.title}</h3>
                  <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">{n.description}</p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {n.attachment_url && (
                    <a href={n.attachment_url} target="_blank" rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
                      View PDF
                    </a>
                  )}
                  <Link href="/chat"
                    className="inline-flex items-center gap-1.5 rounded-xl border border-[#E7E0D4] bg-[#F8F4EC] px-4 py-2 text-xs font-semibold text-[#44563E] hover:bg-[#F0EAE1] transition">
                    Ask AI <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}

        <UniSphereCallout
          title="Looking for Specific Notice Details?"
          description="UniSphere AI retrieves exact circulars, exam schedule notifications, fee deadlines, and holiday announcements from official documents."
          suggestedQuestions={[
            "What is the latest notice about examination registration?",
            "When is the fee payment deadline?",
            "What are the official guidelines for semester enrollment?",
            "What notices have been published for admissions?"
          ]}
          documentsCovered={["Official Circulars & Notifications", "Examination Registration Rules", "Fee Payment Circulars", "Holiday & Academic Announcements"]}
        />
      </Section>
    </>
  );
}
