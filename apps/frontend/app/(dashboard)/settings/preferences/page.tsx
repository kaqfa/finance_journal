import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function PreferencesPage() {
  return (
    <BuildingInProgress
      backLabel="Back to Dashboard"
      backUrl="/dashboard"
      description="Customize your application experience. Configure themes, language settings, notification preferences, and other app-specific options."
      expectedDate="Q1 2025"
      title="Preferences"
    />
  );
}
