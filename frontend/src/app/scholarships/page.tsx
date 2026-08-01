"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { Award, DollarSign, Download, ArrowRight, CheckCircle2, ShieldCheck, HeartHandshake } from "lucide-react";

export default function ScholarshipsPage() {
  return (
    <>
      <PageHero
        title="Fee Structure & Scholarships"
        description="Affordable high-quality education with transparent fees and extensive merit-based financial aid."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Fees & Scholarships" }]}
      />

      <Section>
        {/* Annual Fee Highlights */}
        <h2 className="text-2xl font-bold text-slate-900 mb-6">Annual Tuition Fee Range</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-12">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">School of CSE</p>
            <p className="text-2xl font-bold text-nexora-800 mt-2">INR 1,80,000</p>
            <p className="text-xs text-slate-500 mt-1">Per academic year</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">School of ECE</p>
            <p className="text-2xl font-bold text-slate-900 mt-2">INR 1,60,000</p>
            <p className="text-xs text-slate-500 mt-1">Per academic year</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">School of Business</p>
            <p className="text-2xl font-bold text-slate-900 mt-2">INR 1,50,000</p>
            <p className="text-xs text-slate-500 mt-1">Per academic year</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Humanities & Sciences</p>
            <p className="text-2xl font-bold text-slate-900 mt-2">INR 90,000</p>
            <p className="text-xs text-slate-500 mt-1">Per academic year</p>
          </div>
        </div>

        {/* Scholarships & Loans Highlights */}
        <div className="grid gap-8 lg:grid-cols-3 mb-12">
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-2xl font-bold text-slate-900">Scholarships & Financial Assistance</h2>
            <div className="grid gap-4 sm:grid-cols-2 pt-2">
              <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700 mb-3">
                  <Award className="h-5 w-5" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">Merit Scholarship</h3>
                <p className="text-xs text-slate-500 mt-1">Up to 50% tuition fee waiver for students with 95%+ marks in qualifying exams.</p>
              </div>

              <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-50 text-blue-700 mb-3">
                  <HeartHandshake className="h-5 w-5" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm">Need-Based Assistance</h3>
                <p className="text-xs text-slate-500 mt-1">30% fee reduction for eligible students from families earning under INR 3.5 Lakhs/yr.</p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-gradient-to-br from-nexora-900 to-slate-900 p-6 text-white flex flex-col justify-between shadow-lg">
            <div>
              <h3 className="text-lg font-bold text-white mb-2">Official Fee Structure</h3>
              <p className="text-xs text-nexora-100/90 leading-relaxed mb-6">
                Download the official fee handbook containing exam fees, caution deposits, payment instalments, and loan approval details.
              </p>
            </div>
            <a
              href="http://localhost:8000/knowledge_base/Fee_Structure_2026.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-nexora-900 transition hover:bg-nexora-50 shadow"
            >
              <Download className="h-4 w-4" /> Download Fee Structure PDF
            </a>
          </div>
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Detailed Fee Breakups or Instalment Rules?"
          description="UniSphere AI can answer specific questions regarding exam fees, caution deposit refund rules, semester instalment deadlines, and scholarship criteria."
          suggestedQuestions={[
            "What are the tuition fees for B.Tech Computer Science?",
            "Is the caution deposit refundable?",
            "What are the eligibility rules for the 50% Merit Scholarship?",
            "Can tuition fees be paid in semester instalments?"
          ]}
          documentsCovered={[
            "Annual Fee Structure 2026-2027",
            "Scholarship & Financial Aid Scheme",
            "Educational Loan Partner Banks List",
            "Fee Payment & Refund Rules"
          ]}
        />
      </Section>
    </>
  );
}
