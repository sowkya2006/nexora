"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  Bell,
  Calendar,
  BarChart3,
  Settings,
  LogOut,
} from "lucide-react";
import { logoutAdmin } from "@/lib/api";

const sidebarLinks = [
  { href: "/admin", label: "Dashboard", icon: LayoutDashboard },
  { href: "/admin/documents", label: "Documents", icon: FileText },
  { href: "/admin/notices", label: "Notices", icon: Bell },
  { href: "/admin/events", label: "Events", icon: Calendar },
  { href: "/admin/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/admin/settings", label: "Settings", icon: Settings },
];

export function AdminSidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    // Clear token + user from localStorage
    logoutAdmin();
    // Replace history so back button cannot return to admin
    router.replace("/admin/login");
  };

  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-[#384833] bg-[#44563E] text-white min-h-screen">
      {/* Header Branding */}
      <div className="border-b border-[#384833] p-6 space-y-1">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#D9B97A] text-[#44563E] font-extrabold text-sm shadow">
            NU
          </div>
          <div>
            <h2 className="text-base font-extrabold text-white tracking-tight">Nexora Admin</h2>
            <p className="text-[11px] font-semibold text-[#D9B97A]">Management Portal</p>
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 space-y-1.5 p-4">
        <p className="px-3 pb-1 text-[10px] font-bold uppercase tracking-wider text-[#A3B899]">
          Admin Operations
        </p>
        {sidebarLinks.map((link) => {
          const active = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-3 rounded-xl px-3.5 py-3 text-xs font-bold transition-all ${
                active
                  ? "bg-[#4A5D45] text-white shadow-sm border border-[#5B7155]"
                  : "text-[#D9E3D4] hover:bg-[#384833] hover:text-white"
              }`}
            >
              <link.icon className={`h-4 w-4 shrink-0 ${active ? "text-[#D9B97A]" : "text-[#A3B899]"}`} />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Logout Action */}
      <div className="border-t border-[#384833] p-4">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 rounded-xl px-3.5 py-3 text-xs font-bold text-[#D9E3D4] transition hover:bg-[#384833] hover:text-white"
        >
          <LogOut className="h-4 w-4 text-[#D9B97A]" />
          <span>Exit Admin Portal</span>
        </button>
      </div>
    </aside>
  );
}

export function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="storybook-card p-6 flex flex-col justify-between">
      <p className="text-xs font-bold text-[#8C857C] uppercase tracking-wider">{label}</p>
      <p className="mt-2 text-3xl font-extrabold text-[#44563E]">{value}</p>
    </div>
  );
}

