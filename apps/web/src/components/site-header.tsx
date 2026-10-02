"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/components/auth-provider";
import { useCart } from "@/components/cart-provider";
import { ThemeToggle } from "@/components/theme-toggle";

const primaryLinks = [
  { href: "/vehicles", label: "Inventory" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

export function SiteHeader() {
  const pathname = usePathname();
  const { isAuthenticated, isLoading, user, signOut } = useAuth();
  const { itemCount } = useCart();
  const [menuOpen, setMenuOpen] = useState(false);
  const [menuVisible, setMenuVisible] = useState(false);

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <header className="site-header">
      <Link href="/" className="wordmark" aria-label="GP Autos home">GP<span>AUTOS</span></Link>

      <nav className="nav-links" aria-label="Main navigation">
        {primaryLinks.map((link) => (
          <Link key={link.href} href={link.href} className={isActive(link.href) ? "nav-link active" : "nav-link"}>
            {link.label}
          </Link>
        ))}
      </nav>

      <div className="header-actions">
        <ThemeToggle />

        {isLoading ? (
          <span className="header-status">Checking account…</span>
        ) : isAuthenticated ? (
          <>
            <Link href="/orders" className="nav-mini-link">Orders</Link>
            <Link href="/cart" className="cart-link" aria-label={`Cart, ${itemCount} items`}>
              Cart <span className="cart-count">{itemCount}</span>
            </Link>
            <div className="account-menu">
              <button type="button" className="account-trigger" aria-haspopup="menu" aria-expanded={menuVisible} onClick={() => setMenuVisible((open) => !open)}>
                {user?.name?.split(" ")[0] ?? "Account"}
              </button>
              {menuVisible ? (
                <div className="account-dropdown" role="menu">
                  <Link href="/orders" role="menuitem">Orders</Link>
                  <Link href="/cart" role="menuitem">Cart</Link>
                  <button type="button" role="menuitem" onClick={() => { setMenuVisible(false); void signOut(); }} className="account-signout">
                    Sign out
                  </button>
                </div>
              ) : null}
            </div>
          </>
        ) : (
          <Link href="/auth/sign-in" className="sign-in">Sign in</Link>
        )}
      </div>

      <button
        type="button"
        className="mobile-nav-toggle"
        aria-label={menuOpen ? "Close navigation" : "Open navigation"}
        aria-expanded={menuOpen}
        onClick={() => setMenuOpen((open) => !open)}
      >
        Menu
      </button>

      {menuOpen ? (
        <div className="mobile-nav-panel" aria-label="Mobile navigation">
          <div className="mobile-nav-header">
            <span className="wordmark" aria-label="GP Autos home">GP<span>AUTOS</span></span>
            <button type="button" className="close-mobile-nav" aria-label="Close menu" onClick={() => setMenuOpen(false)}>×</button>
          </div>

          <nav className="mobile-nav-links" aria-label="Mobile navigation links">
            {primaryLinks.map((link) => (
              <Link key={link.href} href={link.href} className={isActive(link.href) ? "mobile-link active" : "mobile-link"} onClick={() => setMenuOpen(false)}>
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="mobile-nav-account">
            <ThemeToggle />
            {isLoading ? <span className="header-status">Checking account…</span> : isAuthenticated ? (
              <>
                <Link href="/orders" onClick={() => setMenuOpen(false)}>Orders</Link>
                <Link href="/cart" onClick={() => setMenuOpen(false)}>Cart</Link>
                <button type="button" onClick={() => { setMenuOpen(false); void signOut(); }} className="account-signout">Sign out</button>
              </>
            ) : (
              <Link href="/auth/sign-in" onClick={() => setMenuOpen(false)}>Sign In</Link>
            )}
          </div>
        </div>
      ) : null}
    </header>
  );
}
