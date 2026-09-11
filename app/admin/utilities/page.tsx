import Link from "next/link"
import { ArrowRight, QrCode } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function UtilitiesPage() {
  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-4 sm:px-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Utilities</h1>
        <p className="mt-2 text-muted-foreground">Practical tools for running Epoch activities.</p>
      </div>

      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        <Card className="flex min-h-64 flex-col border-primary/20 bg-primary/5">
          <CardHeader>
            <span className="mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-primary-foreground">
              <QrCode className="h-6 w-6" aria-hidden="true" />
            </span>
            <CardTitle>QR Code Generator</CardTitle>
            <CardDescription>Create branded QR codes for links or text and measure visits to tracked links.</CardDescription>
          </CardHeader>
          <CardContent className="mt-auto">
            <Button asChild className="w-full justify-between">
              <Link href="/admin/utilities/qr-code-generator">Open generator<ArrowRight className="h-4 w-4" /></Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
