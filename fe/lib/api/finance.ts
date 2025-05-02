import { authApi, createEndpoint } from '../config/axios';

const FINANCE_BASE = 'finance';

const financeAPI = {
  // Wallet endpoints
  getWallets: () => 
    authApi.get(createEndpoint(`${FINANCE_BASE}/wallets/`)),
  
  // Transaction endpoints
  getTransactions: () => 
    authApi.get(createEndpoint(`${FINANCE_BASE}/transactions/`)),
  
  // Category endpoints
  getCategories: () => 
    authApi.get(createEndpoint(`${FINANCE_BASE}/categories/`)),
  
  // Transfer endpoints
  getTransfers: () => 
    authApi.get(createEndpoint(`${FINANCE_BASE}/transfers/`))
};

export default financeAPI;