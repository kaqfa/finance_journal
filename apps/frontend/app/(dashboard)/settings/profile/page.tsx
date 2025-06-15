import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function ProfilePage() {
  return (
    <BuildingInProgress 
      title="Profile"
      description="Manage your account information and personal settings. Update your profile details, change password, and configure account preferences."
      expectedDate="Q1 2025"
      backUrl="/dashboard"
      backLabel="Back to Dashboard"
    />
  );
}