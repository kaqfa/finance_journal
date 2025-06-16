// fe/types/heroui.d.ts
declare module "@heroui/spinner" {
  import React from "react";

  export interface SpinnerProps {
    size?: "sm" | "md" | "lg";
    color?:
      | "default"
      | "primary"
      | "secondary"
      | "success"
      | "warning"
      | "danger";
    labelText?: string;
    className?: string;
    style?: React.CSSProperties;
  }

  export const Spinner: React.FC<SpinnerProps>;
}

declare module "@heroui/dropdown" {
  import React from "react";

  export interface DropdownProps {
    children: React.ReactNode;
    placement?:
      | "top"
      | "bottom"
      | "right"
      | "left"
      | "top-start"
      | "top-end"
      | "bottom-start"
      | "bottom-end"
      | "left-start"
      | "left-end"
      | "right-start"
      | "right-end";
    offset?: number;
    type?: "menu" | "listbox";
    showArrow?: boolean;
    isDisabled?: boolean;
    className?: string;
    variant?: "solid" | "bordered" | "light" | "flat" | "faded" | "shadow";
  }

  export interface DropdownItemProps {
    key?: React.Key;
    children?: React.ReactNode;
    description?: React.ReactNode;
    startContent?: React.ReactNode;
    endContent?: React.ReactNode;
    isDisabled?: boolean;
    isReadOnly?: boolean;
    isSelected?: boolean;
    className?: string;
    color?:
      | "default"
      | "primary"
      | "secondary"
      | "success"
      | "warning"
      | "danger";
    onClick?: () => void;
  }

  export interface DropdownTriggerProps {
    children: React.ReactNode;
    className?: string;
  }

  export interface DropdownMenuProps {
    "aria-label"?: string;
    items?: any[];
    children?: React.ReactNode;
    className?: string;
    variant?: "solid" | "bordered" | "light" | "flat" | "faded" | "shadow";
  }

  export const Dropdown: React.FC<DropdownProps>;
  export const DropdownTrigger: React.FC<DropdownTriggerProps>;
  export const DropdownMenu: React.FC<DropdownMenuProps>;
  export const DropdownItem: React.FC<DropdownItemProps>;
}

declare module "@heroui/avatar" {
  import React from "react";

  export interface AvatarProps {
    src?: string;
    name?: string;
    alt?: string;
    icon?: React.ReactNode;
    as?: React.ElementType;
    children?: React.ReactNode;
    size?: "sm" | "md" | "lg";
    radius?: "none" | "sm" | "md" | "lg" | "full";
    color?:
      | "default"
      | "primary"
      | "secondary"
      | "success"
      | "warning"
      | "danger";
    isBordered?: boolean;
    isDisabled?: boolean;
    isFocusable?: boolean;
    showFallback?: boolean;
    fallback?: React.ReactNode;
    className?: string;
    imgProps?: React.ImgHTMLAttributes<HTMLImageElement>;
    onClick?: () => void;
  }

  export const Avatar: React.FC<AvatarProps>;
}
