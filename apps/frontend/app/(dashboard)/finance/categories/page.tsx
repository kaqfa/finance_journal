import { BuildingInProgress } from "@/components/ui/building-in-progress";

export default function CategoriesPage() {
  return (
    <BuildingInProgress 
      title="Categories"
      description="Organize your transactions with custom categories. Create, edit, and manage income and expense categories to better track your spending patterns."
      expectedDate="Q1 2025"
      backUrl="/finance"
      backLabel="Back to Finance"
    />
  );
}