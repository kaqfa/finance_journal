import { 
  LayoutDashboard, 
  Wallet, 
  TrendingUp, 
  PieChart, 
  CreditCard,
  ArrowUpDown,
  Users,
  Settings,
  HelpCircle,
  FileText,
  Target,
  BarChart3
} from "lucide-react";

export interface NavItem {
  title: string;
  href?: string;
  icon?: any;
  badge?: string;
  items?: NavItem[];
}

export interface NavSection {
  title: string;
  items: NavItem[];
}

export const navigation: NavSection[] = [
  {
    title: "Overview",
    items: [
      {
        title: "Dashboard",
        href: "/dashboard",
        icon: LayoutDashboard,
      },
      {
        title: "Analytics",
        href: "/analytics",
        icon: BarChart3,
        badge: "New"
      }
    ]
  },
  {
    title: "Finance",
    items: [
      {
        title: "Wallets",
        href: "/finance/wallets",
        icon: Wallet,
      },
      {
        title: "Transactions",
        href: "/finance/transactions", 
        icon: ArrowUpDown,
      },
      {
        title: "Categories",
        href: "/finance/categories",
        icon: PieChart,
      },
      {
        title: "Transfers",
        href: "/finance/transfers",
        icon: CreditCard,
      }
    ]
  },
  {
    title: "Investment",
    items: [
      {
        title: "Portfolios",
        href: "/invest/portfolios",
        icon: TrendingUp,
      },
      {
        title: "Holdings",
        href: "/invest/holdings",
        icon: Target,
      },
      {
        title: "Assets",
        href: "/invest/assets",
        icon: BarChart3,
      }
    ]
  },
  {
    title: "Settings",
    items: [
      {
        title: "Profile",
        href: "/settings/profile",
        icon: Users,
      },
      {
        title: "Preferences",
        href: "/settings/preferences",
        icon: Settings,
      },
      {
        title: "Reports",
        href: "/reports",
        icon: FileText,
      },
      {
        title: "Help",
        href: "/help",
        icon: HelpCircle,
      }
    ]
  }
];