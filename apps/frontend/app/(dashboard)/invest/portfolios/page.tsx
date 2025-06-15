"use client";

import { useState, useEffect } from "react";
import {
  Plus,
  Edit,
  Trash2,
  TrendingUp,
  TrendingDown,
  DollarSign,
  PieChart,
  BarChart3,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import investAPI from "@/lib/api/invest";
import { InvestmentPortfolio } from "@/types";
import { PortfolioForm } from "@/components/invest/PortfolioForm";

export default function PortfoliosPage() {
  const [portfolios, setPortfolios] = useState<InvestmentPortfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPortfolio, setEditingPortfolio] =
    useState<InvestmentPortfolio | null>(null);

  const fetchPortfolios = async () => {
    try {
      setLoading(true);
      const response = await investAPI.getPortfolios();

      setPortfolios(
        Array.isArray(response.data.results) ? response.data.results : [],
      );
    } catch (error) {
      console.error("Failed to fetch portfolios:", error);
      setPortfolios([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const handleCreatePortfolio = async (data: any) => {
    try {
      await investAPI.createPortfolio(data);
      fetchPortfolios();
      setDialogOpen(false);
    } catch (error) {
      console.error("Failed to create portfolio:", error);
    }
  };

  const handleEditPortfolio = (portfolio: InvestmentPortfolio) => {
    setEditingPortfolio(portfolio);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingPortfolio(null);
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case "low":
        return "text-green-600 bg-green-100";
      case "medium":
        return "text-yellow-600 bg-yellow-100";
      case "high":
        return "text-red-600 bg-red-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  const formatCurrency = (amount: string | undefined) => {
    if (!amount) return "0";

    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(parseFloat(amount));
  };

  const formatPercentage = (value: string | undefined) => {
    if (!value) return "0%";
    const num = parseFloat(value);

    return `${num >= 0 ? "+" : ""}${num.toFixed(2)}%`;
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Portfolios</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-6 bg-gray-200 rounded w-2/3" />
                <div className="h-4 bg-gray-100 rounded w-1/3" />
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="h-8 bg-gray-200 rounded" />
                  <div className="h-4 bg-gray-100 rounded" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Investment Portfolios
          </h1>
          <p className="text-muted-foreground">
            Manage and track your investment portfolios across different asset
            classes
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Portfolio
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>
                {editingPortfolio ? "Edit Portfolio" : "Create Portfolio"}
              </DialogTitle>
            </DialogHeader>
            <PortfolioForm
              portfolio={editingPortfolio}
              onCancel={handleCloseDialog}
              onSubmit={handleCreatePortfolio}
            />
          </DialogContent>
        </Dialog>
      </div>

      {/* Portfolio Statistics */}
      {portfolios.length > 0 && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Portfolios
              </CardTitle>
              <PieChart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{portfolios.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Value</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(
                  portfolios
                    .reduce(
                      (sum, p) => sum + parseFloat(p.total_value || "0"),
                      0,
                    )
                    .toString(),
                )}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Active Portfolios
              </CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {portfolios.filter((p) => p.is_active).length}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total P&L</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {formatCurrency(
                  portfolios
                    .reduce((sum, p) => sum + parseFloat(p.total_pnl || "0"), 0)
                    .toString(),
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Portfolio Cards */}
      {portfolios.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <PieChart className="h-16 w-16 mx-auto mb-4 text-muted-foreground opacity-50" />
            <h3 className="text-lg font-medium">No portfolios yet</h3>
            <p className="text-muted-foreground mb-4">
              Create your first investment portfolio to start tracking your
              investments
            </p>
            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Create Portfolio
                </Button>
              </DialogTrigger>
            </Dialog>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {portfolios.map((portfolio) => (
            <Card
              key={portfolio.id}
              className="hover:shadow-md transition-shadow"
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <CardTitle className="text-lg">{portfolio.name}</CardTitle>
                    <div className="flex items-center gap-2">
                      <Badge
                        className={getRiskLevelColor(portfolio.risk_level)}
                        variant="secondary"
                      >
                        {portfolio.risk_level.toUpperCase()} RISK
                      </Badge>
                      {!portfolio.is_active && (
                        <Badge variant="outline">Inactive</Badge>
                      )}
                    </div>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button size="sm" variant="ghost">
                        <Edit className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem
                        onClick={() => handleEditPortfolio(portfolio)}
                      >
                        <Edit className="mr-2 h-4 w-4" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem>
                        <PieChart className="mr-2 h-4 w-4" />
                        View Details
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
                {portfolio.description && (
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {portfolio.description}
                  </p>
                )}
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">
                      Initial Capital
                    </p>
                    <p className="font-medium">
                      {formatCurrency(portfolio.initial_capital)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">
                      Current Value
                    </p>
                    <p className="font-medium">
                      {formatCurrency(portfolio.total_value)}
                    </p>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">P&L</span>
                    <div className="flex items-center gap-1">
                      {portfolio.total_pnl &&
                      parseFloat(portfolio.total_pnl) >= 0 ? (
                        <TrendingUp className="h-3 w-3 text-green-600" />
                      ) : (
                        <TrendingDown className="h-3 w-3 text-red-600" />
                      )}
                      <span
                        className={`text-sm font-medium ${
                          portfolio.total_pnl &&
                          parseFloat(portfolio.total_pnl) >= 0
                            ? "text-green-600"
                            : "text-red-600"
                        }`}
                      >
                        {formatCurrency(portfolio.total_pnl)} (
                        {formatPercentage(portfolio.total_pnl_percentage)})
                      </span>
                    </div>
                  </div>
                </div>

                <div className="text-xs text-muted-foreground">
                  Created {new Date(portfolio.created_at).toLocaleDateString()}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
