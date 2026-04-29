import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ProposalForge — AI Proposal Generator",
  description:
    "Automated Technical Proposal & Bid Generator. Upload client requirements and generate structured project proposals with AI-powered analysis and deterministic pricing.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
