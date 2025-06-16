"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowLeft,
  Save,
  AlertCircle,
  Wallet,
  FolderOpen,
  Tags,
  Calendar,
  DollarSign,
  Plus,
  X,
} from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { WalletList, Category, Tag, CreateTransactionData } from "@/types";
import financeAPI from "@/lib/api/finance";

export default function NewTransactionPage() {
  const router = useRouter();
  const [wallets, setWallets] = useState<WalletList[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<CreateTransactionData>({
    wallet: 0,
    amount: "",
    type: "expense",
    description: "",
    transaction_date: new Date().toISOString().split("T")[0],
    category: undefined,
    tag_ids: [],
  });

  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);
  const [errors, setErrors] = useState<Partial<CreateTransactionData>>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        console.log("Fetching form data...");
        const [walletsRes, categoriesRes, tagsRes] = await Promise.all([
          financeAPI.getWallets(),
          financeAPI.getCategories(),
          financeAPI.getTags(),
        ]);

        console.log("Wallets response:", walletsRes.data);
        console.log("Categories response:", categoriesRes.data);
        console.log("Tags response:", tagsRes.data);

        setWallets(
          Array.isArray(walletsRes.data.results) ? walletsRes.data.results : [],
        );
        
        // Handle both direct array and paginated response for categories
        const categoriesData = Array.isArray(categoriesRes.data) 
          ? categoriesRes.data 
          : categoriesRes.data?.results || [];
        console.log("Processed categories:", categoriesData);
        setCategories(categoriesData);
        
        // Handle both direct array and paginated response for tags
        const tagsData = Array.isArray(tagsRes.data) 
          ? tagsRes.data 
          : tagsRes.data?.results || [];
        console.log("Processed tags:", tagsData);
        setTags(tagsData);
        
        setError(null);
      } catch (err: any) {
        console.error("Error fetching data:", err);
        console.error("Error response:", err.response);
        setError("Failed to load form data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const validateForm = (): boolean => {
    const newErrors: Partial<CreateTransactionData> = {};

    if (!formData.wallet || formData.wallet === 0) {
      newErrors.wallet = 1; // Use 1 to indicate error since wallet is number
    }

    if (
      !formData.amount ||
      isNaN(parseFloat(formData.amount)) ||
      parseFloat(formData.amount) <= 0
    ) {
      newErrors.amount = "Valid amount is required";
    }

    if (!formData.description?.trim()) {
      newErrors.description = "Description is required";
    }

    if (!formData.transaction_date) {
      newErrors.transaction_date = "Transaction date is required";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    try {
      setSubmitting(true);
      const submitData = {
        ...formData,
        tag_ids: selectedTags.map((tag) => tag.id),
      };

      await financeAPI.createTransaction(submitData);
      router.push("/finance/transactions");
    } catch (err: any) {
      console.error("Error creating transaction:", err);
      setError(err.response?.data?.detail || "Failed to create transaction");
    } finally {
      setSubmitting(false);
    }
  };

  const addTag = (tag: Tag) => {
    const currentTags = Array.isArray(selectedTags) ? selectedTags : [];

    if (!currentTags.find((t) => t.id === tag.id)) {
      setSelectedTags([...currentTags, tag]);
    }
  };

  const removeTag = (tagId: number) => {
    setSelectedTags(
      Array.isArray(selectedTags)
        ? selectedTags.filter((tag) => tag.id !== tagId)
        : [],
    );
  };

  const filteredCategories = Array.isArray(categories)
    ? categories.filter((cat) => cat.type === formData.type)
    : [];
  const availableTags = Array.isArray(tags)
    ? tags.filter(
        (tag) =>
          !Array.isArray(selectedTags) ||
          !selectedTags.find((t) => t.id === tag.id),
      )
    : [];

  if (loading) {
    return (
      <div className="flex-1 space-y-6 p-6 md:p-8">
        <div className="flex items-center gap-4">
          <Button asChild size="icon" variant="ghost">
            <Link href="/finance/transactions">
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight">
              Add Transaction
            </h1>
            <p className="text-muted-foreground">
              Create a new income or expense record
            </p>
          </div>
        </div>
        <div className="flex justify-center items-center min-h-[200px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-6 p-6 md:p-8">
      {/* Page Header */}
      <div className="flex items-center gap-4">
        <Button asChild size="icon" variant="ghost">
          <Link href="/finance/transactions">
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight">Add Transaction</h1>
          <p className="text-muted-foreground">
            Create a new income or expense record for your financial tracking
          </p>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Transaction Form */}
      <form className="max-w-2xl space-y-6" onSubmit={handleSubmit}>
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5" />
              Transaction Details
            </CardTitle>
            <CardDescription>
              Enter the basic information for your transaction
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Transaction Type */}
            <div className="space-y-2">
              <Label htmlFor="type">Transaction Type</Label>
              <Select
                value={formData.type}
                onValueChange={(value) =>
                  setFormData((prev) => ({
                    ...prev,
                    type: value as "income" | "expense",
                    category: undefined, // Reset category when type changes
                  }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="income">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-green-500" />
                      Income
                    </div>
                  </SelectItem>
                  <SelectItem value="expense">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-red-500" />
                      Expense
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Amount */}
            <div className="space-y-2">
              <Label htmlFor="amount">Amount (IDR)</Label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground text-sm">
                  Rp
                </span>
                <Input
                  className={`pl-12 ${errors.amount ? "border-destructive" : ""}`}
                  id="amount"
                  placeholder="0"
                  step="0.01"
                  type="number"
                  value={formData.amount}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, amount: e.target.value }))
                  }
                />
              </div>
              {errors.amount && (
                <p className="text-sm text-destructive">{errors.amount}</p>
              )}
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                className={errors.description ? "border-destructive" : ""}
                id="description"
                placeholder="Enter transaction description..."
                rows={3}
                value={formData.description}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    description: e.target.value,
                  }))
                }
              />
              {errors.description && (
                <p className="text-sm text-destructive">{errors.description}</p>
              )}
            </div>

            {/* Transaction Date */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2" htmlFor="date">
                <Calendar className="h-4 w-4" />
                Transaction Date
              </Label>
              <Input
                className={errors.transaction_date ? "border-destructive" : ""}
                id="date"
                type="date"
                value={formData.transaction_date}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    transaction_date: e.target.value,
                  }))
                }
              />
              {errors.transaction_date && (
                <p className="text-sm text-destructive">
                  {errors.transaction_date}
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Wallet and Category */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Wallet className="h-5 w-5" />
              Wallet & Category
            </CardTitle>
            <CardDescription>
              Choose the wallet and category for this transaction
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Wallet Selection */}
            <div className="space-y-2">
              <Label htmlFor="wallet">Wallet</Label>
              <Select
                value={formData.wallet.toString()}
                onValueChange={(value) =>
                  setFormData((prev) => ({ ...prev, wallet: parseInt(value) }))
                }
              >
                <SelectTrigger
                  className={errors.wallet ? "border-destructive" : ""}
                >
                  <SelectValue placeholder="Select wallet" />
                </SelectTrigger>
                <SelectContent>
                  {wallets.map((wallet) => (
                    <SelectItem key={wallet.id} value={wallet.id.toString()}>
                      <div className="flex items-center justify-between w-full">
                        <span>{wallet.name}</span>
                        <Badge className="ml-2" variant="outline">
                          {wallet.wallet_type}
                        </Badge>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.wallet && (
                <p className="text-sm text-destructive">
                  Please select a wallet
                </p>
              )}
            </div>

            {/* Category Selection */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2" htmlFor="category">
                <FolderOpen className="h-4 w-4" />
                Category (Optional)
              </Label>
              <Select
                value={formData.category?.toString() || "none"}
                onValueChange={(value) =>
                  setFormData((prev) => ({
                    ...prev,
                    category: value === "none" ? undefined : parseInt(value),
                  }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">No category</SelectItem>
                  {filteredCategories.map((category) => (
                    <SelectItem
                      key={category.id}
                      value={category.id.toString()}
                    >
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Tags */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Tags className="h-5 w-5" />
              Tags
            </CardTitle>
            <CardDescription>
              Add tags to help organize and filter your transactions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Selected Tags */}
            {selectedTags.length > 0 && (
              <div className="space-y-2">
                <Label>Selected Tags</Label>
                <div className="flex flex-wrap gap-2">
                  {selectedTags.map((tag) => (
                    <Badge
                      key={tag.id}
                      className="flex items-center gap-1"
                      variant="default"
                    >
                      {tag.name}
                      <Button
                        className="h-auto p-0 text-current hover:bg-transparent"
                        size="sm"
                        type="button"
                        variant="ghost"
                        onClick={() => removeTag(tag.id)}
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Available Tags */}
            {availableTags.length > 0 && (
              <div className="space-y-2">
                <Label>Available Tags</Label>
                <div className="flex flex-wrap gap-2">
                  {availableTags.map((tag) => (
                    <Badge
                      key={tag.id}
                      className="cursor-pointer hover:bg-muted"
                      variant="outline"
                      onClick={() => addTag(tag)}
                    >
                      <Plus className="h-3 w-3 mr-1" />
                      {tag.name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {availableTags.length === 0 && selectedTags.length === 0 && (
              <p className="text-sm text-muted-foreground">
                No tags available. You can create tags in the tag management
                section.
              </p>
            )}
          </CardContent>
        </Card>

        {/* Form Actions */}
        <div className="flex items-center gap-4 pt-6">
          <Button className="min-w-24" disabled={submitting} type="submit">
            {submitting ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Save Transaction
              </>
            )}
          </Button>
          <Button asChild type="button" variant="outline">
            <Link href="/finance/transactions">Cancel</Link>
          </Button>
        </div>
      </form>
    </div>
  );
}
