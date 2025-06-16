"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useAuth } from "@/contexts/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const {
    login,
    loading: authLoading,
    error: authError,
    clearError,
  } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [showRegistrationSuccess, setShowRegistrationSuccess] = useState(false);

  useEffect(() => {
    // Check if user just registered successfully
    const registered = searchParams.get("registered");

    if (registered === "true") {
      setShowRegistrationSuccess(true);
    }

    // Set error from auth context if it exists
    if (authError) {
      setError(authError);
    }

    return () => {
      clearError();
    };
  }, [searchParams, authError, clearError]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear errors when typing
    if (error) {
      setError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // Menggunakan fungsi login dari AuthContext
      await login(formData.username, formData.password);
      // Redirect akan ditangani otomatis oleh fungsi login
    } catch (err: any) {
      console.error("Login error:", err);
      setError(
        err.response?.data?.detail ||
          "Gagal login. Silakan cek kembali username dan password Anda.",
      );
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Welcome Back</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Enter your credentials to sign in to your account
        </p>
      </div>

      {showRegistrationSuccess && (
        <div className="bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 p-3 rounded-lg border border-green-200 dark:border-green-800">
          Registration successful! You can now log in with your credentials.
        </div>
      )}

      {error && (
        <div className="bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300 p-3 rounded-lg border border-red-200 dark:border-red-800">
          {error}
        </div>
      )}

      <form className="space-y-4" onSubmit={handleSubmit}>
        <div className="space-y-2">
          <Label htmlFor="username">Username</Label>
          <Input
            required
            className="w-full"
            id="username"
            name="username"
            placeholder="Enter your username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            required
            className="w-full"
            id="password"
            name="password"
            placeholder="Enter your password"
            type="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className="flex justify-end">
          <Link
            className="text-sm text-primary hover:underline"
            href="/forget-password"
          >
            Forgot password?
          </Link>
        </div>
        <Button className="w-full" disabled={authLoading} type="submit">
          {authLoading ? "Signing In..." : "Sign In"}
        </Button>
      </form>

      <Separator className="my-4" />

      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          Don&apos;t have an account?{" "}
          <Link
            className="text-primary hover:underline font-medium"
            href="/register"
          >
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}
