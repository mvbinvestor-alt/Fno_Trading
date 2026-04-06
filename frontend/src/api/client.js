import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API methods
export const api = {
  // Health
  health: () => apiClient.get('/health'),
  
  // Signals
  generateSignals: (manual = true) => apiClient.post('/signals/generate', { manual }),
  getSignals: (limit = 50, status = 'ACTIVE') => apiClient.get('/signals', { params: { limit, status } }),
  getSignal: (id) => apiClient.get(`/signals/${id}`),
  
  // Market
  getMarketRegime: () => apiClient.get('/market/regime'),
  getSectorStrength: () => apiClient.get('/market/sectors'),
  
  // Backtest
  runBacktest: (data) => apiClient.post('/backtest/run', data),
  getBacktestResults: (limit = 10) => apiClient.get('/backtest/results', { params: { limit } }),
  
  // Trades
  getTrades: (limit = 50) => apiClient.get('/trades', { params: { limit } }),
  
  // Analytics
  getPerformanceAnalytics: () => apiClient.get('/analytics/performance'),
  
  // Config
  updateCapital: (capital) => apiClient.post('/config/capital', { capital }),
  
  // Scheduler
  controlScheduler: (action) => apiClient.post('/scheduler/control', { action }),
  getSchedulerStatus: () => apiClient.get('/scheduler/status'),
  
  // System
  getSystemStatus: () => apiClient.get('/system/status')
};

export default apiClient;