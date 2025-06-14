import { SVGProps } from "react";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

// Common Types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Finance Types
export interface Wallet {
  id: number;
  name: string;
  wallet_type: 'cash' | 'bank' | 'ewallet' | 'credit' | 'other';
  currency: string;
  initial_balance: string;
  current_balance: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface WalletList {
  id: number;
  name: string;
  wallet_type: 'cash' | 'bank' | 'ewallet' | 'credit' | 'other';
  currency: string;
  current_balance: string;
  is_active: boolean;
}

export interface Transaction {
  id: number;
  wallet: number;
  wallet_name: string;
  category?: number;
  category_name: string;
  amount: string;
  type: 'income' | 'expense' | 'transfer';
  description?: string;
  transaction_date: string;
  created_at: string;
  updated_at: string;
  tag_ids: number[];
}

export interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  icon?: string;
  color?: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: number;
  name: string;
  created_at: string;
}

export interface Transfer {
  id: number;
  from_wallet: number;
  from_wallet_name: string;
  to_wallet: number;
  to_wallet_name: string;
  amount: string;
  description?: string;
  transfer_date: string;
  created_at: string;
  updated_at: string;
}

// Form interfaces
export interface CreateWalletData {
  name: string;
  wallet_type: 'cash' | 'bank' | 'ewallet' | 'credit' | 'other';
  currency: string;
  initial_balance: string;
  is_active?: boolean;
}

export interface CreateTransactionData {
  wallet: number;
  category?: number;
  amount: string;
  type: 'income' | 'expense';
  description?: string;
  transaction_date: string;
  tag_ids?: number[];
}

export interface CreateTransferData {
  from_wallet: number;
  to_wallet: number;
  amount: string;
  description?: string;
  transfer_date: string;
}
