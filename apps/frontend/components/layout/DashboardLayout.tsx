// fe/components/layout/DashboardLayout.tsx
"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/contexts/AuthContext";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, NavbarMenu, NavbarMenuItem, NavbarMenuToggle } from "@heroui/navbar";
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@heroui/dropdown";
import { Avatar } from "@heroui/avatar";
import { Button } from "@heroui/button";
import { ThemeSwitch } from "@/components/theme-switch";
import { getInitials } from "@/lib/utils";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const navItems = [
    { 
      name: "Dashboard", 
      href: "/dashboard",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 12L5 10M5 10L12 3L19 10M5 10V20C5 20.5523 5.44772 21 6 21H9M19 10L21 12M19 10V20C19 20.5523 18.5523 21 18 21H15M9 21C9.55228 21 10 20.5523 10 20V16C10 15.4477 10.4477 15 11 15H13C13.5523 15 14 15.4477 14 16V20C14 20.5523 14.4477 21 15 21M9 21H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    },
    { 
      name: "Journal", 
      href: "/journal",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 6.25278V19.2528M12 6.25278C10.8321 5.47686 9.24649 5 7.5 5C5.75351 5 4.16789 5.47686 3 6.25278V19.2528C4.16789 18.4769 5.75351 18 7.5 18C9.24649 18 10.8321 18.4769 12 19.2528M12 6.25278C13.1679 5.47686 14.7535 5 16.5 5C18.2465 5 19.8321 5.47686 21 6.25278V19.2528C19.8321 18.4769 18.2465 18 16.5 18C14.7535 18 13.1679 18.4769 12 19.2528" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    },
    { 
      name: "Finance", 
      href: "/finance",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 1V23M17 5H9.5C8.57174 5 7.6815 5.36875 7.02513 6.02513C6.36875 6.6815 6 7.57174 6 8.5C6 9.42826 6.36875 10.3185 7.02513 10.9749C7.6815 11.6313 8.57174 12 9.5 12H14.5C15.4283 12 16.3185 12.3687 16.9749 13.0251C17.6313 13.6815 18 14.5717 18 15.5C18 16.4283 17.6313 17.3185 16.9749 17.9749C16.3185 18.6313 15.4283 19 14.5 19H6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      submenu: [
        { name: "Wallets", href: "/finance/wallets" },
        { name: "Transactions", href: "/finance/transactions" },
        { name: "Categories", href: "/finance/categories" },
        { name: "Tags", href: "/finance/tags" }
      ]
    },
    { 
      name: "Info & Data", 
      href: "/info",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M13 16H12V12H11M12 8H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      submenu: [
        { name: "List Asset", href: "/info/assets" },
        { name: "List Sekuritas", href: "/info/securities" }
      ]
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <Navbar maxWidth="full" position="sticky" className="shadow-sm bg-background">
        <NavbarContent className="sm:gap-4" justify="start">
          <NavbarMenuToggle 
            aria-label={isMenuOpen ? "Close menu" : "Open menu"} 
            className="sm:hidden" 
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          />
          <NavbarBrand>
            <Link href="/dashboard" className="flex items-center gap-2">
              <Image
                src="/logo.svg"
                alt="Finance Journal Logo"
                width={32}
                height={32}
              />
              <p className="font-bold text-inherit hidden sm:block">Finance Journal</p>
            </Link>
          </NavbarBrand>
        </NavbarContent>

        <NavbarContent className="hidden sm:flex gap-4" justify="center">
          {navItems.map((item) => (
            <NavbarItem key={item.name}>
              {item.submenu ? (
                <Dropdown>
                  <DropdownTrigger>
                    <Button
                      variant="light"
                      className="font-semibold flex items-center gap-2"
                    >
                      {item.icon}
                      {item.name}
                    </Button>
                  </DropdownTrigger>
                  <DropdownMenu aria-label={`${item.name} submenu`}>
                    {item.submenu.map((subitem) => (
                      <DropdownItem key={subitem.name}>
                        <Link href={subitem.href} className="w-full">
                          {subitem.name}
                        </Link>
                      </DropdownItem>
                    ))}
                  </DropdownMenu>
                </Dropdown>
              ) : (
                <Link 
                  href={item.href}
                  className="font-semibold text-foreground/80 hover:text-foreground transition-colors flex items-center gap-2"
                >
                  {item.icon}
                  {item.name}
                </Link>
              )}
            </NavbarItem>
          ))}
        </NavbarContent>

        <NavbarContent justify="end">
          <NavbarItem className="flex gap-2">
            <ThemeSwitch />
          </NavbarItem>
          <NavbarItem>
            <Dropdown placement="bottom-end">
              <DropdownTrigger>
                <Avatar
                  as="button"
                  className="transition-transform"
                  name={user?.first_name || user?.username || "User"}
                  size="sm"
                  showFallback
                  fallback={
                    <div className="bg-primary/20 text-primary">
                      {getInitials(user?.first_name ? `${user.first_name} ${user.last_name || ''}` : user?.username || "User")}
                    </div>
                  }
                />
              </DropdownTrigger>
              <DropdownMenu aria-label="Profile Actions" variant="flat">
                <DropdownItem key="profile" className="h-14 gap-2">
                  <p className="font-semibold">Signed in as</p>
                  <p className="font-semibold">{user?.email}</p>
                </DropdownItem>
                <DropdownItem key="settings">
                  <Link href="/settings/profile">Profile Settings</Link>
                </DropdownItem>
                <DropdownItem key="logout" color="danger" onClick={handleLogout}>
                  Log Out
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </NavbarItem>
        </NavbarContent>

        <NavbarMenu>
          {navItems.map((item, index) => (
            <React.Fragment key={`${item.name}-${index}`}>
              <NavbarMenuItem>
                {item.submenu ? (
                  <div className="space-y-2">
                    <div className="font-semibold flex items-center gap-2 text-default-900">
                      {item.icon}
                      {item.name}
                    </div>
                    <div className="pl-6 space-y-1">
                      {item.submenu.map((subitem) => (
                        <NavbarMenuItem key={subitem.name}>
                          <Link
                            href={subitem.href}
                            className="w-full text-default-700 hover:text-primary transition-colors"
                            onClick={() => setIsMenuOpen(false)}
                          >
                            {subitem.name}
                          </Link>
                        </NavbarMenuItem>
                      ))}
                    </div>
                  </div>
                ) : (
                  <Link
                    href={item.href}
                    className="w-full text-default-900 hover:text-primary transition-colors font-semibold flex items-center gap-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {item.icon}
                    {item.name}
                  </Link>
                )}
              </NavbarMenuItem>
            </React.Fragment>
          ))}
          <NavbarMenuItem className="mt-8">
            <Button color="danger" variant="flat" fullWidth onClick={handleLogout}>
              Log Out
            </Button>
          </NavbarMenuItem>
        </NavbarMenu>
      </Navbar>

      <main className="flex-grow p-4 md:p-6 max-w-7xl mx-auto w-full">
        {children}
      </main>
    </div>
  );
}