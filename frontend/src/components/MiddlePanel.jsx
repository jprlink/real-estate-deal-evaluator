import React from 'react';
import { TrendingUp, DollarSign, BarChart3, PieChart, AlertCircle, Info } from 'lucide-react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import CashFlowTable from './CashFlowTable';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MiddlePanel = ({ evaluationResult, propertyData, loading }) => {
  if (loading) {
    return (
      <div className="card h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Analyzing property...</p>
        </div>
      </div>
    );
  }

  if (!evaluationResult) {
    return (
      <div className="card h-full flex items-center justify-center">
        <div className="text-center text-gray-500">
          <BarChart3 className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium mb-2">No Analysis Yet</p>
          <p className="text-sm">Enter property details and click "Analyze Property" to begin</p>
        </div>
      </div>
    );
  }

  const { metrics, cash_flow_projections, appreciation_source } = evaluationResult;

  // Use real cash flow data from backend
  const cashFlowData = {
    labels: cash_flow_projections?.map((cf) => `Year ${cf.year}`) || Array.from({ length: 10 }, (_, i) => `Year ${i + 1}`),
    datasets: [
      {
        label: 'Annual Cash Flow',
        data: cash_flow_projections?.map((cf) => cf.cash_flow) || Array.from({ length: 10 }, () => Math.random() * 10000 + 5000),
        borderColor: 'rgb(14, 165, 233)',
        backgroundColor: 'rgba(14, 165, 233, 0.1)',
        tension: 0.4
      },
      {
        label: 'Cumulative Cash Flow',
        data: cash_flow_projections?.map((cf) => cf.cumulative_cash_flow) || [],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '10-Year Cash Flow Projection'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => `€${(value / 1000).toFixed(0)}k`
        }
      }
    }
  };

  return (
    <div className="space-y-4">
      {/* Financial Metrics Grid */}
      <div className="grid grid-cols-2 gap-4">
        <MetricCard
          icon={<DollarSign className="w-5 h-5" />}
          label="Monthly Payment"
          value={`€${metrics.monthly_payment.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`}
          color="blue"
        />
        <MetricCard
          icon={<TrendingUp className="w-5 h-5" />}
          label="DSCR"
          value={metrics.dscr.toFixed(2)}
          color={metrics.dscr >= 1.2 ? 'green' : metrics.dscr >= 1.0 ? 'yellow' : 'red'}
          subtitle={metrics.dscr >= 1.0 ? 'Positive Cash Flow' : 'Negative Cash Flow'}
        />
        <MetricCard
          icon={<PieChart className="w-5 h-5" />}
          label="Cap Rate"
          value={`${(metrics.cap_rate * 100).toFixed(2)}%`}
          color="blue"
        />
        <MetricCard
          icon={<BarChart3 className="w-5 h-5" />}
          label="Cash-on-Cash"
          value={`${(metrics.cash_on_cash * 100).toFixed(2)}%`}
          color="blue"
        />
      </div>

      {/* Additional Metrics */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Key Metrics</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <p className="text-sm text-gray-600">NOI (Annual)</p>
            <p className="text-lg font-semibold">€{metrics.noi.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">IRR</p>
            <p className="text-lg font-semibold">{(metrics.irr * 100).toFixed(1)}%</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">LTV</p>
            <p className="text-lg font-semibold">{(metrics.ltv * 100).toFixed(0)}%</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Price per m²</p>
            <p className="text-lg font-semibold">€{metrics.price_per_m2.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}</p>
          </div>
        </div>
      </div>

      {/* Cash Flow Chart */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Cash Flow Projection</h3>
        <div className="h-64">
          <Line data={cashFlowData} options={chartOptions} />
        </div>

        {/* Appreciation Rate Footnote */}
        {metrics.appreciation_rate_display && (
          <div className="mt-3 flex items-start space-x-2 text-xs text-gray-600 bg-blue-50 p-3 rounded-lg">
            <Info className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-gray-700">
                Property appreciation: {metrics.appreciation_rate_display} per year
              </p>
              {appreciation_source && (
                <p className="mt-1">{appreciation_source}</p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Cash Flow Table */}
      {cash_flow_projections && cash_flow_projections.length > 0 && (
        <div className="card">
          <CashFlowTable
            cashFlowData={cash_flow_projections}
            appreciationRate={metrics.appreciation_rate}
          />
        </div>
      )}

      {/* Summary */}
      <div className="card">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold mb-2">Analysis Summary</h3>
            <p className="text-sm text-gray-700">{evaluationResult.summary}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon, label, value, subtitle, color = 'blue' }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    red: 'bg-red-100 text-red-600'
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-2">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
      <p className="text-sm text-gray-600 mb-1">{label}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
    </div>
  );
};

export default MiddlePanel;