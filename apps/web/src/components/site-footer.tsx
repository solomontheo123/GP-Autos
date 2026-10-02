"use client";

import Link from "next/link";
import { useAuth } from "@/components/auth-provider";
import { WhatsAppLink } from "@/components/whatsapp-link";

export function SiteFooter() {
  const { isAuthenticated } = useAuth();

  return (
    <footer className="site-footer">
      <div className="footer-grid">
        <div className="footer-column footer-brand">
          <Link href="/" className="wordmark" aria-label="GP Autos home">GP<span>AUTOS</span></Link>
          <p>
            A trusted destination for carefully selected vehicles and a straightforward vehicle-buying experience.
          </p>
        </div>

        <div className="footer-column">
          <h3>Explore</h3>
          <ul>
            <li><Link href="/vehicles">Inventory</Link></li>
            <li><Link href="/about">About</Link></li>
            <li><Link href="/contact">Contact</Link></li>
          </ul>
        </div>

        <div className="footer-column">
          <h3>Customer</h3>
          <ul>
            {!isAuthenticated ? <li><Link href="/auth/sign-in">Sign In</Link></li> : null}
            {isAuthenticated ? <li><Link href="/orders">Orders</Link></li> : null}
            {isAuthenticated ? <li><Link href="/cart">Cart</Link></li> : null}
          </ul>
        </div>

        <div className="footer-column">
          <h3>Contact</h3>
          <ul>
            <li><span>Ikeja / Ogba, Lagos</span></li>
            <li><span>WhatsApp: +234 816 860 6202</span></li>
            <li>
              <WhatsAppLink className="footer-whatsapp" message="Hello GP Autos, I would like to learn more about your vehicles.">
                Chat with GP Autos
              </WhatsAppLink>
            </li>
          </ul>
        </div>
      </div>

      <div className="footer-cta">
        <div>
          <p className="eyebrow">Looking for your next vehicle?</p>
          <h3>Talk to GP Autos or browse our current inventory.</h3>
        </div>
        <div className="footer-cta-actions">
          <Link className="button button-dark" href="/vehicles">Browse inventory</Link>
          <WhatsAppLink className="button button-cyan" message="Hello GP Autos, I would like to enquire about a vehicle.">
            Chat on WhatsApp
          </WhatsAppLink>
        </div>
      </div>

      <div className="footer-bottom">
        <span>GP AUTOS</span>
        <span>© {new Date().getFullYear()} GP Autos. All rights reserved.</span>
      </div>
    </footer>
  );
}
