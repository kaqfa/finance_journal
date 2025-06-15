import { authApi, createEndpoint } from "../config/axios";
import {
  Wallet,
  WalletList,
  Transaction,
  Category,
  Tag,
  Transfer,
  CreateWalletData,
  CreateTransactionData,
  CreateTransferData,
  PaginatedResponse,
} from "../../types";

const FINANCE_BASE = "finance";

const financeAPI = {
  // Wallet endpoints
  getWallets: (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    ordering?: string;
  }) =>
    authApi.get<PaginatedResponse<WalletList>>(
      createEndpoint(`${FINANCE_BASE}/wallets/`),
      { params },
    ),

  getWallet: (id: number) =>
    authApi.get<Wallet>(createEndpoint(`${FINANCE_BASE}/wallets/${id}/`)),

  createWallet: (data: CreateWalletData) =>
    authApi.post<Wallet>(createEndpoint(`${FINANCE_BASE}/wallets/`), data),

  updateWallet: (id: number, data: Partial<CreateWalletData>) =>
    authApi.put<Wallet>(createEndpoint(`${FINANCE_BASE}/wallets/${id}/`), data),

  deleteWallet: (id: number) =>
    authApi.delete(createEndpoint(`${FINANCE_BASE}/wallets/${id}/`)),

  getWalletChoices: () =>
    authApi.get<any>(createEndpoint(`${FINANCE_BASE}/wallets/choices/`)),

  recalculateWallet: (id: number) =>
    authApi.post<Wallet>(
      createEndpoint(`${FINANCE_BASE}/wallets/${id}/recalculate/`),
    ),

  // Transaction endpoints
  getTransactions: (params?: {
    wallet?: number;
    limit?: number;
    offset?: number;
  }) =>
    authApi.get<{
      count: number;
      next: string | null;
      previous: string | null;
      results: Transaction[];
    }>(createEndpoint(`${FINANCE_BASE}/transactions/`), { params }),

  getTransaction: (id: number) =>
    authApi.get<Transaction>(
      createEndpoint(`${FINANCE_BASE}/transactions/${id}/`),
    ),

  createTransaction: (data: CreateTransactionData) =>
    authApi.post<Transaction>(
      createEndpoint(`${FINANCE_BASE}/transactions/`),
      data,
    ),

  updateTransaction: (id: number, data: Partial<CreateTransactionData>) =>
    authApi.put<Transaction>(
      createEndpoint(`${FINANCE_BASE}/transactions/${id}/`),
      data,
    ),

  deleteTransaction: (id: number) =>
    authApi.delete(createEndpoint(`${FINANCE_BASE}/transactions/${id}/`)),

  // Category endpoints
  getCategories: () =>
    authApi.get<Category[]>(createEndpoint(`${FINANCE_BASE}/categories/`)),

  createCategory: (data: {
    name: string;
    type: "income" | "expense";
    icon?: string;
    color?: string;
  }) =>
    authApi.post<Category>(createEndpoint(`${FINANCE_BASE}/categories/`), data),

  updateCategory: (
    id: number,
    data: {
      name?: string;
      type?: "income" | "expense";
      icon?: string;
      color?: string;
    },
  ) =>
    authApi.put<Category>(
      createEndpoint(`${FINANCE_BASE}/categories/${id}/`),
      data,
    ),

  deleteCategory: (id: number) =>
    authApi.delete(createEndpoint(`${FINANCE_BASE}/categories/${id}/`)),

  // Tag endpoints
  getTags: () => authApi.get<Tag[]>(createEndpoint(`${FINANCE_BASE}/tags/`)),

  createTag: (data: { name: string }) =>
    authApi.post<Tag>(createEndpoint(`${FINANCE_BASE}/tags/`), data),

  updateTag: (id: number, data: { name: string }) =>
    authApi.put<Tag>(createEndpoint(`${FINANCE_BASE}/tags/${id}/`), data),

  deleteTag: (id: number) =>
    authApi.delete(createEndpoint(`${FINANCE_BASE}/tags/${id}/`)),

  // Transfer endpoints
  getTransfers: (params?: { limit?: number; offset?: number }) =>
    authApi.get<{
      count: number;
      next: string | null;
      previous: string | null;
      results: Transfer[];
    }>(createEndpoint(`${FINANCE_BASE}/transfers/`), { params }),

  createTransfer: (data: CreateTransferData) =>
    authApi.post<Transfer>(createEndpoint(`${FINANCE_BASE}/transfers/`), data),
};

export default financeAPI;
