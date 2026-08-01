"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { BookOpen, Clock, Laptop, ShieldCheck, Download, Search, FileText } from "lucide-react";

export default function LibraryPage() {
  return (
    <>
      <PageHero
        title="Central Library & Knowledge Resource Center"
        description="Over 100,000 physical volumes, digital journals, and round-the-clock research spaces."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Library" }]}
      />

      <Section>
        {/* Library Highlights */}
        <div className="grid gap-8 lg:grid-cols-3 mb-12">
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-2xl font-bold text-slate-900">Knowledge Center Overview</h2>
            <p className="text-slate-600 text-sm leading-relaxed">
              The Nexora Central Library offers quiet study zones, group discussion cubicles, high-speed digital terminals, and access to international journal databases (IEEE, Springer, ScienceDirect, JSTOR).
            </p>
            <div className="grid gap-4 sm:grid-cols-2 pt-2">
              <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm flex items-start gap-3">
                <Clock className="h-5 w-5 text-nexora-600 shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs font-semibold text-slate-900">Operating Hours</p>
                  <p className="text-xs text-slate-500 mt-0.5">Weekdays: 8:00 AM - 11:00 PM</p>
                  <p className="text-[11px] text-slate-400">Exams: 24/7 Reading Room</p>
                </div>
              </div>

              <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm flex items-start gap-3">
                <Laptop className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs font-semibold text-slate-900">Digital Library</p>
                  <p className="text-xs text-slate-500 mt-0.5">Off-campus VPN access</p>
                  <p className="text-[11px] text-slate-400">10,000+ e-journals & e-books</p>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-gradient-to-br from-nexora-900 to-slate-900 p-6 text-white flex flex-col justify-between shadow-lg">
            <div>
              <h3 className="text-lg font-bold text-white mb-2">Library Guide</h3>
              <p className="text-xs text-nexora-100/90 leading-relaxed mb-6">
                Download the official library handbook for borrowing limits, fine policies, and database access steps.
              </p>
            </div>
            <a
              href="http://localhost:8000/knowledge_base/Library_Guide_2026.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-nexora-900 transition hover:bg-nexora-50 shadow"
            >
              <Download className="h-4 w-4" /> Download Library Guide
            </a>
          </div>
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Borrowing Rules or Database Access Guides?"
          description="UniSphere AI can answer specific questions regarding book issue limits, renewal policies, late return fines, and remote e-journal credentials."
          suggestedQuestions={[
            "What are the library opening hours during exams?",
            "How many books can a B.Tech student borrow?",
            "How do I access IEEE e-journals off-campus?",
            "What is the late return fine per day?"
          ]}
          documentsCovered={[
            "Library Membership Rules 2026",
            "E-Resource Access Guidelines",
            "Circulation & Fine Policy",
            "Quiet Study & Discussion Room Rules"
          ]}
        />
      </Section>
    </>
  );
}
