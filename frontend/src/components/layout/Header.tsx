"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, Search, Bot, BookOpen, Shield } from "lucide-react";
import { NAV_LINKS, UNIVERSITY } from "@/lib/constants";

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-[#E7E0D4] bg-[#FFFDF8]/95 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6 lg:px-8">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#44563E] text-white font-extrabold text-base shadow-sm group-hover:bg-[#384833] transition">
            NU
          </div>
          <div>
            <p className="text-sm font-extrabold text-[#3E3A34] tracking-tight">{UNIVERSITY.name}</p>
            <p className="text-[11px] font-semibold text-[#44563E]">UniSphere AI Portal</p>
          </div>
        </Link>

        {/* Public Website Navigation */}
        <nav className="hidden items-center gap-1 xl:flex">
          {NAV_LINKS.slice(0, 9).map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded-xl px-3 py-2 text-xs font-bold text-[#3E3A34] transition hover:bg-[#F0EAE1] hover:text-[#44563E]"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Public Actions & AI Shortcut */}
        <div className="flex items-center gap-2.5">
          <Link
            href="/documents"
            className="hidden rounded-xl border border-[#E7E0D4] bg-[#F8F4EC] p-2.5 text-[#3E3A34] transition hover:bg-[#F0EAE1] sm:flex"
            aria-label="Search documents"
          >
            <Search className="h-4 w-4" />
          </Link>

          <Link
            href="/chat"
            className="flex items-center gap-2 rounded-2xl bg-[#44563E] px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-[#384833]"
          >
            <Bot className="h-4 w-4 text-[#D9B97A]" />
            <span>Ask UniSphere AI</span>
          </Link>

          <Link
            href="/admin/login"
            className="hidden sm:inline-flex items-center gap-1.5 rounded-2xl border border-[#E7E0D4] bg-[#F8F4EC] px-3.5 py-2 text-xs font-bold text-[#3E3A34] hover:bg-[#F0EAE1] transition"
          >
            <Shield className="h-3.5 w-3.5 text-[#44563E]" /> Admin Login
          </Link>

          <button
            type="button"
            className="rounded-xl p-2.5 text-[#3E3A34] hover:bg-[#F0EAE1] xl:hidden"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav className="border-t border-[#E7E0D4] bg-[#FFFDF8] px-4 py-4 xl:hidden">
          <div className="grid grid-cols-2 gap-1.5">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-xl px-3 py-2 text-xs font-bold text-[#3E3A34] hover:bg-[#F0EAE1]"
                onClick={() => setMobileOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            <Link
              href="/admin/login"
              className="rounded-xl px-3 py-2 text-xs font-bold text-[#44563E] bg-[#F0EAE1] col-span-2 text-center mt-2"
              onClick={() => setMobileOpen(false)}
            >
              Admin Portal Login →
            </Link>
          </div>
        </nav>
      )}
    </header>
  );
}

