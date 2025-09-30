import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Award, TrendingUp } from 'lucide-react';

const RightPanel = ({ evaluationResult, loading }) => {
  if (loading || !evaluationResult) {
    return (
      <div className="space-y-4">
        <div className="card h-32 flex items-center justify-center">
          <p className="text-gray-400 text-sm">Awaiting analysis...</p>
        </div>
        <div className="card h-32 flex items-center justify-center">
          <p className="text-gray-400 text-sm">Awaiting analysis...</p>
        </div>
        <div className="card h-32 flex items-center justify-center">
          <p className="text-gray-400 text-sm">Awaiting analysis...</p>
        </div>
      </div>
    );
  }

  const { verdict, price_verdict, legal_rent_status, strategy_fits } = evaluationResult;

  return (
    <div className="space-y-4">
      {/* Main Verdict */}
      <VerdictCard
        title="Investment Verdict"
        verdict={verdict}
        verdictConfig={{
          'BUY': { color: 'green', icon: CheckCircle, text: 'Positive cash flow opportunity' },
          'CAUTION': { color: 'yellow', icon: AlertTriangle, text: 'Marginal cash flow' },
          'PASS': { color: 'red', icon: XCircle, text: 'Negative cash flow risk' }
        }}
      />

      {/* Price Verdict */}
      <VerdictCard
        title="Price Verdict"
        verdict={price_verdict}
        verdictConfig={{
          'Under-priced': { color: 'green', icon: TrendingUp, text: 'Below market value' },
          'Average': { color: 'blue', icon: TrendingUp, text: 'Market value' },
          'Overpriced': { color: 'red', icon: TrendingUp, text: 'Above market value' }
        }}
      />

      {/* Legal Rent Status */}
      <VerdictCard
        title="Legal Rent Check"
        verdict={legal_rent_status}
        verdictConfig={{
          'Conformant – Low': { color: 'green', icon: CheckCircle, text: 'Below rent ceiling' },
          'Conformant – High': { color: 'yellow', icon: AlertTriangle, text: 'Near rent ceiling' },
          'Non-conformant': { color: 'red', icon: XCircle, text: 'Exceeds legal limit' }
        }}
      />

      {/* Strategy Fits */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Award className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold">Top Investment Strategies</h3>
        </div>

        <div className="space-y-3">
          {strategy_fits.map((fit, index) => (
            <StrategyFitCard key={index} fit={fit} rank={index + 1} />
          ))}
        </div>
      </div>
    </div>
  );
};

const VerdictCard = ({ title, verdict, verdictConfig }) => {
  const config = verdictConfig[verdict] || { color: 'gray', icon: AlertTriangle, text: verdict };
  const Icon = config.icon;

  const colorClasses = {
    green: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      badge: 'badge-success',
      icon: 'text-green-600'
    },
    yellow: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-200',
      badge: 'badge-warning',
      icon: 'text-yellow-600'
    },
    red: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      badge: 'badge-danger',
      icon: 'text-red-600'
    },
    blue: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      badge: 'badge-info',
      icon: 'text-blue-600'
    },
    gray: {
      bg: 'bg-gray-50',
      border: 'border-gray-200',
      badge: 'badge',
      icon: 'text-gray-600'
    }
  };

  const classes = colorClasses[config.color];

  return (
    <div className={`card border-2 ${classes.border} ${classes.bg}`}>
      <h3 className="text-sm font-medium text-gray-700 mb-3">{title}</h3>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Icon className={`w-6 h-6 ${classes.icon}`} />
          <span className={`${classes.badge} text-base font-semibold`}>{verdict}</span>
        </div>
      </div>
      <p className="text-xs text-gray-600 mt-2">{config.text}</p>
    </div>
  );
};

const StrategyFitCard = ({ fit, rank }) => {
  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-600 bg-green-100';
    if (score >= 50) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-gray-400">#{rank}</span>
          <h4 className="font-semibold text-sm">{fit.strategy}</h4>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-bold ${getScoreColor(fit.score)}`}>
          {fit.score.toFixed(0)}
        </span>
      </div>

      {fit.pros && fit.pros.length > 0 && (
        <div className="mt-2">
          <p className="text-xs text-gray-600 mb-1">Pros:</p>
          <ul className="text-xs text-gray-700 space-y-0.5">
            {fit.pros.slice(0, 2).map((pro, i) => (
              <li key={i} className="flex items-start">
                <span className="text-green-500 mr-1">✓</span>
                <span className="flex-1">{pro}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {fit.cons && fit.cons.length > 0 && (
        <div className="mt-2">
          <p className="text-xs text-gray-600 mb-1">Cons:</p>
          <ul className="text-xs text-gray-700 space-y-0.5">
            {fit.cons.slice(0, 2).map((con, i) => (
              <li key={i} className="flex items-start">
                <span className="text-red-500 mr-1">✗</span>
                <span className="flex-1">{con}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RightPanel;