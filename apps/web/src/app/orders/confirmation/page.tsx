"use client";

import Link from "next/link";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { SiteHeader } from "@/components/site-header";
import { apiRequest } from "@/lib/api";

type VerifiedPayment = { order_id: string; order_status: string; payment_status: string };

function PaymentConfirmation() {
  const searchParams = useSearchParams();
  const reference = searchParams.get("reference");
  const [result, setResult] = useState<VerifiedPayment | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    if (!reference) return;
    apiRequest<VerifiedPayment>(`/api/payments/verify/${encodeURIComponent(reference)}`).then(setResult).catch((cause: unknown) => setError(cause instanceof Error ? cause.message : "Payment verification failed"));
  }, [reference]);
  const failureMessage = error || (!reference ? "Payment reference is missing." : "");
  return <main><SiteHeader /><section className="auth-card confirmation-card"><p className="eyebrow">Payment verification</p>{result?.payment_status === "success" ? <><h1>It’s yours.</h1><p>Your payment is confirmed and your order is ready.</p><Link className="button button-dark" href={`/orders/${result.order_id}`}>View your order ↗</Link></> : failureMessage ? <><h1>We couldn’t confirm that yet.</h1><p>{failureMessage}</p><Link className="button button-dark" href="/orders">View your orders ↗</Link></> : <><h1>Confirming your payment.</h1><p>We’re checking your payment securely with Paystack.</p></>}</section></main>;
}

export default function OrderConfirmationPage() {
  return <Suspense fallback={<main><SiteHeader /><section className="auth-card confirmation-card"><p className="eyebrow">Payment verification</p><h1>Confirming your payment.</h1></section></main>}><PaymentConfirmation /></Suspense>;
}
