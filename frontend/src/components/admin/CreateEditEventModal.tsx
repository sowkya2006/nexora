"use client";

import { useState, useEffect } from "react";
import { X, Calendar, MapPin, Building2, Link as LinkIcon, Users, CheckCircle2, AlertCircle } from "lucide-react";

export interface EventData {
  id?: string;
  name: string;
  description: string;
  venue: string;
  date: string;
  time?: string;
  organizer: string;
  department?: string;
  poster_url?: string;
  registration_link?: string;
  capacity?: number;
  status: "upcoming" | "active" | "completed" | "cancelled" | "archived";
}

interface CreateEditEventModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (event: EventData, isEdit: boolean) => void;
  eventToEdit?: EventData | null;
}

export function CreateEditEventModal({
  isOpen,
  onClose,
  onSuccess,
  eventToEdit,
}: CreateEditEventModalProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [venue, setVenue] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("10:00 AM");
  const [organizer, setOrganizer] = useState("");
  const [department, setDepartment] = useState("Computer Science & Engineering");
  const [posterUrl, setPosterUrl] = useState("");
  const [registrationLink, setRegistrationLink] = useState("");
  const [capacity, setCapacity] = useState<number>(200);
  const [status, setStatus] = useState<EventData["status"]>("upcoming");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (eventToEdit) {
      setName(eventToEdit.name || "");
      setDescription(eventToEdit.description || "");
      setVenue(eventToEdit.venue || "");
      setDate(eventToEdit.date || new Date().toISOString().split("T")[0]);
      setTime(eventToEdit.time || "10:00 AM");
      setOrganizer(eventToEdit.organizer || "");
      setDepartment(eventToEdit.department || "Computer Science & Engineering");
      setPosterUrl(eventToEdit.poster_url || "");
      setRegistrationLink(eventToEdit.registration_link || "");
      setCapacity(eventToEdit.capacity || 200);
      setStatus(eventToEdit.status || "upcoming");
    } else {
      setName("");
      setDescription("");
      setVenue("");
      setDate(new Date().toISOString().split("T")[0]);
      setTime("10:00 AM");
      setOrganizer("CSE Department");
      setDepartment("Computer Science & Engineering");
      setPosterUrl("");
      setRegistrationLink("");
      setCapacity(200);
      setStatus("upcoming");
    }
    setError("");
  }, [eventToEdit, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !description.trim() || !venue.trim() || !date.trim()) {
      setError("Please fill in all required fields.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const eventPayload: EventData = {
        id: eventToEdit?.id || `event-${Date.now()}`,
        name: name.trim(),
        description: description.trim(),
        venue: venue.trim(),
        date,
        time,
        organizer: organizer.trim() || "University Event Committee",
        department,
        poster_url: posterUrl.trim() || undefined,
        registration_link: registrationLink.trim() || undefined,
        capacity: Number(capacity) || 200,
        status,
      };

      onSuccess(eventPayload, !!eventToEdit);
      onClose();
    } catch (err: any) {
      setError(err?.message || "Failed to save event.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 p-4 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-xl rounded-2xl bg-white shadow-2xl overflow-hidden border border-slate-100">
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-nexora-100 text-nexora-700">
              <Calendar className="h-4 w-4" />
            </div>
            <h2 className="text-lg font-bold text-slate-900">
              {eventToEdit ? "Edit Campus Event" : "Create New Event"}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200 hover:text-slate-700 transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {error && (
          <div className="mx-6 mt-4 flex items-center gap-2 rounded-lg bg-rose-50 p-3 text-xs font-medium text-rose-700 border border-rose-200">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Event Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Nexora Hackathon 2026"
              className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Description *</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Event summary & guidelines..."
              className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500"
              required
            />
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Venue *</label>
              <input
                type="text"
                value={venue}
                onChange={(e) => setVenue(e.target.value)}
                placeholder="e.g. Innovation Lab / Seminar Hall A"
                className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Organizer</label>
              <input
                type="text"
                value={organizer}
                onChange={(e) => setOrganizer(e.target.value)}
                placeholder="e.g. CSE Department / AI Club"
                className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Date *</label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Time</label>
              <input
                type="text"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                placeholder="e.g. 10:00 AM"
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Capacity</label>
              <input
                type="number"
                value={capacity}
                onChange={(e) => setCapacity(Number(e.target.value))}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Department</label>
              <select
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              >
                <option value="Computer Science & Engineering">Computer Science & Engineering</option>
                <option value="Electronics & Communication">Electronics & Communication</option>
                <option value="School of Business">School of Business</option>
                <option value="Humanities & Basic Sciences">Humanities & Basic Sciences</option>
                <option value="General Campus Event">General Campus Event</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">Status</label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as any)}
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm focus:border-nexora-500 focus:outline-none"
              >
                <option value="upcoming">Upcoming</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-nexora-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-nexora-800 transition shadow-md disabled:opacity-50"
            >
              {loading ? "Saving..." : eventToEdit ? "Update Event" : "Create Event"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
