"use client";

import { useState } from "react";
import Link from "next/link";
import { loginAdmin } from "@/lib/api";

export default function AdminLoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await loginAdmin({ email, password });
      if (res && res.status === "success") {
        window.location.href = "/admin";
      } else {
        setError(res?.message || "Invalid credentials. Please try again.");
      }
    } catch (err: any) {
      setError(err?.message || "Login failed. Please check network connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-nexora-900 to-nexora-700 px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-slate-900">Nexora Admin</h1>
          <p className="mt-2 text-sm text-slate-600">Sign in to manage the university portal</p>
        </div>

        {error && (
          <div className="mt-4 rounded-lg bg-rose-50 p-3 text-sm text-rose-700 border border-rose-200 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
              placeholder="admin@nexorauniversity.edu"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-slate-700">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
              placeholder="••••••••"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-nexora-700 py-2.5 text-sm font-semibold text-white transition hover:bg-nexora-800 disabled:opacity-50"
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          <Link href="/" className="text-nexora-600 hover:underline">← Back to website</Link>
        </p>
      </div>
    </div>
  );
}
