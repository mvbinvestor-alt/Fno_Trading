import React from 'react';
import { TrendUp, TrendDown, Minus } from '@phosphor-icons/react';

export const RegimeBadge = ({ regime }) => {
  const getRegimeStyles = () => {
    switch (regime) {
      case 'BULLISH':
        return {
          color: 'text-green-600',
          bg: 'bg-green-50',
          border: 'border-green-200',
          icon: <TrendUp size={16} weight="bold" />
        };
      case 'BEARISH':
        return {
          color: 'text-red-600',
          bg: 'bg-red-50',
          border: 'border-red-200',
          icon: <TrendDown size={16} weight="bold" />
        };
      default:
        return {
          color: 'text-amber-600',
          bg: 'bg-amber-50',
          border: 'border-amber-200',
          icon: <Minus size={16} weight="bold" />
        };
    }
  };

  const styles = getRegimeStyles();

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border ${styles.bg} ${styles.border} ${styles.color}`}
      data-testid="regime-badge"
    >
      {styles.icon}
      <span className="text-sm font-semibold tracking-wide">{regime}</span>
    </div>
  );
};

export const SignalBadge = ({ type }) => {
  const isLong = type === 'LONG';
  
  return (
    <span
      className={`inline-block px-3 py-1 rounded-sm text-xs font-bold uppercase tracking-wider ${
        isLong ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      }`}
      data-testid="signal-badge"
    >
      {type}
    </span>
  );
};

export const StatusBadge = ({ status }) => {
  const getStatusStyles = () => {
    switch (status) {
      case 'connected':
      case 'configured':
      case true:
        return 'bg-green-500 text-white';
      case 'disconnected':
      case 'not_configured':
      case false:
        return 'bg-red-500 text-white';
      default:
        return 'bg-gray-400 text-white';
    }
  };

  const displayStatus = typeof status === 'boolean' 
    ? (status ? 'Active' : 'Inactive')
    : String(status).replace('_', ' ');

  return (
    <span
      className={`inline-block px-2 py-1 rounded-sm text-xs font-semibold uppercase tracking-wide ${getStatusStyles()}`}
      data-testid="status-badge"
    >
      {displayStatus}
    </span>
  );
};