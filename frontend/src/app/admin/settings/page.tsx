"use client";

import { useState, useEffect, useRef } from "react";
import { fetchWithAuth } from "@/lib/api";
import { UNIVERSITY } from "@/lib/constants";
import {
  Save, CheckCircle2, AlertCircle, Loader2, Building2,
  Phone, Mail, MapPin, Link as LinkIcon, Image, Sparkles
} from "lucide-react";

interface SettingsForm {
  name: string;
  tagline: string;
  description: string;
  vision: string;
  mission: string;
  email: string;
  phone: string;
  address: string;
  logo_url: string;
  banner_url: string;
  social_links: {
    facebook: string;
    twitter: string;
    linkedin: string;
    instagram: string;
  };
}

const DEFAULT_FORM: SettingsForm = {
  name: UNIVERSITY.name,
  tagline: UNIVERSITY.tagline,
  description: UNIVERSITY.shortDescription,
  vision: "To be a globally recognized center of excellence in education, research, and innovation.",
  mission: "Deliver world-class education, foster cutting-edge research, and empower student growth.",
  email: UNIVERSITY.email,
  phone: UNIVERSITY.phone,
  address: UNIVERSITY.address,
  logo_url: "/assets/logo.png",
  banner_url: "/assets/banner.jpg",
  social_links: {
    facebook: UNIVERSITY.social.facebook,
    twitter: UNIVERSITY.social.twitter,
    linkedin: UNIVERSITY.social.linkedin,
    instagram: UNIVERSITY.social.instagram,
  },
};

type ToastType = "success" | "error" | null;

