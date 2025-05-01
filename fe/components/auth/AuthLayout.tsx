"use client";

import React from "react";
import { Card, CardBody } from "@heroui/card";
import Image from "next/image";
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
              src="/logo.svg"
              alt="Finance Journal Logo"
              width={64}
              height={64}
              className="h-16 w-16"
              priority
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
          <CardBody>
            {children}
          </CardBody>
        </Card>
        
        <div className="mt-8 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>© {new Date().getFullYear()} Finance Journal. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
}