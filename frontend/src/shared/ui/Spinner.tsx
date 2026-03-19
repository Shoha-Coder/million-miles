import { cn } from "@/shared/lib/cn";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function Spinner({ size = "md", className }: SpinnerProps) {
  return (
    <div
      role="status"
      aria-label="Loading"
      className={cn(
        "border-brand-500 animate-spin rounded-full border-2 border-t-transparent",
        { sm: "h-4 w-4", md: "h-8 w-8", lg: "h-12 w-12" }[size],
        className,
      )}
    />
  );
}
