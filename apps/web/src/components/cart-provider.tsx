"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type CartItem = { vehicleListingId: string; quantity: number };
type CartContextValue = {
  items: CartItem[];
  itemCount: number;
  addItem: (vehicleListingId: string) => void;
  removeItem: (vehicleListingId: string) => void;
  clearCart: () => void;
};

const CartContext = createContext<CartContextValue | null>(null);
const CART_STORAGE_KEY = "gp-autos-cart";

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    queueMicrotask(() => {
      try {
        const savedItems: unknown = JSON.parse(localStorage.getItem(CART_STORAGE_KEY) ?? "[]");
        if (Array.isArray(savedItems)) {
          setItems(savedItems.filter((item): item is CartItem =>
            typeof item?.vehicleListingId === "string" && Number.isInteger(item?.quantity) && item.quantity > 0,
          ));
        }
      } catch {
        localStorage.removeItem(CART_STORAGE_KEY);
      } finally {
        setLoaded(true);
      }
    });
  }, []);

  useEffect(() => {
    if (loaded) localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
  }, [items, loaded]);

  function addItem(vehicleListingId: string) {
    setItems((current) => current.some((item) => item.vehicleListingId === vehicleListingId)
      ? current
      : [...current, { vehicleListingId, quantity: 1 }]);
  }

  function removeItem(vehicleListingId: string) {
    setItems((current) => current.filter((item) => item.vehicleListingId !== vehicleListingId));
  }

  function clearCart() {
    setItems([]);
  }

  const value = { items, itemCount: items.reduce((total, item) => total + item.quantity, 0), addItem, removeItem, clearCart };
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart(): CartContextValue {
  const context = useContext(CartContext);
  if (!context) throw new Error("useCart must be used inside CartProvider");
  return context;
}
