"use client";

import { useState } from "react";
import { useCart } from "@/components/cart-provider";

export function AddToCartButton({ vehicleListingId, buyNow = false }: { vehicleListingId: string; buyNow?: boolean }) {
  const { addItem } = useCart();
  const [added, setAdded] = useState(false);

  async function add() {
    await addItem(vehicleListingId);
    setAdded(true);
  }

  return <button className={`button ${buyNow ? "button-orange" : "button-dark"}`} type="button" onClick={() => { void add(); }}>{added ? "Added to cart ✓" : buyNow ? "Buy now" : "Add to cart"}</button>;
}
