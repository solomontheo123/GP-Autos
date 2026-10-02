import Link from "next/link";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";

export default function NotFound() {
  return (
    <main>
      <SiteHeader />
      <section className="empty-state">
        <p className="eyebrow">Not found</p>
        <h1>This listing has moved on.</h1>
        <p>Take a look at the vehicles we have available now.</p>
        <Link className="button button-dark" href="/vehicles">Browse vehicles ↗</Link>
      </section>
      <SiteFooter />
    </main>
  );
}
