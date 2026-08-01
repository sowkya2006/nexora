"use client";

import Link from "next/link";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { Wifi, ShieldCheck, Utensils, Shirt, Home, Download, ArrowRight, CheckCircle2 } from "lucide-react";

const HOSTEL_FACILITIES = [
  { icon: Home, title: "Modern Rooms", desc: "Fully furnished single, double, and triple sharing rooms with study desks." },
  { icon: Wifi, title: "High-Speed Wi-Fi", desc: "24/7 campus-wide optical fiber network for seamless digital learning." },
  { icon: Utensils, title: "Nutritious Dining", desc: "Hygienic mess serving balanced vegetarian & non-vegetarian meals 4 times daily." },
  { icon: ShieldCheck, title: "24/7 Campus Security", desc: "Biometric access control, CCTV coverage, and warden supervision." },
  { icon: Shirt, title: "In-House Laundry", desc: "Professional automated laundry and ironing facility for residents." },
];

export default function HostelPage() {
  return (
    <>
      <PageHero
        title="Hostel & Residential Life"
        description="A secure, comfortable home away from home with world-class residential amenities."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Hostel" }]}
      />

      <Section>
        {/* Hostel Overview & Highlights */}
        <div className="grid gap-8 lg:grid-cols-3 mb-12">
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-2xl font-bold text-slate-900">Student Residence Overview</h2>
            <p className="text-slate-600 text-sm leading-relaxed">
              Nexora University provides separate residential campuses for male and female students with round-the-clock security, medical support, recreation spaces, and dining facilities.
            </p>
            <div className="grid gap-4 sm:grid-cols-2 pt-2">
              <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <p className="text-xs font-medium text-slate-500">Accommodation Fee</p>
                <p className="text-xl font-bold text-nexora-800 mt-1">INR 75,000 / year</p>
                <p className="text-[11px] text-slate-400 mt-0.5">Includes Mess, Wi-Fi & Laundry</p>
              </div>
              <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <p className="text-xs font-medium text-slate-500">Security Deposit</p>
                <p className="text-xl font-bold text-slate-900 mt-1">INR 5,000</p>
                <p className="text-[11px] text-slate-400 mt-0.5">Refundable at check-out</p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-gradient-to-br from-nexora-900 to-slate-900 p-6 text-white flex flex-col justify-between shadow-lg">
            <div>
              <h3 className="text-lg font-bold text-white mb-2">Hostel Handbook</h3>
              <p className="text-xs text-nexora-100/90 leading-relaxed mb-6">
                Download the complete handbook containing residence guidelines, room allocation process, and dining menus.
              </p>
            </div>
            <a
              href="http://localhost:8000/knowledge_base/Hostel_Accommodation_Guide.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-nexora-900 transition hover:bg-nexora-50 shadow"
            >
              <Download className="h-4 w-4" /> Download Hostel Handbook
            </a>
          </div>
        </div>

        {/* Hostel Facilities */}
        <h2 className="text-xl font-bold text-slate-900 mb-6">Key Facilities</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-12">
          {HOSTEL_FACILITIES.map((f) => (
            <div key={f.title} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow transition">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-nexora-50 text-nexora-700 mb-3">
                <f.icon className="h-5 w-5" />
              </div>
              <h3 className="font-bold text-slate-900 text-sm">{f.title}</h3>
              <p className="mt-1 text-xs text-slate-500 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>

        {/* UniSphere AI Callout */}
        <UniSphereCallout
          title="Need Hostel Rules & Timings?"
          description="UniSphere AI can answer specific questions regarding curfew timings, mess schedules, visitor policies, room leave approvals, and night passes."
          suggestedQuestions={[
            "What is the hostel curfew timing?",
            "What is the hostel fee?",
            "What are the visitor lounge rules?",
            "Are cooking appliances allowed in rooms?"
          ]}
          documentsCovered={[
            "Hostel Rules & Regulations 2026",
            "Mess Menu & Dining Guidelines",
            "Visitor & Night Pass Rules",
            "Fee Payment & Refund Terms"
          ]}
        />
      </Section>
    </>
  );
}
