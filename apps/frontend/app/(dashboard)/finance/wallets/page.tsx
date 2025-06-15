'use client';

import { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { WalletList, Wallet } from "@/types";
import financeAPI from "@/lib/api/finance";
import WalletCard from "@/components/finance/WalletCard";
import WalletForm from "@/components/finance/WalletForm";
import { Plus, Wallet as WalletIcon, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function WalletsPage() {
  const [wallets, setWallets] = useState<WalletList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedWallet, setSelectedWallet] = useState<Wallet | undefined>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const fetchWallets = async () => {
    try {
      setLoading(true);
      const response = await financeAPI.getWallets();
      setWallets(response.data.results);
      setError(null);
    } catch (err) {
      console.error('Error fetching wallets:', err);
      setError('Failed to fetch wallets');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWallets();
  }, []);

  const handleCreateWallet = async (data: any) => {
    try {
      setIsSubmitting(true);
      if (selectedWallet) {
        await financeAPI.updateWallet(selectedWallet.id, data);
      } else {
        await financeAPI.createWallet(data);
      }
      await fetchWallets();
      setSelectedWallet(undefined);
    } catch (err) {
      console.error('Error saving wallet:', err);
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEditWallet = async (wallet: WalletList) => {
    try {
      // Fetch full wallet details for editing
      const response = await financeAPI.getWallet(wallet.id);
      setSelectedWallet(response.data);
      setIsDialogOpen(true);
    } catch (err) {
      console.error('Error fetching wallet details:', err);
      alert('Failed to load wallet details');
    }
  };

  const handleDeleteWallet = async (wallet: WalletList) => {
    if (confirm(`Are you sure you want to delete "${wallet.name}"?`)) {
      try {
        await financeAPI.deleteWallet(wallet.id);
        await fetchWallets();
      } catch (err) {
        console.error('Error deleting wallet:', err);
        alert('Failed to delete wallet');
      }
    }
  };

  const handleAddNew = () => {
    setSelectedWallet(undefined);
    setIsDialogOpen(true);
  };

  const handleFormClose = () => {
    setSelectedWallet(undefined);
    setIsDialogOpen(false);
  };

  if (loading) {
    return (
      <div className="flex-1 space-y-6 p-6 md:p-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Wallets</h1>
          <p className="text-muted-foreground">
            Manage your wallets and accounts
          </p>
        </div>
        <div className="flex justify-center items-center min-h-[200px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 space-y-6 p-6 md:p-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Wallets</h1>
          <p className="text-muted-foreground">
            Manage your wallets and accounts
          </p>
        </div>
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            {error}
          </AlertDescription>
        </Alert>
        <div className="flex justify-center">
          <Button onClick={fetchWallets}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-6 p-6 md:p-8">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Wallets</h1>
          <p className="text-muted-foreground">
            Manage your wallets and accounts
          </p>
        </div>
        <Button onClick={handleAddNew}>
          <Plus className="mr-2 h-4 w-4" />
          Add Wallet
        </Button>
      </div>

      {/* Wallet Grid or Empty State */}
      {wallets.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center min-h-[400px] gap-6 pt-6">
            <div className="rounded-full bg-muted p-6">
              <WalletIcon className="h-12 w-12 text-muted-foreground" />
            </div>
            <div className="text-center space-y-3 max-w-md">
              <h3 className="text-xl font-semibold">No wallets found</h3>
              <p className="text-muted-foreground leading-relaxed">
                Create your first wallet to get started with tracking your finances. 
                You can add different types of accounts like cash, bank accounts, and e-wallets.
              </p>
            </div>
            <Button onClick={handleAddNew} size="lg">
              <Plus className="mr-2 h-4 w-4" />
              Create Your First Wallet
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {wallets.map((wallet) => (
            <WalletCard
              key={wallet.id}
              wallet={wallet}
              onEdit={handleEditWallet}
              onDelete={handleDeleteWallet}
            />
          ))}
        </div>
      )}

      {/* Wallet Form Dialog */}
      <WalletForm
        isOpen={isDialogOpen}
        onClose={handleFormClose}
        onSubmit={handleCreateWallet}
        wallet={selectedWallet}
        isLoading={isSubmitting}
      />
    </div>
  );
}