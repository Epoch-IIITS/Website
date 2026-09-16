"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Upload, X, ImageIcon } from "lucide-react"
import { toast } from "sonner"
import type { MediaPurpose } from "@/lib/cloudinary-media"
import { CONTENT_IMAGE_TYPES, IMAGE_UPLOAD_MAX_LABEL, imageUploadErrorMessage, uploadImage } from "@/lib/image-upload"

interface ImageUploadProps {
  value: string
  onChange: (url: string) => void
  label?: string
  disabled?: boolean
  purpose?: Exclude<MediaPurpose, "team">
}

export function ImageUpload({ value, onChange, label = "Image", disabled = false, purpose = "blog" }: ImageUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState("")
  const fileInputRef = useRef<HTMLInputElement>(null)
  const uploadInProgress = useRef(false)

  const handleFileUpload = async (file: File) => {
    if (!file || disabled || uploadInProgress.current) return

    uploadInProgress.current = true
    setUploading(true)
    setError("")
    try {
      const data = await uploadImage(file, purpose)
      onChange(data.url)
      toast.success("Image uploaded successfully!")
    } catch (error) {
      const message = `${file.name}: ${imageUploadErrorMessage(error)}`
      setError(message)
      toast.error(message)
    } finally {
      uploadInProgress.current = false
      setUploading(false)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    e.target.value = ""
    if (file) handleFileUpload(file)
  }

  const removeImage = () => {
    setError("")
    onChange("")
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="space-y-4">
      <Label>{label}</Label>

      {value ? (
        <div className="relative">
          <img
            src={value || "/placeholder.svg"}
            alt="Uploaded image"
            className="w-full h-48 object-cover rounded-lg border"
          />
          <Button
            type="button"
            variant="destructive"
            size="sm"
            className="absolute top-2 right-2"
            onClick={removeImage}
            disabled={disabled || uploading}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
            dragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25"
          } ${disabled || uploading ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => !disabled && !uploading && fileInputRef.current?.click()}
        >
          <ImageIcon className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-sm text-muted-foreground mb-2">
            {uploading ? "Uploading..." : "Drag and drop an image here, or click to select"}
          </p>
          <p className="text-xs text-muted-foreground">Supports: JPEG, PNG, GIF, WebP (max {IMAGE_UPLOAD_MAX_LABEL})</p>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept={CONTENT_IMAGE_TYPES.join(",")}
        onChange={handleFileSelect}
        className="hidden"
        disabled={disabled || uploading}
      />

      {error && <p role="alert" className="break-words text-sm text-destructive">{error}</p>}

      <div className="flex gap-2">
        <Button
          type="button"
          variant="outline"
          onClick={() => fileInputRef.current?.click()}
          disabled={disabled || uploading}
        >
          <Upload className="mr-2 h-4 w-4" />
          {uploading ? "Uploading..." : "Upload Image"}
        </Button>
      </div>
    </div>
  )
}
