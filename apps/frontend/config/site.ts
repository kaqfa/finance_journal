export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Finance Journal App",
  description: "Manage your investments and finances in one place",
  navItems: [
    {
      label: "Dashboard",
      href: "/dashboard",
    },
    {
      label: "Portfolio",
      href: "/portfolio",
    },
    {
      label: "Trading",
      href: "/trading",
    },
    {
      label: "Finance",
      href: "/finance",
    },
    {
      label: "Settings",
      href: "/settings",
    },
  ],
  navMenuItems: [
    {
      label: "Dashboard",
      href: "/dashboard",
    },
    {
      label: "Portfolio",
      href: "/portfolio",
    },
    {
      label: "Trading",
      href: "/trading",
    },
    {
      label: "Finance",
      href: "/finance",
    },
    {
      label: "Settings",
      href: "/settings",
    },
    {
      label: "Logout",
      href: "/api/auth/logout",
    },
  ],
  links: {
    github: "https://github.com/yourusername/finance-journal",
    docs: "https://finance-journal.com/docs",
    sponsor: "https://finance-journal.com"
  },
};