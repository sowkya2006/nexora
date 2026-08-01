"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, Search, Bot, Menu, Sparkles, Calendar as CalendarIcon, User, Shield } from "lucide-react";

interface TopHeaderProps {
  onToggleMobileSidebar: () => void;
}

export function TopHeader({ onToggleMobileSidebar }: TopHeaderProps) {
  const pathname = usePathname();
  const [currentDateTime, setCurrentDateTime] = useState<string>("");
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const options: Intl.DateTimeFormatOptions = {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      setCurrentDateTime(now.toLocaleDateString("en-US", options));
    };
    updateTime();
    const interval = setInterval(updateTime, 30000);
    return () => clearInterval(interval);
  }, []);

  const getPageTitle = () => {
    if (pathname === "/") return "Student Dashboard";
    if (pathname.startsWith("/admissions")) return "Admissions & Eligibility Portal";
    if (pathname.startsWith("/academics")) return "Academic Programs & Curriculum";
    if (pathname.startsWith("/departments")) return "Academic Departments";
    if (pathname.startsWith("/faculty")) return "Faculty Directory";
    if (pathname.startsWith("/documents")) return "Knowledge Base Documents";
    if (pathname.startsWith("/chat")) return "UniSphere AI Assistant";
    if (pathname.startsWith("/notices")) return "Official University Notices";
    if (pathname.startsWith("/events")) return "Campus Events & Calendar";
    if (pathname.startsWith("/library")) return "Digital Library & Resources";
    if (pathname.startsWith("/placements")) return "Placement & Career Center";
    if (pathname.startsWith("/hostel")) return "Hostel & Housing Services";
    if (pathname.startsWith("/admin")) return "System Administrator Center";
    return "Nexora University Portal";
  };

  return (
    <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200/80 bg-white/90 px-6 backdrop-blur-md">
      <div className="flex items-center gap-4">
        <button
          onClick={onToggleMobileSidebar}
          className="rounded-xl border border-slate-200 p-2.5 text-slate-600 hover:bg-slate-100 lg:hidden"
          aria-label="Toggle Navigation"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">{getPageTitle()}</h1>
            <span className="hidden rounded-full bg-nexora-50 px-2.5 py-0.5 text-[10px] font-bold text-nexora-700 sm:inline-block border border-nexora-200/60">
              Live Portal
            </span>
          </div>
          <p className="text-xs text-slate-400">Nexora University Intelligent AI Operating System</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Date & Time Widget */}
        <div className="hidden items-center gap-2 rounded-2xl border border-slate-200/80 bg-slate-50/80 px-3.5 py-2 text-xs font-semibold text-slate-600 sm:flex shadow-inner">
          <CalendarIcon className="h-4 w-4 text-nexora-600" />
          <span>{currentDateTime || "Aug 1, 2026"}</span>
        </div>

        {/* Global AI Chat Shortcut */}
        <Link
          href="/chat"
          className="flex items-center gap-2 rounded-2xl bg-gradient-to-r from-nexora-700 to-nexora-900 px-4 py-2.5 text-xs font-bold text-white shadow-md transition hover:shadow-lg hover:-translate-y-0.5"
        >
          <Bot className="h-4 w-4 text-nexora-200" />
          <span className="hidden sm:inline">Ask UniSphere AI</span>
        </Link>

        {/* Notification Bell Badge */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative rounded-2xl border border-slate-200 p-2.5 text-slate-600 hover:bg-slate-100 transition shadow-xs"
            aria-label="Notifications"
          >
            <Bell className="h-5 w-5" />
            <span className="absolute top-1.5 right-1.5 h-2.5 w-2.5 rounded-full bg-nexora-600 ring-2 ring-white" />
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-3 w-80 rounded-2xl border border-slate-200 bg-white p-4 shadow-xl z-50 animate-fade-in space-y-3">
              <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                <h3 className="text-xs font-bold text-slate-900">Notifications</h3>
                <span className="rounded-full bg-nexora-100 px-2 py-0.5 text-[10px] font-bold text-nexora-800">2 New</span>
              </div>
              <div className="space-y-2">
                <div className="rounded-xl bg-slate-50 p-2.5 text-xs border border-slate-100">
                  <p className="font-semibold text-slate-800">Admissions 2026 Open</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">Submit applications before May 30 for merit waivers.</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-2.5 text-xs border border-slate-100">
                  <p className="font-semibold text-slate-800">Updated Hostel Fees Document</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">Hostel_Rules_and_Fees_2026.pdf indexed into RAG pipeline.</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* User Profile Avatar */}
        <Link href="/admin" className="flex items-center gap-2.5 rounded-2xl border border-slate-200/80 bg-slate-50/80 p-1.5 pr-3 hover:bg-slate-100 transition shadow-xs">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-nexora-700 to-indigo-700 text-white font-bold text-xs shadow">
            NU
          </div>
          <div className="hidden text-left md:block">
            <p className="text-xs font-bold text-slate-800 leading-tight">University Portal</p>
            <p className="text-[10px] text-slate-400 font-medium">Administrator</p>
          </div>
        </Link>
      </div>
    </header>
  );
}
