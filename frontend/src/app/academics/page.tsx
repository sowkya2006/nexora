"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { BookOpen, Award, Download, ArrowRight, Cpu, Microchip, Briefcase, Atom, Calendar } from "lucide-react";

const SCHOOLS = [
  {
    icon: Cpu,
    name: "School of Computer Science & Engineering",
    desc: "B.Tech CSE, AI & Data Science, Cybersecurity, M.Tech, PhD.",
  },
  {
    icon: Microchip,
    name: "School of Electronics & Communication",
    desc: "B.Tech ECE, EEE, VLSI Systems, Embedded Research.",
  },
  {
    icon: Briefcase,
    name: "School of Business Administration",
    desc: "BBA, B.Com (Hons), MBA in Finance, Marketing & Analytics.",
  },
  {
    icon: Atom,
    name: "School of Humanities & Basic Sciences",
    desc: "B.Sc Mathematics, Physics, B.A. Journalism & Media.",
  },
];

export default function AcademicsPage() {
  return (
    <>
      <PageHero
        title="Academics & Research"
        description="Choice-based credit system, world-class faculty, and industry-aligned curricula."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Academics" }]}
      />

      <Section>
        {/* Schools Overview */}
        <h2 className="text-2xl font-bold text-slate-900 mb-6">Our Academic Schools</h2>
        <div className="grid gap-6 sm:grid-cols-2 mb-12">
          {SCHOOLS.map((school) => (
            <div key={school.name} className="flex gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-nexora-50 text-nexora-700">
                <school.icon className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-bold text-slate-900">{school.name}</h3>
                <p className="mt-1 text-xs text-slate-600 leading-relaxed">{school.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Academic Downloads & Resources */}
        <div className="rounded-2xl bg-slate-900 p-8 text-white shadow-xl mb-12">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Calendar className="h-5 w-5 text-nexora-300" /> Academic Schedules & Catalogs
              </h2>
              <p className="mt-1 text-xs text-slate-300 max-w-xl">
                Download the official academic calendar for term dates, exam windows, and semester schedules.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <a
                href="http://localhost:8000/knowledge_base/Academic_Calendar_2026.pdf"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl bg-nexora-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-nexora-700 shadow"
              >
                <Download className="h-4 w-4" /> Download Academic Calendar 2026
              </a>
              <a
                href="http://localhost:8000/knowledge_base/Course_Catalog_and_Programs.pdf"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-800 px-5 py-3 text-sm font-semibold text-slate-200 transition hover:bg-slate-700"
              >
                <Download className="h-4 w-4" /> Download Course Catalog
              </a>
            </div>
          </div>
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Subject-Wise Course Details?"
          description="Ask UniSphere AI about specific course credit requirements, elective offerings, grading policies, and attendance rules."
          suggestedQuestions={[
            "What courses are offered in Computer Science?",
            "What electives are available for B.Tech CSE?",
            "When do Fall semester exams start?",
            "What is the grading scheme and credit system?"
          ]}
          documentsCovered={[
            "Academic Course Catalog 2026",
            "Official Academic Calendar 2026-2027",
            "Choice Based Credit System (CBCS) Rules",
            "Examination & Attendance Policy"
          ]}
        />
      </Section>
    </>
  );
}
