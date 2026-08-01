"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { Sparkles, Download, ArrowRight, CheckCircle, GraduationCap, Globe, ShieldCheck, Mail, Calendar } from "lucide-react";

export default function AdmissionsPage() {
  return (
    <>
      <PageHero
        title="Admissions 2026-2027"
        description="Join a global community of innovators, researchers, and leaders at Nexora University."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Admissions" }]}
      />

      <Section>
        {/* Admissions Open Banner */}
        <div className="mb-10 rounded-2xl bg-gradient-to-r from-nexora-800 via-nexora-700 to-nexora-900 p-8 text-white shadow-xl">
          <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-300 border border-emerald-500/30 mb-3">
                <Sparkles className="h-3.5 w-3.5" /> Admissions Now Open for Academic Year 2026-2027
              </div>
              <h2 className="text-2xl font-bold sm:text-3xl">Begin Your Future at Nexora</h2>
              <p className="mt-1 text-sm text-nexora-100/90 max-w-xl">
                Applications are open for Undergraduate, Postgraduate, and Doctoral programs across Engineering, Business, Humanities, and Basic Sciences.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link
                href="/chat"
                className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-nexora-900 transition hover:bg-nexora-50 shadow-md"
              >
                Apply Online <ArrowRight className="h-4 w-4" />
              </Link>
              <a
                href="http://localhost:8000/knowledge_base/Admission_Handbook_2026.pdf"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl border border-white/30 bg-white/10 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/20 backdrop-blur-sm"
              >
                <Download className="h-4 w-4" /> Download Brochure
              </a>
            </div>
          </div>
        </div>

        {/* Quick Highlights */}
        <h2 className="text-xl font-bold text-slate-900 mb-6">Key Admission Highlights</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-12">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-nexora-50 text-nexora-700 mb-4">
              <Calendar className="h-5 w-5" />
            </div>
            <h3 className="font-semibold text-slate-900">Applications Open</h3>
            <p className="mt-1 text-xs text-slate-500">Apply for 2026 intake before May 30, 2026.</p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700 mb-4">
              <GraduationCap className="h-5 w-5" />
            </div>
            <h3 className="font-semibold text-slate-900">Merit Scholarships</h3>
            <p className="mt-1 text-xs text-slate-500">Up to 50% tuition waiver for top qualifying scorers.</p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-blue-700 mb-4">
              <Globe className="h-5 w-5" />
            </div>
            <h3 className="font-semibold text-slate-900">Global Applicants</h3>
            <p className="mt-1 text-xs text-slate-500">Dedicated desk & support for international students.</p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700 mb-4">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <h3 className="font-semibold text-slate-900">Transparent Process</h3>
            <p className="mt-1 text-xs text-slate-500">Online merit list declaration and counseling.</p>
          </div>
        </div>

        {/* Admission Timeline */}
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm mb-12">
          <h2 className="text-xl font-bold text-slate-900 mb-6 text-center">Admission Steps</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <div className="relative text-center p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-nexora-700 text-white font-bold text-sm mb-3">1</div>
              <h3 className="font-semibold text-slate-900 text-sm">Online Application</h3>
              <p className="mt-1 text-xs text-slate-500">Submit form & required academic details online.</p>
            </div>

            <div className="relative text-center p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-nexora-700 text-white font-bold text-sm mb-3">2</div>
              <h3 className="font-semibold text-slate-900 text-sm">Entrance / Verification</h3>
              <p className="mt-1 text-xs text-slate-500">NUXSAT exam or national entrance score review.</p>
            </div>

            <div className="relative text-center p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-nexora-700 text-white font-bold text-sm mb-3">3</div>
              <h3 className="font-semibold text-slate-900 text-sm">Merit Selection</h3>
              <p className="mt-1 text-xs text-slate-500">Online seat allocation & merit list declaration.</p>
            </div>

            <div className="relative text-center p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-emerald-600 text-white font-bold text-sm mb-3">4</div>
              <h3 className="font-semibold text-slate-900 text-sm">Seat Confirmation</h3>
              <p className="mt-1 text-xs text-slate-500">Fee payment and document verification.</p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-12">
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 rounded-xl bg-nexora-700 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-nexora-800 shadow-md"
          >
            Apply Now <ArrowRight className="h-4 w-4" />
          </Link>
          <a
            href="http://localhost:8000/knowledge_base/Admission_Handbook_2026.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 shadow-sm"
          >
            <Download className="h-4 w-4" /> Download Admission Handbook
          </a>
          <a
            href="mailto:admissions@nexorauniversity.edu"
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-100 px-6 py-3.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-200"
          >
            <Mail className="h-4 w-4" /> Contact Admissions Helpdesk
          </a>
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Detailed Admission Guidelines?"
          description="UniSphere AI can answer specific questions regarding course-wise cutoffs, reservation rules, fee refund policies, and document verification."
          suggestedQuestions={[
            "What is the exact eligibility for B.Tech CSE?",
            "What are the key admission dates for 2026?",
            "How do I apply for the Merit Scholarship?",
            "What is the application fee amount?"
          ]}
          documentsCovered={[
            "Admission Handbook 2026-2027",
            "NUXSAT Entrance Syllabus",
            "Scholarship & Financial Aid Rules",
            "Seat Matrix & Reservation Rules"
          ]}
        />
      </Section>
    </>
  );
}
