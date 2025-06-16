"use client";

import { useState } from "react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { authAPI } from "@/lib/api";

export default function ForgetPasswordPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // Menggunakan authAPI untuk reset password
      await authAPI.resetPassword(email);

      // Set success state untuk menampilkan konfirmasi
      setSuccess(true);
    } catch (err: any) {
      console.error("Password reset error:", err);
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Terjadi kesalahan saat memproses permintaan reset password. Silakan coba lagi.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Reset Password</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Enter your email to receive password reset instructions
        </p>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300 p-3 rounded-lg border border-red-200 dark:border-red-800">
          {error}
        </div>
      )}

      {success ? (
        <div className="space-y-4">
          <div className="bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 p-4 rounded-lg text-center border border-green-200 dark:border-green-800">
            <h3 className="text-lg font-medium mb-2">Reset Email Sent!</h3>
            <p>
              If an account exists with the email you entered, you&apos;ll
              receive password reset instructions.
            </p>
          </div>
          <Button asChild className="w-full">
            <Link href="/login">Return to Login</Link>
          </Button>
        </div>
      ) : (
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              required
              className="w-full"
              id="email"
              placeholder="Enter your email address"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <Button className="w-full" disabled={isLoading} type="submit">
            {isLoading ? "Sending..." : "Send Reset Link"}
          </Button>
        </form>
      )}

      <Separator className="my-4" />

      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          Remember your password?{" "}
          <Link
            className="text-primary hover:underline font-medium"
            href="/login"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
