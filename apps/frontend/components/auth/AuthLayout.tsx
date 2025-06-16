"use client";

import React from "react";
import Image from "next/image";

import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface AuthLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export default function AuthLayout({ children, className }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-slate-100 dark:from-gray-900 dark:to-gray-950 p-4">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center justify-center mb-8">
          <div className="mb-4 p-2 bg-white dark:bg-gray-800 rounded-full shadow-md">
            <Image
              priority
              alt="Finance Journal Logo"
              className="h-16 w-16"
              height={64}
              src="/logo.svg"
              width={64}
            />
          </div>
          <h1 className="text-2xl font-bold text-center text-gray-900 dark:text-white">
            Finance Journal App
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-1">
            Manage your investments and finances in one place
          </p>
        </div>

        <Card className={cn("w-full", className)}>
          <CardContent className="p-6">{children}</CardContent>
        </Card>

        <div className="mt-8 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>
            © {new Date().getFullYear()} Finance Journal. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
