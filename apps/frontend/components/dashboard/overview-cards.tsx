"use client";

import {
  DollarSign,
  TrendingUp,
  Wallet,
  ArrowUpDown,
  Target,
  PieChart,
} from "lucide-react";

import { MetricCard } from "./metric-card";

export function OverviewCards() {
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard
        description="All accounts combined"
        icon={DollarSign}
        title="Total Balance"
        trend={{
          value: 12.5,
          label: "from last month",
        }}
        value="Rp 45,231,890"
      />
      <MetricCard
        description="Income this month"
        icon={TrendingUp}
        title="Monthly Income"
        trend={{
          value: 8.2,
          label: "from last month",
        }}
        value="Rp 15,500,000"
      />
      <MetricCard
        description="Expenses this month"
        icon={ArrowUpDown}
        title="Monthly Expenses"
        trend={{
          value: -2.4,
          label: "from last month",
        }}
        value="Rp 8,750,000"
      />
      <MetricCard
        description="Across all accounts"
        icon={Wallet}
        title="Active Wallets"
        value="8"
      />
    </div>
  );
}

export function InvestmentOverviewCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <MetricCard
        description="Total investment value"
        icon={Target}
        title="Portfolio Value"
        trend={{
          value: 15.7,
          label: "from last month",
        }}
        value="Rp 125,890,000"
      />
      <MetricCard
        description="Unrealized gains"
        icon={TrendingUp}
        title="Total P&L"
        trend={{
          value: 24.8,
          label: "from last month",
        }}
        value="Rp 18,450,000"
      />
      <MetricCard
        description="Across 3 portfolios"
        icon={PieChart}
        title="Active Holdings"
        value="24"
      />
    </div>
  );
}
