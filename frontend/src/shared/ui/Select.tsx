"use client";

import { useEffect, useId, useRef, useState } from "react";
import { cn } from "@/shared/lib/cn";

export interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  label?:       string;
  options:      SelectOption[];
  placeholder?: string;
  value?:       string;
  onChange?:    (value: string) => void;
  disabled?:    boolean;
  id?:          string;
  className?:   string;
}

export function Select({
  label,
  options,
  placeholder = "All",
  value,
  onChange,
  disabled,
  id,
  className,
}: SelectProps) {
  const [open, setOpen]     = useState(false);
  const [search, setSearch] = useState("");
  const containerRef        = useRef<HTMLDivElement>(null);
  const searchRef           = useRef<HTMLInputElement>(null);
  const uid                 = useId();
  const selectId            = id ?? uid;

  const selected = options.find((o) => o.value === value);
  const filtered = search
    ? options.filter((o) => o.label.toLowerCase().includes(search.toLowerCase()))
    : options;

  // Close when clicking outside
  useEffect(() => {
    function onOutsideClick(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
        setSearch("");
      }
    }
    if (open) document.addEventListener("mousedown", onOutsideClick);
    return () => document.removeEventListener("mousedown", onOutsideClick);
  }, [open]);

  // Focus the search field as soon as the dropdown opens
  useEffect(() => {
    if (open) {
      const t = setTimeout(() => searchRef.current?.focus(), 30);
      return () => clearTimeout(t);
    }
  }, [open]);

  function handleSelect(val: string) {
    onChange?.(val);
    setOpen(false);
    setSearch("");
  }

  function toggleOpen() {
    if (!disabled) setOpen((o) => !o);
  }

  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label htmlFor={selectId} className="text-sm font-medium text-gray-700">
          {label}
        </label>
      )}

      <div ref={containerRef} className="relative">
        {/* Trigger button */}
        <button
          id={selectId}
          type="button"
          disabled={disabled}
          onClick={toggleOpen}
          aria-haspopup="listbox"
          aria-expanded={open}
          className={cn(
            "flex w-full items-center justify-between gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm transition-colors",
            "hover:border-gray-400 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500",
            "disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-400",
            open && "border-brand-500 ring-1 ring-brand-500",
            className,
          )}
        >
          <span className={cn("truncate", selected ? "text-gray-900" : "text-gray-400")}>
            {selected ? selected.label : placeholder}
          </span>

          {/* Animated chevron */}
          <svg
            className={cn("h-4 w-4 shrink-0 text-gray-400 transition-transform duration-200", open && "rotate-180")}
            viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}
            strokeLinecap="round" strokeLinejoin="round"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>

        {/* Dropdown panel */}
        {open && (
          <div className="absolute z-50 mt-1 w-full min-w-[160px] rounded-xl border border-gray-200 bg-white shadow-lg overflow-hidden">

            {/* Search bar */}
            <div className="flex items-center gap-2 border-b border-gray-100 px-3 py-2">
              <svg
                className="h-4 w-4 shrink-0 text-gray-400"
                viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}
                strokeLinecap="round" strokeLinejoin="round"
              >
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <input
                ref={searchRef}
                type="text"
                placeholder="Search..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full bg-transparent text-sm text-gray-900 placeholder-gray-400 outline-none"
              />
              {search && (
                <button
                  type="button"
                  onClick={() => setSearch("")}
                  className="shrink-0 text-gray-300 hover:text-gray-500"
                  tabIndex={-1}
                >
                  ✕
                </button>
              )}
            </div>

            {/* Options list */}
            <ul role="listbox" className="max-h-52 overflow-y-auto py-1">
              {/* "All" / clear selection */}
              {placeholder && !search && (
                <li
                  role="option"
                  aria-selected={!value}
                  onClick={() => handleSelect("")}
                  className={cn(
                    "cursor-pointer px-3 py-2 text-sm transition-colors",
                    !value
                      ? "font-semibold text-brand-600"
                      : "text-gray-500 hover:bg-gray-50",
                  )}
                >
                  {placeholder}
                </li>
              )}

              {filtered.length === 0 ? (
                <li className="px-3 py-4 text-center text-sm text-gray-400">
                  No results
                </li>
              ) : (
                filtered.map((opt) => (
                  <li
                    key={opt.value}
                    role="option"
                    aria-selected={opt.value === value}
                    onClick={() => handleSelect(opt.value)}
                    className={cn(
                      "cursor-pointer px-3 py-2 text-sm transition-colors",
                      opt.value === value
                        ? "font-semibold text-brand-600"
                        : "text-gray-700 hover:bg-gray-50",
                    )}
                  >
                    {opt.label}
                  </li>
                ))
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
