"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { TrendingUp, Award, Building2, Briefcase, Download, CheckCircle2 } from "lucide-react";

const RECRUITERS = ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro", "Accenture", "IBM", "Intel", "Deloitte", "Oracle", "Cisco"];

export default function PlacementsPage() {
  return (
    <>
      <PageHero
        title="Career & Placement Cell"
        description="Empowering students with industry internships, global placements, and career mentorship."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Placements" }]}
      />

      <Section>
        {/* Placement Key Stats */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-12">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Highest Package</p>
            <p className="text-3xl font-extrabold text-emerald-700 mt-2">₹44.5 LPA</p>
            <p className="text-xs text-slate-500 mt-1">International Placement</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Average Package</p>
            <p className="text-3xl font-extrabold text-nexora-800 mt-2">₹9.2 LPA</p>
            <p className="text-xs text-slate-500 mt-1">Across all B.Tech branches</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Placement Rate</p>
            <p className="text-3xl font-extrabold text-blue-700 mt-2">94.8%</p>
            <p className="text-xs text-slate-500 mt-1">Eligible students placed</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Recruiting Partners</p>
            <p className="text-3xl font-extrabold text-amber-700 mt-2">250+</p>
            <p className="text-xs text-slate-500 mt-1">Top MNCs & Tech Unicorns</p>
          </div>
        </div>

        {/* Major Recruiters */}
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm mb-12">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Major Recruiting Partners</h2>
              <p className="text-xs text-slate-500 mt-0.5">Top global technology, consulting, and core engineering corporations.</p>
            </div>
            <a
              href="http://localhost:8000/knowledge_base/Placement_Report_2026.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-sm"
            >
              <Download className="h-4 w-4" /> Download Placement Report
            </a>
          </div>

          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
            {RECRUITERS.map((r) => (
              <div key={r} className="flex h-16 items-center justify-center rounded-xl bg-slate-50 border border-slate-100 font-bold text-slate-700 text-sm hover:border-nexora-300 transition">
                {r}
              </div>
            ))}
          </div>
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Branch-Wise Placement Statistics?"
          description="UniSphere AI can answer specific questions regarding CSE median salaries, internship stipends, top visiting companies, and eligibility rules."
          suggestedQuestions={[
            "What is the average package for Computer Science graduates?",
            "Which companies visit Nexora for campus placements?",
            "What is the highest domestic package offered?",
            "What placement training programs are provided?"
          ]}
          documentsCovered={[
            "Annual Placement Report 2025-2026",
            "Recruiter Directory & Sector Breakdown",
            "Internship & Co-Op Guidelines",
            "Career Development Cell Overview"
          ]}
        />
      </Section>
    </>
  );
}
