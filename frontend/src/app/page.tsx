"use client";

import Link from "next/link";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import {
  Bot,
  GraduationCap,
  BookOpen,
  Award,
  Sparkles,
  ArrowRight,
  Download,
  Calendar,
  Building2,
  TrendingUp,
  Globe,
  ChevronRight,
  CheckCircle2,
  FileText,
  ShieldCheck
} from "lucide-react";

const STATS = [
  { value: "15,000+", label: "Students Enrolled", description: "Across UG, PG, and PhD" },
  { value: "94.8%", label: "Placement Rate", description: "Top global recruiters" },
  { value: "250+", label: "Industry Partners", description: "MNCs & Research Labs" },
  { value: "100+", label: "Degree Programs", description: "Choice-Based Credit System" },
];

const SCHOOLS_DATA = [
  { title: "Computer Science & Engineering", description: "B.Tech CSE, AI & Data Science, Cybersecurity, M.Tech, PhD.", stats: "45+ Faculty · 3 Research Labs" },
  { title: "Electronics & Communication", description: "B.Tech ECE, EEE, VLSI Design, Embedded Systems Research.", stats: "38+ Faculty · 2 Research Centers" },
  { title: "School of Business Administration", description: "BBA, B.Com (Hons), MBA in Finance, Marketing & Analytics.", stats: "30+ Faculty · Incubation Center" },
  { title: "Humanities & Basic Sciences", description: "B.Sc Mathematics, Physics, B.A. Journalism & Mass Comm.", stats: "25+ Faculty · Interdisciplinary" },
];

const REASON_CARDS_DATA = [
  { title: "World-Class Curriculum", description: "Industry-aligned choice-based credit system (CBCS) updated annually." },
  { title: "Top Campus Placements", description: "Highest package of ₹44.5 LPA and average package of ₹9.2 LPA." },
  { title: "Advanced Research Labs", description: "AI High-Performance Computing clusters, VLSI suites, and Incubation." },
  { title: "Global Exposure", description: "International university collaborations, student exchanges, and guest lectures." },
];

