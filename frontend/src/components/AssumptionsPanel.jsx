import React from 'react';
import { Info } from 'lucide-react';

const AssumptionsPanel = () => {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-3">
      <div className="flex items-center space-x-2">
        <Info className="w-5 h-5 text-blue-600" />
        <h3 className="text-sm font-semibold text-blue-900">Calculation Assumptions</h3>
      </div>

      <div className="space-y-2 text-xs text-blue-800">
        <div className="grid grid-cols-2 gap-2">
          <div>
            <p className="font-semibold">Revenue Assumptions:</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>Vacancy rate: <span className="font-mono">5%</span></li>
              <li>Effective rent = Gross rent × 95%</li>
            </ul>
          </div>

          <div>
            <p className="font-semibold">Expense Assumptions:</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>Operating expenses: <span className="font-mono">25%</span> of gross rent</li>
              <li>Includes: taxes, insurance, maintenance, HOA</li>
            </ul>
          </div>
        </div>

        <div className="pt-2 border-t border-blue-200">
          <p className="font-semibold">French Property Selling Costs:</p>
          <ul className="list-disc list-inside space-y-1 ml-2">
            <li>Notary fees: <span className="font-mono">7-8%</span> of sale price</li>
            <li>Real estate agency: <span className="font-mono">3-10%</span> (typically 5%)</li>
            <li>Total estimated: <span className="font-mono">~8%</span> of sale price</li>
          </ul>
        </div>

        <div className="pt-2 border-t border-blue-200">
          <p className="font-semibold">Property Appreciation:</p>
          <ul className="list-disc list-inside space-y-1 ml-2">
            <li>Source: Notaires de France Q4 2024 / Q1 2025</li>
            <li>Department-specific historical rates</li>
            <li>Forward adjustment: <span className="font-mono">+1.5%</span></li>
          </ul>
        </div>

        <div className="pt-2 border-t border-blue-200 text-blue-700">
          <p className="italic">
            ⓘ All calculations use consistent assumptions across DSCR, cash flow projections, and IRR analysis.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AssumptionsPanel;
