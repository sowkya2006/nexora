"use client";

import { usePathname } from "next/navigation";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

export function LayoutShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAdmin = pathname.startsWith("/admin");

  if (isAdmin) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#F8F4EC] text-[#3E3A34] font-sans antialiased">
      <Header />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}


