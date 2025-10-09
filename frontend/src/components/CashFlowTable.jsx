import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const CashFlowTable = ({ cashFlowData, appreciationRate }) => {
  if (!cashFlowData || cashFlowData.length === 0) {
    return null;
  }

  const formatCurrency = (value) => {
    return `€${Math.round(value).toLocaleString('en-US')}`;
  };

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="space-y-3">
      {/* Table Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          {cashFlowData.length}-Year Cash Flow Analysis
        </h3>
        {appreciationRate !== undefined && (
          <div className="flex items-center space-x-1 text-sm">
            {appreciationRate >= 0 ? (
              <TrendingUp className="w-4 h-4 text-green-600" />
            ) : (
              <TrendingDown className="w-4 h-4 text-red-600" />
            )}
            <span className={appreciationRate >= 0 ? 'text-green-600' : 'text-red-600'}>
              {formatPercentage(appreciationRate)} appreciation
            </span>
          </div>
        )}
      </div>

      {/* Scrollable Table */}
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50">
                Year
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rental Income
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Operating Expenses
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Mortgage Payment
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                NOI
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider font-semibold">
                Cash Flow
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider font-semibold">
                Cumulative CF
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Property Value
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Equity
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {cashFlowData.map((row) => (
              <tr key={row.year} className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 sticky left-0 bg-white">
                  {row.year}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right">
                  {formatCurrency(row.rental_income)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right">
                  {formatCurrency(row.operating_expenses)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right">
                  {formatCurrency(row.mortgage_payment)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right">
                  {formatCurrency(row.noi)}
                </td>
                <td className={`px-4 py-3 whitespace-nowrap text-sm font-semibold text-right ${
                  row.cash_flow >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {formatCurrency(row.cash_flow)}
                </td>
                <td className={`px-4 py-3 whitespace-nowrap text-sm font-semibold text-right ${
                  row.cumulative_cash_flow >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {formatCurrency(row.cumulative_cash_flow)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right">
                  {formatCurrency(row.property_value)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right font-medium">
                  {formatCurrency(row.equity)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Summary Row */}
      <div className="grid grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
        <div>
          <p className="text-xs text-gray-600">Total Cash Flow (10Y)</p>
          <p className={`text-lg font-bold ${
            cashFlowData[cashFlowData.length - 1]?.cumulative_cash_flow >= 0
              ? 'text-green-600'
              : 'text-red-600'
          }`}>
            {formatCurrency(cashFlowData[cashFlowData.length - 1]?.cumulative_cash_flow || 0)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-600">Final Property Value</p>
          <p className="text-lg font-bold text-gray-900">
            {formatCurrency(cashFlowData[cashFlowData.length - 1]?.property_value || 0)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-600">Final Equity</p>
          <p className="text-lg font-bold text-primary-600">
            {formatCurrency(cashFlowData[cashFlowData.length - 1]?.equity || 0)}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CashFlowTable;
