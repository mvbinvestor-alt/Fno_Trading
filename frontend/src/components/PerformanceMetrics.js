import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { Target, TrendUp, Percent, ChartLineUp } from '@phosphor-icons/react';

const PerformanceMetrics = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      setError(null);
      const response = await api.getPerformanceAnalytics();
      if (response.data && response.data.metrics) {
        setMetrics(response.data.metrics);
      }
    } catch (error) {
      console.error('Error fetching metrics:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const MetricCard = ({ icon: Icon, label, value, color = 'text-slate-900' }) => (
    <div className="flex items-center justify-between py-2">
      <div className="flex items-center gap-2">
        <Icon size={18} weight="bold" className="text-slate-400" />
        <span className="text-xs uppercase tracking-wider text-slate-500">{label}</span>
      </div>
      <span className={`font-mono text-base font-semibold ${color}`}>{value}</span>
    </div>
  );

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-md p-4">
        <p className="text-slate-500">Loading metrics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white border border-slate-200 rounded-md p-4" data-testid="performance-metrics">
        <h3 className="text-lg font-bold tracking-tight text-slate-900 mb-2">Performance</h3>
        <p className="text-sm text-red-500">Error: {error}</p>
      </div>
    );
  }

  if (!metrics || !metrics.total_trades || metrics.total_trades === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-md p-4" data-testid="performance-metrics">
        <h3 className="text-lg font-bold tracking-tight text-slate-900 mb-2">Performance</h3>
        <p className="text-sm text-slate-500">No trade data available yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-md p-4" data-testid="performance-metrics">
      <div className="mb-4">
        <h3 className="text-lg font-bold tracking-tight text-slate-900">Performance</h3>
        <p className="text-xs text-slate-500 mt-0.5">Overall statistics</p>
      </div>

      <div className="space-y-1">
        <MetricCard
          icon={Target}
          label="Total Trades"
          value={metrics.total_trades || 0}
        />
        <MetricCard
          icon={TrendUp}
          label="Win Rate"
          value={`${(metrics.win_rate || 0).toFixed(1)}%`}
          color={(metrics.win_rate || 0) >= 50 ? 'text-green-600' : 'text-red-600'}
        />
        <MetricCard
          icon={ChartLineUp}
          label="Total P&L"
          value={`₹${(metrics.total_pnl || 0).toFixed(2)}`}
          color={(metrics.total_pnl || 0) >= 0 ? 'text-green-600' : 'text-red-600'}
        />
        <MetricCard
          icon={Percent}
          label="Avg Win"
          value={`₹${(metrics.avg_win || 0).toFixed(2)}`}
          color="text-green-600"
        />
        <MetricCard
          icon={Percent}
          label="Avg Loss"
          value={`₹${Math.abs(metrics.avg_loss || 0).toFixed(2)}`}
          color="text-red-600"
        />
      </div>
    </div>
  );
};

export default PerformanceMetrics;
