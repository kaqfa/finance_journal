"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { InvestmentPortfolio } from "@/types";

const portfolioSchema = z.object({
  name: z
    .string()
    .min(1, "Portfolio name is required")
    .max(100, "Name too long"),
  description: z.string().max(500, "Description too long").optional(),
  initial_capital: z
    .string()
    .min(1, "Initial capital is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
      message: "Initial capital must be a positive number",
    }),
  risk_level: z.enum(["low", "medium", "high"], {
    required_error: "Please select a risk level",
  }),
  is_active: z.boolean().default(true),
});

type PortfolioFormData = z.infer<typeof portfolioSchema>;

interface PortfolioFormProps {
  portfolio?: InvestmentPortfolio | null;
  onSubmit: (data: PortfolioFormData) => Promise<void>;
  onCancel: () => void;
}

const riskLevelOptions = [
  {
    value: "low",
    label: "Low Risk",
    description:
      "Conservative investments with lower returns but higher safety",
    color: "text-green-600",
  },
  {
    value: "medium",
    label: "Medium Risk",
    description: "Balanced approach with moderate risk and returns",
    color: "text-yellow-600",
  },
  {
    value: "high",
    label: "High Risk",
    description: "Aggressive investments with higher potential returns",
    color: "text-red-600",
  },
];

export function PortfolioForm({
  portfolio,
  onSubmit,
  onCancel,
}: PortfolioFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<PortfolioFormData>({
    resolver: zodResolver(portfolioSchema),
    defaultValues: {
      name: portfolio?.name || "",
      description: portfolio?.description || "",
      initial_capital: portfolio?.initial_capital || "",
      risk_level: portfolio?.risk_level || "medium",
      is_active: portfolio?.is_active ?? true,
    },
  });

  const handleSubmit = async (data: PortfolioFormData) => {
    try {
      setIsSubmitting(true);
      await onSubmit(data);
    } catch (error) {
      console.error("Failed to submit portfolio:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const watchedCapital = form.watch("initial_capital");
  const formatCurrency = (amount: string) => {
    if (!amount || isNaN(Number(amount))) return "";

    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(Number(amount));
  };

  return (
    <Form {...form}>
      <form className="space-y-6" onSubmit={form.handleSubmit(handleSubmit)}>
        <div className="grid gap-6 md:grid-cols-2">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Portfolio Name</FormLabel>
                <FormControl>
                  <Input placeholder="Enter portfolio name" {...field} />
                </FormControl>
                <FormDescription>
                  Choose a descriptive name for your portfolio
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="initial_capital"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Initial Capital</FormLabel>
                <FormControl>
                  <Input placeholder="1000000" type="number" {...field} />
                </FormControl>
                <FormDescription>
                  {watchedCapital && formatCurrency(watchedCapital)}
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description (Optional)</FormLabel>
              <FormControl>
                <Textarea
                  className="min-h-[100px]"
                  placeholder="Describe your investment strategy, goals, or notes..."
                  {...field}
                />
              </FormControl>
              <FormDescription>
                Add details about your investment strategy or goals
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="risk_level"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Risk Level</FormLabel>
              <Select defaultValue={field.value} onValueChange={field.onChange}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select risk level" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {riskLevelOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      <div className="flex flex-col">
                        <span className={`font-medium ${option.color}`}>
                          {option.label}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          {option.description}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormDescription>
                Choose the risk level that matches your investment strategy
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="is_active"
          render={({ field }) => (
            <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
              <div className="space-y-0.5">
                <FormLabel className="text-base">Active Portfolio</FormLabel>
                <FormDescription>
                  Active portfolios are included in calculations and reports
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
            </FormItem>
          )}
        />

        <div className="flex gap-3 pt-4">
          <Button
            disabled={isSubmitting}
            type="button"
            variant="outline"
            onClick={onCancel}
          >
            Cancel
          </Button>
          <Button disabled={isSubmitting} type="submit">
            {isSubmitting
              ? "Saving..."
              : portfolio
                ? "Update Portfolio"
                : "Create Portfolio"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