export default function AdminSettingsPage() {
  const [form, setForm] = useState<SettingsForm>(DEFAULT_FORM);
  const [saved, setSaved] = useState<SettingsForm>(DEFAULT_FORM);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState<{ type: ToastType; message: string }>({ type: null, message: "" });
  const [isDirty, setIsDirty] = useState(false);
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  // Track unsaved changes
  useEffect(() => {
    setIsDirty(JSON.stringify(form) !== JSON.stringify(saved));
  }, [form, saved]);

  // Warn on page unload if dirty
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = "";
      }
    };
    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, [isDirty]);

  const showToast = (type: ToastType, message: string) => {
    setToast({ type, message });
    if (toastTimer.current) clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast({ type: null, message: "" }), 4000);
  };

  const loadSettings = async () => {
    setLoading(true);
    try {
      const data = await fetchWithAuth("/settings/");
      if (data?.status === "success" && data.data) {
        const s = data.data;
        const loaded: SettingsForm = {
          name: s.name || DEFAULT_FORM.name,
          tagline: s.tagline || DEFAULT_FORM.tagline,
          description: s.description || DEFAULT_FORM.description,
          vision: s.vision || DEFAULT_FORM.vision,
          mission: s.mission || DEFAULT_FORM.mission,
          email: s.email || DEFAULT_FORM.email,
          phone: s.phone || DEFAULT_FORM.phone,
          address: s.address || DEFAULT_FORM.address,
          logo_url: s.logo_url || DEFAULT_FORM.logo_url,
          banner_url: s.banner_url || DEFAULT_FORM.banner_url,
          social_links: {
            facebook: s.social_links?.facebook || DEFAULT_FORM.social_links.facebook,
            twitter: s.social_links?.twitter || DEFAULT_FORM.social_links.twitter,
            linkedin: s.social_links?.linkedin || DEFAULT_FORM.social_links.linkedin,
            instagram: s.social_links?.instagram || DEFAULT_FORM.social_links.instagram,
          },
        };
        setForm(loaded);
        setSaved(loaded);
      }
    } catch {
      // Use defaults on error
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof SettingsForm, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSocialChange = (key: keyof SettingsForm["social_links"], value: string) => {
    setForm((prev) => ({
      ...prev,
      social_links: { ...prev.social_links, [key]: value },
    }));
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();

    // Basic validation
    if (!form.name.trim()) { showToast("error", "University name is required."); return; }
    if (!form.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      showToast("error", "Please enter a valid email address."); return;
    }

    setSaving(true);
    try {
      const payload = {
        name: form.name.trim(),
        tagline: form.tagline.trim(),
        description: form.description.trim(),
        vision: form.vision.trim(),
        mission: form.mission.trim(),
        email: form.email.trim(),
        phone: form.phone.trim(),
        address: form.address.trim(),
        logo_url: form.logo_url.trim(),
        banner_url: form.banner_url.trim(),
        social_links: form.social_links,
      };

      const data = await fetchWithAuth("/settings/", {
        method: "PUT",
        body: JSON.stringify(payload),
      });

      if (data?.status === "success") {
        setSaved({ ...form });
        setIsDirty(false);
        showToast("success", "University settings saved successfully.");
      } else {
        showToast("error", data?.message || "Failed to save settings. Please try again.");
      }
    } catch {
      showToast("error", "Network error. Please check your connection and try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleDiscard = () => {
    setForm({ ...saved });
  };

  const inputClass =
    "mt-1 w-full rounded-lg border border-slate-200 px-4 py-2.5 text-sm focus:border-nexora-500 focus:outline-none focus:ring-1 focus:ring-nexora-500 transition";
  const labelClass = "block text-sm font-medium text-slate-700";

  if (loading) {
    return (
      <div className="p-8 space-y-6 animate-fade-in">
        <div className="skeleton skeleton-title w-48 mb-2" />
        <div className="skeleton skeleton-card w-full" />
        <div className="skeleton skeleton-card w-full" />
      </div>
    );
  }

  return (
    <div className="p-8 max-w-4xl space-y-8 animate-fade-in">
      {/* Toast */}
      {toast.type && (
        <div
          className={`fixed top-6 right-6 z-50 flex items-center gap-3 rounded-xl px-5 py-3.5 text-sm font-semibold text-white shadow-2xl animate-fade-in ${
            toast.type === "success" ? "bg-emerald-600" : "bg-rose-600"
          }`}
        >
          {toast.type === "success" ? (
            <CheckCircle2 className="h-4 w-4 shrink-0" />
          ) : (
            <AlertCircle className="h-4 w-4 shrink-0" />
          )}
          {toast.message}
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">University Settings</h1>
          <p className="mt-1 text-slate-500 text-sm">Manage university information, branding, and contact details</p>
        </div>
        {isDirty && (
          <div className="flex items-center gap-2 rounded-xl bg-amber-50 border border-amber-200 px-3 py-2 text-xs font-semibold text-amber-700">
            <AlertCircle className="h-3.5 w-3.5" />
            Unsaved changes
          </div>
        )}
      </div>

      <form onSubmit={handleSave} className="space-y-8">
        {/* University Identity */}
        <section className="os-card p-6 space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <Building2 className="h-4 w-4 text-nexora-600" />
            <h2 className="text-base font-bold text-slate-900">University Identity</h2>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label className={labelClass}>University Name *</label>
              <input type="text" value={form.name} onChange={(e) => handleChange("name", e.target.value)} className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Tagline</label>
              <input type="text" value={form.tagline} onChange={(e) => handleChange("tagline", e.target.value)} className={inputClass} />
            </div>
            <div className="sm:col-span-2">
              <label className={labelClass}>Short Description</label>
              <textarea rows={2} value={form.description} onChange={(e) => handleChange("description", e.target.value)} className={inputClass} />
            </div>
            <div>
              <label className={labelClass}>Vision Statement</label>
              <textarea rows={2} value={form.vision} onChange={(e) => handleChange("vision", e.target.value)} className={inputClass} />
            </div>
            <div>
              <label className={labelClass}>Mission Statement</label>
              <textarea rows={2} value={form.mission} onChange={(e) => handleChange("mission", e.target.value)} className={inputClass} />
            </div>
          </div>
        </section>

        {/* Contact Details */}
        <section className="os-card p-6 space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <Phone className="h-4 w-4 text-nexora-600" />
            <h2 className="text-base font-bold text-slate-900">Contact Details</h2>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label className={labelClass}>Email Address *</label>
              <input type="email" value={form.email} onChange={(e) => handleChange("email", e.target.value)} className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Phone Number</label>
              <input type="text" value={form.phone} onChange={(e) => handleChange("phone", e.target.value)} className={inputClass} />
            </div>
            <div className="sm:col-span-2">
              <label className={labelClass}>Campus Address</label>
              <input type="text" value={form.address} onChange={(e) => handleChange("address", e.target.value)} className={inputClass} />
            </div>
          </div>
        </section>

        {/* Branding */}
        <section className="os-card p-6 space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <Image className="h-4 w-4 text-nexora-600" />
            <h2 className="text-base font-bold text-slate-900">Branding & Media</h2>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label className={labelClass}>Logo URL</label>
              <input type="text" value={form.logo_url} onChange={(e) => handleChange("logo_url", e.target.value)} placeholder="/assets/logo.png" className={inputClass} />
            </div>
            <div>
              <label className={labelClass}>Banner URL</label>
              <input type="text" value={form.banner_url} onChange={(e) => handleChange("banner_url", e.target.value)} placeholder="/assets/banner.jpg" className={inputClass} />
            </div>
          </div>
        </section>

        {/* Social Links */}
        <section className="os-card p-6 space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <LinkIcon className="h-4 w-4 text-nexora-600" />
            <h2 className="text-base font-bold text-slate-900">Social Media Links</h2>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            {(["facebook", "twitter", "linkedin", "instagram"] as const).map((key) => (
              <div key={key}>
                <label className={labelClass}>{key.charAt(0).toUpperCase() + key.slice(1)}</label>
                <input
                  type="url"
                  value={form.social_links[key]}
                  onChange={(e) => handleSocialChange(key, e.target.value)}
                  placeholder={`https://${key}.com/nexorauniversity`}
                  className={inputClass}
                />
              </div>
            ))}
          </div>
        </section>

        {/* Actions */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-200">
          {isDirty ? (
            <button
              type="button"
              onClick={handleDiscard}
              className="rounded-lg border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 transition"
            >
              Discard Changes
            </button>
          ) : (
            <div />
          )}
          <button
            type="submit"
            disabled={saving || !isDirty}
            className="inline-flex items-center gap-2 rounded-xl bg-nexora-700 px-6 py-2.5 text-sm font-bold text-white hover:bg-nexora-800 transition shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? (
              <><Loader2 className="h-4 w-4 animate-spin" /> Saving…</>
            ) : (
              <><Save className="h-4 w-4" /> Save Settings</>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
