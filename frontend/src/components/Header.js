import React, { useState, useEffect } from 'react';
import { ChartLine, Play, Stop } from '@phosphor-icons/react';
import { RegimeBadge, StatusBadge } from './Badges';
import { api } from '../api/client';

const Header = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [marketRegime, setMarketRegime] = useState(null);
  const [schedulerRunning, setSchedulerRunning] = useState(false);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const [systemRes, regimeRes, schedulerRes] = await Promise.all([
        api.getSystemStatus(),
        api.getMarketRegime(),
        api.getSchedulerStatus()
      ]);
      
      setSystemStatus(systemRes.data.system);
      setMarketRegime(regimeRes.data.regime);
      setSchedulerRunning(schedulerRes.data.scheduler.is_running);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  const handleSchedulerToggle = async () => {
    try {
      const action = schedulerRunning ? 'stop' : 'start';
      await api.controlScheduler(action);
      setSchedulerRunning(!schedulerRunning);
    } catch (error) {
      console.error('Error controlling scheduler:', error);
    }
  };

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50" data-testid="dashboard-header">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <ChartLine size={32} weight="bold" className="text-slate-900" />
              <div>
                <h1 className="text-2xl font-black tracking-tight text-slate-900">F&O Trading System</h1>
                <p className="text-xs text-slate-500 tracking-wider uppercase">Intraday Signal Generator</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-6">
            {marketRegime && (
              <div>
                <p className="text-xs uppercase tracking-wider text-slate-500 mb-1">Market</p>
                <RegimeBadge regime={marketRegime} />
              </div>
            )}

            <div>
              <p className="text-xs uppercase tracking-wider text-slate-500 mb-1">Scheduler</p>
              <button
                onClick={handleSchedulerToggle}
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md border border-slate-200 hover:border-slate-300 transition-colors"
                data-testid="scheduler-toggle-btn"
              >
                {schedulerRunning ? (
                  <Stop size={16} weight="fill" className="text-red-500" />
                ) : (
                  <Play size={16} weight="fill" className="text-green-500" />
                )}
                <span className="text-sm font-semibold">
                  {schedulerRunning ? 'Running' : 'Stopped'}
                </span>
              </button>
            </div>

            {systemStatus && (
              <div>
                <p className="text-xs uppercase tracking-wider text-slate-500 mb-1">Status</p>
                <div className="flex gap-2">
                  <StatusBadge status={systemStatus.database} />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;