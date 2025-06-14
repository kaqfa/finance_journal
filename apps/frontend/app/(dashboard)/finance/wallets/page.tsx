'use client';

import { useState, useEffect } from 'react';
import { Button } from "@heroui/button";
import { Spinner } from "@heroui/spinner";
import { useDisclosure } from "@heroui/modal";
import { WalletList, Wallet } from "@/types";
import financeAPI from "@/lib/api/finance";
import WalletCard from "@/components/finance/WalletCard";
import WalletForm from "@/components/finance/WalletForm";

export default function WalletsPage() {
  const [wallets, setWallets] = useState<WalletList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedWallet, setSelectedWallet] = useState<Wallet | undefined>();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { isOpen, onOpen, onClose } = useDisclosure();

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
      onOpen();
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
    onOpen();
  };

  const handleFormClose = () => {
    setSelectedWallet(undefined);
    onClose();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[200px] gap-4">
        <p className="text-danger">{error}</p>
        <Button color="primary" onPress={fetchWallets}>
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Wallets</h1>
          <p className="text-default-500">Manage your wallets and accounts</p>
        </div>
        <Button color="primary" onPress={handleAddNew}>
          Add Wallet
        </Button>
      </div>

      {wallets.length === 0 ? (
        <div className="flex flex-col items-center justify-center min-h-[300px] gap-4">
          <p className="text-default-500 text-center">
            No wallets found. Create your first wallet to get started.
          </p>
          <Button color="primary" onPress={handleAddNew}>
            Create Wallet
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {wallets && wallets.length > 0 && wallets.map((wallet) => (
            <WalletCard
              key={wallet.id}
              wallet={wallet}
              onEdit={handleEditWallet}
              onDelete={handleDeleteWallet}
            />
          ))}
        </div>
      )}

      <WalletForm
        isOpen={isOpen}
        onClose={handleFormClose}
        onSubmit={handleCreateWallet}
        wallet={selectedWallet}
        isLoading={isSubmitting}
      />
    </div>
  );
}