"use client";

import { 
  DollarSign, 
  TrendingUp, 
  Wallet, 
  ArrowUpDown,
  Target,
  PieChart
} from "lucide-react";
import { MetricCard } from "./metric-card";

export function OverviewCards() {
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard
        title="Total Balance"
        value="Rp 45,231,890"
        description="All accounts combined"
        icon={DollarSign}
        trend={{
          value: 12.5,
          label: "from last month"
        }}
      />
      <MetricCard
        title="Monthly Income"
        value="Rp 15,500,000"
        description="Income this month"
        icon={TrendingUp}
        trend={{
          value: 8.2,
          label: "from last month"
        }}
      />
      <MetricCard
        title="Monthly Expenses"
        value="Rp 8,750,000"
        description="Expenses this month"
        icon={ArrowUpDown}
        trend={{
          value: -2.4,
          label: "from last month"
        }}
      />
      <MetricCard
        title="Active Wallets"
        value="8"
        description="Across all accounts"
        icon={Wallet}
      />
    </div>
  );
}

export function InvestmentOverviewCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <MetricCard
        title="Portfolio Value"
        value="Rp 125,890,000"
        description="Total investment value"
        icon={Target}
        trend={{
          value: 15.7,
          label: "from last month"
        }}
      />
      <MetricCard
        title="Total P&L"
        value="Rp 18,450,000"
        description="Unrealized gains"
        icon={TrendingUp}
        trend={{
          value: 24.8,
          label: "from last month"
        }}
      />
      <MetricCard
        title="Active Holdings"
        value="24"
        description="Across 3 portfolios"
        icon={PieChart}
      />
    </div>
  );
}