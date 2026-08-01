import { PageHero, Section } from "@/components/ui/PageHero";
import { UNIVERSITY } from "@/lib/constants";

export const metadata = { title: "About University" };

export default function AboutPage() {
  return (
    <>
      <PageHero
        title="About Nexora University"
        description="Discover our vision, mission, and commitment to excellence in education."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "About" }]}
      />
      <Section title="University Overview">
        <div className="prose max-w-none text-slate-600">
          <p className="text-lg leading-relaxed">
            Established in {UNIVERSITY.established}, {UNIVERSITY.name} has grown into a premier institution
            known for academic excellence, cutting-edge research, and strong industry partnerships.
            Our campus provides a vibrant environment where students develop the skills needed for tomorrow&apos;s challenges.
          </p>
        </div>
      </Section>
      <Section title="Vision & Mission" className="bg-white">
        <div className="grid gap-8 md:grid-cols-2">
          <div className="rounded-xl border border-slate-200 p-6">
            <h3 className="text-xl font-bold text-nexora-800">Vision</h3>
            <p className="mt-3 text-slate-600">
              To be a globally recognized center of excellence in education, research, and innovation,
              producing leaders who transform society through knowledge and technology.
            </p>
          </div>
          <div className="rounded-xl border border-slate-200 p-6">
            <h3 className="text-xl font-bold text-nexora-800">Mission</h3>
            <ul className="mt-3 space-y-2 text-slate-600">
              <li>• Deliver quality education with industry-relevant curriculum</li>
              <li>• Foster innovation through research and development</li>
              <li>• Build strong industry-academia collaboration</li>
              <li>• Develop ethical, responsible global citizens</li>
            </ul>
          </div>
        </div>
      </Section>
      <Section title="Core Values">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {["Excellence", "Integrity", "Innovation", "Collaboration", "Responsibility"].map((value) => (
            <div key={value} className="rounded-lg bg-nexora-50 p-4 text-center">
              <p className="font-semibold text-nexora-800">{value}</p>
            </div>
          ))}
        </div>
      </Section>
      <Section title="Leadership" className="bg-white">
        <div className="grid gap-6 md:grid-cols-3">
          {[
            { role: "Chancellor", name: "Dr. Venkata Rao", desc: "Distinguished academic leader with 30+ years of experience" },
            { role: "Vice Chancellor", name: "Dr. Lakshmi Devi", desc: "Former IIT professor and research pioneer" },
            { role: "Registrar", name: "Prof. Krishna Murthy", desc: "Expert in academic administration and policy" },
          ].map((leader) => (
            <div key={leader.role} className="rounded-xl border border-slate-200 p-6">
              <p className="text-sm font-medium text-nexora-600">{leader.role}</p>
              <h3 className="mt-1 text-lg font-bold text-slate-900">{leader.name}</h3>
              <p className="mt-2 text-sm text-slate-600">{leader.desc}</p>
            </div>
          ))}
        </div>
      </Section>
    </>
  );
}
