"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { SiteHeader } from "@/components/site-header";
import { apiRequest } from "@/lib/api";
import { formatPrice } from "@/lib/vehicles";

type OrderDetail = { id: string; status: string; total: number; subtotal: number; currency: string; payment_status: string; payment_reference: string | null; created_at: string; items: { id: string; vehicle_listing_id: string; quantity: number; unit_price: number; subtotal: number; vehicle_listing: { title: string; slug: string; image_url: string } }[] };

export default function OrderDetailPage() {
  const params = useParams<{ id: string }>();
  const [order, setOrder] = useState<OrderDetail | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    apiRequest<OrderDetail>(`/api/orders/${params.id}`).then(setOrder).catch((cause: unknown) => setError(cause instanceof Error ? cause.message : "Order not found"));
  }, [params.id]);
  return <main><SiteHeader /><section className="page-intro"><p className="eyebrow">Order details</p><h1>{order ? `Order ${order.id.slice(0, 8).toUpperCase()}` : "Your order."}</h1></section>
    {error ? <section className="empty-state"><h2>We couldn’t find that order.</h2><p>{error}</p><Link className="button button-dark" href="/orders">Back to orders</Link></section> : !order ? <p className="state-message">Loading order details…</p> : <section className="cart-layout"><div className="order-items">{order.items.map((item) => <article className="cart-row" key={item.id}><Link href={`/vehicles/${item.vehicle_listing.slug}`}><div className="cart-thumb" style={{ backgroundImage: `url("${item.vehicle_listing.image_url}")` }} /></Link><div><h2>{item.vehicle_listing.title}</h2><p>Quantity {item.quantity}</p></div><span className="price">{formatPrice(Number(item.unit_price))}</span></article>)}</div><aside className="summary-box"><h2>Payment details</h2><div className="summary-line"><span>Order status</span><span className={`status-label status-${order.status}`}>{order.status}</span></div><div className="summary-line"><span>Payment status</span><span>{order.payment_status}</span></div><div className="summary-line"><span>Reference</span><span>{order.payment_reference ?? "Pending"}</span></div><div className="summary-line summary-total"><span>Total</span><span>{formatPrice(Number(order.total))}</span></div></aside></section>}
  </main>;
}
