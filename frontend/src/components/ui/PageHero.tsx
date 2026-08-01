import Link from "next/link";
import { ArrowRight } from "lucide-react";

interface PageHeroProps {
  title: string;
  description?: string;
  breadcrumb?: { label: string; href?: string }[];
}

export function PageHero({ title, description, breadcrumb }: PageHeroProps) {
  return (
    <section className="bg-gradient-to-br from-nexora-800 via-nexora-700 to-nexora-900 px-4 py-16 text-white sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        {breadcrumb && (
          <nav className="mb-4 flex items-center gap-2 text-sm text-nexora-200">
            {breadcrumb.map((item, i) => (
              <span key={item.label} className="flex items-center gap-2">
                {i > 0 && <span>/</span>}
                {item.href ? (
                  <Link href={item.href} className="hover:text-white transition">
                    {item.label}
                  </Link>
                ) : (
                  <span className="text-white">{item.label}</span>
                )}
              </span>
            ))}
          </nav>
        )}
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl lg:text-5xl">{title}</h1>
        {description && (
          <p className="mt-4 max-w-2xl text-lg text-nexora-100">{description}</p>
        )}
      </div>
    </section>
  );
}

interface SectionProps {
  title?: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export function Section({ title, description, children, className = "" }: SectionProps) {
  return (
    <section className={`py-12 sm:py-16 ${className}`}>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {(title || description) && (
          <div className="mb-8">
            {title && <h2 className="text-2xl font-bold text-slate-900 sm:text-3xl">{title}</h2>}
            {description && <p className="mt-2 text-slate-600">{description}</p>}
          </div>
        )}
        {children}
      </div>
    </section>
  );
}

interface InfoCardProps {
  title: string;
  description?: string;
  href?: string;
  icon?: React.ReactNode;
}

export function InfoCard({ title, description, href, icon }: InfoCardProps) {
  const content = (
    <div className="group flex h-full flex-col rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-nexora-200 hover:shadow-md">
      {icon && <div className="mb-4 text-nexora-600">{icon}</div>}
      <h3 className="text-lg font-semibold text-slate-900 group-hover:text-nexora-700">{title}</h3>
      {description && <p className="mt-2 flex-1 text-sm text-slate-600">{description}</p>}
      {href && (
        <span className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-nexora-600">
          Learn more <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
        </span>
      )}
    </div>
  );

  if (href) {
    return <Link href={href}>{content}</Link>;
  }
  return content;
}
