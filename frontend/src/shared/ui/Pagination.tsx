"use client";

import { cn } from "@/shared/lib/cn";

interface PaginationProps {
  page: number;
  pages: number;
  total: number;
  limit: number;
  onChange: (page: number) => void;
}

export function Pagination({ page, pages, total, limit, onChange }: PaginationProps) {
  if (pages <= 1) return null;

  const from = (page - 1) * limit + 1;
  const to   = Math.min(page * limit, total);

  // Show at most 7 page buttons; always include first, last, current ±1
  const getVisiblePages = (): (number | "...")[] => {
    if (pages <= 7) return Array.from({ length: pages }, (_, i) => i + 1);

    const result: (number | "...")[] = [1];
    if (page > 3) result.push("...");
    for (let i = Math.max(2, page - 1); i <= Math.min(pages - 1, page + 1); i++) {
      result.push(i);
    }
    if (page < pages - 2) result.push("...");
    result.push(pages);
    return result;
  };

  return (
    <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-between">
      <p className="text-sm text-gray-600">
        Showing <span className="font-medium">{from}–{to}</span> of{" "}
        <span className="font-medium">{total}</span> cars
      </p>

      <nav className="flex items-center gap-1" aria-label="Pagination">
        <PageBtn onClick={() => onChange(page - 1)} disabled={page === 1}>
          ←
        </PageBtn>

        {getVisiblePages().map((p, i) =>
          p === "..." ? (
            <span key={`ellipsis-${i}`} className="px-2 text-gray-400">…</span>
          ) : (
            <PageBtn key={p} onClick={() => onChange(p)} active={p === page}>
              {p}
            </PageBtn>
          ),
        )}

        <PageBtn onClick={() => onChange(page + 1)} disabled={page === pages}>
          →
        </PageBtn>
      </nav>
    </div>
  );
}

function PageBtn({
  children,
  onClick,
  disabled,
  active,
}: {
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
  active?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "min-w-[36px] h-9 px-2 rounded-lg text-sm font-medium transition-colors",
        "disabled:opacity-40 disabled:cursor-not-allowed",
        active
          ? "bg-brand-600 text-white"
          : "text-gray-700 hover:bg-gray-100",
      )}
    >
      {children}
    </button>
  );
}
