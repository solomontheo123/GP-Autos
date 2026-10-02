import Link from "next/link";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";

export default function AboutPage() {
  return (
    <main>
      <SiteHeader />
      <section className="page-intro">
        <p className="eyebrow">About GP Autos</p>
        <h1>Thoughtful vehicles. Clear decisions.</h1>
        <p>
          GP Autos brings together carefully selected cars, transparent details, and a buying experience built for
          confidence.
        </p>
      </section>

      <section className="section info-grid">
        <article className="info-card">
          <p className="eyebrow">What we do</p>
          <h2>Curated for real buyers.</h2>
          <p>We focus on vehicles that deliver value, reliability and a clear story for drivers in Nigeria.</p>
        </article>

        <article className="info-card">
          <p className="eyebrow">Why it matters</p>
          <h2>Buying should feel simpler.</h2>
          <p>From pricing to condition to vehicle availability, we aim to remove the friction that makes car shopping stressful.</p>
        </article>

        <article className="info-card">
          <p className="eyebrow">Our approach</p>
          <h2>Trust over noise.</h2>
          <p>We keep the experience direct, helpful and built around the information that matters before the first test drive.</p>
        </article>
      </section>

      <section className="section about-cta">
        <p className="eyebrow">Ready to move</p>
        <h2>Find the right fit for your next drive.</h2>
        <div className="footer-cta-actions">
          <Link className="button button-dark" href="/vehicles">Browse inventory</Link>
          <Link className="button button-cyan" href="/contact">Contact GP Autos</Link>
        </div>
      </section>
      <SiteFooter />
    </main>
  );
}
