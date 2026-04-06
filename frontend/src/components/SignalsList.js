import React, { useState, useEffect } from 'react';
import { SignalBadge } from './Badges';
import { api } from '../api/client';
import { ArrowUp, ArrowDown, Clock } from '@phosphor-icons/react';

const SignalsList = () => {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchSignals();
    const interval = setInterval(fetchSignals, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchSignals = async () => {
    try {
      const response = await api.getSignals(20, 'ACTIVE');
      setSignals(response.data.signals);
    } catch (error) {
      console.error('Error fetching signals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSignals = async () => {
    setGenerating(true);
    try {
      await api.generateSignals(true);
      await fetchSignals();
    } catch (error) {
      console.error('Error generating signals:', error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-md p-4">
        <p className="text-slate-500">Loading signals...</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-md" data-testid="signals-list">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-extrabold tracking-tight text-slate-900">Active Signals</h2>
          <p className="text-xs text-slate-500 mt-0.5">{signals.length} signals generated</p>
        </div>
        <button
          onClick={handleGenerateSignals}
          disabled={generating}
          className="px-4 py-2 bg-slate-900 text-white rounded-md text-sm font-bold hover:bg-slate-800 transition-colors disabled:opacity-50"
          data-testid="generate-signals-btn"
        >
          {generating ? 'Generating...' : 'Generate Signals'}
        </button>
      </div>

      {signals.length === 0 ? (
        <div className="p-8 text-center">
          <p className="text-slate-500">No active signals. Click "Generate Signals" to start.</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full" data-testid="signals-table">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="px-4 py-3 text-left text-xs uppercase tracking-wider font-semibold text-slate-500">Stock</th>
                <th className="px-4 py-3 text-center text-xs uppercase tracking-wider font-semibold text-slate-500">Type</th>
                <th className="px-4 py-3 text-right text-xs uppercase tracking-wider font-semibold text-slate-500">Entry</th>
                <th className="px-4 py-3 text-right text-xs uppercase tracking-wider font-semibold text-slate-500">Stop Loss</th>
                <th className="px-4 py-3 text-right text-xs uppercase tracking-wider font-semibold text-slate-500">Target 1</th>
                <th className="px-4 py-3 text-right text-xs uppercase tracking-wider font-semibold text-slate-500">Target 2</th>
                <th className="px-4 py-3 text-right text-xs uppercase tracking-wider font-semibold text-slate-500">Qty</th>
                <th className="px-4 py-3 text-center text-xs uppercase tracking-wider font-semibold text-slate-500">Confidence</th>
                <th className="px-4 py-3 text-left text-xs uppercase tracking-wider font-semibold text-slate-500">Sector</th>
              </tr>
            </thead>
            <tbody>
              {signals.map((signal, idx) => {
                if (!signal) return null;
                return (
                  <tr
                    key={idx}
                    className="border-b border-slate-200 hover:bg-slate-50 transition-colors"
                    data-testid="signal-row"
                  >
                    <td className="px-4 py-3">
                      <span className="font-bold text-slate-900">{signal.stock || 'N/A'}</span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <SignalBadge type={signal.signal_type || 'LONG'} />
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-sm text-slate-900">
                      ₹{(signal.entry || 0).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-sm text-slate-900">
                      ₹{(signal.stop_loss || 0).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-sm text-slate-900">
                      ₹{(signal.target_1 || 0).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-sm text-slate-900">
                      ₹{(signal.target_2 || 0).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-sm text-slate-900">
                      {signal.position_size || 0}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="font-mono text-sm font-semibold text-slate-900">
                        {(signal.confidence_score || 0).toFixed(1)}/10
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-sm text-slate-600">{signal.sector || 'N/A'}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default SignalsList;