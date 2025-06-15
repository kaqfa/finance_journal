import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function AssetsPage() {
  return (
    <BuildingInProgress 
      title="Assets"
      description="Discover and research investment opportunities. Browse stocks, crypto, bonds, and other assets with detailed information, price charts, and market data."
      expectedDate="Q2 2025"
      backUrl="/dashboard"
      backLabel="Back to Dashboard"
    />
  );
}