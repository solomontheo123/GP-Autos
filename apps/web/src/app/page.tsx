import Link from "next/link";
import { vehicles } from "@/lib/vehicles";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { PartsMechanicsShowcase } from "@/components/parts-mechanics-showcase";
import { VehicleCard } from "@/components/vehicle-card";

export default function Home() {
  const featuredVehicles = vehicles.slice(0, 6);
  return (
    <main>
      <SiteHeader />
      <section className="hero-wrap">
        <div className="hero-copy">
          <p className="eyebrow">A better way to buy your next car</p>
          <h1>Find the car<br />that moves you.</h1>
          <p className="hero-description">Thoughtfully selected vehicles. Clear details. A purchase you can feel good about.</p>
          <Link className="button button-light" href="/vehicles">Explore vehicles <span aria-hidden="true">↗</span></Link>
          <div className="hero-proof"><span className="proof-mark">✓</span><span>Quality checked, ready for the road</span></div>
        </div>
        <div className="hero-meta"><span>LAGOS · ABUJA · PORT HARCOURT</span><span>01 / 03</span></div>
      </section>
      <section className="section featured-section">
        <div className="section-heading">
          <div><p className="eyebrow">The right kind of different</p><h2>Find your next favourite.</h2></div>
          <Link className="text-link" href="/vehicles">View all vehicles <span aria-hidden="true">↗</span></Link>
        </div>
        <div className="vehicle-grid">
          {featuredVehicles.map((vehicle) => <VehicleCard key={vehicle.slug} vehicle={vehicle} />)}
        </div>
      </section>
      <section className="trust-band" id="why-gp-autos">
        <div className="trust-inner">
          <p className="eyebrow">Confidence comes standard</p>
          <h2>Good cars.<br />No guesswork.</h2>
          <div className="trust-points">
            <article><span className="trust-number">01</span><h3>Know what you’re buying</h3><p>Every listing tells the full story, from mileage to condition.</p></article>
            <article><span className="trust-number">02</span><h3>Pay with peace of mind</h3><p>A clear, secure checkout keeps your purchase straightforward.</p></article>
            <article><span className="trust-number">03</span><h3>Made for your market</h3><p>Local vehicles, local context, and prices in naira.</p></article>
          </div>
        </div>
      </section>
      <PartsMechanicsShowcase />
      <SiteFooter />
    </main>
  );
}
