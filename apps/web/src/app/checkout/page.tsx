"use client";

import Link from "next/link";
import { useState } from "react";
import { SiteHeader } from "@/components/site-header";
import { useCart } from "@/components/cart-provider";
import { apiRequest } from "@/lib/api";
import { formatPrice, vehicles } from "@/lib/vehicles";

type CreatedOrder = { id: string };
type InitializedPayment = { authorization_url: string; reference: string };

export default function CheckoutPage() {
  const { items } = useCart();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const cartItems = items.filter((item) => item.title && item.price !== undefined);

  async function continueToPayment() {
    setBusy(true);
    setError("");
    try {
      const order = await apiRequest<CreatedOrder>("/api/orders", {
        method: "POST",
        body: JSON.stringify({ items: items.map(({ vehicleListingId, quantity }) => ({ vehicle_listing_id: vehicleListingId, quantity })) }),
      });
      const payment = await apiRequest<InitializedPayment>("/api/payments/initialize", {
        method: "POST",
        body: JSON.stringify({ order_id: order.id }),
      });
      window.location.assign(payment.authorization_url);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "We couldn't start checkout. Please try again.");
      setBusy(false);
    }
  }

  return (
    <main>
      <SiteHeader />
      <section className="page-intro"><p className="eyebrow">Almost there</p><h1>Checkout.</h1><p>Review your vehicle selection before continuing to secure payment.</p></section>
      {cartItems.length === 0 ? <section className="empty-state"><h2>Your cart is empty.</h2><Link className="button button-dark" href="/vehicles">Explore vehicles ↗</Link></section> : <section className="cart-layout">
        <div className="checkout-items"><h2>Order details</h2>{cartItems.map((item) => item.title && item.imageUrl && <article className="cart-row" key={item.vehicleListingId}><div className="cart-thumb" style={{ backgroundImage: `url("${item.imageUrl}")` }} /><div><h2>{item.title}</h2><p>Quantity {item.quantity}</p></div><span className="price">{formatPrice(item.price ?? 0)}</span></article>)}<p className="checkout-note">Sign in with Google is required before an order can be created. The server validates availability and calculates your final price.</p></div>
        <aside className="summary-box"><h2>Payment summary</h2><div className="summary-line"><span>Vehicle count</span><span>{cartItems.length}</span></div><div className="summary-line"><span>Amount</span><span>Calculated by server</span></div><div className="summary-line summary-total"><span>Total</span><span>Confirmed at checkout</span></div><button className="button button-orange" disabled={busy} type="button" onClick={() => { void continueToPayment(); }}>{busy ? "Connecting securely…" : "Continue to payment →"}</button>{error && <p className="error-message" role="alert">{error}{error.includes("Authentication required") || error.includes("Session expired") || (error.includes("Request failed") && error.includes("401")) ? <> <Link href="/auth/sign-in">Sign in ↗</Link></> : null}</p>}<p className="checkout-note">You’ll be redirected to Paystack. GP Autos never handles or stores your card details.</p></aside>
      </section>}
    </main>
  );
}
