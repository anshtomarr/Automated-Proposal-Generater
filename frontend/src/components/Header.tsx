"use client";

import React from "react";
import { Zap, Cpu } from "lucide-react";

export default function Header() {
  return (
    <header className="h-14 flex items-center justify-between px-6 glass-panel border-b border-[var(--color-border)]">
      <div className="flex items-center gap-3">
        <div className="relative">
          <Zap className="w-6 h-6 text-[var(--color-accent)]" />
          <div className="absolute inset-0 w-6 h-6 bg-[var(--color-accent)] rounded-full opacity-20 blur-md" />
        </div>
        <h1 className="text-lg font-bold tracking-tight">
          <span className="text-[var(--color-accent)] text-glow">Proposal</span>
          <span className="text-[var(--color-text-primary)]">Forge</span>
        </h1>
        <span className="text-[10px] font-mono text-[var(--color-text-muted)] border border-[var(--color-border)] rounded px-1.5 py-0.5 ml-1">
          v1.0
        </span>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-xs text-[var(--color-text-muted)]">
          <Cpu className="w-3.5 h-3.5" />
          <span className="font-mono">AI ENGINE</span>
          <div className="w-2 h-2 rounded-full bg-[var(--color-success)] pulse-dot" />
        </div>
      </div>
    </header>
  );
}
