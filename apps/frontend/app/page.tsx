"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Spinner } from "@/components/ui/spinner";
import { isAuthenticated } from "@/lib/auth";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Fungsi untuk memeriksa token
    const checkAuthToken = () => {
      try {
        // Cek apakah ada token di localStorage
        const accessToken = localStorage.getItem('accessToken');
        const refreshToken = localStorage.getItem('refreshToken');
        
        if (accessToken && refreshToken) {
          console.log("Found authentication tokens, redirecting to dashboard");
          // Jika ada token, redirect ke dashboard
          router.push("/dashboard");
        } else {
          console.log("No authentication tokens found, redirecting to login");
          // Jika tidak ada token, redirect ke login
          router.push("/login");
        }
      } catch (error) {
        console.error("Error checking authentication:", error);
        // Jika terjadi error, amannya redirect ke login
        router.push("/login");
      }
    };
    
    // Panggil fungsi check token
    checkAuthToken();
  }, [router]);

  // Show loading spinner while redirecting
  return (
    <div className="flex justify-center items-center min-h-screen">
      <Spinner size="lg" label="Redirecting..." />
    </div>
  );
}