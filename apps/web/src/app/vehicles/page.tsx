import { InventoryMarketplace } from "@/components/inventory-marketplace";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { vehicles } from "@/lib/vehicles";

export default function VehiclesPage() {
  return (
    <main>
      <SiteHeader />
      <section className="page-intro">
        <p className="eyebrow">Our collection</p>
        <h1>Vehicles with<br />a little more thought.</h1>
        <p>Clear details, considered choices, and quality vehicles for the roads ahead.</p>
      </section>
      <InventoryMarketplace initialVehicles={vehicles} />
      <SiteFooter />
    </main>
  );
}
