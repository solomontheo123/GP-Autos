import type { ReactNode } from "react";

const WHATSAPP_BASE = "https://wa.me/2348168606202";

export function buildVehicleWhatsAppMessage(vehicleName: string) {
  return `Hello GP Autos, I'm interested in ${vehicleName}. Please share more details and availability.`;
}

export function WhatsAppLink({
  children,
  className,
  message,
}: {
  children: ReactNode;
  className?: string;
  message?: string;
}) {
  const url = message ? `${WHATSAPP_BASE}?text=${encodeURIComponent(message)}` : WHATSAPP_BASE;

  return (
    <a className={className} href={url} target="_blank" rel="noreferrer" aria-label="Chat with GP Autos on WhatsApp">
      {children}
    </a>
  );
}
