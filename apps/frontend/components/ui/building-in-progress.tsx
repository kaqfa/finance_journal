"use client";

import { Construction, ArrowLeft, Clock } from "lucide-react";
import Link from "next/link";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface BuildingInProgressProps {
  title: string;
  description?: string;
  expectedDate?: string;
  backUrl?: string;
  backLabel?: string;
}

export function BuildingInProgress({
  title,
  description,
  expectedDate,
  backUrl = "/dashboard",
  backLabel = "Back to Dashboard",
}: BuildingInProgressProps) {
  return (
    <div className="flex-1 space-y-6 p-6 md:p-8">
      {/* Page Header */}
      <div className="flex items-center gap-4">
        <Button asChild size="icon" variant="ghost">
          <Link href={backUrl}>
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
          <p className="text-muted-foreground">
            This feature is currently under development
          </p>
        </div>
      </div>

      {/* Building in Progress Card */}
      <Card className="max-w-2xl">
        <CardContent className="flex flex-col items-center justify-center min-h-[400px] gap-6 pt-6">
          {/* Construction Icon */}
          <div className="rounded-full bg-amber-100 p-6 dark:bg-amber-900/20">
            <Construction className="h-12 w-12 text-amber-600 dark:text-amber-400" />
          </div>

          {/* Content */}
          <div className="text-center space-y-3 max-w-md">
            <h3 className="text-xl font-semibold">Building in Progress</h3>
            <p className="text-muted-foreground leading-relaxed">
              {description ||
                `We're working hard to bring you the ${title.toLowerCase()} feature. This page will be available soon with all the functionality you need.`}
            </p>

            {expectedDate && (
              <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground mt-4 p-3 bg-muted rounded-lg">
                <Clock className="h-4 w-4" />
                <span>Expected completion: {expectedDate}</span>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            <Button asChild>
              <Link href={backUrl}>
                <ArrowLeft className="mr-2 h-4 w-4" />
                {backLabel}
              </Link>
            </Button>
            <Button asChild variant="outline">
              <Link href="/dashboard">Go to Dashboard</Link>
            </Button>
          </div>

          {/* Progress Indicator */}
          <div className="w-full max-w-sm space-y-2">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Development Progress</span>
              <span>Coming Soon</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-amber-600 h-2 rounded-full animate-pulse"
                style={{ width: "35%" }}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
