"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { SiteHeader } from "@/components/site-header";
import { apiRequest } from "@/lib/api";
import { formatPrice } from "@/lib/vehicles";

type OrderSummary = { id: string; status: string; total: number; currency: string; payment_status: string; created_at: string };

export default function OrdersPage() {
  const [orders, setOrders] = useState<OrderSummary[] | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    apiRequest<OrderSummary[]>("/api/orders").then(setOrders).catch((cause: unknown) => setError(cause instanceof Error ? cause.message : "Orders are unavailable"));
  }, []);

  return <main><SiteHeader /><section className="page-intro"><p className="eyebrow">Your account</p><h1>Your orders.</h1><p>Purchases made with GP Autos, all in one place.</p></section>
    {orders === null && !error ? <p className="state-message">Loading your orders…</p> : error ? <section className="empty-state"><h2>Sign in to see your orders.</h2><p>{error}</p><Link className="button button-dark" href="/auth/sign-in">Continue with Google ↗</Link></section> : orders?.length === 0 ? <section className="empty-state"><h2>Your next drive starts here.</h2><p>You haven’t placed an order yet.</p><Link className="button button-dark" href="/vehicles">Explore vehicles ↗</Link></section> : <section className="listing-wrap order-list">{orders?.map((order) => <Link className="order-row" key={order.id} href={`/orders/${order.id}`}><span><strong>Order {order.id.slice(0, 8).toUpperCase()}</strong><small>{new Date(order.created_at).toLocaleDateString("en-NG", { dateStyle: "medium" })}</small></span><span className={`status-label status-${order.status}`}>{order.status}</span><span>{formatPrice(Number(order.total))}</span><span aria-hidden="true">↗</span></Link>)}</section>}
  </main>;
}
