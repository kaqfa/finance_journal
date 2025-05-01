"use client";

import { useState } from "react";
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import { Link } from "@heroui/link";
import { Divider } from "@heroui/divider";
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
      // Use the API utility instead of direct fetch
      await authAPI.resetPassword(email);
      setSuccess(true);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.error || 
        err.message || 
        "An error occurred during the password reset request"
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
        <div className="bg-danger-50 text-danger p-3 rounded-lg">
          {error}
        </div>
      )}
      
      {success ? (
        <div className="space-y-4">
          <div className="bg-success-50 text-success p-4 rounded-lg text-center">
            <h3 className="text-lg font-medium mb-2">Reset Email Sent!</h3>
            <p>
              If an account exists with the email you entered, you'll receive password reset instructions.
            </p>
          </div>
          <Button 
            as={Link} 
            href="/login" 
            color="primary" 
            fullWidth
          >
            Return to Login
          </Button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email"
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            variant="bordered"
            isRequired
            fullWidth
          />
          <Button
            type="submit"
            color="primary"
            isLoading={isLoading}
            fullWidth
          >
            Send Reset Link
          </Button>
        </form>
      )}
      
      <Divider className="my-4" />
      
      <div className="text-center">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Remember your password?{" "}
          <Link href="/login" color="primary">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}