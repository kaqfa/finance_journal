import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function TransfersPage() {
  return (
    <BuildingInProgress
      backLabel="Back to Finance"
      backUrl="/finance"
      description="Transfer money between your wallets seamlessly. Track inter-wallet movements and maintain accurate balance records across all your accounts."
      expectedDate="Q1 2025"
      title="Transfers"
    />
  );
}
