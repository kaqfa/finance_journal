import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function PortfoliosPage() {
  return (
    <BuildingInProgress 
      title="Portfolios"
      description="Manage your investment portfolios with comprehensive tracking. Create portfolios, monitor performance, and analyze your investment strategy across different asset classes."
      expectedDate="Q2 2025"
      backUrl="/dashboard"
      backLabel="Back to Dashboard"
    />
  );
}