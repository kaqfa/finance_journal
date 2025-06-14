'use client';

import { Card, CardBody, CardHeader } from "@heroui/card";
import { Chip } from "@heroui/chip";
import { Button } from "@heroui/button";
import { WalletList } from "@/types";
import { formatCurrency } from "@/lib/utils";

interface WalletCardProps {
  wallet: WalletList;
  onEdit?: (wallet: WalletList) => void;
  onDelete?: (wallet: WalletList) => void;
  onView?: (wallet: WalletList) => void;
}

const getWalletTypeColor = (type: string): "default" | "primary" | "secondary" | "success" | "warning" | "danger" => {
  switch (type) {
    case 'cash': return 'success';
    case 'bank': return 'primary';
    case 'ewallet': return 'secondary';
    case 'credit': return 'warning';
    default: return 'default';
  }
};

const getWalletTypeLabel = (type: string) => {
  switch (type) {
    case 'cash': return 'Cash';
    case 'bank': return 'Bank';
    case 'ewallet': return 'E-Wallet';
    case 'credit': return 'Credit';
    case 'other': return 'Other';
    default: return type;
  }
};

export default function WalletCard({ wallet, onEdit, onDelete, onView }: WalletCardProps) {
  const balanceColor = parseFloat(wallet.current_balance) >= 0 ? 'text-success' : 'text-danger';

  return (
    <Card className="w-full">
      <CardHeader className="flex gap-3 justify-between">
        <div className="flex flex-col">
          <p className="text-md font-semibold">{wallet.name}</p>
          <Chip 
            color={getWalletTypeColor(wallet.wallet_type)}
            size="sm" 
            variant="flat"
          >
            {getWalletTypeLabel(wallet.wallet_type)}
          </Chip>
        </div>
        <div className="flex gap-1">
          {onView && (
            <Button
              size="sm"
              variant="light"
              onPress={() => onView(wallet)}
            >
              View
            </Button>
          )}
          {onEdit && (
            <Button
              size="sm"
              variant="light"
              color="primary"
              onPress={() => onEdit(wallet)}
            >
              Edit
            </Button>
          )}
          {onDelete && (
            <Button
              size="sm"
              variant="light"
              color="danger"
              onPress={() => onDelete(wallet)}
            >
              Delete
            </Button>
          )}
        </div>
      </CardHeader>
      
      <CardBody className="pt-0">
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <span className="text-small text-default-500">Current Balance</span>
            <span className={`text-lg font-bold ${balanceColor}`}>
              {formatCurrency(parseFloat(wallet.current_balance), wallet.currency)}
            </span>
          </div>
          
          
          <div className="flex justify-between items-center">
            <span className="text-small text-default-500">Status</span>
            <Chip 
              color={wallet.is_active ? 'success' : 'default'}
              size="sm"
              variant="flat"
            >
              {wallet.is_active ? 'Active' : 'Inactive'}
            </Chip>
          </div>
        </div>
      </CardBody>
    </Card>
  );
}