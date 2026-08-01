import { PageHero, Section } from "@/components/ui/PageHero";
import { clubs } from "@/lib/data";

export const metadata = { title: "Clubs" };

export default function ClubsPage() {
  return (
    <>
      <PageHero
        title="Student Clubs"
        description="Join vibrant student organizations on campus."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Clubs" }]}
      />
      <Section>
        <div className="grid gap-6 md:grid-cols-2">
          {clubs.map((club) => (
            <div key={club.name} className="rounded-xl border border-slate-200 bg-white p-6">
              <h3 className="text-xl font-bold text-nexora-800">{club.name}</h3>
              <p className="mt-2 text-slate-600">{club.description}</p>
              <div className="mt-4">
                <h4 className="text-sm font-semibold text-slate-900">Activities</h4>
                <div className="mt-2 flex flex-wrap gap-2">
                  {club.activities.map((a) => (
                    <span key={a} className="rounded-full bg-nexora-50 px-3 py-1 text-xs text-nexora-700">{a}</span>
                  ))}
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-500">🏆 {club.achievements}</p>
            </div>
          ))}
        </div>
      </Section>
    </>
  );
}