export default function HomePage() {
  return (
    <div className="space-y-16 pb-16 animate-fade-in">
      {/* Storybook Hero Banner */}
      <section className="relative overflow-hidden bg-gradient-to-br from-[#44563E] via-[#384833] to-[#2B3927] py-20 text-white md:py-28">
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl text-center space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#D9B97A]/40 bg-[#4A5D45]/60 px-4 py-1.5 text-xs font-bold text-[#D9B97A] backdrop-blur-md">
              <Sparkles className="h-4 w-4 text-[#D9B97A] animate-pulse" />
              <span>Nexora University – Powered by UniSphere AI</span>
            </div>

            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl leading-tight">
              Shaping the Future through <span className="text-[#D9B97A]">Innovation & AI</span>
            </h1>

            <p className="mx-auto max-w-2xl text-base text-[#E2D9CB] sm:text-lg leading-relaxed font-medium">
              Explore world-class academic programs, pioneering research labs, and global career opportunities. Need specific answers? Ask our official AI assistant anytime.
            </p>

            <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
              <Link
                href="/chat"
                className="inline-flex items-center gap-3 rounded-2xl bg-[#FFFDF8] px-7 py-4 text-base font-bold text-[#44563E] shadow-lg transition hover:bg-[#F0EAE1] hover:-translate-y-0.5"
              >
                <Bot className="h-5 w-5 text-[#44563E]" />
                <span>Ask UniSphere AI</span>
                <ArrowRight className="h-4 w-4 text-[#D9B97A]" />
              </Link>
              <Link
                href="/admissions"
                className="inline-flex items-center gap-2 rounded-2xl border border-white/30 bg-white/10 px-7 py-4 text-base font-bold text-white transition hover:bg-white/20 backdrop-blur-sm"
              >
                <span>Explore Admissions</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-16">
        {/* Admissions Open Alert Banner */}
        <section className="storybook-card-static bg-gradient-to-r from-[#44563E] to-[#4A5D45] p-6 sm:p-8 text-white shadow-md">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div className="space-y-1">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#D9B97A]/20 px-3 py-0.5 text-xs font-bold text-[#D9B97A] border border-[#D9B97A]/30">
                Admissions 2026-2027 Open
              </span>
              <h2 className="text-xl font-extrabold sm:text-2xl text-white">Undergraduate & Postgraduate Applications Open</h2>
              <p className="text-xs text-[#E2D9CB]">Apply before May 30, 2026 for Merit Scholarships up to 50% tuition waiver.</p>
            </div>
            <div className="flex flex-wrap gap-3 shrink-0">
              <Link
                href="/admissions"
                className="inline-flex items-center gap-2 rounded-xl bg-[#FFFDF8] px-5 py-3 text-xs font-extrabold text-[#44563E] hover:bg-[#F0EAE1] transition shadow"
              >
                Apply Online <ArrowRight className="h-3.5 w-3.5" />
              </Link>
              <a
                href="/knowledge_base/Admission_Brochure_2026.pdf"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-5 py-3 text-xs font-semibold text-white hover:bg-white/20 transition"
              >
                <Download className="h-3.5 w-3.5" /> Download Brochure
              </a>
            </div>
          </div>
        </section>

        {/* Quick University Stats */}
        <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {STATS.map((stat) => (
            <div key={stat.label} className="storybook-card p-6 text-center space-y-1">
              <p className="text-3xl font-extrabold text-[#44563E]">{stat.value}</p>
              <p className="text-sm font-bold text-[#3E3A34]">{stat.label}</p>
              <p className="text-xs text-[#8C857C]">{stat.description}</p>
            </div>
          ))}
        </section>

        {/* Academic Schools */}
        <section className="space-y-6">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-2xl font-extrabold text-[#3E3A34] sm:text-3xl">Academic Schools</h2>
              <p className="text-xs text-[#8C857C]">Explore our multidisciplinary faculties and degree programs.</p>
            </div>
            <Link href="/academics" className="inline-flex items-center gap-1 text-xs font-bold text-[#44563E] hover:underline">
              View All Programs <ChevronRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {SCHOOLS_DATA.map((school) => (
              <div key={school.title} className="storybook-card p-6 flex flex-col justify-between">
                <div>
                  <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#F0EAE1] text-[#44563E] mb-3">
                    <GraduationCap className="h-5 w-5" />
                  </div>
                  <h3 className="font-extrabold text-[#3E3A34] text-base">{school.title}</h3>
                  <p className="mt-2 text-xs text-[#8C857C] leading-relaxed">{school.description}</p>
                </div>
                <div className="mt-4 border-t border-[#E7E0D4] pt-3">
                  <span className="text-[11px] font-bold text-[#44563E]">{school.stats}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Placements & Research Highlights */}
        <section className="grid gap-8 lg:grid-cols-2">
          <div className="storybook-card p-8 flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 rounded-full bg-[#F0EAE1] px-3.5 py-1 text-xs font-bold text-[#44563E]">
                <TrendingUp className="h-4 w-4 text-[#44563E]" /> Placement Highlights 2025-2026
              </div>
              <h3 className="text-2xl font-extrabold text-[#3E3A34]">Global Career Excellence</h3>
              <p className="text-xs text-[#8C857C] leading-relaxed">
                Nexora graduates are placed in leading multinational technology firms, global management consultancies, and research laboratories.
              </p>
              <div className="grid grid-cols-2 gap-4 pt-2">
                <div className="rounded-2xl bg-[#F8F4EC] p-4 border border-[#E7E0D4]">
                  <p className="text-xs text-[#8C857C]">Highest Package</p>
                  <p className="text-2xl font-extrabold text-[#44563E] mt-0.5">₹44.5 LPA</p>
                </div>
                <div className="rounded-2xl bg-[#F8F4EC] p-4 border border-[#E7E0D4]">
                  <p className="text-xs text-[#8C857C]">Average Package</p>
                  <p className="text-2xl font-extrabold text-[#44563E] mt-0.5">₹9.2 LPA</p>
                </div>
              </div>
            </div>
            <div className="border-t border-[#E7E0D4] pt-4">
              <Link href="/placements" className="inline-flex items-center gap-2 text-xs font-bold text-[#44563E] hover:underline">
                View Placement Statistics <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </div>

          <div className="storybook-card p-8 flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 rounded-full bg-[#F0EAE1] px-3.5 py-1 text-xs font-bold text-[#44563E]">
                <Globe className="h-4 w-4 text-[#44563E]" /> Campus Life & Facilities
              </div>
              <h3 className="text-2xl font-extrabold text-[#3E3A34]">World-Class Campus Ecosystem</h3>
              <p className="text-xs text-[#8C857C] leading-relaxed">
                Enjoy 24/7 security, high-speed Wi-Fi hostels, digital library access, sports complexes, and vibrant student clubs.
              </p>
              <div className="grid grid-cols-2 gap-4 pt-2">
                <div className="rounded-2xl bg-[#F8F4EC] p-4 border border-[#E7E0D4]">
                  <p className="text-xs text-[#8C857C]">Hostel Fee</p>
                  <p className="text-xl font-extrabold text-[#3E3A34] mt-0.5">₹75,000 / yr</p>
                </div>
                <div className="rounded-2xl bg-[#F8F4EC] p-4 border border-[#E7E0D4]">
                  <p className="text-xs text-[#8C857C]">Library Books</p>
                  <p className="text-xl font-extrabold text-[#3E3A34] mt-0.5">100,000+</p>
                </div>
              </div>
            </div>
            <div className="border-t border-[#E7E0D4] pt-4 flex gap-4 text-xs font-bold text-[#44563E]">
              <Link href="/hostel" className="hover:underline">Hostel Overview →</Link>
              <Link href="/library" className="hover:underline">Library Services →</Link>
            </div>
          </div>
        </section>

        {/* Why Choose Nexora */}
        <section className="space-y-6">
          <div className="text-center max-w-2xl mx-auto space-y-1">
            <h2 className="text-2xl font-extrabold text-[#3E3A34] sm:text-3xl">Why Choose Nexora University?</h2>
            <p className="text-xs text-[#8C857C]">Excellence in teaching, research, and career outcomes.</p>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {REASON_CARDS_DATA.map((card) => (
              <div key={card.title} className="storybook-card p-6 space-y-2">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#F0EAE1] text-[#44563E]">
                  <Award className="h-5 w-5" />
                </div>
                <h3 className="font-extrabold text-[#3E3A34] text-base">{card.title}</h3>
                <p className="text-xs text-[#8C857C] leading-relaxed">{card.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* UniSphere AI Assistant Banner */}
        <UniSphereCallout
          title="Have Questions About Nexora University?"
          description="UniSphere AI is trained on official university handbooks, hostel regulations, fee structures, and academic calendars. Ask any question to get immediate answers with page citations."
          suggestedQuestions={[
            "What is the hostel fee?",
            "What are the admission requirements?",
            "What are tuition fees for Computer Science?",
            "What courses are available?"
          ]}
          documentsCovered={[
            "Admission Handbook 2026-2027",
            "Annual Fee Structure 2026-2027",
            "Hostel Accommodation & Fee Rules",
            "Official Academic Calendar 2026",
            "Course Catalog & Electives List",
            "Department & Faculty Information"
          ]}
        />
      </div>
    </div>
  );
}

