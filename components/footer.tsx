import Link from "next/link";

const links = [
  { label: "Team", href: "/team" },
  { label: "Contact", href: "/contact" },
  { label: "Instagram", href: "https://www.instagram.com/epoch.iiits/", external: true },
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
];

export function Footer() {
  return (
    <footer className="border-t">
      <div className="mx-auto flex max-w-[1200px] flex-wrap justify-between gap-6 px-4 py-10 text-sm text-muted-foreground sm:px-8">
        <div className="flex flex-col gap-1.5">
          <span className="font-semibold text-foreground">Epoch</span>
          <span>AI/ML Club, IIIT Sri City · © {new Date().getFullYear()}</span>
        </div>
        <nav aria-label="Footer" className="flex flex-wrap items-center gap-x-6 gap-y-2">
          {links.map((link) => link.external ? (
            <a key={link.label} href={link.href} target="_blank" rel="noopener noreferrer" className="transition-colors hover:text-foreground">{link.label}</a>
          ) : (
            <Link key={link.label} href={link.href} className="transition-colors hover:text-foreground">{link.label}</Link>
          ))}
        </nav>
      </div>
    </footer>
  );
}
