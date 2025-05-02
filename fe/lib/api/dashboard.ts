import { authApi, createEndpoint } from '../config/axios';

const DASHBOARD_BASE = 'dashboard';

const dashboardAPI = {
  getSummary: () => 
    authApi.get(createEndpoint(`${DASHBOARD_BASE}/summary/`))
};

export default dashboardAPI;