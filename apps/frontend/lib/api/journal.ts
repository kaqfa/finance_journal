import { authApi, createEndpoint } from '../config/axios';

const JOURNAL_BASE = 'journal';

const journalAPI = {
  getPortfolios: () => 
    authApi.get(createEndpoint(`${JOURNAL_BASE}/portfolios/`)),
    
  getPortfolio: (id: number) => 
    authApi.get(createEndpoint(`${JOURNAL_BASE}/portfolios/${id}/`)),
  
  createPortfolio: (data: any) => 
    authApi.post(createEndpoint(`${JOURNAL_BASE}/portfolios/`), data),
  
  updatePortfolio: (id: number, data: any) => 
    authApi.put(createEndpoint(`${JOURNAL_BASE}/portfolios/${id}/`), data),
  
  deletePortfolio: (id: number) => 
    authApi.delete(createEndpoint(`${JOURNAL_BASE}/portfolios/${id}/`))
};

export default journalAPI;