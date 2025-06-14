"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { useAuth } from "@/contexts/AuthContext";

export default function RegisterPage() {
  const router = useRouter();
  const {
    register,
    loading: authLoading,
    error: authError,
    clearError,
  } = useAuth();

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    password2: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    // Set general error from auth context if it exists
    if (authError) {
      setErrors((prev) => ({
        ...prev,
        general: authError,
      }));
    }

    return () => {
      clearError();
    };
  }, [authError, clearError]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear specific field error when typing
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };

        delete newErrors[name];

        return newErrors;
      });
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.first_name.trim()) {
      newErrors.first_name = "First name is required";
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = "Last name is required";
    }

    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    } else if (formData.username.length < 3) {
      newErrors.username = "Username must be at least 3 characters";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    if (formData.password !== formData.password2) {
      newErrors.password2 = "Passwords do not match";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    try {
      // Menggunakan fungsi register dari AuthContext
      await register({
        first_name: formData.first_name,
        last_name: formData.last_name,
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password2: formData.password2,
      });

      // Redirect akan ditangani oleh AuthContext
    } catch (err: any) {
      console.error("Registration error:", err);
      if (err.response?.data) {
        // Handle API error responses
        const apiErrors = err.response.data;

        setErrors((prev) => ({
          ...prev,
          ...apiErrors,
          general: apiErrors.detail || "Registration failed. Please try again.",
        }));
      } else {
        // Handle network or other errors
        setErrors((prev) => ({
          ...prev,
          general: "An error occurred during registration. Please try again.",
        }));
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Create an Account</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Enter your information to create an account
        </p>
      </div>

      {errors.general && (
        <div className="bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300 p-3 rounded-lg border border-red-200 dark:border-red-800">
          {errors.general}
        </div>
      )}

      <form className="space-y-4" onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="first_name">First Name</Label>
            <Input
              required
              className={errors.first_name ? "border-destructive" : ""}
              id="first_name"
              name="first_name"
              placeholder="Enter your first name"
              value={formData.first_name}
              onChange={handleChange}
            />
            {errors.first_name && (
              <p className="text-sm text-destructive">{errors.first_name}</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="last_name">Last Name</Label>
            <Input
              required
              className={errors.last_name ? "border-destructive" : ""}
              id="last_name"
              name="last_name"
              placeholder="Enter your last name"
              value={formData.last_name}
              onChange={handleChange}
            />
            {errors.last_name && (
              <p className="text-sm text-destructive">{errors.last_name}</p>
            )}
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="username">Username</Label>
          <Input
            required
            className={errors.username ? "border-destructive" : ""}
            id="username"
            name="username"
            placeholder="Choose a username"
            value={formData.username}
            onChange={handleChange}
          />
          {errors.username && (
            <p className="text-sm text-destructive">{errors.username}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            required
            className={errors.email ? "border-destructive" : ""}
            id="email"
            name="email"
            placeholder="Enter your email"
            type="email"
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && (
            <p className="text-sm text-destructive">{errors.email}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            required
            className={errors.password ? "border-destructive" : ""}
            id="password"
            name="password"
            placeholder="Create a password"
            type="password"
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && (
            <p className="text-sm text-destructive">{errors.password}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="password2">Confirm Password</Label>
          <Input
            required
            className={errors.password2 ? "border-destructive" : ""}
            id="password2"
            name="password2"
            placeholder="Confirm your password"
            type="password"
            value={formData.password2}
            onChange={handleChange}
          />
          {errors.password2 && (
            <p className="text-sm text-destructive">{errors.password2}</p>
          )}
        </div>
        <Button className="w-full" disabled={authLoading} type="submit">
          {authLoading ? "Creating Account..." : "Create Account"}
        </Button>
      </form>

      <Separator className="my-4" />

      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link
            className="text-primary hover:underline font-medium"
            href="/login"
          >
            Sign in instead
          </Link>
        </p>
      </div>
    </div>
  );
}
