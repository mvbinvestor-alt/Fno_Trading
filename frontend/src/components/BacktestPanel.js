import React, { useState } from 'react';
import { api } from '../api/client';
import { Play, Spinner } from '@phosphor-icons/react';

const BacktestPanel = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [capital, setCapital] = useState(500000);

  const handleRunBacktest = async () => {
    setLoading(true);
    try {
      const response = await api.runBacktest({ capital });
      setResults(response.data.results);
    } catch (error) {
      console.error('Error running backtest:', error);
      alert('Error running backtest. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-md p-4" data-testid="backtest-panel">
      <div className="mb-4">
        <h3 className="text-lg font-bold tracking-tight text-slate-900">Backtest Engine</h3>
        <p className="text-xs text-slate-500 mt-0.5">Test strategy performance</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs uppercase tracking-wider text-slate-500 mb-2">
            Initial Capital
          </label>
          <input
            type="number"
            value={capital}
            onChange={(e) => setCapital(Number(e.target.value))}
            className="w-full px-3 py-2 border border-slate-200 rounded-md text-sm font-mono focus:outline-none focus:ring-2 focus:ring-slate-900"
            data-testid="backtest-capital-input"
          />
        </div>

        <button
          onClick={handleRunBacktest}
          disabled={loading}
          className="w-full px-4 py-2 bg-slate-900 text-white rounded-md text-sm font-bold hover:bg-slate-800 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          data-testid="run-backtest-btn"
        >
          {loading ? (
            <>
              <Spinner size={16} className="animate-spin" />
              Running...
            </>
          ) : (
            <>
              <Play size={16} weight="fill" />
              Run Backtest
            </>
          )}
        </button>

        {results && results.metrics && (
          <div className="mt-4 p-4 bg-slate-50 rounded-md border border-slate-200">
            <h4 className="text-sm font-bold text-slate-900 mb-3">Results</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500">Total Trades:</span>
                <span className="font-mono font-semibold">{results.total_trades}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Win Rate:</span>
                <span className="font-mono font-semibold text-green-600">
                  {results.metrics.win_rate}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Avg R:R:</span>
                <span className="font-mono font-semibold">{results.metrics.avg_rr}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Max Drawdown:</span>
                <span className="font-mono font-semibold text-red-600">
                  {results.metrics.max_drawdown}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Total Return:</span>
                <span className={`font-mono font-semibold ${
                  results.metrics.total_return >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {results.metrics.total_return > 0 ? '+' : ''}{results.metrics.total_return}%
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BacktestPanel;