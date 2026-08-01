"use client";

import { useState } from "react";
import { PageHero, Section } from "@/components/ui/PageHero";
import { faculty } from "@/lib/data";
import { Search } from "lucide-react";

export default function FacultyPage() {
  const [query, setQuery] = useState("");
  const [department, setDepartment] = useState("all");

  const departments = [...new Set(faculty.map((f) => f.department))];

  const filtered = faculty.filter((f) => {
    const matchesQuery = f.name.toLowerCase().includes(query.toLowerCase()) ||
      f.researchInterests.some((r) => r.toLowerCase().includes(query.toLowerCase()));
    const matchesDept = department === "all" || f.department === department;
    return matchesQuery && matchesDept;
  });

  return (
    <>
      <PageHero
        title="Faculty Directory"
        description="Meet our distinguished faculty members."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Faculty" }]}
      />
      <Section>
        <div className="mb-6 flex flex-col gap-4 sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by name or specialization..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full rounded-lg border border-slate-200 py-2 pl-10 pr-4 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
            />
          </div>
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="rounded-lg border border-slate-200 px-4 py-2 text-sm focus:border-nexora-500 focus:outline-none"
          >
            <option value="all">All Departments</option>
            {departments.map((d) => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((member) => (
            <div key={member.id} className="rounded-xl border border-slate-200 bg-white p-6">
              <h3 className="text-lg font-bold text-slate-900">{member.name}</h3>
              <p className="text-sm font-medium text-nexora-600">{member.designation}</p>
              <p className="mt-1 text-sm text-slate-500">{member.department}</p>
              <p className="mt-3 text-sm text-slate-600">{member.qualification}</p>
              <div className="mt-3 flex flex-wrap gap-1">
                {member.researchInterests.map((r) => (
                  <span key={r} className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600">{r}</span>
                ))}
              </div>
              <p className="mt-3 text-sm text-nexora-600">{member.email}</p>
            </div>
          ))}
        </div>
      </Section>
    </>
  );
}
