"use client";

import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { Check, MonitorSmartphone, MoonStar, SunMedium } from "lucide-react";
import { useTheme } from "@/components/theme-provider";

const themeOptions = [
  { value: "dark", label: "Dark", icon: MoonStar },
  { value: "light", label: "Light", icon: SunMedium },
  { value: "system", label: "System", icon: MonitorSmartphone },
] as const;

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const ActiveIcon = themeOptions.find((option) => option.value === theme)?.icon ?? MonitorSmartphone;

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button type="button" className="theme-trigger" aria-label="Select theme">
          <ActiveIcon size={15} aria-hidden="true" />
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content className="theme-dropdown" align="end" sideOffset={8}>
          <DropdownMenu.RadioGroup value={theme} onValueChange={(value) => setTheme(value as "dark" | "light" | "system")}>
            {themeOptions.map((option) => {
              const Icon = option.icon;

              return (
                <DropdownMenu.RadioItem key={option.value} value={option.value} className="theme-option">
                  <span className="theme-option-label">
                    <Icon size={14} aria-hidden="true" />
                    {option.label}
                  </span>
                  <DropdownMenu.ItemIndicator>
                    <Check size={14} aria-hidden="true" />
                  </DropdownMenu.ItemIndicator>
                </DropdownMenu.RadioItem>
              );
            })}
          </DropdownMenu.RadioGroup>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
