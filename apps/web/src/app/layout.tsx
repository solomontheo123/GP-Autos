import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import type { ReactNode } from "react";
import { AuthProvider } from "@/components/auth-provider";
import { CartProvider } from "@/components/cart-provider";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-sans",
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "GP Autos | Find your next favourite",
  description: "Thoughtfully selected vehicles. Clear details. A better way to buy your next car.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning className={`${manrope.variable} h-full antialiased`}>
      <body className="min-h-full">
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  const stored = window.localStorage.getItem('gp-autos-theme');
                  const preferred = stored || 'dark';
                  const systemTheme = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
                  const theme = preferred === 'system' ? systemTheme : preferred;
                  document.documentElement.dataset.theme = theme;
                } catch (error) {
                  document.documentElement.dataset.theme = 'dark';
                }
              })();
            `,
          }}
        />
        <ThemeProvider>
          <AuthProvider>
            <CartProvider>{children}</CartProvider>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
