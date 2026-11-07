import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function PageKicker({
  children,
  className,
  as: Tag = "h1",
}: {
  children: ReactNode;
  className?: string;
  /** Use "p" when the page renders its own h1 title below the kicker. */
  as?: "h1" | "p";
}) {
  return (
    <header className={cn("mb-12", className)}>
      <Tag className="kicker">{children}</Tag>
    </header>
  );
}
