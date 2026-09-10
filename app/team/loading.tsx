export default function Loading() {
  return (
    <div role="status" className="mx-auto max-w-7xl animate-pulse px-8 py-20">
      <p className="mb-8 text-muted-foreground">Loading the team…</p>
      <div className="h-16 w-2/3 rounded-xl bg-muted" />
      <div className="mt-12 grid gap-6 sm:grid-cols-3">
        {[1, 2, 3].map((n) => (
          <div key={n} className="h-80 rounded-2xl bg-muted" />
        ))}
      </div>
    </div>
  );
}
