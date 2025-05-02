"use client";

import { useState, useEffect } from "react";
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import { Link } from "@heroui/link";
import { Divider } from "@heroui/divider";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();
  const { register, loading: authLoading, error: authError, clearError } = useAuth();
  
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
      setErrors(prev => ({
        ...prev,
        general: authError
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
        password2: formData.password2
      });
      
      // Redirect akan ditangani oleh AuthContext
    } catch (err: any) {
      console.error("Registration error:", err);
      if (err.response?.data) {
        // Handle API error responses
        const apiErrors = err.response.data;
        setErrors(prev => ({
          ...prev,
          ...apiErrors,
          general: apiErrors.detail || 'Registration failed. Please try again.'
        }));
      } else {
        // Handle network or other errors
        setErrors(prev => ({
          ...prev,
          general: 'An error occurred during registration. Please try again.'
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
        <div className="bg-danger-50 text-danger p-3 rounded-lg">
          {errors.general}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input
            label="First Name"
            name="first_name"
            placeholder="Enter your first name"
            value={formData.first_name}
            onChange={handleChange}
            variant="bordered"
            isInvalid={!!errors.first_name}
            errorMessage={errors.first_name}
            isRequired
          />
          <Input
            label="Last Name"
            name="last_name"
            placeholder="Enter your last name"
            value={formData.last_name}
            onChange={handleChange}
            variant="bordered"
            isInvalid={!!errors.last_name}
            errorMessage={errors.last_name}
            isRequired
          />
        </div>
        <Input
          label="Username"
          name="username"
          placeholder="Choose a username"
          value={formData.username}
          onChange={handleChange}
          variant="bordered"
          isInvalid={!!errors.username}
          errorMessage={errors.username}
          isRequired
        />
        <Input
          label="Email"
          name="email"
          type="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={handleChange}
          variant="bordered"
          isInvalid={!!errors.email}
          errorMessage={errors.email}
          isRequired
        />
        <Input
          label="Password"
          name="password"
          type="password"
          placeholder="Create a password"
          value={formData.password}
          onChange={handleChange}
          variant="bordered"
          isInvalid={!!errors.password}
          errorMessage={errors.password}
          isRequired
        />
        <Input
          label="Confirm Password"
          name="password2"
          type="password"
          placeholder="Confirm your password"
          value={formData.password2}
          onChange={handleChange}
          variant="bordered"
          isInvalid={!!errors.password2}
          errorMessage={errors.password2}
          isRequired
        />
        <Button
          type="submit"
          color="primary"
          isLoading={authLoading}
          fullWidth
        >
          Create Account
        </Button>
      </form>
      
      <Divider className="my-4" />
      
      <div className="text-center">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Already have an account?{" "}
          <Link href="/login" color="primary">
            Sign in instead
          </Link>
        </p>
      </div>
    </div>
  );
}