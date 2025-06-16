import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function HoldingsPage() {
  return (
    <BuildingInProgress
      backLabel="Back to Dashboard"
      backUrl="/dashboard"
      description="View all your current investment positions in one place. Track your holdings across portfolios with real-time P&L, cost basis, and performance metrics."
      expectedDate="Q2 2025"
      title="Holdings"
    />
  );
}
