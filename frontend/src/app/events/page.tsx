"use client";

import { useState, useEffect } from "react";
import { PageHero, Section } from "@/components/ui/PageHero";
import { UniSphereCallout } from "@/components/ui/UniSphereCallout";
import { events as staticEvents } from "@/lib/data";
import { Calendar, MapPin, User, Download, Loader2, AlertCircle } from "lucide-react";

interface EventItem {
  id: string;
  name: string;
  description: string;
  date: string;
  venue: string;
  organizer: string;
  status: string;
  brochure_url?: string;
}

export default function EventsPage() {
  const [events, setEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
        const res = await fetch(`${API_URL}/events/`);
        if (res.ok) {
          const data = await res.json();
          if (data?.events?.length > 0) {
            setEvents(data.events.map((e: any) => ({
              id: e.id,
              name: e.name,
              description: e.description || "",
              date: e.date,
              venue: e.venue || "TBD",
              organizer: e.organizer || "University",
              status: e.status || "upcoming",
              brochure_url: e.brochure_url || e.poster_url,
            })));
            return;
          }
        }
      } catch {
        setError(true);
      }
      // Fallback to static data
      setEvents(staticEvents.map((e) => ({
        id: e.id, name: e.name, description: e.description,
        date: e.date, venue: e.venue, organizer: e.organizer,
        status: e.status, brochure_url: e.brochureUrl,
      })));
      setLoading(false);
    };
    fetchEvents().finally(() => setLoading(false));
  }, []);

  const statusColor: Record<string, string> = {
    upcoming: "bg-blue-50 text-blue-700 border-blue-200",
    active: "bg-emerald-50 text-emerald-700 border-emerald-200",
    completed: "bg-slate-100 text-slate-600 border-slate-200",
    cancelled: "bg-rose-50 text-rose-700 border-rose-200",
  };

  return (
    <>
      <PageHero
        title="Events & Campus Activities"
        description="Hackathons, cultural fests, symposiums, placement drives and more."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Events" }]}
      />
      <Section>
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Upcoming Campus Events</h2>
            <p className="text-xs text-slate-500 mt-0.5">Live from university events database</p>
          </div>
          <a href="http://localhost:8000/knowledge_base/Academic_Calendar_2026.pdf" target="_blank" rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-xs font-semibold text-white hover:bg-slate-800 transition shrink-0">
            <Download className="h-3.5 w-3.5" /> Academic Calendar PDF
          </a>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="h-6 w-6 animate-spin text-nexora-600 mr-2" />
            <span className="text-sm text-slate-400">Loading events…</span>
          </div>
        ) : events.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center">
            <AlertCircle className="h-8 w-8 text-slate-300 mx-auto mb-2" />
            <p className="text-slate-600 font-medium">No events scheduled currently.</p>
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-12">
            {events.map((evt) => (
              <div key={evt.id} className="storybook-card p-6 flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="inline-flex items-center gap-1 rounded-full bg-[#F0EAE1] px-2.5 py-0.5 text-xs font-semibold text-[#44563E]">
                      <Calendar className="h-3 w-3" /> {evt.date}
                    </span>
                    <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold border capitalize ${statusColor[evt.status] || "bg-slate-100 text-slate-600 border-slate-200"}`}>
                      {evt.status}
                    </span>
                  </div>
                  <h3 className="font-bold text-slate-900 text-base leading-snug">{evt.name}</h3>
                  <p className="text-xs text-slate-500 leading-relaxed line-clamp-3">{evt.description}</p>
                </div>
                <div className="mt-4 border-t border-slate-100 pt-3 text-xs text-slate-400 space-y-1">
                  {evt.venue && <p className="flex items-center gap-1.5"><MapPin className="h-3.5 w-3.5" /> {evt.venue}</p>}
                  {evt.organizer && <p className="flex items-center gap-1.5"><User className="h-3.5 w-3.5" /> {evt.organizer}</p>}
                </div>
              </div>
            ))}
          </div>
        )}

        <UniSphereCallout
          title="Need Event Timings or Registration Deadlines?"
          description="UniSphere AI answers questions about event schedules, guest speakers, venue details, and registration links from official documents."
          suggestedQuestions={[
            "When is the annual cultural fest scheduled?",
            "What are the dates for mid-semester exams?",
            "When does the hackathon registration open?",
            "What holidays are listed in the academic calendar?"
          ]}
          documentsCovered={["Official Academic Calendar 2026-2027", "Cultural & Technical Fest Guidelines", "Student Club Event Schedule"]}
        />
      </Section>
    </>
  );
}
