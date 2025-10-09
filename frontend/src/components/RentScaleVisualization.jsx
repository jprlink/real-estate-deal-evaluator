import React from 'react';
import { Check, X, AlertTriangle } from 'lucide-react';

const RentScaleVisualization = ({ rentBand }) => {
  if (!rentBand) {
    return (
      <div className="text-sm text-gray-600 text-center py-4">
        <p>No rent data available for this area</p>
      </div>
    );
  }

  const {
    min_rent,
    max_rent,
    median_rent,
    property_rent_per_m2,
    is_compliant,
    compliance_percentage,
    is_estimate = false
  } = rentBand;

  // Calculate position on scale (percentage from left)
  const propertyPosition = Math.min(Math.max(compliance_percentage, 0), 100);

  // Determine color based on compliance
  const getStatusColor = () => {
    if (!is_compliant) {
      return 'text-red-600';
    }
    return property_rent_per_m2 <= median_rent ? 'text-green-600' : 'text-yellow-600';
  };

  const getStatusIcon = () => {
    if (!is_compliant) {
      return <X className="w-5 h-5" />;
    }
    return property_rent_per_m2 <= median_rent ?
      <Check className="w-5 h-5" /> :
      <AlertTriangle className="w-5 h-5" />;
  };

  return (
    <div className="space-y-4">
      {/* Estimate Warning if applicable */}
      {is_estimate && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-2">
          <p className="text-xs text-blue-700">
            <strong>Market Estimate:</strong> No legal rent control in this area. Showing typical market range for comparison.
          </p>
        </div>
      )}

      {/* Status Badge */}
      <div className={`flex items-center space-x-2 ${getStatusColor()}`}>
        {getStatusIcon()}
        <span className="font-semibold">
          {is_estimate ? (
            // Market estimate labels
            is_compliant ? (
              property_rent_per_m2 <= median_rent ? 'Within Market Range - Below Median' : 'Within Market Range - Above Median'
            ) : (
              property_rent_per_m2 > max_rent ? 'Above Market Range' : 'Below Market Range'
            )
          ) : (
            // Legal control labels
            is_compliant ? (
              property_rent_per_m2 <= median_rent ? 'Compliant - Below Median' : 'Compliant - Above Median'
            ) : (
              'Non-Compliant'
            )
          )}
        </span>
      </div>

      {/* Rent Values */}
      <div className="grid grid-cols-3 gap-2 text-center text-xs">
        <div>
          <p className="text-gray-500">{is_estimate ? 'Typical Min' : 'Legal Min'}</p>
          <p className="font-semibold text-gray-700">€{min_rent.toFixed(1)}/m²</p>
        </div>
        <div>
          <p className="text-gray-500">Median</p>
          <p className="font-semibold text-primary-600">€{median_rent.toFixed(1)}/m²</p>
        </div>
        <div>
          <p className="text-gray-500">{is_estimate ? 'Typical Max' : 'Legal Max'}</p>
          <p className="font-semibold text-gray-700">€{max_rent.toFixed(1)}/m²</p>
        </div>
      </div>

      {/* Visual Scale */}
      <div className="space-y-2">
        <div className="relative">
          {/* Background bar */}
          <div className="h-8 bg-gradient-to-r from-green-200 via-yellow-200 to-red-200 rounded-lg relative overflow-hidden">
            {/* Median marker */}
            <div
              className="absolute top-0 bottom-0 w-0.5 bg-primary-600"
              style={{ left: '50%' }}
            >
              <div className="absolute -top-1 left-1/2 transform -translate-x-1/2">
                <div className="w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-primary-600"></div>
              </div>
            </div>

            {/* Property marker */}
            <div
              className="absolute top-0 bottom-0 w-1 bg-gray-900 transform -translate-x-1/2"
              style={{ left: `${propertyPosition}%` }}
            >
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                <div className="w-0 h-0 border-l-6 border-r-6 border-b-6 border-l-transparent border-r-transparent border-b-gray-900"></div>
              </div>
            </div>
          </div>

          {/* Labels */}
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>{is_estimate ? 'Typical Min' : 'Legal Min'}</span>
            <span>{is_estimate ? 'Typical Max' : 'Legal Max'}</span>
          </div>
        </div>

        {/* Current Rent Display */}
        <div className="text-center">
          <p className="text-sm text-gray-600">Your Proposed Rent</p>
          <p className={`text-2xl font-bold ${getStatusColor()}`}>
            €{property_rent_per_m2.toFixed(1)}/m²
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {is_compliant ? (
              property_rent_per_m2 <= median_rent ? (
                <>Below median by €{(median_rent - property_rent_per_m2).toFixed(1)}/m²</>
              ) : (
                <>Above median by €{(property_rent_per_m2 - median_rent).toFixed(1)}/m²</>
              )
            ) : (
              property_rent_per_m2 > max_rent ? (
                <>Exceeds maximum by €{(property_rent_per_m2 - max_rent).toFixed(1)}/m²</>
              ) : (
                <>Below minimum by €{(min_rent - property_rent_per_m2).toFixed(1)}/m²</>
              )
            )}
          </p>
        </div>
      </div>

      {/* Recommended Adjustment */}
      {!is_compliant && !is_estimate && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-sm font-semibold text-red-800 mb-1">Action Required</p>
          <p className="text-xs text-red-700">
            {property_rent_per_m2 > max_rent ? (
              <>
                Reduce rent to comply with legal maximum (€{max_rent.toFixed(1)}/m²).
                Recommended rent: €{(max_rent * (property_rent_per_m2 / property_rent_per_m2 < max_rent ? property_rent_per_m2 : max_rent)).toFixed(0)}/month
              </>
            ) : (
              <>
                Increase rent to comply with legal minimum (€{min_rent.toFixed(1)}/m²).
              </>
            )}
          </p>
        </div>
      )}

      {/* Market guidance for estimates */}
      {!is_compliant && is_estimate && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
          <p className="text-sm font-semibold text-yellow-800 mb-1">Market Guidance</p>
          <p className="text-xs text-yellow-700">
            {property_rent_per_m2 > max_rent ? (
              <>
                Your proposed rent is above the typical market range. Consider adjusting to €{max_rent.toFixed(1)}/m² or lower for better tenant appeal.
              </>
            ) : (
              <>
                Your proposed rent is below the typical market range. You may be able to increase it to €{min_rent.toFixed(1)}/m² or higher.
              </>
            )}
          </p>
        </div>
      )}

      {/* Info about median */}
      {is_compliant && property_rent_per_m2 <= median_rent && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
          <p className="text-xs text-green-700">
            ✓ Your proposed rent is below the median for this area, making it attractive to tenants{!is_estimate && ' while remaining legally compliant'}.
          </p>
        </div>
      )}
    </div>
  );
};

export default RentScaleVisualization;
