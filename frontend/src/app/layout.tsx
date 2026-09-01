import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ProjectScope AI — AI Requirement Analysis & Development Scoping Engine',
  description: 'Converts natural-language software project briefs into structured, validated software development plans, normalized features, and engineering tasks.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 antialiased min-h-screen flex flex-col font-sans">
        {children}
      </body>
    </html>
  );
}
