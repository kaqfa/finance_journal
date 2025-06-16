import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function AnalyticsPage() {
  return (
    <BuildingInProgress
      backLabel="Back to Dashboard"
      backUrl="/dashboard"
      description="Get comprehensive insights into your financial data with interactive charts, spending patterns, and custom reports to make informed financial decisions."
      expectedDate="Q2 2025"
      title="Analytics"
    />
  );
}
