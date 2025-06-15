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
  wallet_type: "cash" | "bank" | "ewallet" | "credit" | "other";
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
  wallet_type: "cash" | "bank" | "ewallet" | "credit" | "other";
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
  type: "income" | "expense" | "transfer";
  description?: string;
  transaction_date: string;
  created_at: string;
  updated_at: string;
  tag_ids: number[];
}

export interface Category {
  id: number;
  name: string;
  type: "income" | "expense";
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
  wallet_type: "cash" | "bank" | "ewallet" | "credit" | "other";
  currency: string;
  initial_balance: string;
  is_active?: boolean;
}

export interface CreateTransactionData {
  wallet: number;
  category?: number;
  amount: string;
  type: "income" | "expense";
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

// Investment Types
export interface Asset {
  id: string;
  symbol: string;
  name: string;
  type: "stock" | "crypto" | "bond" | "reit" | "mutual_fund";
  exchange?: string;
  sector?: string;
  currency: string;
  is_active: boolean;
  latest_price?: string;
  price_change_24h?: string;
  created_at: string;
  updated_at: string;
}

export interface InvestmentPortfolio {
  id: string;
  name: string;
  description?: string;
  initial_capital: string;
  risk_level: "low" | "medium" | "high";
  is_active: boolean;
  created_at: string;
  updated_at: string;
  total_value?: string;
  total_pnl?: string;
  total_pnl_percentage?: string;
}

export interface InvestmentHolding {
  id: string;
  portfolio: string;
  portfolio_name: string;
  asset: string;
  asset_symbol: string;
  asset_name: string;
  quantity: string;
  average_price: string;
  current_price?: string;
  current_value?: string;
  unrealized_pnl?: string;
  unrealized_pnl_percentage?: string;
  last_updated: string;
}

export interface InvestmentTransaction {
  id: string;
  portfolio: string;
  portfolio_name: string;
  asset: string;
  asset_symbol: string;
  asset_name: string;
  type: "buy" | "sell" | "dividend";
  quantity: string;
  price: string;
  total_amount: string;
  fees?: string;
  transaction_date: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Investment Form interfaces
export interface CreatePortfolioData {
  name: string;
  description?: string;
  initial_capital: string;
  risk_level: "low" | "medium" | "high";
  is_active?: boolean;
}

export interface CreateInvestmentTransactionData {
  portfolio: string;
  asset: string;
  type: "buy" | "sell" | "dividend";
  quantity: string;
  price: string;
  fees?: string;
  transaction_date: string;
  notes?: string;
}
