"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  GraduationCap,
  BookOpen,
  Building2,
  Users,
  FileText,
  Bot,
  Bell,
  Calendar,
  Library,
  Briefcase,
  Home as HostelIcon,
  Settings,
  Sparkles,
  ChevronRight,
  ShieldCheck,
  Zap
} from "lucide-react";
import { UNIVERSITY } from "@/lib/constants";

export const SIDEBAR_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/admissions", label: "Admissions", icon: GraduationCap },
  { href: "/academics", label: "Academics", icon: BookOpen },
  { href: "/departments", label: "Departments", icon: Building2 },
  { href: "/faculty", label: "Faculty", icon: Users },
  { href: "/documents", label: "Documents", icon: FileText },
  { href: "/chat", label: "AI Assistant", icon: Bot, highlight: true },
  { href: "/notices", label: "Notices", icon: Bell },
  { href: "/events", label: "Events", icon: Calendar },
  { href: "/library", label: "Library", icon: Library },
  { href: "/placements", label: "Placements", icon: Briefcase },
  { href: "/hostel", label: "Hostel", icon: HostelIcon },
  { href: "/admin", label: "Settings", icon: Settings },
];

interface SidebarProps {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export function Sidebar({ mobileOpen = false, onCloseMobile }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-sm lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 flex w-72 flex-col border-r border-slate-200/80 bg-white transition-transform duration-300 ease-in-out lg:static lg:translate-x-0 ${
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Header Branding */}
        <div className="flex items-center gap-3 border-b border-slate-100 px-6 py-5">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-nexora-700 to-nexora-900 text-white font-extrabold text-lg shadow-md shadow-nexora-900/20">
            NU
          </div>
          <div>
            <h1 className="font-extrabold text-slate-900 text-base leading-tight tracking-tight">
              {UNIVERSITY.name}
            </h1>
            <div className="mt-0.5 flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[11px] font-semibold text-nexora-700">UniSphere OS v2.0</span>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
          <p className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            University Operating System
          </p>

          {SIDEBAR_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onCloseMobile}
                className={`group flex items-center justify-between rounded-2xl px-3.5 py-3 text-xs font-semibold transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-nexora-700 to-nexora-800 text-white shadow-md shadow-nexora-700/25"
                    : item.highlight
                    ? "bg-nexora-50/80 text-nexora-800 hover:bg-nexora-100/70 border border-nexora-200/60"
                    : "text-slate-600 hover:bg-slate-100/80 hover:text-slate-900"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon
                    className={`h-4 w-4 shrink-0 transition-transform group-hover:scale-110 ${
                      isActive ? "text-white" : item.highlight ? "text-nexora-700" : "text-slate-400 group-hover:text-slate-700"
                    }`}
                  />
                  <span>{item.label}</span>
                </div>
                {item.highlight && !isActive && (
                  <span className="rounded-full bg-nexora-600 px-2 py-0.5 text-[9px] font-extrabold text-white">
                    AI ACTIVE
                  </span>
                )}
                {isActive && <ChevronRight className="h-3.5 w-3.5 text-white/80" />}
              </Link>
            );
          })}

          {/* Quick AI Tip Widget */}
          <div className="pt-4">
            <div className="rounded-2xl border border-nexora-200/70 bg-gradient-to-br from-nexora-50/90 to-blue-50/50 p-4 shadow-sm">
              <div className="flex items-center gap-2 text-nexora-800">
                <Sparkles className="h-4 w-4 text-nexora-600 animate-spin" style={{ animationDuration: "8s" }} />
                <span className="text-xs font-bold">Quick AI Assistant</span>
              </div>
              <p className="mt-1.5 text-[11px] leading-relaxed text-slate-600">
                Ask UniSphere AI about admissions, fee structures, or hostel rules anytime.
              </p>
              <Link
                href="/chat"
                className="mt-3 inline-flex w-full items-center justify-center gap-1.5 rounded-xl bg-nexora-700 px-3 py-2 text-xs font-bold text-white shadow transition hover:bg-nexora-800"
              >
                <Zap className="h-3.5 w-3.5" /> Start Chat
              </Link>
            </div>
          </div>
        </div>

        {/* Footer User Profile Card */}
        <div className="border-t border-slate-100 p-4">
          <div className="flex items-center justify-between rounded-2xl bg-slate-50 p-3 border border-slate-200/60">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-purple-600 to-indigo-600 text-white font-bold text-xs shadow">
                SU
              </div>
              <div className="min-w-0">
                <p className="truncate text-xs font-bold text-slate-800">Student Portal</p>
                <p className="truncate text-[10px] text-slate-400">Nexora Academic 2026</p>
              </div>
            </div>
            <ShieldCheck className="h-4 w-4 text-emerald-600 shrink-0" />
          </div>
        </div>
      </aside>
    </>
  );
}
