"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { AdminSidebar } from "@/components/admin/AdminSidebar";
import { getAdminToken } from "@/lib/api";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const isLogin = pathname === "/admin/login";
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    if (isLogin) {
      setAuthorized(true);
      return;
    }

    const token = getAdminToken();
    if (!token) {
      setAuthorized(false);
      // Replace so back-button cannot return to protected page
      router.replace("/admin/login");
    } else {
      setAuthorized(true);
    }
  }, [pathname, isLogin, router]);

  // On admin pages, disable browser back to unauthenticated state
  useEffect(() => {
    if (!isLogin && authorized) {
      // Push a dummy state so back-button hits it first instead of leaving admin
      window.history.pushState(null, "", window.location.href);
      const handlePop = () => {
        const token = getAdminToken();
        if (!token) {
          router.replace("/admin/login");
        } else {
          window.history.pushState(null, "", window.location.href);
        }
      };
      window.addEventListener("popstate", handlePop);
      return () => window.removeEventListener("popstate", handlePop);
    }
  }, [isLogin, authorized, router]);

  if (isLogin) {
    return <>{children}</>;
  }

  if (!authorized) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-nexora-700 border-t-transparent mx-auto"></div>
          <p className="mt-3 text-sm text-slate-500 font-medium">Authenticating admin access...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      <AdminSidebar />
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  );
}
