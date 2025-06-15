"use client";

import { useState, useEffect } from "react";
import {
  Search,
  Filter,
  TrendingUp,
  TrendingDown,
  BarChart3,
  Building,
  Bitcoin,
  Coins,
  FileText,
  Landmark,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import investAPI from "@/lib/api/invest";
import { Asset } from "@/types";

const assetTypeIcons = {
  stock: Building,
  crypto: Bitcoin,
  bond: FileText,
  reit: Landmark,
  mutual_fund: Coins,
};

const assetTypeColors = {
  stock: "text-blue-600 bg-blue-100",
  crypto: "text-orange-600 bg-orange-100",
  bond: "text-green-600 bg-green-100",
  reit: "text-purple-600 bg-purple-100",
  mutual_fund: "text-indigo-600 bg-indigo-100",
};

export default function AssetsPage() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedType, setSelectedType] = useState<string>("all");
  const [sortBy, setSortBy] = useState<string>("name");

  const fetchAssets = async () => {
    try {
      setLoading(true);
      const response = await investAPI.getAssets({
        search: searchTerm || undefined,
        type: selectedType !== "all" ? selectedType : undefined,
        ordering: sortBy,
      });

      setAssets(
        Array.isArray(response.data.results) ? response.data.results : [],
      );
    } catch (error) {
      console.error("Failed to fetch assets:", error);
      setAssets([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchAssets();
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm, selectedType, sortBy]);

  const formatCurrency = (amount: string | undefined) => {
    if (!amount) return "N/A";

    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(parseFloat(amount));
  };

  const formatPercentage = (value: string | undefined) => {
    if (!value) return "N/A";
    const num = parseFloat(value);

    return `${num >= 0 ? "+" : ""}${num.toFixed(2)}%`;
  };

  const getAssetTypeIcon = (type: string) => {
    const IconComponent =
      assetTypeIcons[type as keyof typeof assetTypeIcons] || BarChart3;

    return IconComponent;
  };

  const filteredAssets = assets.filter((asset) => {
    const matchesSearch =
      asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      asset.symbol.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = selectedType === "all" || asset.type === selectedType;

    return matchesSearch && matchesType;
  });

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Assets</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
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
          <h1 className="text-3xl font-bold tracking-tight">Asset Browser</h1>
          <p className="text-muted-foreground">
            Discover and research investment opportunities across different
            asset classes
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            className="pl-10"
            placeholder="Search assets by name or symbol..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="flex gap-2">
          <Select value={selectedType} onValueChange={setSelectedType}>
            <SelectTrigger className="w-[140px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="stock">Stocks</SelectItem>
              <SelectItem value="crypto">Crypto</SelectItem>
              <SelectItem value="bond">Bonds</SelectItem>
              <SelectItem value="reit">REITs</SelectItem>
              <SelectItem value="mutual_fund">Mutual Funds</SelectItem>
            </SelectContent>
          </Select>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button size="sm" variant="outline">
                <Filter className="mr-2 h-4 w-4" />
                Sort
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setSortBy("name")}>
                Name (A-Z)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setSortBy("-name")}>
                Name (Z-A)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setSortBy("symbol")}>
                Symbol (A-Z)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setSortBy("-latest_price")}>
                Price (High to Low)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setSortBy("latest_price")}>
                Price (Low to High)
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Asset Statistics */}
      <div className="grid gap-4 md:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{filteredAssets.length}</div>
          </CardContent>
        </Card>
        {Object.entries(assetTypeIcons).map(([type, IconComponent]) => {
          const count = filteredAssets.filter(
            (asset) => asset.type === type,
          ).length;

          return (
            <Card key={type}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium capitalize">
                  {type.replace("_", " ")}
                </CardTitle>
                <IconComponent className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{count}</div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Asset Cards */}
      {filteredAssets.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <BarChart3 className="h-16 w-16 mx-auto mb-4 text-muted-foreground opacity-50" />
            <h3 className="text-lg font-medium">No assets found</h3>
            <p className="text-muted-foreground">
              {searchTerm
                ? "Try adjusting your search terms or filters"
                : "No assets available for the selected criteria"}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredAssets.map((asset) => {
            const IconComponent = getAssetTypeIcon(asset.type);
            const priceChange = asset.price_change_24h
              ? parseFloat(asset.price_change_24h)
              : 0;

            return (
              <Card
                key={asset.id}
                className="hover:shadow-md transition-shadow cursor-pointer"
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <IconComponent className="h-5 w-5 text-muted-foreground" />
                        <CardTitle className="text-lg">
                          {asset.symbol}
                        </CardTitle>
                      </div>
                      <p className="text-sm text-muted-foreground line-clamp-1">
                        {asset.name}
                      </p>
                      <Badge
                        className={
                          assetTypeColors[
                            asset.type as keyof typeof assetTypeColors
                          ]
                        }
                        variant="secondary"
                      >
                        {asset.type.replace("_", " ").toUpperCase()}
                      </Badge>
                    </div>
                  </div>
                  {asset.exchange && (
                    <p className="text-xs text-muted-foreground">
                      {asset.exchange}
                    </p>
                  )}
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-muted-foreground">
                        Current Price
                      </p>
                      <p className="font-medium">
                        {formatCurrency(asset.latest_price)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">
                        24h Change
                      </p>
                      <div className="flex items-center gap-1">
                        {priceChange >= 0 ? (
                          <TrendingUp className="h-3 w-3 text-green-600" />
                        ) : (
                          <TrendingDown className="h-3 w-3 text-red-600" />
                        )}
                        <span
                          className={`text-sm font-medium ${
                            priceChange >= 0 ? "text-green-600" : "text-red-600"
                          }`}
                        >
                          {formatPercentage(asset.price_change_24h)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {asset.sector && (
                    <div>
                      <p className="text-sm text-muted-foreground">Sector</p>
                      <p className="text-sm font-medium">{asset.sector}</p>
                    </div>
                  )}

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div
                        className={`w-2 h-2 rounded-full ${
                          asset.is_active ? "bg-green-500" : "bg-gray-400"
                        }`}
                      />
                      <span className="text-xs text-muted-foreground">
                        {asset.is_active ? "Active" : "Inactive"}
                      </span>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {asset.currency}
                    </span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
