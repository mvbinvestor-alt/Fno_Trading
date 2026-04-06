import React from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import SignalsList from './components/SignalsList';
import SectorHeatmap from './components/SectorHeatmap';
import PerformanceMetrics from './components/PerformanceMetrics';
import BacktestPanel from './components/BacktestPanel';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      
      <main className="px-6 py-6">
        {/* Main Signals Section */}
        <div className="mb-6">
          <SignalsList />
        </div>

        {/* Grid Layout for Additional Panels */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <SectorHeatmap />
          <PerformanceMetrics />
          <BacktestPanel />
        </div>

        {/* System Information */}
        <div className="mt-6 bg-white border border-slate-200 rounded-md p-4">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900 mb-2">About This System</h3>
              <div className="text-xs text-slate-600 space-y-1">
                <p><strong>Purpose:</strong> Production-grade F&O intraday trading signal generator</p>
                <p><strong>Strategy:</strong> Multi-factor analysis (Price Action + Volume + Option Chain + Sector + Regime)</p>
                <p><strong>Features:</strong> Automated signal generation, Telegram/Email alerts, Backtesting engine</p>
                <p><strong>Market Hours:</strong> Mon-Fri, 9:15 AM - 3:30 PM IST (Signals generated every 5 minutes)</p>
              </div>
            </div>
            
            <div className="text-right">
              <p className="text-xs uppercase tracking-wider text-slate-500 mb-1">Configuration</p>
              <div className="text-xs text-slate-600 space-y-1">
                <p>Risk per trade: <strong className="font-mono">1%</strong></p>
                <p>Max concurrent: <strong className="font-mono">3 trades</strong></p>
                <p>Min score: <strong className="font-mono">8/13</strong></p>
              </div>
            </div>
          </div>
        </div>

        {/* Setup Instructions */}
        <div className="mt-4 bg-amber-50 border border-amber-200 rounded-md p-4">
          <h4 className="text-sm font-bold text-amber-900 mb-2">⚠️ Setup Required</h4>
          <div className="text-xs text-amber-800 space-y-1">
            <p>• Configure 5paisa API credentials (Secret Key & Client ID) in backend/.env</p>
            <p>• Add your Telegram Chat ID to receive alerts</p>
            <p>• Set up Gmail App Password for email notifications</p>
            <p>• Restart backend server after updating .env file</p>
          </div>
        </div>
      </main>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
