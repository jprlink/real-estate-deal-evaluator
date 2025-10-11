# Changelog

All notable changes to the France Real Estate Investment Analyzer project.

## [Unreleased] - 2025-10-10

### Added
- **Interactive metric tooltips**: Hover over financial metrics (DSCR, IRR, Cap Rate, etc.) to see detailed explanations and formulas
- **DVF database integration**: Price verdicts now use real French property transaction data from Demandes de Valeurs Foncières database
- **Comprehensive DVF API client**: Fetches comparable sales from data.gouv.fr API with surface filtering (±30%)
- **Automatic city detection**: All postal codes now automatically display corresponding French city/village names

### Changed
- **Consolidated key metrics display**: All 8 financial metrics now shown in single unified card above cash flow graph
- **Improved rent label clarity**: Changed "Your Proposed Rent" to "Your Input Rent" to clarify user input vs. system calculation
- **Compacted cash flow table**: Table now has scrollable height (max 340px) showing ~5 years initially with sticky headers
- **Enhanced tooltip rendering**: Fixed tooltip overflow issues with proper positioning and word wrapping
- **DVF-based price analysis**: Price verdict logic updated from static thresholds to dynamic DVF comparisons:
  - Fetches recent sales (2 years) for similar properties (±30% surface)
  - Calculates median market price per m²
  - Applies ±10% tolerance for "Average" verdict
  - Falls back to Paris market ranges if insufficient DVF data (<3 comps)

### Removed
- **Detected Location field**: Removed redundant location display from RightPanel (information already in form)
- **Separate metric cards**: Replaced scattered 2x2 grid + separate key metrics card with unified layout
- **MetricCard component**: Removed unused component after consolidation

### Technical Details
- Updated `backend/integrations/dvf.py` with real API integration (APUR Île-de-France DVF dataset)
- Modified `backend/api/routes/evaluate.py` to call DVF API for price analysis
- Enhanced `frontend/src/components/MiddlePanel.jsx` with MetricWithTooltip component
- Updated `frontend/src/components/RentScaleVisualization.jsx` with clearer labeling
- Improved `frontend/src/components/CashFlowTable.jsx` with sticky headers and compact display
- Added httpx async API calls with 10-second timeout and proper error handling

### Fixed
- Tooltip text no longer cuts off at container boundaries
- Cash flow table properly scrollable both vertically and horizontally
- DSCR calculation consistency with cash flow projections (both use 5% vacancy rate)

## Previous Updates

See git history for earlier changes including:
- DSCR vs cash flow consistency fixes
- Nationwide French coverage implementation
- CSV export functionality
- Rent control data for all French departments
- Property appreciation rates from Notaires de France
