"use client";

import React, { useState, useCallback, useRef } from "react";
import Header from "@/components/Header";
import DropZone from "@/components/DropZone";
import TerminalConsole, { LogEntry } from "@/components/TerminalConsole";
import ProposalView from "@/components/ProposalView";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [proposalData, setProposalData] = useState<any>(null);
  const logIdRef = useRef(0);

  const addLog = useCallback(
    (message: string, type: LogEntry["type"] = "info") => {
      const now = new Date();
      const ts = now.toLocaleTimeString("en-US", {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      setLogs((prev) => [
        ...prev,
        {
          id: `log-${logIdRef.current++}`,
          message,
          timestamp: ts,
          type,
        },
      ]);
    },
    []
  );

  const handleFileSelected = useCallback(
    async (file: File) => {
      setIsProcessing(true);
      setProposalData(null);
      setLogs([]);

      addLog(`System initialized — ProposalForge v1.0`, "info");
      addLog(`File received: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`, "info");

      const formData = new FormData();
      formData.append("file", file);

      try {
        addLog("Connecting to processing pipeline...", "processing");

        const response = await fetch(`${API_BASE}/api/generate-stream`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const err = await response.json().catch(() => ({ detail: "Unknown error" }));
          throw new Error(err.detail || `Server error: ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error("Failed to get response stream");
        }

        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          const events = buffer.split("\n\n");
          buffer = events.pop() || "";

          for (const event of events) {
            if (!event.trim()) continue;

            const lines = event.split("\n");
            let eventType = "";
            let eventData = "";

            for (const line of lines) {
              if (line.startsWith("event: ")) {
                eventType = line.slice(7);
              } else if (line.startsWith("data: ")) {
                eventData = line.slice(6);
              }
            }

            if (!eventType || !eventData) continue;

            try {
              const parsed = JSON.parse(eventData);

              if (eventType === "status") {
                const logType =
                  parsed.step?.includes("complete") || parsed.step?.includes("parsed") || parsed.step?.includes("results")
                    ? "success"
                    : "processing";
                addLog(parsed.message, logType);
              } else if (eventType === "result") {
                addLog("═══════════════════════════════════", "info");
                addLog("Pipeline execution complete", "success");
                addLog(
                  `Total cost: $${parsed.pricing.grand_total.toLocaleString()} USD`,
                  "success"
                );
                setProposalData(parsed);
              } else if (eventType === "error") {
                addLog(parsed.message, "error");
              }
            } catch {
              // Skip malformed JSON
            }
          }
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : "Unknown error";
        addLog(`Error: ${message}`, "error");

        // Fallback: try the non-streaming endpoint
        addLog("Retrying via synchronous endpoint...", "processing");
        try {
          const formData2 = new FormData();
          formData2.append("file", file);
          const res = await fetch(`${API_BASE}/api/generate`, {
            method: "POST",
            body: formData2,
          });
          if (res.ok) {
            const data = await res.json();
            addLog("Fallback succeeded!", "success");
            addLog(
              `Total cost: $${data.pricing.grand_total.toLocaleString()} USD`,
              "success"
            );
            setProposalData(data);
          } else {
            const err = await res.json().catch(() => ({ detail: "Server error" }));
            addLog(`Fallback failed: ${err.detail}`, "error");
          }
        } catch (fallbackErr) {
          addLog(
            `Fallback error: ${fallbackErr instanceof Error ? fallbackErr.message : "Unknown"}`,
            "error"
          );
        }
      } finally {
        setIsProcessing(false);
      }
    },
    [addLog]
  );

  return (
    <div className="h-screen flex flex-col bg-[var(--color-background)]">
      <Header />

      {/* Three-Panel Layout */}
      <main className="flex-1 flex overflow-hidden">
        {/* Left Panel — Ingestion */}
        <section className="w-[280px] shrink-0 glass-panel-accent border-r border-[rgba(250,204,21,0.1)]">
          <DropZone onFileSelected={handleFileSelected} isProcessing={isProcessing} />
        </section>

        {/* Middle Panel — The Brain */}
        <section className="w-[340px] shrink-0 glass-panel border-r border-[var(--color-border)]">
          <TerminalConsole logs={logs} isProcessing={isProcessing} />
        </section>

        {/* Right Panel — The Artifact */}
        <section className="flex-1 glass-panel">
          <ProposalView data={proposalData} />
        </section>
      </main>

      {/* Status Bar */}
      <footer className="h-7 flex items-center justify-between px-4 border-t border-[var(--color-border)] bg-[var(--color-surface)]">
        <div className="flex items-center gap-3 text-[10px] font-mono text-[var(--color-text-muted)]">
          <span className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-[var(--color-success)]" />
            API CONNECTED
          </span>
          <span>|</span>
          <span>RAG: 3 PROJECTS</span>
          <span>|</span>
          <span>ENGINE: {proposalData?.metadata?.mode === "live" ? "GEMINI" : "MOCK"}</span>
        </div>
        <span className="text-[10px] font-mono text-[var(--color-text-muted)]">
          ProposalForge © 2026
        </span>
      </footer>
    </div>
  );
}
