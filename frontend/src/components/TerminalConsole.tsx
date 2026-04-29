"use client";

import React, { useEffect, useRef } from "react";
import { Terminal, Cpu } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export interface LogEntry {
  id: string;
  message: string;
  timestamp: string;
  type: "info" | "success" | "error" | "processing";
}

interface TerminalConsoleProps {
  logs: LogEntry[];
  isProcessing: boolean;
}

export default function TerminalConsole({ logs, isProcessing }: TerminalConsoleProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const getLogColor = (type: LogEntry["type"]) => {
    switch (type) {
      case "success":
        return "text-[var(--color-success)]";
      case "error":
        return "text-[var(--color-error)]";
      case "processing":
        return "text-[var(--color-accent)]";
      default:
        return "text-[var(--color-terminal-text)]";
    }
  };

  const getPrefix = (type: LogEntry["type"]) => {
    switch (type) {
      case "success":
        return "[✓]";
      case "error":
        return "[✗]";
      case "processing":
        return "[~]";
      default:
        return "[>]";
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Panel Header */}
      <div className="px-4 py-3 border-b border-[var(--color-border)] flex items-center gap-2">
        <Terminal className="w-4 h-4 text-[var(--color-accent)]" />
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          THE BRAIN
        </h2>
        <span className="text-[10px] font-mono text-[var(--color-text-muted)] ml-auto flex items-center gap-1.5">
          {isProcessing && (
            <span className="w-2 h-2 rounded-full bg-[var(--color-accent)] animate-pulse" />
          )}
          {isProcessing ? "ACTIVE" : "STANDBY"}
        </span>
      </div>

      {/* Terminal Display */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 bg-[var(--color-terminal-bg)] terminal-text"
      >
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center gap-3 opacity-40">
            <Cpu className="w-10 h-10 text-[var(--color-text-muted)]" />
            <div>
              <p className="text-xs text-[var(--color-text-muted)]">
                Awaiting input...
              </p>
              <p className="text-[10px] text-[var(--color-text-muted)] mt-1">
                Upload a PDF to begin analysis
              </p>
            </div>
          </div>
        ) : (
          <AnimatePresence>
            {logs.map((log) => (
              <motion.div
                key={log.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2 }}
                className="flex gap-2 mb-1.5"
              >
                <span className="text-[var(--color-text-muted)] shrink-0 select-none">
                  {log.timestamp}
                </span>
                <span className={`shrink-0 ${getLogColor(log.type)}`}>
                  {getPrefix(log.type)}
                </span>
                <span className={getLogColor(log.type)}>{log.message}</span>
              </motion.div>
            ))}
          </AnimatePresence>
        )}

        {/* Blinking cursor */}
        {isProcessing && (
          <div className="flex items-center gap-1 mt-1">
            <span className="text-[var(--color-accent)]">❯</span>
            <span className="w-2 h-4 bg-[var(--color-accent)] animate-pulse" />
          </div>
        )}
      </div>
    </div>
  );
}
