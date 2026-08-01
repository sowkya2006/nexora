"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { Cpu, Microchip, Briefcase, Atom, Users, Award, Download, ArrowRight } from "lucide-react";

const DEPARTMENTS = [
  {
    icon: Cpu,
    name: "Computer Science & Engineering (CSE)",
    facultyCount: "45+ Faculty",
    labs: "AI Research Lab, HPC Cluster, Cybersecurity Sim Labs",
    hod: "Dr. Rajesh Sharma (IIT Bombay)",
    desc: "Focuses on Machine Learning, Distributed Systems, Cloud Computing, and Blockchain.",
    doc: "http://localhost:8000/knowledge_base/Department_Handbook_CSE.pdf"
  },
  {
    icon: Microchip,
    name: "Electronics & Communication (ECE)",
    facultyCount: "38+ Faculty",
    labs: "VLSI Design Suite, Embedded Research, IoT Lab",
    hod: "Dr. Ananya Sen (IISc Bangalore)",
    desc: "Specializes in Signal Processing, VLSI Systems, Wireless Communications, and Robotics.",
    doc: "http://localhost:8000/knowledge_base/Department_Handbook_CSE.pdf"
  },
  {
    icon: Briefcase,
    name: "School of Business Management",
    facultyCount: "30+ Faculty",
    labs: "Financial Trading Lab, Incubation Center",
    hod: "Prof. Vikramaditya Rao (IIM Ahmedabad)",
    desc: "Provides case-study driven education in Finance, Marketing, and Business Analytics.",
    doc: "http://localhost:8000/knowledge_base/Department_Handbook_CSE.pdf"
  },
  {
    icon: Atom,
    name: "Basic Sciences & Humanities",
    facultyCount: "25+ Faculty",
    labs: "Advanced Physics Lab, Computational Math Center",
    hod: "Dr. Meenakshi Sundaram (IIT Madras)",
    desc: "Fosters fundamental science research, mathematics, and interdisciplinary humanities.",
    doc: "http://localhost:8000/knowledge_base/Department_Handbook_CSE.pdf"
  }
];

export default function DepartmentsPage() {
  return (
    <>
      <PageHero
        title="Departments & Faculty"
        description="World-class academic departments led by distinguished researchers and industry experts."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Departments" }]}
      />

      <Section>
        {/* Department Overview Cards */}
        <div className="grid gap-6 sm:grid-cols-2 mb-12">
          {DEPARTMENTS.map((dept) => (
            <div key={dept.name} className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-nexora-50 text-nexora-700">
                    <dept.icon className="h-5 w-5" />
                  </div>
                  <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                    <Users className="h-3 w-3 text-nexora-600" /> {dept.facultyCount}
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 text-lg">{dept.name}</h3>
                <p className="mt-1 text-xs text-slate-600 leading-relaxed">{dept.desc}</p>
                <div className="mt-3 text-xs text-slate-500 space-y-1 border-t border-slate-100 pt-3">
                  <p><span className="font-semibold text-slate-700">HOD:</span> {dept.hod}</p>
                  <p><span className="font-semibold text-slate-700">Labs:</span> {dept.labs}</p>
                </div>
              </div>

              <div className="mt-6 border-t border-slate-100 pt-4">
                <a
                  href={dept.doc}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-nexora-700 hover:text-nexora-900 transition"
                >
                  <Download className="h-3.5 w-3.5" /> Download Department Brochure
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Department Research Profiles & Faculty List?"
          description="UniSphere AI can answer specific questions regarding department labs, faculty research papers, ongoing projects, and PhD seats."
          suggestedQuestions={[
            "Who is the Head of Computer Science Department?",
            "What research labs are available in CSE?",
            "What are the research areas in Electronics Department?",
            "Does the business school have an incubation center?"
          ]}
          documentsCovered={[
            "Department Information & Faculty Guide 2026",
            "Research Publications & Patents Catalog",
            "Laboratory Equipment & Software Specs",
            "Faculty Academic Qualifications"
          ]}
        />
      </Section>
    </>
  );
}
