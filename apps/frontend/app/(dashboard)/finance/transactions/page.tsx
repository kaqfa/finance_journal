"use client";

import { useState, useEffect } from "react";
import {
  Plus,
  Search,
  Filter,
  AlertCircle,
  Receipt,
  ArrowUpRight,
  ArrowDownLeft,
  Calendar,
  Wallet as WalletIcon,
  MoreHorizontal,
  Edit,
  Trash2,
} from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Transaction, WalletList } from "@/types";
import financeAPI from "@/lib/api/finance";
import { formatCurrency } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [wallets, setWallets] = useState<WalletList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedWallet, setSelectedWallet] = useState<string>("all");
  const [selectedType, setSelectedType] = useState<string>("all");

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const params: any = {};

      if (selectedWallet !== "all") {
        params.wallet = parseInt(selectedWallet);
      }

      const response = await financeAPI.getTransactions(params);

      setTransactions(response.data.results);
      setError(null);
    } catch (err) {
      console.error("Error fetching transactions:", err);
      setError("Failed to fetch transactions");
    } finally {
      setLoading(false);
    }
  };

  const fetchWallets = async () => {
    try {
      const response = await financeAPI.getWallets();

      setWallets(response.data.results);
    } catch (err) {
      console.error("Error fetching wallets:", err);
    }
  };

  useEffect(() => {
    fetchWallets();
    fetchTransactions();
  }, [selectedWallet]);

  const handleDeleteTransaction = async (transaction: Transaction) => {
    if (
      confirm(
        `Are you sure you want to delete this transaction: "${transaction.description || "Untitled"}"?`,
      )
    ) {
      try {
        await financeAPI.deleteTransaction(transaction.id);
        await fetchTransactions();
      } catch (err) {
        console.error("Error deleting transaction:", err);
        alert("Failed to delete transaction");
      }
    }
  };

  const filteredTransactions = transactions.filter((transaction) => {
    const matchesSearch =
      searchQuery === "" ||
      transaction.description
        ?.toLowerCase()
        .includes(searchQuery.toLowerCase()) ||
      transaction.category_name
        .toLowerCase()
        .includes(searchQuery.toLowerCase()) ||
      transaction.wallet_name.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesType =
      selectedType === "all" || transaction.type === selectedType;

    return matchesSearch && matchesType;
  });

  if (loading) {
    return (
      <div className="flex-1 space-y-6 p-6 md:p-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Transactions</h1>
          <p className="text-muted-foreground">
            Track your income and expenses
          </p>
        </div>
        <div className="flex justify-center items-center min-h-[200px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 space-y-6 p-6 md:p-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Transactions</h1>
          <p className="text-muted-foreground">
            Track your income and expenses
          </p>
        </div>
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <div className="flex justify-center">
          <Button onClick={fetchTransactions}>Try Again</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-6 p-6 md:p-8">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Transactions</h1>
          <p className="text-muted-foreground">
            Track your income and expenses across all wallets
          </p>
        </div>
        <Button asChild>
          <Link href="/finance/transactions/new">
            <Plus className="mr-2 h-4 w-4" />
            Add Transaction
          </Link>
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-center">
            {/* Search */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                className="pl-9"
                placeholder="Search transactions, categories, or wallets..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            {/* Wallet Filter */}
            <div className="flex items-center gap-2">
              <WalletIcon className="h-4 w-4 text-muted-foreground" />
              <Select value={selectedWallet} onValueChange={setSelectedWallet}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="All wallets" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All wallets</SelectItem>
                  {wallets.map((wallet) => (
                    <SelectItem key={wallet.id} value={wallet.id.toString()}>
                      {wallet.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Type Filter */}
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-muted-foreground" />
              <Select value={selectedType} onValueChange={setSelectedType}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="All types" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All types</SelectItem>
                  <SelectItem value="income">Income</SelectItem>
                  <SelectItem value="expense">Expense</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Transaction List */}
      {filteredTransactions.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center min-h-[400px] gap-6 pt-6">
            <div className="rounded-full bg-muted p-6">
              <Receipt className="h-12 w-12 text-muted-foreground" />
            </div>
            <div className="text-center space-y-3 max-w-md">
              <h3 className="text-xl font-semibold">No transactions found</h3>
              <p className="text-muted-foreground leading-relaxed">
                {searchQuery ||
                selectedWallet !== "all" ||
                selectedType !== "all"
                  ? "No transactions match your current filters. Try adjusting your search criteria."
                  : "Start tracking your finances by adding your first transaction."}
              </p>
            </div>
            <Button asChild size="lg">
              <Link href="/finance/transactions/new">
                <Plus className="mr-2 h-4 w-4" />
                Add Your First Transaction
              </Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredTransactions.map((transaction) => (
            <Card
              key={transaction.id}
              className="transition-all hover:shadow-md"
            >
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  {/* Transaction Icon */}
                  <div
                    className={`rounded-full p-3 ${
                      transaction.type === "income"
                        ? "bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400"
                        : "bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400"
                    }`}
                  >
                    {transaction.type === "income" ? (
                      <ArrowDownLeft className="h-4 w-4" />
                    ) : (
                      <ArrowUpRight className="h-4 w-4" />
                    )}
                  </div>

                  {/* Transaction Details */}
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center gap-2">
                      <p className="font-medium">
                        {transaction.description || "Untitled Transaction"}
                      </p>
                      {transaction.category_name && (
                        <Badge className="text-xs" variant="secondary">
                          {transaction.category_name}
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <WalletIcon className="h-3 w-3" />
                        <span>{transaction.wallet_name}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        <span>
                          {new Date(
                            transaction.transaction_date,
                          ).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Amount */}
                  <div className="text-right">
                    <div
                      className={`text-lg font-semibold ${
                        transaction.type === "income"
                          ? "text-green-600 dark:text-green-400"
                          : "text-red-600 dark:text-red-400"
                      }`}
                    >
                      {transaction.type === "income" ? "+" : "-"}
                      {formatCurrency(parseFloat(transaction.amount), "IDR")}
                    </div>
                  </div>

                  {/* Actions */}
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button className="h-8 w-8 p-0" variant="ghost">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem asChild>
                        <Link
                          href={`/finance/transactions/${transaction.id}/edit`}
                        >
                          <Edit className="mr-2 h-4 w-4" />
                          Edit
                        </Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem
                        className="text-destructive"
                        onClick={() => handleDeleteTransaction(transaction)}
                      >
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
