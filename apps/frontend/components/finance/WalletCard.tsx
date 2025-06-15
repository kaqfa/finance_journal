'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import { WalletList } from "@/types";
import { formatCurrency } from "@/lib/utils";
import { MoreHorizontal, Edit, Trash2, Wallet, CreditCard, Smartphone, Banknote } from "lucide-react";

interface WalletCardProps {
  wallet: WalletList;
  onEdit?: (wallet: WalletList) => void;
  onDelete?: (wallet: WalletList) => void;
  onView?: (wallet: WalletList) => void;
}

const getWalletTypeColor = (type: string): "default" | "secondary" | "destructive" | "outline" => {
  switch (type) {
    case 'cash': return 'default';
    case 'bank': return 'secondary';
    case 'ewallet': return 'outline';
    case 'credit': return 'destructive';
    default: return 'default';
  }
};

const getWalletTypeIcon = (type: string) => {
  switch (type) {
    case 'cash': return Banknote;
    case 'bank': return Wallet;
    case 'ewallet': return Smartphone;
    case 'credit': return CreditCard;
    default: return Wallet;
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
  const balanceColor = parseFloat(wallet.current_balance) >= 0 
    ? 'text-green-600 dark:text-green-400' 
    : 'text-red-600 dark:text-red-400';
  
  const WalletTypeIcon = getWalletTypeIcon(wallet.wallet_type);

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div className="flex items-center space-x-2">
          <WalletTypeIcon className="h-4 w-4 text-muted-foreground" />
          <CardTitle className="text-sm font-medium">{wallet.name}</CardTitle>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {onView && (
              <DropdownMenuItem onClick={() => onView(wallet)}>
                View Details
              </DropdownMenuItem>
            )}
            {onEdit && (
              <DropdownMenuItem onClick={() => onEdit(wallet)}>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
            )}
            {onDelete && (
              <DropdownMenuItem 
                onClick={() => onDelete(wallet)}
                className="text-destructive"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Wallet Type Badge */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Type</span>
          <Badge variant={getWalletTypeColor(wallet.wallet_type)}>
            {getWalletTypeLabel(wallet.wallet_type)}
          </Badge>
        </div>
        
        {/* Current Balance */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Balance</span>
          <span className={`text-lg font-bold ${balanceColor}`}>
            {formatCurrency(parseFloat(wallet.current_balance), wallet.currency)}
          </span>
        </div>
        
        {/* Status */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Status</span>
          <Badge variant={wallet.is_active ? 'default' : 'secondary'}>
            {wallet.is_active ? 'Active' : 'Inactive'}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}