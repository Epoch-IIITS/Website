"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Download, Link as LinkIcon, Share2 } from "lucide-react";
export function ShareActions({ id, name }: { id: string; name: string }) {
  const [message, setMessage] = useState("");
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap justify-center gap-3">
        <Button asChild>
          <a href={`/team/member/${id}/image?download=1`} download>
            <Download className="mr-2 h-4 w-4" />
            Download PNG
          </a>
        </Button>
        <Button
          variant="outline"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(window.location.href);
              setMessage("Link copied");
            } catch {
              setMessage("Copy the link from your address bar.");
            }
          }}
        >
          <LinkIcon className="mr-2 h-4 w-4" />
          Copy link
        </Button>
        <Button
          variant="outline"
          onClick={async () => {
            try {
              if (navigator.share)
                await navigator.share({
                  title: `${name} · Epoch`,
                  url: window.location.href,
                });
              else {
                await navigator.clipboard.writeText(window.location.href);
                setMessage("Link copied — share it with your friends");
              }
            } catch (e: any) {
              if (e.name !== "AbortError")
                setMessage("Copy the link from your address bar to share.");
            }
          }}
        >
          <Share2 className="mr-2 h-4 w-4" />
          Share
        </Button>
      </div>
      <p className="text-center text-sm text-muted-foreground" role="status">
        {message}
      </p>
    </div>
  );
}
