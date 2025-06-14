'use client';

import { useState } from 'react';
import { 
  Modal, 
  ModalContent, 
  ModalHeader, 
  ModalBody, 
  ModalFooter
} from "@heroui/modal";
import { Button } from "@heroui/button";
import { Input } from "@heroui/input";
import { Select, SelectItem } from "@heroui/select";
import { Switch } from "@heroui/switch";
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
    <Modal 
      isOpen={isOpen} 
      onClose={handleClose}
      placement="top-center"
    >
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">
          {wallet ? 'Edit Wallet' : 'Create New Wallet'}
        </ModalHeader>
        
        <ModalBody>
          <Input
            autoFocus
            label="Wallet Name"
            placeholder="Enter wallet name"
            value={formData.name}
            onValueChange={(value) => setFormData(prev => ({ ...prev, name: value }))}
            isInvalid={!!errors.name}
            errorMessage={errors.name}
          />

          <Select
            label="Wallet Type"
            placeholder="Select wallet type"
            selectedKeys={[formData.wallet_type]}
            onSelectionChange={(keys) => {
              const selectedKey = Array.from(keys)[0] as string;
              setFormData(prev => ({ ...prev, wallet_type: selectedKey as any }));
            }}
          >
            {walletTypes.map((type) => (
              <SelectItem key={type.key} value={type.key}>
                {type.label}
              </SelectItem>
            ))}
          </Select>

          <Select
            label="Currency"
            placeholder="Select currency"
            selectedKeys={[formData.currency]}
            onSelectionChange={(keys) => {
              const selectedKey = Array.from(keys)[0] as string;
              setFormData(prev => ({ ...prev, currency: selectedKey }));
            }}
          >
            {currencies.map((currency) => (
              <SelectItem key={currency.key} value={currency.key}>
                {currency.label}
              </SelectItem>
            ))}
          </Select>

          <Input
            label="Initial Balance"
            placeholder="0"
            type="number"
            step="0.01"
            value={formData.initial_balance}
            onValueChange={(value) => setFormData(prev => ({ ...prev, initial_balance: value }))}
            isInvalid={!!errors.initial_balance}
            errorMessage={errors.initial_balance}
            startContent={
              <div className="pointer-events-none flex items-center">
                <span className="text-default-400 text-small">{formData.currency}</span>
              </div>
            }
          />

          <Switch
            isSelected={formData.is_active}
            onValueChange={(value) => setFormData(prev => ({ ...prev, is_active: value }))}
          >
            <span className="text-small">Active</span>
          </Switch>
        </ModalBody>
        
        <ModalFooter>
          <Button 
            color="danger" 
            variant="flat" 
            onPress={handleClose}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button 
            color="primary" 
            onPress={handleSubmit}
            isLoading={isLoading}
          >
            {wallet ? 'Update' : 'Create'} Wallet
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}