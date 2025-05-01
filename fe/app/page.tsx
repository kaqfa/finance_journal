"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Spinner } from "@/components/ui/spinner";
import { isAuthenticated } from "@/lib/auth";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Check if the user is authenticated
    if (isAuthenticated()) {
      // If authenticated, redirect to dashboard
      router.push("/dashboard");
    } else {
      // If not authenticated, redirect to login
      router.push("/login");
    }
  }, [router]);

  // Show loading spinner while redirecting
  return (
    <div className="flex justify-center items-center min-h-screen">
      <Spinner size="lg" label="Redirecting..." />
    </div>
  );
}