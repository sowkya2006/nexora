"use client";

import Link from "next/link";
import { Bot, ArrowRight, CheckCircle2, Sparkles, HelpCircle } from "lucide-react";

interface UniSphereCalloutProps {
  title?: string;
  description?: string;
  suggestedQuestions?: string[];
  documentsCovered?: string[];
}

export function UniSphereCallout({
  title = "Still Have Detailed Questions?",
  description = "UniSphere AI is trained on official university documents and can provide immediate, accurate answers with exact page citations.",
  suggestedQuestions = [
    "What are the detailed eligibility criteria?",
    "What is the complete fee structure & deposit?",
    "What are the hostel rules & curfew timings?",
    "What are the scholarship waiver rules?"
  ],
  documentsCovered = [
    "Admission Handbook",
    "Fee Structure & Deposit",
    "Hostel Rules & Regulations",
    "Academic Calendar",
    "Course Curricula & Electives",
    "Scholarship Schemes",
    "Placement Statistics",
    "Department Profiles"
  ]
}: UniSphereCalloutProps) {
  return (
    <section className="my-12 overflow-hidden rounded-3xl border border-nexora-800/20 bg-gradient-to-br from-nexora-900 via-nexora-800 to-slate-900 p-8 text-white shadow-2xl md:p-12">
      <div className="mx-auto max-w-5xl">
        <div className="flex flex-col items-start justify-between gap-8 lg:flex-row lg:items-center">
          <div className="max-w-2xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full border border-nexora-400/30 bg-nexora-800/60 px-3.5 py-1 text-xs font-semibold text-nexora-200 backdrop-blur-md">
              <Sparkles className="h-3.5 w-3.5 text-nexora-300 animate-pulse" />
              <span>AI-Powered Knowledge Assistant</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-white sm:text-3xl lg:text-4xl">
              {title}
            </h2>
            <p className="text-sm text-nexora-100/90 sm:text-base leading-relaxed">
              {description}
            </p>
          </div>

          <div className="shrink-0 w-full lg:w-auto">
            <Link
              href="/chat"
              className="group inline-flex w-full items-center justify-center gap-3 rounded-2xl bg-white px-7 py-4 text-base font-bold text-nexora-900 shadow-lg transition-all hover:bg-nexora-50 hover:shadow-2xl hover:-translate-y-0.5 sm:w-auto"
            >
              <Bot className="h-5 w-5 text-nexora-700 transition group-hover:scale-110" />
              <span>Ask UniSphere AI</span>
              <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
            </Link>
          </div>
        </div>

        <div className="mt-8 border-t border-nexora-700/50 pt-6">
          <p className="text-xs font-semibold uppercase tracking-wider text-nexora-300 flex items-center gap-1.5">
            <HelpCircle className="h-3.5 w-3.5" />
            UniSphere AI answers directly from official documents:
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            {documentsCovered.map((doc) => (
              <span
                key={doc}
                className="inline-flex items-center gap-1.5 rounded-lg border border-nexora-700/60 bg-nexora-800/40 px-3 py-1 text-xs font-medium text-nexora-100"
              >
                <CheckCircle2 className="h-3 w-3 text-emerald-400 shrink-0" />
                {doc}
              </span>
            ))}
          </div>
        </div>

        {suggestedQuestions && suggestedQuestions.length > 0 && (
          <div className="mt-6 border-t border-nexora-700/30 pt-4">
            <p className="text-xs font-medium text-nexora-300">Try asking UniSphere AI:</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {suggestedQuestions.map((q) => (
                <Link
                  key={q}
                  href="/chat"
                  className="rounded-full border border-white/10 bg-white/5 px-3.5 py-1.5 text-xs text-nexora-100 transition hover:border-white/30 hover:bg-white/15"
                >
                  "{q}"
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
