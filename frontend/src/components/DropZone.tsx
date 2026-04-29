"use client";

import React, { useCallback, useState, useRef } from "react";
import { Upload, FileText, X, CheckCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface DropZoneProps {
  onFileSelected: (file: File) => void;
  isProcessing: boolean;
}

export default function DropZone({ onFileSelected, isProcessing }: DropZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = e.dataTransfer.files;
      if (files.length > 0 && files[0].type === "application/pdf") {
        setSelectedFile(files[0]);
      }
    },
    []
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        setSelectedFile(files[0]);
      }
    },
    []
  );

  const handleGenerate = () => {
    if (selectedFile) {
      onFileSelected(selectedFile);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Panel Header */}
      <div className="px-4 py-3 border-b border-[var(--color-border)] flex items-center gap-2">
        <Upload className="w-4 h-4 text-[var(--color-accent)]" />
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          INGESTION
        </h2>
        <span className="text-[10px] font-mono text-[var(--color-text-muted)] ml-auto">
          PDF UPLOAD
        </span>
      </div>

      {/* Drop Zone */}
      <div className="flex-1 p-4 flex flex-col gap-4">
        <div
          className={`drop-zone rounded-xl flex-1 flex flex-col items-center justify-center cursor-pointer relative overflow-hidden ${
            isDragging ? "active" : ""
          }`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {/* Scan line effect */}
          <div className="scan-line absolute inset-0 pointer-events-none" />

          <AnimatePresence mode="wait">
            {selectedFile ? (
              <motion.div
                key="file-selected"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="flex flex-col items-center gap-3 z-10"
              >
                <div className="relative">
                  <FileText className="w-12 h-12 text-[var(--color-accent)]" />
                  <CheckCircle className="w-5 h-5 text-[var(--color-success)] absolute -bottom-1 -right-1" />
                </div>
                <div className="text-center">
                  <p className="text-sm font-medium text-[var(--color-text-primary)] truncate max-w-[200px]">
                    {selectedFile.name}
                  </p>
                  <p className="text-xs text-[var(--color-text-muted)] mt-1">
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </p>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    clearFile();
                  }}
                  className="text-xs text-[var(--color-text-muted)] hover:text-[var(--color-error)] flex items-center gap-1 transition-colors"
                >
                  <X className="w-3 h-3" />
                  Remove
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="upload-prompt"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center gap-3 z-10"
              >
                <div className="w-16 h-16 rounded-2xl bg-[var(--color-accent-dim)] flex items-center justify-center">
                  <Upload className="w-7 h-7 text-[var(--color-accent)]" />
                </div>
                <div className="text-center">
                  <p className="text-sm font-medium text-[var(--color-text-primary)]">
                    Drop client PDF here
                  </p>
                  <p className="text-xs text-[var(--color-text-muted)] mt-1">
                    or click to browse
                  </p>
                </div>
                <span className="text-[10px] font-mono text-[var(--color-text-muted)] border border-[var(--color-border)] rounded px-2 py-0.5">
                  .PDF ONLY
                </span>
              </motion.div>
            )}
          </AnimatePresence>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileInput}
            className="hidden"
            id="pdf-upload-input"
          />
        </div>

        {/* Generate Button */}
        <motion.button
          id="generate-proposal-btn"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleGenerate}
          disabled={!selectedFile || isProcessing}
          className={`w-full py-3 rounded-xl font-bold text-sm tracking-wide transition-all ${
            selectedFile && !isProcessing
              ? "btn-primary cursor-pointer"
              : "bg-[var(--color-surface-3)] text-[var(--color-text-muted)] cursor-not-allowed"
          }`}
        >
          {isProcessing ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              PROCESSING...
            </span>
          ) : (
            "⚡ GENERATE PROPOSAL"
          )}
        </motion.button>
      </div>
    </div>
  );
}
