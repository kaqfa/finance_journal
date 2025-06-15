import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function TransfersPage() {
  return (
    <BuildingInProgress 
      title="Transfers"
      description="Transfer money between your wallets seamlessly. Track inter-wallet movements and maintain accurate balance records across all your accounts."
      expectedDate="Q1 2025"
      backUrl="/finance"
      backLabel="Back to Finance"
    />
  );
}