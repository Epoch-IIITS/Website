import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function PageKicker({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <header className={cn("mb-12", className)}>
      <h1 className="text-sm font-semibold uppercase tracking-[0.2em] text-primary">
        {children}
      </h1>
    </header>
  );
}
