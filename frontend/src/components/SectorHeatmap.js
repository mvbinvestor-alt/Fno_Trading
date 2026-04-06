import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { TrendUp, TrendDown, ChartLine, Fire } from '@phosphor-icons/react';

const SectorHeatmap = () => {
  const [sectors, setSectors] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSectors();
    const interval = setInterval(fetchSectors, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchSectors = async () => {
    try {
      const response = await api.getSectorStrength();
      setSectors(response.data.sectors);
    } catch (error) {
      console.error('Error fetching sectors:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSectorColor = (value) => {
    if (value > 0.5) return 'bg-green-500';
    if (value > 0) return 'bg-green-400';
    if (value > -0.5) return 'bg-red-400';
    return 'bg-red-500';
  };

  const getSectorTextColor = (value) => {
    if (value > 0.5) return 'text-green-600';
    if (value > 0) return 'text-green-500';
    if (value > -0.5) return 'text-red-500';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-md p-4">
        <p className="text-slate-500">Loading sector data...</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-md p-4" data-testid="sector-heatmap">
      <div className="mb-4">
        <h3 className="text-lg font-bold tracking-tight text-slate-900">Sector Strength</h3>
        <p className="text-xs text-slate-500 mt-0.5">Intraday performance</p>
      </div>

      <div className="space-y-3">
        {Object.entries(sectors).map(([sector, value]) => (
          <div key={sector} className="flex items-center justify-between" data-testid="sector-item">
            <div className="flex items-center gap-3 flex-1">
              <div className={`w-1 h-8 rounded-full ${getSectorColor(value)}`}></div>
              <span className="text-sm font-semibold text-slate-900">{sector}</span>
            </div>
            <div className="flex items-center gap-2">
              {value > 0 ? (
                <TrendUp size={16} weight="bold" className="text-green-600" />
              ) : (
                <TrendDown size={16} weight="bold" className="text-red-600" />
              )}
              <span className={`font-mono text-sm font-semibold ${getSectorTextColor(value)}`}>
                {value > 0 ? '+' : ''}{value.toFixed(2)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SectorHeatmap;