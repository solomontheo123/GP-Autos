import Link from "next/link";
import { notFound } from "next/navigation";
import { AddToCartButton } from "@/components/add-to-cart-button";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { buildVehicleWhatsAppMessage, WhatsAppLink } from "@/components/whatsapp-link";
import { formatMileage, formatPrice, vehicles } from "@/lib/vehicles";

type VehicleDetailPageProps = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return vehicles.map((vehicle) => ({ slug: vehicle.slug }));
}

export default async function VehicleDetailPage({ params }: VehicleDetailPageProps) {
  const { slug } = await params;
  const vehicle = vehicles.find((item) => item.slug === slug);
  if (!vehicle) notFound();

  return (
    <main>
      <SiteHeader />
      <div className="detail-layout">
        <div className="detail-image" role="img" aria-label={vehicle.title} style={{ backgroundImage: `url("${vehicle.imageUrl}")` }} />
        <section className="detail-copy">
          <Link className="text-link" href="/vehicles">← All vehicles</Link>
          <p className="eyebrow" style={{ marginTop: 28 }}>{vehicle.badge} · {vehicle.location}</p>
          <h1>{vehicle.title}</h1>
          <p className="detail-price">{formatPrice(vehicle.price)}</p>
          <p>{vehicle.description}</p>
          <dl className="detail-specs">
            <div><dt>Year</dt><dd>{vehicle.year}</dd></div>
            <div><dt>Mileage</dt><dd>{formatMileage(vehicle.mileage)}</dd></div>
            <div><dt>Condition</dt><dd>{vehicle.condition}</dd></div>
            <div><dt>Transmission</dt><dd>{vehicle.transmission}</dd></div>
            <div><dt>Fuel</dt><dd>{vehicle.fuelType}</dd></div>
            <div><dt>Body type</dt><dd>{vehicle.bodyType}</dd></div>
          </dl>
          <div className="detail-actions">
            <AddToCartButton vehicleListingId={vehicle.id} buyNow />
            <AddToCartButton vehicleListingId={vehicle.id} />
            <WhatsAppLink className="button button-dark" message={buildVehicleWhatsAppMessage(vehicle.title)}>
              Chat on WhatsApp
            </WhatsAppLink>
          </div>
        </section>
      </div>
      <SiteFooter />
    </main>
  );
}
