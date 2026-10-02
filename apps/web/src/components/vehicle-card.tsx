import Link from "next/link";
import { buildVehicleWhatsAppMessage, WhatsAppLink } from "@/components/whatsapp-link";
import { formatMileage, formatPrice, type Vehicle } from "@/lib/vehicles";

export function VehicleCard({ vehicle }: { vehicle: Vehicle }) {
  return (
    <article className="vehicle-card">
      <Link href={`/vehicles/${vehicle.slug}`} aria-label={`View ${vehicle.title}`}>
        <div className="vehicle-image" style={{ backgroundImage: `url("${vehicle.imageUrl}")` }}>
          <span className="vehicle-tag">{vehicle.badge}</span>
        </div>
      </Link>
      <div className="vehicle-card-body">
        <div className="vehicle-kicker"><span>{vehicle.location}</span><span>{vehicle.condition}</span></div>
        <h3><Link href={`/vehicles/${vehicle.slug}`}>{vehicle.title}</Link></h3>
        <div className="vehicle-specs"><span>{vehicle.year}</span><span>{formatMileage(vehicle.mileage)}</span><span>{vehicle.transmission}</span></div>
        <div className="vehicle-card-bottom">
          <span className="price">{formatPrice(vehicle.price)}</span>
          <div className="vehicle-card-actions">
            <Link className="arrow-link" href={`/vehicles/${vehicle.slug}`} aria-label={`Details for ${vehicle.title}`}>View ↗</Link>
            <WhatsAppLink className="whatsapp-inline" message={buildVehicleWhatsAppMessage(vehicle.title)}>
              Ask ↗
            </WhatsAppLink>
          </div>
        </div>
      </div>
    </article>
  );
}
