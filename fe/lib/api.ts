import axios from 'axios';
import { getTokens, refreshAccessToken, removeTokens } from './auth';

// Create base axios instance
const baseAxios = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// API instance for authenticated requests
export const authApi = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
authApi.interceptors.request.use(
  async (config) => {
    const tokens = getTokens();
    if (tokens) {
      config.headers.Authorization = `Bearer ${tokens.access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token refresh on 401 errors
authApi.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const newToken = await refreshAccessToken();
        
        if (newToken) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return authApi(originalRequest);
        } else {
          // If refresh fails, redirect to login
          removeTokens();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
      } catch (refreshError) {
        // If refresh fails, redirect to login
        removeTokens();
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API endpoints
export const authAPI = {
  register: (data: {
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    password: string;
    password2: string;
  }) => {
    return baseAxios.post('/v1/auth/register/', data);
  },
  
  login: (data: { username: string; password: string }) => {
    return baseAxios.post('/v1/auth/login/', data);
  },
  
  logout: (refreshToken: string) => {
    return authApi.post('/v1/auth/logout/', { refresh: refreshToken });
  },
  
  getProfile: () => {
    return authApi.get('/v1/auth/profile/');
  },
  
  updateProfile: (data: { first_name?: string; last_name?: string; email?: string }) => {
    return authApi.patch('/v1/auth/profile/', data);
  },
  
  changePassword: (data: { old_password: string; new_password: string; new_password2: string }) => {
    return authApi.put('/v1/auth/password/change/', data);
  },
  
  resetPassword: (email: string) => {
    return baseAxios.post('/v1/auth/password/reset/', { email });
  }
};

// Journal API endpoints (to be implemented)
export const journalAPI = {
  // Portfolio endpoints
  getPortfolios: () => {
    return authApi.get('/v1/journal/portfolios/');
  },
  
  getPortfolio: (id: number) => {
    return authApi.get(`/v1/journal/portfolios/${id}/`);
  },
  
  createPortfolio: (data: any) => {
    return authApi.post('/v1/journal/portfolios/', data);
  },
  
  updatePortfolio: (id: number, data: any) => {
    return authApi.put(`/v1/journal/portfolios/${id}/`, data);
  },
  
  deletePortfolio: (id: number) => {
    return authApi.delete(`/v1/journal/portfolios/${id}/`);
  },
  
  // Investment endpoints (to be implemented)
  
  // Trading endpoints (to be implemented)
  
  // Transaction endpoints (to be implemented)
};

// Finance API endpoints (to be implemented)
export const financeAPI = {
  // Wallet endpoints
  
  // Transaction endpoints
  
  // Category endpoints
  
  // Transfer endpoints
};

// Dashboard API endpoints (to be implemented)
export const dashboardAPI = {
  getSummary: () => {
    return authApi.get('/v1/dashboard/summary/');
  }
};

export default {
  auth: authAPI,
  journal: journalAPI,
  finance: financeAPI,
  dashboard: dashboardAPI
};