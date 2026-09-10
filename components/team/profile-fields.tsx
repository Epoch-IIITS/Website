"use client";
import { useEffect, useRef, useState } from "react";
import { PhotoCropDialog } from "@/components/team/photo-crop-dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export const emptyProfile = {
  name: "",
  linkedin: "",
  currentRole: "",
  organization: "",
  photo: "",
  tagline: "",
};
export function ProfileFields({
  value,
  onChange,
  onUploadingChange,
}: {
  value: typeof emptyProfile;
  onChange: (value: typeof emptyProfile) => void;
  onUploadingChange?: (busy: boolean) => void;
}) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [cropSource, setCropSource] = useState("");
  const [cropOpen, setCropOpen] = useState(false);
  const cropTrigger = useRef<HTMLElement | null>(null);
  useEffect(
    () => () => {
      if (cropSource.startsWith("blob:")) URL.revokeObjectURL(cropSource);
    },
    [cropSource],
  );
  return (
    <div className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        {(
          [
            ["name", "Name", 100],
            ["linkedin", "LinkedIn profile URL", 300],
            ["currentRole", "Current job role / study", 120],
            ["organization", "Current organization / institute", 120],
            ["tagline", "Tagline", 180],
          ] as const
        ).map(([key, label, max]) => (
          <Label key={key} className={key === "tagline" ? "sm:col-span-2" : ""}>
            {label}
            <Input
              className="mt-2"
              value={value[key]}
              maxLength={max}
              required={key === "name"}
              type={key === "linkedin" ? "url" : "text"}
              onChange={(e) => onChange({ ...value, [key]: e.target.value })}
            />
          </Label>
        ))}
      </div>
      <Label className="block">
        Profile photo
        <input
          className="mt-2 block w-full text-sm"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          disabled={uploading}
          onChange={(e) => {
            const file = e.target.files?.[0];
            e.target.value = "";
            if (!file) return;
            if (
              !["image/jpeg", "image/png", "image/webp"].includes(file.type)
            ) {
              setError("Choose a JPG, PNG or WebP photo.");
              return;
            }
            if (file.size > 5 * 1024 * 1024) {
              setError("Photo must be under 5 MB");
              return;
            }
            setError("");
            cropTrigger.current = e.currentTarget;
            setCropSource(URL.createObjectURL(file));
            setCropOpen(true);
          }}
        />
      </Label>
      <p className="text-xs text-muted-foreground">
        {uploading
          ? "Uploading photo… Wait for the preview before saving."
          : "JPG, PNG or WebP, up to 5 MB. Choose the visible area before uploading."}
      </p>
      {value.photo && (
        <div className="flex flex-wrap items-center gap-3">
          <img
            src={value.photo}
            alt="Profile preview"
            className="h-24 w-24 rounded-xl object-cover"
          />
          <Button
            type="button"
            variant="outline"
            onClick={(event) => {
              cropTrigger.current = event.currentTarget;
              setCropSource(value.photo);
              setCropOpen(true);
            }}
          >
            Adjust crop
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => onChange({ ...value, photo: "" })}
          >
            Remove photo
          </Button>
        </div>
      )}
      {cropSource && (
        <PhotoCropDialog
          source={cropSource}
          open={cropOpen}
          returnFocusTo={cropTrigger.current}
          onClose={() => setCropOpen(false)}
          onConfirm={async (photo) => {
            setUploading(true);
            onUploadingChange?.(true);
            setError("");
            try {
              const body = new FormData();
              body.append("file", photo, "profile.jpg");
              const response = await fetch("/api/team/upload", {
                method: "POST",
                body,
              });
              const data = await response.json();
              if (!response.ok)
                throw new Error(
                  data.error || "Photo upload failed. Please try again.",
                );
              onChange({ ...value, photo: data.url });
              setCropOpen(false);
            } finally {
              setUploading(false);
              onUploadingChange?.(false);
            }
          }}
        />
      )}
      {error && (
        <p role="alert" className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}
