'use client';

import { useState, useEffect } from 'react';
import { OverviewCards } from "@/components/dashboard/overview-cards";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { 
  Plus, 
  Wallet, 
  ArrowUpDown, 
  TrendingUp, 
  Receipt,
  Tags,
  FolderOpen 
} from "lucide-react";
import Link from "next/link";

const quickActions = [
  {
    title: "Wallets",
    description: "Manage your wallets and accounts",
    icon: Wallet,
    href: "/finance/wallets",
    color: "text-blue-600"
  },
  {
    title: "Transactions",
    description: "View and add transactions",
    icon: Receipt,
    href: "/finance/transactions",
    color: "text-green-600"
  },
  {
    title: "Categories",
    description: "Organize transaction categories",
    icon: FolderOpen,
    href: "/finance/categories",
    color: "text-purple-600"
  },
  {
    title: "Tags",
    description: "Manage transaction tags",
    icon: Tags,
    href: "/finance/tags",
    color: "text-orange-600"
  },
  {
    title: "Transfers",
    description: "Transfer between wallets",
    icon: ArrowUpDown,
    href: "/finance/transfers",
    color: "text-indigo-600"
  },
  {
    title: "Reports",
    description: "Financial insights and analytics",
    icon: TrendingUp,
    href: "/finance/reports",
    color: "text-red-600"
  }
];

export default function FinancePage() {
  return (
    <div className="flex-1 space-y-6 p-6 md:p-8">
      {/* Page Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Finance Overview</h1>
        <p className="text-muted-foreground">
          Manage your personal finances, track expenses and monitor your wealth
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
        <Button variant="outline" asChild>
          <Link href="/finance/wallets">
            <Wallet className="mr-2 h-4 w-4" />
            Manage Wallets
          </Link>
        </Button>
      </div>

      {/* Financial Overview Cards */}
      <OverviewCards />

      {/* Finance Modules */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Finance Tools</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Card key={action.title} className="group transition-all hover:shadow-md">
                <Link href={action.href} className="block">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-muted p-2">
                        <Icon className={`h-5 w-5 ${action.color}`} />
                      </div>
                      <CardTitle className="text-lg group-hover:text-primary transition-colors">
                        {action.title}
                      </CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-sm leading-relaxed">
                      {action.description}
                    </CardDescription>
                  </CardContent>
                </Link>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}