"use client";

import Link from "next/link";
import { SiteHeader } from "@/components/site-header";
import { useCart } from "@/components/cart-provider";
import { formatPrice, vehicles } from "@/lib/vehicles";

export default function CartPage() {
  const { items, removeItem } = useCart();
  const cartItems = items.filter((item) => item.title && item.price !== undefined);
  const total = cartItems.reduce((sum, item) => sum + (item.price ?? 0) * item.quantity, 0);

  return (
    <main>
      <SiteHeader />
      <section className="page-intro"><p className="eyebrow">Your shortlist</p><h1>Your cart.</h1><p>Take one more look before moving ahead.</p></section>
      {cartItems.length === 0 ? <section className="empty-state"><h2>Nothing here just yet.</h2><p>Find a vehicle that feels right and add it to your cart.</p><Link className="button button-dark" href="/vehicles">Explore vehicles ↗</Link></section> : (
        <section className="cart-layout">
          <div>{cartItems.map((item) => item.title && item.slug && item.imageUrl && <article className="cart-row" key={item.vehicleListingId}>
            <Link href={`/vehicles/${item.slug}`}><div className="cart-thumb" style={{ backgroundImage: `url("${item.imageUrl}")` }} /></Link>
            <div><h2>{item.title}</h2><p>{item.year} · {item.location} · Qty {item.quantity}</p><button className="remove-button" type="button" onClick={() => { void removeItem(item.vehicleListingId); }}>Remove</button></div>
            <span className="price">{formatPrice(item.price ?? 0)}</span>
          </article>)}</div>
          <aside className="summary-box"><h2>Order summary</h2><div className="summary-line"><span>Vehicles ({cartItems.length})</span><span>{formatPrice(total)}</span></div><div className="summary-line"><span>Delivery</span><span>Arranged after purchase</span></div><div className="summary-line summary-total"><span>Subtotal</span><span>{formatPrice(total)}</span></div><Link className="button button-dark" href="/checkout">Continue to checkout <span aria-hidden="true">→</span></Link><p className="checkout-note">Final payment is calculated and confirmed securely at checkout.</p></aside>
        </section>
      )}
    </main>
  );
}
