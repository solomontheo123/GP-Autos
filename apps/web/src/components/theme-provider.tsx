"use client";

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

type Theme = "dark" | "light" | "system";
type ResolvedTheme = "dark" | "light";

type ThemeContextValue = {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

function getSystemTheme(): ResolvedTheme {
  if (typeof window === "undefined") return "dark";
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    if (typeof window === "undefined") return "dark";
    const saved = window.localStorage.getItem("gp-autos-theme") as Theme | null;
    return saved ?? "dark";
  });

  useEffect(() => {
    const resolvedTheme = theme === "system" ? getSystemTheme() : theme;
    document.documentElement.dataset.theme = resolvedTheme;
    window.localStorage.setItem("gp-autos-theme", theme);
  }, [theme]);

  useEffect(() => {
    if (theme !== "system") return;

    const media = window.matchMedia("(prefers-color-scheme: light)");
    const handleChange = () => {
      document.documentElement.dataset.theme = getSystemTheme();
    };

    media.addEventListener("change", handleChange);
    return () => media.removeEventListener("change", handleChange);
  }, [theme]);

  const value = useMemo<ThemeContextValue>(() => ({
    theme,
    resolvedTheme: theme === "system" ? getSystemTheme() : theme,
    setTheme: setThemeState,
  }), [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be used within a ThemeProvider");
  return context;
}
