import authAPI from './api/auth';
import journalAPI from './api/journal';
import financeAPI from './api/finance';
import dashboardAPI from './api/dashboard';

export { authAPI, journalAPI, financeAPI, dashboardAPI };

export default {
  auth: authAPI,
  journal: journalAPI,
  finance: financeAPI,
  dashboard: dashboardAPI
};