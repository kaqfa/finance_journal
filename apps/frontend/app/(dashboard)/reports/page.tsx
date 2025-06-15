import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function ReportsPage() {
  return (
    <BuildingInProgress 
      title="Reports"
      description="Generate comprehensive financial reports and insights. View detailed analytics, export data, and track your financial progress over time with customizable reports."
      expectedDate="Q2 2025"
      backUrl="/dashboard"
      backLabel="Back to Dashboard"
    />
  );
}