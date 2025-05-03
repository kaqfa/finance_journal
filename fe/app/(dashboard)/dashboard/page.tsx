// fe/app/(dashboard)/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import { Card, CardBody, CardHeader, CardFooter } from "@heroui/card";
import { Button } from "@heroui/button";
import { Divider } from "@heroui/divider";
import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { Spinner } from "@/components/ui/spinner";

// Mock data for initial development
const mockData = {
  portfolioCount: 3,
  walletCount: 5,
  totalInvestment: 25000000,
  totalBalance: 15000000
};

export default function DashboardPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(mockData);
  
  useEffect(() => {
    // Simulate loading data from API
    const timer = setTimeout(() => {
      setLoading(false);
      setData(mockData);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Spinner size="lg" label="Loading dashboard data..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <Card className="bg-gradient-to-r from-blue-100 to-blue-200 dark:from-blue-800/30 dark:to-blue-900/30">
        <CardBody className="py-8">
          <div className="max-w-3xl">
            <h1 className="text-2xl md:text-3xl font-bold mb-2 text-blue-900 dark:text-blue-100">
              Welcome back, {user?.first_name && user?.last_name ? `${user.first_name} ${user.last_name}` : user?.username || "Investor"}!
            </h1>
            <p className="text-blue-800/90 dark:text-blue-200/90 text-sm md:text-base">
              Your financial journey is an ongoing process. Track your investments, manage your finances,
              and make informed decisions to build a secure financial future.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Button as={Link} href="/journal" color="primary" variant="shadow">
                Manage Investments
              </Button>
              <Button as={Link} href="/finance" color="secondary" variant="flat">
                Track Finances
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Summary Cards */}
      <h2 className="text-xl font-semibold text-foreground mt-8 mb-4">Your Summary</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Portfolio Card */}
        <Card className="bg-background shadow-sm">
          <CardHeader className="flex gap-3 pb-0">
            <div className="p-2 rounded-lg bg-primary/10 flex items-center justify-center">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-primary"
              >
                <path
                  d="M20 7H4C2.89543 7 2 7.89543 2 9V19C2 20.1046 2.89543 21 4 21H20C21.1046 21 22 20.1046 22 19V9C22 7.89543 21.1046 7 20 7Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M16 7V5C16 3.89543 15.1046 3 14 3H10C8.89543 3 8 3.89543 8 5V7"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M12 12V16"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M9 14H15"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <p className="text-md">Portfolios</p>
              <p className="text-sm text-default-500">Investment portfolios</p>
            </div>
          </CardHeader>
          <CardBody className="py-4">
            <h3 className="text-2xl font-bold">{data.portfolioCount}</h3>
          </CardBody>
          <Divider />
          <CardFooter>
            <Link href="/journal" className="text-primary text-sm">View Portfolios →</Link>
          </CardFooter>
        </Card>

        {/* Wallet Card */}
        <Card className="bg-background shadow-sm">
          <CardHeader className="flex gap-3 pb-0">
            <div className="p-2 rounded-lg bg-success/10 flex items-center justify-center">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-success"
              >
                <path
                  d="M2 6H22V19C22 19.5304 21.7893 20.0391 21.4142 20.4142C21.0391 20.7893 20.5304 21 20 21H4C3.46957 21 2.96086 20.7893 2.58579 20.4142C2.21071 20.0391 2 19.5304 2 19V6Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M22 6L19.56 3.56C19.1987 3.19866 18.7471 2.91358 18.2489 2.72427C17.7507 2.53496 17.2166 2.44566 16.68 2.46H4C3.46957 2.46 2.96086 2.67071 2.58579 3.04579C2.21071 3.42086 2 3.92957 2 4.46V19C2 18.4696 2.21071 17.9609 2.58579 17.5858C2.96086 17.2107 3.46957 17 4 17H20C20.5304 17 21.0391 17.2107 21.4142 17.5858C21.7893 17.9609 22 18.4696 22 19V6Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M17 11C17.5523 11 18 10.5523 18 10C18 9.44772 17.5523 9 17 9C16.4477 9 16 9.44772 16 10C16 10.5523 16.4477 11 17 11Z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <p className="text-md">Wallets</p>
              <p className="text-sm text-default-500">Financial accounts</p>
            </div>
          </CardHeader>
          <CardBody className="py-4">
            <h3 className="text-2xl font-bold">{data.walletCount}</h3>
          </CardBody>
          <Divider />
          <CardFooter>
            <Link href="/finance" className="text-success text-sm">View Wallets →</Link>
          </CardFooter>
        </Card>

        {/* Total Investment Card */}
        <Card className="bg-background shadow-sm">
          <CardHeader className="flex gap-3 pb-0">
            <div className="p-2 rounded-lg bg-warning/10 flex items-center justify-center">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-warning"
              >
                <path
                  d="M12 2L19.17 6.5V17.5L12 22L4.83 17.5V6.5L12 2Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M12 22V12"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M19.17 6.5L12 12L4.83 6.5"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <p className="text-md">Total Investment</p>
              <p className="text-sm text-default-500">All portfolios</p>
            </div>
          </CardHeader>
          <CardBody className="py-4">
            <h3 className="text-2xl font-bold">Rp 25,000,000</h3>
          </CardBody>
          <Divider />
          <CardFooter>
            <Link href="/journal" className="text-warning text-sm">Investment Details →</Link>
          </CardFooter>
        </Card>

        {/* Total Balance Card */}
        <Card className="bg-background shadow-sm">
          <CardHeader className="flex gap-3 pb-0">
            <div className="p-2 rounded-lg bg-secondary/10 flex items-center justify-center">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-secondary"
              >
                <path
                  d="M12 1V23"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M17 5H9.5C8.57174 5 7.6815 5.36875 7.02513 6.02513C6.36875 6.6815 6 7.57174 6 8.5C6 9.42826 6.36875 10.3185 7.02513 10.9749C7.6815 11.6313 8.57174 12 9.5 12H14.5C15.4283 12 16.3185 12.3687 16.9749 13.0251C17.6313 13.6815 18 14.5717 18 15.5C18 16.4283 17.6313 17.3185 16.9749 17.9749C16.3185 18.6313 15.4283 19 14.5 19H6"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <p className="text-md">Total Balance</p>
              <p className="text-sm text-default-500">All wallets</p>
            </div>
          </CardHeader>
          <CardBody className="py-4">
            <h3 className="text-2xl font-bold">Rp 15,000,000</h3>
          </CardBody>
          <Divider />
          <CardFooter>
            <Link href="/finance" className="text-secondary text-sm">Finance Details →</Link>
          </CardFooter>
        </Card>
      </div>

      {/* Quick Actions Section */}
      <h2 className="text-xl font-semibold text-foreground mt-8 mb-4">Quick Actions</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="bg-background shadow-sm">
          <CardBody className="p-6">
            <h3 className="text-lg font-semibold mb-4">Investment Actions</h3>
            <div className="flex flex-wrap gap-2">
              <Button as={Link} href="/journal/portfolio/create" size="sm" color="primary">
                Create Portfolio
              </Button>
              <Button as={Link} href="/journal/transaction/create" size="sm" color="primary" variant="flat">
                Add Transaction
              </Button>
              <Button as={Link} href="/journal" size="sm" color="primary" variant="light">
                View All
              </Button>
            </div>
          </CardBody>
        </Card>
        
        <Card className="bg-background shadow-sm">
          <CardBody className="p-6">
            <h3 className="text-lg font-semibold mb-4">Finance Actions</h3>
            <div className="flex flex-wrap gap-2">
              <Button as={Link} href="/finance/wallet/create" size="sm" color="success">
                Create Wallet
              </Button>
              <Button as={Link} href="/finance/transaction/create" size="sm" color="success" variant="flat">
                Add Transaction
              </Button>
              <Button as={Link} href="/finance" size="sm" color="success" variant="light">
                View All
              </Button>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}