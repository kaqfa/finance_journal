"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const transactions = [
  {
    id: 1,
    type: "income",
    description: "Salary Payment",
    amount: "+Rp 15,500,000",
    date: "2 hours ago",
    category: "Salary",
    avatar: "💰",
  },
  {
    id: 2,
    type: "expense",
    description: "Grocery Shopping",
    amount: "-Rp 450,000",
    date: "4 hours ago",
    category: "Food",
    avatar: "🛒",
  },
  {
    id: 3,
    type: "investment",
    description: "BBRI Stock Purchase",
    amount: "-Rp 2,500,000",
    date: "1 day ago",
    category: "Investment",
    avatar: "📈",
  },
  {
    id: 4,
    type: "expense",
    description: "Electricity Bill",
    amount: "-Rp 350,000",
    date: "2 days ago",
    category: "Utilities",
    avatar: "⚡",
  },
  {
    id: 5,
    type: "income",
    description: "Freelance Project",
    amount: "+Rp 3,500,000",
    date: "3 days ago",
    category: "Freelance",
    avatar: "💻",
  },
];

export function RecentTransactions() {
  return (
    <Card>
      <CardHeader className="pb-4">
        <CardTitle className="text-lg">Recent Transactions</CardTitle>
        <CardDescription>Your latest financial activities</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="flex items-center gap-4">
              <Avatar className="h-10 w-10">
                <AvatarFallback className="text-sm">
                  {transaction.avatar}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">
                  {transaction.description}
                </p>
                <div className="flex items-center gap-2">
                  <Badge
                    className="text-xs"
                    variant={
                      transaction.type === "income" ? "default" : "secondary"
                    }
                  >
                    {transaction.category}
                  </Badge>
                  <span className="text-xs text-muted-foreground">•</span>
                  <p className="text-xs text-muted-foreground">
                    {transaction.date}
                  </p>
                </div>
              </div>
              <div
                className={`font-semibold text-sm ${
                  transaction.type === "income"
                    ? "text-green-600 dark:text-green-400"
                    : "text-red-600 dark:text-red-400"
                }`}
              >
                {transaction.amount}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
