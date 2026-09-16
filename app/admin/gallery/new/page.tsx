"use client"

import type React from "react"
import { useRef, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Upload, X, Calendar, ImageIcon, Star } from "lucide-react"
import Link from "next/link"
import { toast } from "sonner"
import Image from "next/image"
import { CONTENT_IMAGE_TYPES, IMAGE_UPLOAD_MAX_LABEL, imageUploadErrorMessage, uploadImage } from "@/lib/image-upload"

interface ImageData {
  url: string
  caption: string
}

export default function NewGalleryPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadFailures, setUploadFailures] = useState<{ name: string; message: string }[]>([])
  const uploadInProgress = useRef(false)
  const [formData, setFormData] = useState({
    eventName: "",
    eventDate: "",
    description: "",
    coverImage: "",
    images: [] as ImageData[],
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleFileUpload = async (files: File[]) => {
    if (!files.length || loading || uploadInProgress.current) return

    uploadInProgress.current = true
    setUploading(true)
    setUploadFailures([])
    const uploadedImages: ImageData[] = []
    const failures: { name: string; message: string }[] = []

    try {
      for (const file of files) {
        try {
          const result = await uploadImage(file, "gallery")
          uploadedImages.push({ url: result.url, caption: "" })
        } catch (error) {
          failures.push({ name: file.name, message: imageUploadErrorMessage(error) })
        }
      }

      if (uploadedImages.length > 0) {
        setFormData((prev) => {
          const images = [...prev.images, ...uploadedImages]
          return {
            ...prev,
            coverImage: prev.coverImage || images[0]?.url || "",
            images,
          }
        })
      }
      setUploadFailures(failures)
      if (failures.length > 0) {
        toast.error(`${uploadedImages.length} of ${files.length} images uploaded. Review the failed files below.`)
      } else {
        toast.success(`${uploadedImages.length} image(s) uploaded successfully`)
      }
    } finally {
      uploadInProgress.current = false
      setUploading(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const files = Array.from(e.dataTransfer.files)
    handleFileUpload(files)
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    e.target.value = ""
    handleFileUpload(files)
  }

  const updateImageCaption = (index: number, caption: string) => {
    setFormData((prev) => ({
      ...prev,
      images: prev.images.map((img, i) => (i === index ? { ...img, caption } : img)),
    }))
  }

  const removeImage = (index: number) => {
    setFormData((prev) => {
      const removed = prev.images[index]
      const images = prev.images.filter((_, i) => i !== index)
      return {
        ...prev,
        coverImage: removed?.url === prev.coverImage ? images[0]?.url || "" : prev.coverImage,
        images,
      }
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (loading || uploadInProgress.current) return

    if (!formData.eventName || !formData.eventDate || formData.images.length === 0) {
      toast.error("Please fill in all required fields and upload at least one image")
      return
    }

    setLoading(true)
    try {
      const response = await fetch("/api/gallery", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        toast.success("Gallery created successfully!")
        router.push("/admin/gallery")
      } else {
        const error = await response.json()
        throw new Error(error.error || "Failed to create gallery")
      }
    } catch (error) {
      console.error("Gallery creation error:", error)
      toast.error(error instanceof Error ? error.message : "Failed to create gallery")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/admin/gallery">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Gallery
          </Link>
        </Button>
        <h1 className="text-4xl font-bold mb-2">Create New Gallery</h1>
        <p className="text-muted-foreground">Upload photos from your event</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid gap-6">
          {/* Event Details */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Event Details
              </CardTitle>
              <CardDescription>Basic information about the event</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="eventName">Event Name *</Label>
                  <Input
                    id="eventName"
                    name="eventName"
                    value={formData.eventName}
                    onChange={handleInputChange}
                    placeholder="Enter event name"
                    disabled={loading}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="eventDate">Event Date *</Label>
                  <Input
                    id="eventDate"
                    name="eventDate"
                    type="date"
                    value={formData.eventDate}
                    onChange={handleInputChange}
                    disabled={loading}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Brief description of the event"
                  rows={3}
                  disabled={loading}
                />
              </div>
            </CardContent>
          </Card>

          {/* Image Upload */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ImageIcon className="h-5 w-5" />
                Event Photos
              </CardTitle>
              <CardDescription>Upload photos from the event (max {IMAGE_UPLOAD_MAX_LABEL} each)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Upload Area */}
              <div
                className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center hover:border-muted-foreground/50 transition-colors relative"
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
                onDragEnter={(e) => e.preventDefault()}
              >
                {uploading && (
                  <div className="absolute inset-0 bg-background/80 flex items-center justify-center rounded-lg">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                      <p className="text-sm text-muted-foreground">Uploading images...</p>
                    </div>
                  </div>
                )}

                <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">Upload Event Photos</h3>
                <p className="text-muted-foreground mb-4">Drag and drop images here, or click to select files</p>
                <input
                  type="file"
                  multiple
                  accept={CONTENT_IMAGE_TYPES.join(",")}
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                  disabled={uploading || loading}
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => document.getElementById("file-upload")?.click()}
                  disabled={uploading || loading}
                >
                  Select Images
                </Button>
                <p className="text-xs text-muted-foreground mt-2">
                  Supported formats: JPEG, PNG, GIF, WebP (max {IMAGE_UPLOAD_MAX_LABEL} each)
                </p>
              </div>

              {uploadFailures.length > 0 && (
                <div role="alert" className="rounded-lg border border-destructive/30 bg-destructive/5 p-4 text-sm">
                  <p className="font-medium text-destructive">{uploadFailures.length} image(s) could not be uploaded.</p>
                  <ul className="mt-2 space-y-2">
                    {uploadFailures.map((failure, index) => (
                      <li key={index} className="break-words">
                        <span className="font-medium">{failure.name}:</span> {failure.message}
                      </li>
                    ))}
                  </ul>
                  <p className="mt-3 text-muted-foreground">Successfully uploaded images are kept. Select the failed files again to retry.</p>
                </div>
              )}

              {/* Image Grid */}
              {formData.images.length > 0 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold">Uploaded Images ({formData.images.length})</h4>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {formData.images.map((image, index) => (
                      <div key={index} className="space-y-2">
                        <div className="group relative aspect-square overflow-hidden rounded-lg bg-muted">
                          <Image
                            src={image.url || "/placeholder.svg"}
                            alt={`Upload ${index + 1}`}
                            fill
                            className="object-cover"
                            sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
                          />
                          {image.url === formData.coverImage && (
                            <Badge className="absolute left-2 top-2 bg-primary text-primary-foreground hover:bg-primary">
                              <Star className="mr-1 h-3 w-3 fill-current" />
                              Cover
                            </Badge>
                          )}
                          <Button
                            type="button"
                            variant="destructive"
                            size="sm"
                            className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => removeImage(index)}
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                        <Button
                          type="button"
                          variant={image.url === formData.coverImage ? "secondary" : "outline"}
                          size="sm"
                          className="w-full"
                          onClick={() => setFormData((prev) => ({ ...prev, coverImage: image.url }))}
                          disabled={loading || uploading || image.url === formData.coverImage}
                        >
                          <Star className="mr-2 h-4 w-4" />
                          {image.url === formData.coverImage ? "Cover image" : "Set as cover"}
                        </Button>
                        <div>
                          <Input
                            placeholder="Add caption (optional)"
                            value={image.caption}
                            onChange={(e) => updateImageCaption(index, e.target.value)}
                            disabled={loading}
                            className="text-sm"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Submit */}
          <div className="flex gap-4">
            <Button type="submit" disabled={loading || uploading}>
              {loading ? "Creating Gallery..." : "Create Gallery"}
            </Button>
            <Button type="button" variant="outline" asChild>
              <Link href="/admin/gallery">Cancel</Link>
            </Button>
          </div>
        </div>
      </form>
    </div>
  )
}
