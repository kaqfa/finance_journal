"use client";

import { Plus, TrendingUp, Wallet } from "lucide-react";
import Link from "next/link";

import { useAuth } from "@/contexts/AuthContext";
import { OverviewCards } from "@/components/dashboard/overview-cards";
import { RecentTransactions } from "@/components/dashboard/recent-transactions";
import { ExpenseChart } from "@/components/dashboard/expense-chart";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  const { user } = useAuth();

  const userName =
    user?.first_name && user?.last_name
      ? `${user.first_name} ${user.last_name}`
      : user?.username || "User";

  return (
    <div className="flex-1 space-y-6 p-6 md:p-8">
      {/* Welcome Section */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Welcome back, {userName}!
        </h1>
        <p className="text-muted-foreground">
          Here's what's happening with your finances today.
        </p>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-3">
        <Button asChild>
          <Link href="/finance/transactions/new">
            <Plus className="mr-2 h-4 w-4" />
            Add Transaction
          </Link>
        </Button>
        <Button asChild variant="outline">
          <Link href="/finance/wallets">
            <Wallet className="mr-2 h-4 w-4" />
            Manage Wallets
          </Link>
        </Button>
        <Button asChild variant="outline">
          <Link href="/invest/portfolios">
            <TrendingUp className="mr-2 h-4 w-4" />
            Portfolios
          </Link>
        </Button>
      </div>

      {/* Overview Cards */}
      <OverviewCards />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Recent Transactions - Takes more space */}
        <div className="lg:col-span-8">
          <RecentTransactions />
        </div>

        {/* Expense Chart - Takes less space */}
        <div className="lg:col-span-4">
          <ExpenseChart />
        </div>
      </div>

      {/* Navigation Cards */}
      <div className="grid gap-6 sm:grid-cols-2">
        <Card className="transition-all hover:shadow-md">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Wallet className="h-5 w-5 text-blue-600" />
              Finance Management
            </CardTitle>
            <CardDescription className="text-sm">
              Track your income, expenses, and financial goals
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3 sm:grid-cols-2">
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/finance/wallets">Wallets</Link>
              </Button>
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/finance/transactions">Transactions</Link>
              </Button>
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/finance/categories">Categories</Link>
              </Button>
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/finance/transfers">Transfers</Link>
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 text-lg">
              <TrendingUp className="h-5 w-5 text-green-600" />
              Investment Tracking
            </CardTitle>
            <CardDescription className="text-sm">
              Monitor portfolios and investment performance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3 sm:grid-cols-2">
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/invest/portfolios">Portfolios</Link>
              </Button>
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/invest/holdings">Holdings</Link>
              </Button>
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/invest/assets">Assets</Link>
              </Button>
              <Button
                asChild
                className="justify-start"
                size="sm"
                variant="ghost"
              >
                <Link href="/analytics">Analytics</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
