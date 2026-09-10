"use client";
import { Button } from "@/components/ui/button";
export default function TeamError({ reset }: { reset: () => void }) {
  return (
    <div className="mx-auto max-w-xl space-y-4 px-4 py-24 text-center">
      <h1 className="text-2xl font-semibold">We couldn’t load the team</h1>
      <p className="text-muted-foreground">Please try again in a moment.</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
