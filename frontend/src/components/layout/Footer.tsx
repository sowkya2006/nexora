import Link from "next/link";
import { Mail, Phone, MapPin } from "lucide-react";
import { NAV_LINKS, UNIVERSITY } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-slate-200 bg-nexora-900 text-slate-300">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div>
            <h3 className="text-lg font-bold text-white">{UNIVERSITY.name}</h3>
            <p className="mt-2 text-sm leading-relaxed">{UNIVERSITY.shortDescription}</p>
          </div>
          <div>
            <h4 className="mb-3 font-semibold text-white">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              {NAV_LINKS.slice(0, 6).map((link) => (
                <li key={link.href}>
                  <Link href={link.href} className="hover:text-white transition">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="mb-3 font-semibold text-white">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/documents" className="hover:text-white transition">Document Library</Link></li>
              <li><Link href="/chat" className="hover:text-white transition">UniSphere AI</Link></li>
              <li><Link href="/notices" className="hover:text-white transition">Notices</Link></li>
              <li><Link href="/events" className="hover:text-white transition">Events</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="mb-3 font-semibold text-white">Contact</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start gap-2">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0" />
                <span>{UNIVERSITY.address}</span>
              </li>
              <li className="flex items-center gap-2">
                <Phone className="h-4 w-4 shrink-0" />
                <span>{UNIVERSITY.phone}</span>
              </li>
              <li className="flex items-center gap-2">
                <Mail className="h-4 w-4 shrink-0" />
                <span>{UNIVERSITY.email}</span>
              </li>
            </ul>
          </div>
        </div>
        <div className="mt-8 border-t border-slate-700 pt-6 text-center text-sm text-slate-400">
          © {new Date().getFullYear()} {UNIVERSITY.name}. All rights reserved. Powered by UniSphere AI.
        </div>
      </div>
    </footer>
  );
}
