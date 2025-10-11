import React, { useState } from 'react';
import { BarChart3, AlertCircle, Info, HelpCircle } from 'lucide-react';
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
import AssumptionsPanel from './AssumptionsPanel';

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

  // Filter out Year 0 for display (but keep in calculations)
  const displayCashFlow = cash_flow_projections?.filter(cf => cf.year !== 0) || [];
  const year0 = cash_flow_projections?.find(cf => cf.year === 0);

  // Use real cash flow data from backend (excluding Year 0)
  const cashFlowData = {
    labels: displayCashFlow.map((cf) => `Year ${cf.year}`),
    datasets: [
      {
        label: 'Annual Cash Flow',
        data: displayCashFlow.map((cf) => cf.cash_flow),
        borderColor: 'rgb(14, 165, 233)',
        backgroundColor: 'rgba(14, 165, 233, 0.1)',
        tension: 0.4
      },
      {
        label: 'Cumulative Cash Flow',
        data: displayCashFlow.map((cf) => cf.cumulative_cash_flow),
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

  const metricDefinitions = {
    monthly_payment: {
      label: 'Monthly Mortgage Payment',
      tooltip: 'Monthly mortgage payment based on loan amount, interest rate, and term. Formula: M = P × [r(1+r)^n] / [(1+r)^n - 1], where P = principal, r = monthly rate, n = months'
    },
    noi: {
      label: 'NOI (Annual)',
      tooltip: 'Net Operating Income: Annual rental income after vacancy (5%) and operating expenses (25%). Formula: NOI = (Gross Rent × 95%) - Operating Expenses'
    },
    dscr: {
      label: 'DSCR',
      tooltip: 'Debt Service Coverage Ratio: Measures ability to cover mortgage payments. Formula: DSCR = NOI / Annual Debt Service. Above 1.2 is excellent, 1.0-1.2 is caution, below 1.0 means negative cash flow'
    },
    cap_rate: {
      label: 'Cap Rate',
      tooltip: 'Capitalization Rate: Return on investment ignoring financing. Formula: Cap Rate = NOI / Property Price. Higher is better (typical: 4-10%)'
    },
    cash_on_cash: {
      label: 'Cash-on-Cash',
      tooltip: 'Cash-on-Cash Return: Annual return on your down payment. Formula: (Annual Cash Flow / Down Payment) × 100. Measures return on cash invested'
    },
    irr: {
      label: 'IRR',
      tooltip: 'Internal Rate of Return: Annualized return including property appreciation, rental income, and sale proceeds over investment period. Accounts for time value of money'
    },
    ltv: {
      label: 'LTV',
      tooltip: 'Loan-to-Value Ratio: Loan amount as percentage of property price. Formula: LTV = (Loan Amount / Property Price) × 100. Lower is safer (typical: 70-80%)'
    },
    price_per_m2: {
      label: 'Price per m²',
      tooltip: 'Property price divided by surface area. Formula: Price / Surface. Used to compare properties and assess market value'
    }
  };

  return (
    <div className="space-y-4">
      {/* Consolidated Key Metrics */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Key Financial Metrics</h3>
        <div className="grid grid-cols-4 gap-4">
          <MetricWithTooltip
            label={metricDefinitions.monthly_payment.label}
            value={`€${metrics.monthly_payment.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`}
            tooltip={metricDefinitions.monthly_payment.tooltip}
          />
          <MetricWithTooltip
            label={metricDefinitions.noi.label}
            value={`€${metrics.noi.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`}
            tooltip={metricDefinitions.noi.tooltip}
          />
          <MetricWithTooltip
            label={metricDefinitions.dscr.label}
            value={metrics.dscr.toFixed(2)}
            tooltip={metricDefinitions.dscr.tooltip}
            valueColor={metrics.dscr >= 1.2 ? 'text-green-600' : metrics.dscr >= 1.0 ? 'text-yellow-600' : 'text-red-600'}
            subtitle={metrics.dscr >= 1.0 ? 'Positive Cash Flow' : 'Negative Cash Flow'}
          />
          <MetricWithTooltip
            label={metricDefinitions.cap_rate.label}
            value={`${(metrics.cap_rate * 100).toFixed(2)}%`}
            tooltip={metricDefinitions.cap_rate.tooltip}
          />
          <MetricWithTooltip
            label={metricDefinitions.cash_on_cash.label}
            value={`${(metrics.cash_on_cash * 100).toFixed(2)}%`}
            tooltip={metricDefinitions.cash_on_cash.tooltip}
          />
          <MetricWithTooltip
            label={metricDefinitions.irr.label}
            value={`${(metrics.irr * 100).toFixed(1)}%`}
            tooltip={metricDefinitions.irr.tooltip}
          />
          <MetricWithTooltip
            label={metricDefinitions.ltv.label}
            value={`${(metrics.ltv * 100).toFixed(0)}%`}
            tooltip={metricDefinitions.ltv.tooltip}
          />
          <MetricWithTooltip
            label={metricDefinitions.price_per_m2.label}
            value={`€${metrics.price_per_m2.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`}
            tooltip={metricDefinitions.price_per_m2.tooltip}
          />
        </div>
      </div>

      {/* Costs at Purchase */}
      {year0 && evaluationResult.purchase_costs && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Costs at Purchase</h3>
          <div className="grid grid-cols-3 gap-4">
            {/* Row 1: Initial Payments */}
            <MetricWithTooltip
              label="Down Payment"
              value={`€${evaluationResult.purchase_costs.down_payment.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`}
              tooltip="Initial equity payment required to purchase the property. This is your upfront cash investment excluding fees."
            />
            {evaluationResult.purchase_costs.renovation_costs > 0 && (
              <MetricWithTooltip
                label="Renovation Costs"
                value={`€${evaluationResult.purchase_costs.renovation_costs.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`}
                tooltip="Costs for repairs and improvements before renting out the property. Increases total property value (ARV)."
              />
            )}

            {/* Row 2: Detailed Fees */}
            <MetricWithTooltip
              label="Registration Duties"
              value={`€${Math.round(evaluationResult.purchase_costs.registration_duties).toLocaleString('en-US')}`}
              tooltip="Droits d'enregistrement (transfer taxes): ~5.8% of purchase price. Tax paid to the French government when transferring property ownership."
            />
            <MetricWithTooltip
              label="Notaire Fees"
              value={`€${Math.round(evaluationResult.purchase_costs.notaire_fees).toLocaleString('en-US')}`}
              tooltip="Émoluments du notaire: Professional fees for the notaire's services (~1%). Calculated on a sliding scale based on property value."
            />
            <MetricWithTooltip
              label="Disbursements"
              value={`€${Math.round(evaluationResult.purchase_costs.disbursements).toLocaleString('en-US')}`}
              tooltip="Administrative costs and documentation fees: ~0.4% of purchase price. Covers land registry, searches, and certifications."
            />
            {evaluationResult.purchase_costs.mortgage_fees > 0 && (
              <MetricWithTooltip
                label="Mortgage Fees"
                value={`€${Math.round(evaluationResult.purchase_costs.mortgage_fees).toLocaleString('en-US')}`}
                tooltip="Additional fees when financing with a mortgage: ~0.4% of purchase price. Includes mortgage registration and associated legal costs."
              />
            )}

            {/* Row 3: Totals */}
            <MetricWithTooltip
              label="Total Fees"
              value={`€${Math.round(evaluationResult.purchase_costs.total_fees).toLocaleString('en-US')}`}
              tooltip="Sum of all acquisition fees: registration duties + notaire fees + disbursements + mortgage fees. Typically 7-8% of purchase price for resale properties."
              valueColor="text-gray-700"
            />
            <MetricWithTooltip
              label="Total Cash Required"
              value={`€${Math.round(evaluationResult.purchase_costs.total_cash_required).toLocaleString('en-US')}`}
              tooltip="Total cash needed at closing: down payment + renovation costs + all fees. This is your complete initial investment."
              valueColor="text-red-600"
            />
          </div>
        </div>
      )}

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
              {propertyData && propertyData.renovation_costs > 0 && (
                <p className="mt-2 text-gray-600 italic">
                  <strong>Note on ARV:</strong> Renovation costs of €{propertyData.renovation_costs.toLocaleString()} included in property value. Actual After Repair Value (ARV) depends on type of repairs, property type, location, and market conditions.
                </p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Cash Flow Table */}
      {displayCashFlow && displayCashFlow.length > 0 && (
        <div className="card">
          <CashFlowTable
            cashFlowData={displayCashFlow}
            appreciationRate={metrics.appreciation_rate}
          />
        </div>
      )}

      {/* Assumptions Panel */}
      <AssumptionsPanel />

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

const MetricWithTooltip = ({ label, value, tooltip, valueColor = 'text-gray-900', subtitle }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="relative">
      <div className="flex items-center space-x-1 mb-1">
        <p className="text-xs text-gray-600">{label}</p>
        <div
          className="relative inline-block"
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          <HelpCircle className="w-3 h-3 text-gray-400 cursor-help" />
          {showTooltip && (
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 bg-gray-900 text-white text-xs rounded-lg p-3 shadow-lg z-50 w-64 whitespace-normal">
              {tooltip}
              <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1">
                <div className="border-4 border-transparent border-t-gray-900"></div>
              </div>
            </div>
          )}
        </div>
      </div>
      <p className={`text-lg font-bold ${valueColor}`}>{value}</p>
      {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
    </div>
  );
};

export default MiddlePanel;