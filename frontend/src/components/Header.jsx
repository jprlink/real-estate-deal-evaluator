import React from 'react';
import { Building2, TrendingUp } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Building2 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Paris Real Estate Analyzer
              </h1>
              <p className="text-sm text-gray-500">
                AI-Powered Investment Analysis
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <TrendingUp className="w-4 h-4 text-primary-600" />
              <span>60-Second Verdicts</span>
            </div>
            <button className="btn-primary">
              Export Report
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;