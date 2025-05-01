"use client";

import { useState, useEffect } from "react";
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import { Link } from "@heroui/link";
import { Divider } from "@heroui/divider";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

export default function LoginPage() {
  const searchParams = useSearchParams();
  const { login, loading: authLoading, error: authError, clearError } = useAuth();
  
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [showRegistrationSuccess, setShowRegistrationSuccess] = useState(false);

  useEffect(() => {
    // Check if user just registered successfully
    const registered = searchParams.get('registered');
    if (registered === 'true') {
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
      await login(formData.username, formData.password);
      // No need to redirect, Auth context will handle it
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "Login failed");
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
        <div className="bg-success-50 text-success p-3 rounded-lg">
          Registration successful! You can now log in with your credentials.
        </div>
      )}
      
      {error && (
        <div className="bg-danger-50 text-danger p-3 rounded-lg">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Username"
          name="username"
          placeholder="Enter your username"
          value={formData.username}
          onChange={handleChange}
          variant="bordered"
          isRequired
          fullWidth
        />
        <Input
          label="Password"
          name="password"
          placeholder="Enter your password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          variant="bordered"
          isRequired
          fullWidth
        />
        <div className="flex justify-end">
          <Link href="/forget-password" color="primary" size="sm">
            Forgot password?
          </Link>
        </div>
        <Button
          type="submit"
          color="primary"
          isLoading={authLoading}
          fullWidth
        >
          Sign In
        </Button>
      </form>
      
      <Divider className="my-4" />
      
      <div className="text-center">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Don't have an account?{" "}
          <Link href="/register" color="primary">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}