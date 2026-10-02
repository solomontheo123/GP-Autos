import { InventoryMarketplace } from "@/components/inventory-marketplace";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { vehicles as previewVehicles, type Vehicle } from "@/lib/vehicles";

async function getVehicles(): Promise<Vehicle[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  try {
    const response = await fetch(`${apiUrl}/api/vehicles`, { next: { revalidate: 60 } });
    if (!response.ok) return previewVehicles;
    return await response.json() as Vehicle[];
  } catch {
    return previewVehicles;
  }
}

export default async function VehiclesPage() {
  const vehicles = await getVehicles();
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
