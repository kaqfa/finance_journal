import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function HelpPage() {
  return (
    <BuildingInProgress
      backLabel="Back to Dashboard"
      backUrl="/dashboard"
      description="Get assistance with using WealthWise. Access documentation, FAQs, tutorials, and contact our support team for any questions or issues."
      expectedDate="Q1 2025"
      title="Help & Support"
    />
  );
}
