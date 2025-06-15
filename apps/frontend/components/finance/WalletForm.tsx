'use client';

import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Wallet, CreateWalletData } from "@/types";

interface WalletFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CreateWalletData) => Promise<void>;
  wallet?: Wallet;
  isLoading?: boolean;
}

const walletTypes = [
  { key: 'cash', label: 'Cash' },
  { key: 'bank', label: 'Bank Account' },
  { key: 'ewallet', label: 'E-Wallet' },
  { key: 'credit', label: 'Credit Card' },
  { key: 'other', label: 'Other' }
];

const currencies = [
  { key: 'IDR', label: 'Indonesian Rupiah (IDR)' },
  { key: 'USD', label: 'US Dollar (USD)' },
  { key: 'EUR', label: 'Euro (EUR)' },
  { key: 'SGD', label: 'Singapore Dollar (SGD)' }
];

export default function WalletForm({ 
  isOpen, 
  onClose, 
  onSubmit, 
  wallet, 
  isLoading = false 
}: WalletFormProps) {
  const [formData, setFormData] = useState<CreateWalletData>({
    name: wallet?.name || '',
    wallet_type: wallet?.wallet_type || 'cash',
    currency: wallet?.currency || 'IDR',
    initial_balance: wallet?.initial_balance || '0',
    is_active: wallet?.is_active !== undefined ? wallet.is_active : true
  });

  const [errors, setErrors] = useState<Partial<CreateWalletData>>({});

  // Update form data when wallet prop changes
  useState(() => {
    if (wallet) {
      setFormData({
        name: wallet.name || '',
        wallet_type: wallet.wallet_type || 'cash',
        currency: wallet.currency || 'IDR',
        initial_balance: wallet.initial_balance || '0',
        is_active: wallet.is_active !== undefined ? wallet.is_active : true
      });
    }
  });

  const validateForm = (): boolean => {
    const newErrors: Partial<CreateWalletData> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Wallet name is required';
    }

    if (!formData.initial_balance || isNaN(parseFloat(formData.initial_balance))) {
      newErrors.initial_balance = 'Valid initial balance is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      await onSubmit(formData);
      onClose();
      // Reset form
      setFormData({
        name: '',
        wallet_type: 'cash',
        currency: 'IDR',
        initial_balance: '0',
        is_active: true
      });
      setErrors({});
    } catch (error) {
      console.error('Error submitting wallet form:', error);
    }
  };

  const handleClose = () => {
    onClose();
    setErrors({});
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {wallet ? 'Edit Wallet' : 'Create New Wallet'}
          </DialogTitle>
          <DialogDescription>
            {wallet ? 'Update your wallet information.' : 'Add a new wallet to track your finances.'}
          </DialogDescription>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="name">Wallet Name</Label>
            <Input
              id="name"
              placeholder="Enter wallet name"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              className={errors.name ? "border-destructive" : ""}
            />
            {errors.name && (
              <p className="text-sm text-destructive">{errors.name}</p>
            )}
          </div>

          <div className="grid gap-2">
            <Label htmlFor="wallet-type">Wallet Type</Label>
            <Select 
              value={formData.wallet_type} 
              onValueChange={(value) => 
                setFormData(prev => ({ ...prev, wallet_type: value as any }))
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Select wallet type" />
              </SelectTrigger>
              <SelectContent>
                {walletTypes.map((type) => (
                  <SelectItem key={type.key} value={type.key}>
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="currency">Currency</Label>
            <Select 
              value={formData.currency} 
              onValueChange={(value) => 
                setFormData(prev => ({ ...prev, currency: value }))
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Select currency" />
              </SelectTrigger>
              <SelectContent>
                {currencies.map((currency) => (
                  <SelectItem key={currency.key} value={currency.key}>
                    {currency.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="initial-balance">Initial Balance</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground text-sm">
                {formData.currency}
              </span>
              <Input
                id="initial-balance"
                type="number"
                step="0.01"
                placeholder="0"
                value={formData.initial_balance}
                onChange={(e) => setFormData(prev => ({ ...prev, initial_balance: e.target.value }))}
                className={`pl-12 ${errors.initial_balance ? "border-destructive" : ""}`}
              />
            </div>
            {errors.initial_balance && (
              <p className="text-sm text-destructive">{errors.initial_balance}</p>
            )}
          </div>

          <div className="flex items-center space-x-2">
            <Switch
              id="is-active"
              checked={formData.is_active}
              onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_active: checked }))}
            />
            <Label htmlFor="is-active">Active</Label>
          </div>
        </div>
        
        <DialogFooter>
          <Button 
            variant="outline" 
            onClick={handleClose}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button 
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? "Saving..." : (wallet ? 'Update' : 'Create')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}