"use client";

import { useState, useEffect, useRef } from "react";
import {
  Plus, Pencil, Trash2, Calendar, MapPin, Search,
  Filter, CheckCircle2, User, RefreshCw, Loader2,
} from "lucide-react";
import { CreateEditEventModal, EventData } from "@/components/admin/CreateEditEventModal";
import { fetchWithAuth } from "@/lib/api";

type ToastType = "success" | "error";

export default function AdminEventsPage() {
  const [eventsList, setEventsList] = useState<EventData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [eventToEdit, setEventToEdit] = useState<EventData | null>(null);
  const [toast, setToast] = useState<{ type: ToastType; msg: string } | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const showToast = (type: ToastType, msg: string) => {
    setToast({ type, msg });
    if (toastTimer.current) clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(null), 3500);
  };

  const loadEvents = async () => {
    setLoading(true);
    try {
      const data = await fetchWithAuth("/events/");
      if (data?.events) {
        setEventsList(
          data.events.map((e: any) => ({
            id: e.id,
            name: e.name,
            description: e.description || "",
            venue: e.venue || "",
            date: e.date,
            time: e.time || "",
            organizer: e.organizer || "",
            department: e.department || "",
            poster_url: e.poster_url || e.brochure_url || "",
            registration_link: e.registration_link || "",
            capacity: e.capacity || 200,
            status: e.status || "upcoming",
          }))
        );
      }
    } catch {
      showToast("error", "Failed to load events.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadEvents(); }, []);

  const handleCreateOrUpdate = async (event: EventData, isEdit: boolean) => {
    const payload = {
      name: event.name,
      description: event.description,
      date: event.date,
      venue: event.venue,
      organizer: event.organizer,
      brochure_url: event.poster_url || "",
      status: event.status,
    };

    if (isEdit && event.id) {
      // Optimistic update
      setEventsList((prev) => prev.map((e) => (e.id === event.id ? event : e)));
      try {
        const res = await fetchWithAuth(`/events/${event.id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        if (res?.status !== "success") throw new Error();
        showToast("success", "Event updated successfully.");
      } catch {
        showToast("error", "Failed to update event. Changes reverted.");
        loadEvents(); // revert
      }
    } else {
      try {
        const res = await fetchWithAuth("/events/", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        if (res?.status === "success" && res.data) {
          setEventsList((prev) => [{ ...event, id: res.data.id || event.id }, ...prev]);
          showToast("success", "Event created successfully.");
        } else {
          throw new Error();
        }
      } catch {
        showToast("error", "Failed to create event.");
      }
    }
  };

  const handleDelete = async (id?: string) => {
    if (!id) return;
    if (!confirm("Delete this event? This action cannot be undone.")) return;
    setDeletingId(id);
    try {
      await fetchWithAuth(`/events/${id}`, { method: "DELETE" });
      setEventsList((prev) => prev.filter((e) => e.id !== id));
      showToast("success", "Event deleted.");
    } catch {
      showToast("error", "Failed to delete event.");
    } finally {
      setDeletingId(null);
    }
  };

  const handleStatusChange = async (event: EventData, newStatus: EventData["status"]) => {
    const updated = { ...event, status: newStatus };
    setEventsList((prev) => prev.map((e) => (e.id === event.id ? updated : e)));
    try {
      await fetchWithAuth(`/events/${event.id}`, {
        method: "PUT",
        body: JSON.stringify({ status: newStatus }),
      });
      showToast("success", `Status updated to "${newStatus}".`);
    } catch {
      showToast("error", "Failed to update status.");
      loadEvents();
    }
  };

  const filtered = eventsList.filter((e) => {
    const q = searchQuery.toLowerCase();
    const matchSearch = e.name.toLowerCase().includes(q) ||
      (e.venue || "").toLowerCase().includes(q) ||
      (e.organizer || "").toLowerCase().includes(q);
    const matchStatus = statusFilter === "All" || e.status === statusFilter;
    return matchSearch && matchStatus;
  });

  const statusBadge = (s: string) => {
    const map: Record<string, string> = {
      upcoming: "bg-blue-50 text-blue-700 border-blue-200",
      active: "bg-emerald-50 text-emerald-700 border-emerald-200",
      completed: "bg-slate-100 text-slate-600 border-slate-200",
      cancelled: "bg-rose-50 text-rose-700 border-rose-200",
      archived: "bg-slate-100 text-slate-500 border-slate-200",
    };
    return map[s] || "bg-slate-100 text-slate-600 border-slate-200";
  };

  return (
    <div className="p-8 space-y-6 animate-fade-in">
      {toast && (
        <div className={`fixed top-6 right-6 z-50 flex items-center gap-2 rounded-xl px-5 py-3 text-sm font-semibold text-white shadow-2xl animate-fade-in ${toast.type === "success" ? "bg-emerald-600" : "bg-rose-600"}`}>
          <CheckCircle2 className="h-4 w-4 shrink-0" />
          {toast.msg}
        </div>
      )}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Events Management</h1>
          <p className="mt-1 text-slate-500 text-sm">Create, edit, and manage university events</p>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={() => loadEvents()} className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 transition">
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          </button>
          <button
            onClick={() => { setEventToEdit(null); setIsModalOpen(true); }}
            className="inline-flex items-center gap-2 rounded-xl bg-nexora-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-nexora-800 transition shadow-md"
          >
            <Plus className="h-4 w-4" /> Create Event
          </button>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by name, venue, organizer..."
            className="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-4 text-sm focus:border-nexora-500 focus:outline-none"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-400" />
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:outline-none bg-white">
            {["All", "upcoming", "active", "completed", "cancelled", "archived"].map((s) => (
              <option key={s} value={s}>{s === "All" ? "All Statuses" : s.charAt(0).toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="space-y-3">
        {loading ? (
          <div className="os-card p-8 text-center text-slate-400">
            <Loader2 className="h-6 w-6 animate-spin mx-auto mb-2" /> Loading events...
          </div>
        ) : filtered.length === 0 ? (
          <div className="os-card p-10 text-center">
            <Calendar className="h-10 w-10 text-slate-200 mx-auto mb-3" />
            <p className="font-semibold text-slate-700">No events found</p>
            <p className="text-xs text-slate-400 mt-1">Create your first event using the button above.</p>
          </div>
        ) : (
          filtered.map((evt) => (
            <div key={evt.id} className="os-card p-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="inline-flex items-center gap-1 rounded-full bg-nexora-50 px-2.5 py-0.5 text-xs font-semibold text-nexora-700">
                    <Calendar className="h-3 w-3" /> {evt.date} {evt.time ? `· ${evt.time}` : ""}
                  </span>
                  <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold uppercase border ${statusBadge(evt.status)}`}>
                    {evt.status}
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 truncate">{evt.name}</h3>
                <p className="text-xs text-slate-500 line-clamp-2">{evt.description}</p>
                <div className="flex items-center gap-4 text-xs text-slate-400 pt-0.5">
                  {evt.venue && <span className="flex items-center gap-1"><MapPin className="h-3 w-3" /> {evt.venue}</span>}
                  {evt.organizer && <span className="flex items-center gap-1"><User className="h-3 w-3" /> {evt.organizer}</span>}
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <select
                  value={evt.status}
                  onChange={(e) => handleStatusChange(evt, e.target.value as EventData["status"])}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 text-xs font-medium bg-slate-50 focus:outline-none"
                >
                  {["upcoming", "active", "completed", "cancelled", "archived"].map((s) => (
                    <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
                  ))}
                </select>
                <button onClick={() => { setEventToEdit(evt); setIsModalOpen(true); }}
                  className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition" title="Edit">
                  <Pencil className="h-4 w-4" />
                </button>
                <button onClick={() => handleDelete(evt.id)} disabled={deletingId === evt.id}
                  className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition disabled:opacity-50" title="Delete">
                  {deletingId === evt.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <CreateEditEventModal
        isOpen={isModalOpen}
        onClose={() => { setIsModalOpen(false); setEventToEdit(null); }}
        onSuccess={handleCreateOrUpdate}
        eventToEdit={eventToEdit}
      />
    </div>
  );
}
