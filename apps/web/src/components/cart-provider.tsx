"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { useAuth } from "@/components/auth-provider";
import { apiRequest } from "@/lib/api";

export type CartItem = {
  vehicleListingId: string;
  quantity: number;
  title?: string;
  slug?: string;
  make?: string;
  model?: string;
  year?: number;
  mileage?: number;
  location?: string;
  price?: number;
  imageUrl?: string;
};
type BackendCartItem = {
  id: string;
  vehicle_listing_id: string;
  quantity: number;
  vehicle_listing: {
    id: string;
    title: string;
    slug: string;
    make: string;
    model: string;
    year: number;
    mileage: number;
    location: string;
    price: string;
    currency: string;
    image_url: string;
  };
};
type CartContextValue = {
  items: CartItem[];
  itemCount: number;
  isLoading: boolean;
  addItem: (vehicleListingId: string) => Promise<void>;
  removeItem: (vehicleListingId: string) => Promise<void>;
  clearCart: () => Promise<void>;
};

const CartContext = createContext<CartContextValue | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  const [items, setItems] = useState<CartItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadCart = useCallback(async () => {
    if (!isAuthenticated) {
      setItems([]);
      setIsLoading(false);
      return;
    }

    try {
      const backendItems = await apiRequest<BackendCartItem[]>("/api/cart");
      setItems(backendItems.map((item) => ({
        vehicleListingId: item.vehicle_listing_id,
        quantity: item.quantity,
        title: item.vehicle_listing.title,
        slug: item.vehicle_listing.slug,
        make: item.vehicle_listing.make,
        model: item.vehicle_listing.model,
        year: item.vehicle_listing.year,
        mileage: item.vehicle_listing.mileage,
        location: item.vehicle_listing.location,
        price: Number(item.vehicle_listing.price),
        imageUrl: item.vehicle_listing.image_url,
      })));
    } catch {
      setItems([]);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadCart();
    }, 0);

    return () => window.clearTimeout(timer);
  }, [loadCart]);

  const addItem = useCallback(async (vehicleListingId: string) => {
    if (!isAuthenticated) return;
    await apiRequest<BackendCartItem>("/api/cart/items", {
      method: "POST",
      body: JSON.stringify({ vehicle_listing_id: vehicleListingId, quantity: 1 }),
    });
    await loadCart();
  }, [isAuthenticated, loadCart]);

  const removeItem = useCallback(async (vehicleListingId: string) => {
    if (!isAuthenticated) return;
    await apiRequest<unknown>(`/api/cart/items/${vehicleListingId}`, { method: "DELETE" });
    await loadCart();
  }, [isAuthenticated, loadCart]);

  const clearCart = useCallback(async () => {
    if (!isAuthenticated) return;
    await apiRequest<unknown>("/api/cart", { method: "DELETE" });
    await loadCart();
  }, [isAuthenticated, loadCart]);

  const value = useMemo<CartContextValue>(() => ({
    items,
    itemCount: items.reduce((total, item) => total + item.quantity, 0),
    isLoading,
    addItem,
    removeItem,
    clearCart,
  }), [addItem, clearCart, isLoading, items, removeItem]);

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart(): CartContextValue {
  const context = useContext(CartContext);
  if (!context) throw new Error("useCart must be used inside CartProvider");
  return context;
}
