import Link from "next/link";

type PartItem = {
  title: string;
  price: string;
  image: string;
};

type MechanicItem = {
  name: string;
  specialty: string;
  status: "Available" | "Emergency";
  avatar?: string;
  icon?: string;
};

const parts: PartItem[] = [
  {
    title: "Brake Pads Kit",
    price: "₦38,500",
    image:
      "https://images.unsplash.com/photo-1489824904134-891ab64532f1?auto=format&fit=crop&w=900&q=80",
  },
  {
    title: "Oil Filter Set",
    price: "₦12,300",
    image:
      "https://images.unsplash.com/photo-1553440569-bcc63803a83d?auto=format&fit=crop&w=900&q=80",
  },
  {
    title: "Front Headlight Unit",
    price: "₦58,000",
    image:
      "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=900&q=80",
  },
];

const mechanics: MechanicItem[] = [
  {
    name: "Adebayo Musa",
    specialty: "Engine diagnostics & performance tuning",
    status: "Available",
    icon: "🔧",
  },
  {
    name: "Chidi Okafor",
    specialty: "Suspension, brakes & wheel alignment",
    status: "Emergency",
    icon: "🛠️",
  },
  {
    name: "Tola Akin",
    specialty: "Electrical systems & interior upgrades",
    status: "Available",
    icon: "⚙️",
  },
];

export function PartsMechanicsShowcase() {
  return (
    <section className="service-showcase-section">
      <div className="section-container">
        <div className="section-title">
          <p className="eyebrow">Service & support</p>
          <h2>Parts & trusted mechanics</h2>
          <p>Keep your car running smoothly with quality parts, fast repairs, and technicians you can rely on.</p>
        </div>

        <div className="service-panels">
          <div className="service-panel">
            <div className="service-panel-header">
              <div>
                <p className="eyebrow">Top picks</p>
                <h3>Vehicle parts</h3>
              </div>
              <Link href="/vehicles" className="text-link">Browse all</Link>
            </div>

            <div className="parts-grid">
              {parts.map((part) => (
                <article key={part.title} className="service-card part-card">
                  <div className="part-img">
                    <img src={part.image} alt={part.title} />
                  </div>
                  <div className="part-info">
                    <h3>{part.title}</h3>
                    <div className="part-price">{part.price}</div>
                    <button type="button" className="button button-dark service-button-full">
                      Add to cart
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div className="service-panel">
            <div className="service-panel-header">
              <div>
                <p className="eyebrow">Availability</p>
                <h3>Certified mechanics</h3>
              </div>
              <Link href="/contact" className="text-link">Book now</Link>
            </div>

            <div className="mechanics-grid">
              {mechanics.map((mechanic) => (
                <article key={mechanic.name} className="service-card mechanic-card">
                  <div className="avatar-wrap">
                    {mechanic.avatar ? (
                      <img src={mechanic.avatar} alt={mechanic.name} />
                    ) : (
                      <div className="icon-avatar" aria-hidden="true">{mechanic.icon}</div>
                    )}
                  </div>

                  <h3>{mechanic.name}</h3>
                  <p className="specialty">{mechanic.specialty}</p>
                  <span className={`status ${mechanic.status === "Emergency" ? "emergency" : "available"}`}>
                    {mechanic.status}
                  </span>

                  <div className="card-actions">
                    <a href="tel:+2348168606202" className="button button-dark service-action-button">
                      Call
                    </a>
                    <a
                      href="https://wa.me/2348168606202"
                      target="_blank"
                      rel="noreferrer"
                      className="button button-success service-action-button"
                    >
                      WhatsApp
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
