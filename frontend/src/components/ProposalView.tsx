"use client";

import React, { useRef } from "react";
import { FileOutput, Download, Layers, Clock, DollarSign, AlertTriangle, Wrench } from "lucide-react";
import { motion } from "framer-motion";

interface ProposalData {
  proposal: {
    project_summary: string;
    project_type: string;
    tech_stack: { technology: string; justification: string }[];
    milestones: {
      name: string;
      description: string;
      duration_weeks: number;
      features: { name: string; complexity: string }[];
    }[];
    risks: { risk: string; mitigation: string }[];
    estimated_timeline_weeks: number;
  };
  pricing: {
    line_items: {
      milestone: string;
      items: {
        feature: string;
        complexity: string;
        hours: number;
        roles: string[];
        avg_hourly_rate: number;
        cost: number;
      }[];
      subtotal_hours: number;
      subtotal_cost: number;
    }[];
    subtotal_hours: number;
    subtotal_cost: number;
    project_management_overhead: {
      percentage: number;
      cost: number;
    };
    grand_total: number;
    currency: string;
  };
  rag_context: {
    matched_projects: number;
    projects: { title: string; type: string; relevance: number }[];
  };
}

interface ProposalViewProps {
  data: ProposalData | null;
}

export default function ProposalView({ data }: ProposalViewProps) {
  const contentRef = useRef<HTMLDivElement>(null);

  const handleExportPDF = () => {
    if (contentRef.current) {
      const printWindow = window.open("", "_blank");
      if (printWindow) {
        printWindow.document.write(`
          <html>
            <head>
              <title>Project Proposal — ${data?.proposal.project_type || "Proposal"}</title>
              <style>
                body { font-family: 'Inter', -apple-system, sans-serif; padding: 40px; color: #1a1a1a; line-height: 1.6; }
                h1 { color: #b8860b; border-bottom: 2px solid #facc15; padding-bottom: 8px; }
                h2 { color: #333; margin-top: 24px; border-bottom: 1px solid #e5e5e5; padding-bottom: 4px; }
                h3 { color: #555; }
                table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }
                th { background: #f8f4e8; text-align: left; padding: 8px 12px; border: 1px solid #ddd; font-weight: 600; }
                td { padding: 6px 12px; border: 1px solid #ddd; }
                .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
                .low { background: #dcfce7; color: #166534; }
                .medium { background: #fef3c7; color: #92400e; }
                .high { background: #fecaca; color: #991b1b; }
                .total-row { background: #f8f4e8; font-weight: 700; }
                .risk-item { margin: 8px 0; padding: 12px; background: #fff7ed; border-left: 3px solid #f59e0b; border-radius: 4px; }
              </style>
            </head>
            <body>${contentRef.current.innerHTML}</body>
          </html>
        `);
        printWindow.document.close();
        printWindow.print();
      }
    }
  };

  const getComplexityColor = (c: string) => {
    if (c === "Low") return "bg-[#166534]/20 text-[#4ade80] border border-[#166534]/30";
    if (c === "Medium") return "bg-[#92400e]/20 text-[var(--color-accent)] border border-[#92400e]/30";
    return "bg-[#991b1b]/20 text-[#f87171] border border-[#991b1b]/30";
  };

  return (
    <div className="flex flex-col h-full">
      {/* Panel Header */}
      <div className="px-4 py-3 border-b border-[var(--color-border)] flex items-center gap-2">
        <FileOutput className="w-4 h-4 text-[var(--color-accent)]" />
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          THE ARTIFACT
        </h2>
        <span className="text-[10px] font-mono text-[var(--color-text-muted)] ml-auto">
          {data ? "READY" : "AWAITING"}
        </span>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-5">
        {!data ? (
          <div className="flex flex-col items-center justify-center h-full text-center gap-3 opacity-40">
            <Layers className="w-10 h-10 text-[var(--color-text-muted)]" />
            <div>
              <p className="text-xs text-[var(--color-text-muted)]">
                No proposal generated yet
              </p>
              <p className="text-[10px] text-[var(--color-text-muted)] mt-1">
                Upload a PDF and generate to see the output
              </p>
            </div>
          </div>
        ) : (
          <motion.div
            ref={contentRef}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            {/* Project Type & Summary */}
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-[10px] font-mono text-[var(--color-accent)] bg-[var(--color-accent-dim)] px-2 py-0.5 rounded">
                  {data.proposal.project_type}
                </span>
                <span className="text-[10px] font-mono text-[var(--color-text-muted)]">
                  <Clock className="w-3 h-3 inline mr-1" />
                  {data.proposal.estimated_timeline_weeks} weeks
                </span>
              </div>
              <h1 className="text-xl font-bold text-[var(--color-accent)] mb-3 text-glow">
                Project Proposal
              </h1>
              <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed whitespace-pre-line">
                {data.proposal.project_summary}
              </p>
            </div>

            {/* RAG Context */}
            {data.rag_context.matched_projects > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="mb-6 p-3 rounded-lg bg-[var(--color-accent-dim)] border border-[rgba(250,204,21,0.15)]"
              >
                <p className="text-[10px] font-mono text-[var(--color-accent)] mb-1.5">
                  📊 INFORMED BY {data.rag_context.matched_projects} HISTORICAL PROJECT(S)
                </p>
                {data.rag_context.projects.map((p, i) => (
                  <p key={i} className="text-[11px] text-[var(--color-text-muted)]">
                    ↳ {p.title} ({p.type})
                  </p>
                ))}
              </motion.div>
            )}

            {/* Tech Stack */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="mb-6"
            >
              <h2 className="text-sm font-bold text-[var(--color-text-primary)] flex items-center gap-2 mb-3">
                <Wrench className="w-4 h-4 text-[var(--color-accent)]" />
                Recommended Tech Stack
              </h2>
              <div className="grid gap-2">
                {data.proposal.tech_stack.map((tech, i) => (
                  <div
                    key={i}
                    className="p-2.5 rounded-lg bg-[var(--color-surface-2)] border border-[var(--color-border)] hover:border-[rgba(250,204,21,0.2)] transition-colors"
                  >
                    <p className="text-xs font-semibold text-[var(--color-accent)]">
                      {tech.technology}
                    </p>
                    <p className="text-[11px] text-[var(--color-text-muted)] mt-0.5">
                      {tech.justification}
                    </p>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Milestones & Pricing */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="mb-6"
            >
              <h2 className="text-sm font-bold text-[var(--color-text-primary)] flex items-center gap-2 mb-3">
                <Layers className="w-4 h-4 text-[var(--color-accent)]" />
                Milestone Breakdown & Pricing
              </h2>

              {data.pricing.line_items.map((mi, idx) => (
                <div
                  key={idx}
                  className="mb-4 rounded-lg border border-[var(--color-border)] overflow-hidden"
                >
                  <div className="px-3 py-2 bg-[var(--color-surface-3)] flex justify-between items-center">
                    <div>
                      <p className="text-xs font-semibold text-[var(--color-text-primary)]">
                        Phase {idx + 1}: {mi.milestone}
                      </p>
                      {data.proposal.milestones[idx] && (
                        <p className="text-[10px] text-[var(--color-text-muted)] mt-0.5">
                          {data.proposal.milestones[idx].description} · {data.proposal.milestones[idx].duration_weeks} weeks
                        </p>
                      )}
                    </div>
                    <span className="text-xs font-mono text-[var(--color-accent)]">
                      ${mi.subtotal_cost.toLocaleString()}
                    </span>
                  </div>
                  <table className="w-full text-[11px]">
                    <thead>
                      <tr className="bg-[var(--color-surface-2)]">
                        <th className="text-left px-3 py-1.5 text-[var(--color-text-muted)] font-medium">Feature</th>
                        <th className="text-center px-2 py-1.5 text-[var(--color-text-muted)] font-medium">Complexity</th>
                        <th className="text-right px-2 py-1.5 text-[var(--color-text-muted)] font-medium">Hours</th>
                        <th className="text-right px-3 py-1.5 text-[var(--color-text-muted)] font-medium">Cost</th>
                      </tr>
                    </thead>
                    <tbody>
                      {mi.items.map((item, j) => (
                        <tr
                          key={j}
                          className="border-t border-[var(--color-border)] hover:bg-[rgba(250,204,21,0.02)]"
                        >
                          <td className="px-3 py-1.5 text-[var(--color-text-secondary)]">
                            {item.feature}
                          </td>
                          <td className="px-2 py-1.5 text-center">
                            <span className={`inline-block px-1.5 py-0.5 rounded text-[9px] font-semibold ${getComplexityColor(item.complexity)}`}>
                              {item.complexity}
                            </span>
                          </td>
                          <td className="px-2 py-1.5 text-right text-[var(--color-text-muted)] font-mono">
                            {item.hours}h
                          </td>
                          <td className="px-3 py-1.5 text-right text-[var(--color-text-secondary)] font-mono">
                            ${item.cost.toLocaleString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))}

              {/* Total */}
              <div className="rounded-lg border border-[rgba(250,204,21,0.3)] bg-[var(--color-accent-dim)] p-3">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-[var(--color-text-muted)]">Development Subtotal</span>
                  <span className="font-mono text-[var(--color-text-secondary)]">
                    {data.pricing.subtotal_hours}h · ${data.pricing.subtotal_cost.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-[var(--color-text-muted)]">
                    Project Management ({data.pricing.project_management_overhead.percentage}%)
                  </span>
                  <span className="font-mono text-[var(--color-text-secondary)]">
                    ${data.pricing.project_management_overhead.cost.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between items-center pt-2 border-t border-[rgba(250,204,21,0.2)]">
                  <span className="text-sm font-bold text-[var(--color-text-primary)] flex items-center gap-1">
                    <DollarSign className="w-4 h-4 text-[var(--color-accent)]" />
                    Grand Total
                  </span>
                  <span className="text-lg font-bold font-mono text-[var(--color-accent)] text-glow">
                    ${data.pricing.grand_total.toLocaleString()} USD
                  </span>
                </div>
              </div>
            </motion.div>

            {/* Risks */}
            {data.proposal.risks && data.proposal.risks.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="mb-6"
              >
                <h2 className="text-sm font-bold text-[var(--color-text-primary)] flex items-center gap-2 mb-3">
                  <AlertTriangle className="w-4 h-4 text-[var(--color-accent)]" />
                  Risk Assessment
                </h2>
                <div className="grid gap-2">
                  {data.proposal.risks.map((risk, i) => (
                    <div
                      key={i}
                      className="p-2.5 rounded-lg bg-[var(--color-surface-2)] border border-[var(--color-border)] border-l-2 border-l-[var(--color-accent)]"
                    >
                      <p className="text-xs font-medium text-[var(--color-text-primary)]">
                        {risk.risk}
                      </p>
                      <p className="text-[11px] text-[var(--color-success)] mt-1">
                        ✦ Mitigation: {risk.mitigation}
                      </p>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </motion.div>
        )}
      </div>

      {/* Export Button */}
      {data && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="p-4 border-t border-[var(--color-border)]"
        >
          <button
            id="export-pdf-btn"
            onClick={handleExportPDF}
            className="w-full py-3 rounded-xl btn-primary flex items-center justify-center gap-2 text-sm"
          >
            <Download className="w-4 h-4" />
            EXPORT AS PDF
          </button>
        </motion.div>
      )}
    </div>
  );
}
