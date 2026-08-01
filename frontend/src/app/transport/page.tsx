import { PageHero, Section } from "@/components/ui/PageHero";
import { DocumentCard } from "@/components/ui/DocumentCard";
import { busRoutes, documents } from "@/lib/data";

export const metadata = { title: "Transport" };

export default function TransportPage() {
  const busDoc = documents.find((d) => d.name === "Bus Routes");

  return (
    <>
      <PageHero
        title="Campus Transport"
        description="Convenient bus services connecting campus to the city."
        breadcrumb={[{ label: "Home", href: "/" }, { label: "Transport" }]}
      />
      <Section title="Bus Routes">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200">
                <th className="pb-3 font-semibold">Route</th>
                <th className="pb-3 font-semibold">Areas Covered</th>
                <th className="pb-3 font-semibold">Timing</th>
              </tr>
            </thead>
            <tbody>
              {busRoutes.map((route) => (
                <tr key={route.route} className="border-b border-slate-100">
                  <td className="py-3 font-medium text-nexora-700">{route.route}</td>
                  <td className="py-3 text-slate-600">{route.areas.join(", ")}</td>
                  <td className="py-3 text-slate-600">{route.timing}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>
      {busDoc && (
        <Section title="Bus Routes Document" className="bg-white">
          <div className="max-w-md"><DocumentCard document={busDoc} /></div>
        </Section>
      )}
    </>
  );
}
