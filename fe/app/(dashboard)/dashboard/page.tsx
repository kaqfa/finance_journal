"use client";

import { Button } from "@heroui/button";
import { Card, CardBody, CardHeader } from "@heroui/card";
import { useAuth } from "@/contexts/AuthContext";

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="p-4">
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <Button color="primary" variant="flat" onPress={logout}>
            Logout
          </Button>
        </CardHeader>
        <CardBody>
          <p className="mb-4">
            Welcome to your dashboard, <strong>{user?.username}</strong>!
          </p>
          <p>
            This is a temporary dashboard page. The full dashboard features will
            be implemented in future updates.
          </p>
        </CardBody>
      </Card>
    </div>
  );
}