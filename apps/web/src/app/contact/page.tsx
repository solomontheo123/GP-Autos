import Link from "next/link";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { WhatsAppLink } from "@/components/whatsapp-link";

export default function ContactPage() {
  return (
    <main>
      <SiteHeader />
      <section className="page-intro">
        <p className="eyebrow">Contact</p>
        <h1>Talk to GP Autos.</h1>
        <p>We’re here to help you find the right vehicle and move through the process with confidence.</p>
      </section>

      <section className="section contact-grid">
        <article className="info-card">
          <p className="eyebrow">Visit</p>
          <h2>GP Autos</h2>
          <p>Ikeja / Ogba, Lagos</p>
        </article>

        <article className="info-card">
          <p className="eyebrow">WhatsApp</p>
          <h2>Chat directly</h2>
          <WhatsAppLink className="text-link" message="Hello GP Autos, I would like to enquire about a vehicle.">
            Chat with GP Autos ↗
          </WhatsAppLink>
        </article>

        <article className="info-card">
          <p className="eyebrow">Browse</p>
          <h2>Current inventory</h2>
          <Link className="text-link" href="/vehicles">Explore vehicles ↗</Link>
        </article>
      </section>

      <section className="section contact-cta">
        <p className="eyebrow">Need immediate help?</p>
        <h2>Tell us what you are looking for.</h2>
        <p>Whether it is a family SUV, a daily sedan or a premium upgrade, we can help narrow the shortlist.</p>
        <WhatsAppLink className="button button-cyan" message="Hello GP Autos, I'm looking for a vehicle recommendation.">
          Message on WhatsApp
        </WhatsAppLink>
      </section>

      <SiteFooter />
    </main>
  );
}
