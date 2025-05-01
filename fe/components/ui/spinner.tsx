import React from "react";
import { Spinner as HeroUISpinner } from "@heroui/spinner";
import { cn } from "@/lib/utils";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: "primary" | "secondary" | "success" | "warning" | "danger";
  className?: string;
  label?: string;
}

export function Spinner({
  size = "md",
  color = "primary",
  className,
  label = "Loading...",
}: SpinnerProps) {
  return (
    <div className={cn("flex items-center justify-center gap-2", className)}>
      <HeroUISpinner color={color} size={size} />
      {label && <span className="text-sm text-default-500">{label}</span>}
    </div>
  );
}