import { authApi, createEndpoint } from "../config/axios";
import {
  Asset,
  InvestmentPortfolio,
  InvestmentHolding,
  InvestmentTransaction,
  CreatePortfolioData,
  CreateInvestmentTransactionData,
  PaginatedResponse,
} from "../../types";

const INVEST_BASE = "invest";

const investAPI = {
  // Portfolio endpoints
  getPortfolios: (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    ordering?: string;
  }) =>
    authApi.get<PaginatedResponse<InvestmentPortfolio>>(
      createEndpoint(`${INVEST_BASE}/portfolios/`),
      { params },
    ),

  getPortfolio: (id: string) =>
    authApi.get<InvestmentPortfolio>(
      createEndpoint(`${INVEST_BASE}/portfolios/${id}/`),
    ),

  createPortfolio: (data: CreatePortfolioData) =>
    authApi.post<InvestmentPortfolio>(
      createEndpoint(`${INVEST_BASE}/portfolios/`),
      data,
    ),

  updatePortfolio: (id: string, data: Partial<CreatePortfolioData>) =>
    authApi.put<InvestmentPortfolio>(
      createEndpoint(`${INVEST_BASE}/portfolios/${id}/`),
      data,
    ),

  deletePortfolio: (id: string) =>
    authApi.delete(createEndpoint(`${INVEST_BASE}/portfolios/${id}/`)),

  // Asset endpoints
  getAssets: (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    type?: string;
    ordering?: string;
  }) =>
    authApi.get<PaginatedResponse<Asset>>(
      createEndpoint(`${INVEST_BASE}/assets/`),
      { params },
    ),

  getAsset: (id: string) =>
    authApi.get<Asset>(createEndpoint(`${INVEST_BASE}/assets/${id}/`)),

  searchAssets: (query: string, type?: string) =>
    authApi.get<Asset[]>(createEndpoint(`${INVEST_BASE}/assets/search/`), {
      params: { q: query, type },
    }),

  // Holdings endpoints
  getHoldings: (params?: {
    portfolio?: string;
    limit?: number;
    offset?: number;
  }) =>
    authApi.get<{
      count: number;
      next: string | null;
      previous: string | null;
      results: InvestmentHolding[];
    }>(createEndpoint(`${INVEST_BASE}/holdings/`), { params }),

  getHolding: (id: string) =>
    authApi.get<InvestmentHolding>(
      createEndpoint(`${INVEST_BASE}/holdings/${id}/`),
    ),

  // Investment Transaction endpoints
  getInvestmentTransactions: (params?: {
    portfolio?: string;
    asset?: string;
    type?: string;
    limit?: number;
    offset?: number;
  }) =>
    authApi.get<{
      count: number;
      next: string | null;
      previous: string | null;
      results: InvestmentTransaction[];
    }>(createEndpoint(`${INVEST_BASE}/transactions/`), { params }),

  getInvestmentTransaction: (id: string) =>
    authApi.get<InvestmentTransaction>(
      createEndpoint(`${INVEST_BASE}/transactions/${id}/`),
    ),

  createInvestmentTransaction: (data: CreateInvestmentTransactionData) =>
    authApi.post<InvestmentTransaction>(
      createEndpoint(`${INVEST_BASE}/transactions/`),
      data,
    ),

  updateInvestmentTransaction: (
    id: string,
    data: Partial<CreateInvestmentTransactionData>,
  ) =>
    authApi.put<InvestmentTransaction>(
      createEndpoint(`${INVEST_BASE}/transactions/${id}/`),
      data,
    ),

  deleteInvestmentTransaction: (id: string) =>
    authApi.delete(createEndpoint(`${INVEST_BASE}/transactions/${id}/`)),

  // Portfolio analytics
  getPortfolioPerformance: (id: string, period?: string) =>
    authApi.get<any>(
      createEndpoint(`${INVEST_BASE}/portfolios/${id}/performance/`),
      { params: { period } },
    ),

  getPortfolioAllocation: (id: string) =>
    authApi.get<any>(
      createEndpoint(`${INVEST_BASE}/portfolios/${id}/allocation/`),
    ),
};

export default investAPI;
