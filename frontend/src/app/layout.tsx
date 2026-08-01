import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { LayoutShell } from "@/components/layout/LayoutShell";
import { UNIVERSITY } from "@/lib/constants";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: `${UNIVERSITY.name} – UniSphere AI`,
    template: `%s | ${UNIVERSITY.name}`,
  },
  description: UNIVERSITY.shortDescription,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-slate-50">
        <LayoutShell>{children}</LayoutShell>
      </body>
    </html>
  );
}
