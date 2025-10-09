## FEATURE:

- **Primary "Deal Evaluator" Agent (Pydantic-AI)** that returns a **60-second Buy/Pass verdict** using **deterministic math (no AI heuristics)**.
  - **Unified Verdict badges** (green/amber/red) driven by thresholds for **DSCR (Debt Service Coverage Ratio)**, **IRR (Internal Rate of Return)**, **TMC (Total Monthly Cost) vs. rent**, and **compliance** (encadrement des loyers, DPE).
  - Computes **Legal Rent Check** (**nationwide coverage**: Paris encadrement + major cities rent control + regional estimates for all France) with automatic fallback to market estimates for areas without legal control.
  - **Now-cast valuation** from **DVF (Demandes de Valeurs Foncières)** adjusted by listing signals (e.g., price cuts, days-on-market), and a **capital comparison** vs **ETFs (Exchange-Traded Funds)**, **bonds**, **stocks** on equal cash & horizon.
  - **Analytics pane** shows **both**: (1) a compact **cash-flow graph** (annual bars + cumulative line) with **mortgage payoff visibility** and (2) a **customizable year-by-year cash-flow table** (1-50 years, default 30) showing transition to positive cash flow after mortgage is paid off.

- **Research Sub-Agent (tool of the primary agent)** using Brave Search + internal parsers:
  - Normalizes listing facts (address, price, surface, rooms) from user input and PDFs, fetches DVF comps, checks **zone tendue**, rent caps, and prepares typed Pydantic payloads for the evaluator.
  - **Automatic city detection** from postal code using comprehensive French postal code database (all 101 departments + specific city mappings).
  - **Property appreciation rates** based on Notaires de France Q4 2024/Q1 2025 market data by department with forward-looking adjustments (+1.5%).
  - **Environmental Risks (postcode-based)** via Géorisques: summarizes **natural** (e.g., flood, groundwater rise, seismicity, ground movement, clay shrink–swell, radon) and **technological** risks (e.g., ICPE sites, dangerous-materials pipelines, soil pollution), with address- vs commune-level flags and a link for detail.

- **Negotiation Email Sub-Agent (tool of the primary agent)** using Gmail:  
  - Drafts a **Negotiation Pack** email (never auto-sends) with comps table, legal-rent status, DSCR/IRR snapshots, capital-markets alternative, and a clear price/terms ask.

- **Web Application** with modern browser-based frontend (primary interface):
  - **Interactive Dashboard** with real-time evaluation results and analytics visualization
  - **Responsive 3-column layout** optimized for desktop and tablet use
  - **Real-time updates** as user inputs property details and parameters
  - **Nationwide French property support** - evaluates properties in all 101 departments (Paris to Thonon-les-Bains to Marseille)
  - **Customizable projection timeframe** (1-50 years, default 30) with visual cash flow tracking
  - **Export capabilities** for reports and analysis summaries  

- **CLI** as secondary interface for power users and automation:  
  - `evaluate` → verdict + legal rent + now-cast value + strategy fit + cash-flow chart & table.  
  - `research` → due-diligence notes (listing parse + risks + caps).  
  - `negotiate --draft` → creates a Gmail draft using computed analytics.

- **Strategy Fit (0–100) with reasons, sorted best-fit first:**  
  - **Owner-occupier**, **Location nue (unfurnished)**, **LMNP (furnished, micro-BIC)**, **Colocation**, **Value-Add / déficit foncier** — each card shows **Pros & Cons** tied to actual metrics (TMC vs rent, DSCR, IRR, compliance, bedrooms, discount vs median).

**Web Application Layout (UX requirement):**
- **Browser-based interface** accessible at `http://localhost:3000` (frontend) with modern, responsive design
- **Right third of the window:**
  - **Detected Location** badge showing city/village from postal code (e.g., "Thonon-les-Bains" from 74200)
  - **Property Price Verdict:** **Under-priced / Average / Overpriced** (color-coded badges)
  - **Legal Rent Check:** Displays either:
    - **Legal rent control**: **Conformant – Low / Conformant – High / Non-conformant** with legal min/max labels
    - **Market estimate**: Blue banner + **Within Market Range / Above / Below** with typical min/max labels + yellow guidance
  - **Strategy Fit badges:** Top 3 strategy profiles (0–100 with short reason codes) displayed as interactive cards  
- **Middle column:** **Interactive Analytics Dashboard** with real-time updates:
  - **Financial metrics** displayed in clean, readable cards with tooltips
  - **Interactive cash-flow charts** (Chart.js) showing annual cash flow and cumulative totals with **clear mortgage payoff indication** (year 21+ shows €0 mortgage payment)
  - **Customizable cash flow table** (1-50 years) showing:
    - Rental income, operating expenses, mortgage payment, NOI, cash flow, cumulative CF
    - Property value appreciation by year based on local market data
    - Equity buildup over time
    - **Transition to positive cash flow** after mortgage is paid off (clearly visible in table)
  - **Property appreciation footnote** with data source and rate
  - **Risk assessment widgets** for environmental and crime data  
- **Left column:** **Input Panel and Chat Interface**:  
  - **AI Chatbot** (linked to agents) at the top with conversation history  
  - **Property input forms** with validation and auto-complete  
  - **File upload area** for listing PDFs  
  - **Quick action buttons** for common tasks


## EXAMPLES:

The `examples/` folder contains the following **assets to parse or reference**:
- Listing PDFs to test the **parser** of listings (but note that the actual listings are in html):  
  - `examples/listing_1.pdf`  
  - `examples/listing_2.pdf`  
- Environmental-risk report PDFs (examples from https://www.georisques.gouv.fr to test the **parser** of environmenal risks (but note that the actual listings are in html). One needs to first enter the zip code in https://www.georisques.gouv.fr (see pdf of this website):
  - `examples/georisques.pdf` 
and then one reaches the website for the specific zip code (see pdf examples of this website, but note that the actual listings are in html):  
  - `examples/env_risks_1.pdf`  
  - `examples/env_risks_2.pdf`


## DOCUMENTATION:

Pydantic AI documentation: https://ai.pydantic.dev/

- **GMI (Gross Monthly Income)** = Monthly Rent (legal or market) + Other Property Income.  
- **VCL (Vacancy & Credit Loss)** = GMI × Vacancy Rate.  
- **OE (Operating Expenses)** = Sum of recurring non-debt costs (taxes, insurance, syndic/HOA, maintenance, management, landlord-paid utilities, etc.).  
- **NOI (Net Operating Income)** = (GMI − VCL) × 12 − Annual OE.

- **ADS (Annual Debt Service)** = 12 × Monthly Mortgage Payment.  
- **Monthly Mortgage (amortizing)**:  
  \( M = P \times \dfrac{i}{1 - (1 + i)^{-n}} \)  
  where \(P\)=loan principal, \(i\)=monthly interest rate, \(n\)=months.

- **DSCR (Debt Service Coverage Ratio)** = NOI ÷ ADS.

- **TMC (Total Monthly Cost)** = Principal + Interest + Monthly OE + Insurance + Management Fees − Monthly Tax Effects.  
  *The cash-flow **graph** and **table** reflect this breakdown.*

- **Cap Rate (Capitalization Rate)** = NOI ÷ Purchase Price.

- **CoC (Cash-on-Cash Return)** = Annual Pre-Tax Cash Flow ÷ Initial Cash Invested,  
  with **Annual Pre-Tax Cash Flow** = (GMI − VCL − Monthly OE − Monthly Debt Service) × 12.

- **IRR (Internal Rate of Return)** solves \( 0 = \sum_{t=0}^{T} \dfrac{CF_t}{(1+r)^t} \),  
  where \(CF_0 = -\)Initial Equity; \(CF_T\) includes net sale proceeds after costs and remaining loan.

- **NPV (Net Present Value)** at discount rate \(k\):  
  \( \text{NPV} = \sum_{t=0}^{T} \dfrac{CF_t}{(1+k)^t} \).

- **Sale Proceeds (Net)** = Resale Price − Selling Costs − Remaining Loan Balance.

- **Price-to-Rent (Years)** = Purchase Price ÷ Annual Rent.  
- **Yield on Cost** = Stabilized NOI ÷ (Purchase Price + CapEx/Travaux).

- **LTV (Loan-to-Value)** = Loan Amount ÷ Purchase Price.  
- **Equity Multiple (Leverage Ratio)** = Total Distributions to Equity ÷ Total Equity Invested.

- **Taxable Income (by regime):**  
  - **LMNP (furnished) micro-BIC**: Taxable = Gross Rent × (1 − Abatement%). Tax = Taxable × Marginal Rate.  
  - **Location nue (unfurnished) micro-foncier**: Taxable = Gross Rent − Flat Abatement. Tax = Taxable × Marginal Rate.  
  - *(Régime réel: Taxable = Gross Rent − Actual Deductible Expenses − Interest, per rules.)*

- **After-Tax Margin (Monthly)** = Pre-Tax Monthly Cash Flow − (Income Tax + Social Charges)/12.

- **Net Housing Cost vs Renting (Owner-occupier)**  
  = TMC − Imputed Benefits (principal amortization + eligible subsidies/credits) − Saved Rent.

- **Strategy Fit Score (0–100)**  
  \( \text{Fit} = \sum_i w_i \cdot s_i^{\text{norm}} \)  
  with profile-specific weights and normalized metric scores.

- **Nationwide Rent Control & Market Estimates:**
  - **Legal rent control** (encadrement des loyers) for:
    - **Paris**: All 20 arrondissements with quartier-level variations (2024-2025 data)
    - **Major cities**: Lyon (9 arr.), Marseille (10 arr.), Bordeaux, Toulouse, Nice, Lille, Montpellier, Strasbourg, Nantes, Rennes, Grenoble, Toulon, Angers
  - **Regional market estimates** for areas without legal control:
    - All 13 French regions with typical min/median/max rent per m²
    - Department-to-region mapping for accurate fallback
    - National average as final fallback (€9.0-14.0/m², median €11.5)
  - **UI differentiation**:
    - **Legal control**: "Legal Min/Max" labels + compliance verdicts (**Conformant – Low / High / Non-conformant**)
    - **Market estimate**: Blue banner warning + "Typical Min/Max" labels + market range verdicts (**Within Market Range / Above / Below**)

- **Now-Cast Valuation (deterministic):**  
  \( \text{Now-Cast} = \text{DVF Median (matched comps)} \times (1+\Delta_{\text{market}}) \times (1+\Delta_{\text{listing}}) \)  
  where \(\Delta_{\text{listing}}\) aggregates transparent adjustments (e.g., recent price-cut %, days-on-market vs median, condition/DPE penalties).  
  - **Price Verdict labels** displayed in UI: **Under-priced / Average / Overpriced**.

- **Capital Comparison (same cash & horizon):**  
  **Future Value** of alternative = Initial Cash × \((1+r)^{T}\). Compare property **IRR/NPV** to alternative on horizon \(T\).

- **Environmental Risks (postcode/address via https://www.georisques.gouv.fr):**  
  Return **counts and statuses** for natural (e.g., flood, groundwater rise, seismicity, ground movement, clay shrink–swell, radon) and technological risks (e.g., ICPE sites, dangerous-materials pipelines, soil pollution), with address- vs commune-level flags and source links.  
  Display a concise **risk summary widget** alongside inputs; link to the full report.

- **Crime Risks (postcode-level via French open data):**  
  - **Inputs:** official incidence rates (per 1,000 inhabitants) over the last available 12 months for categories such as **burglary**, **theft**, **vehicle theft**, **assault**.  
  - **Normalized Crime Risk Score (0–100):**  
    \( \text{CrimeScore} = 100 \times \sum_c w_c \cdot \frac{\text{rate}_c - p50_c}{p90_c - p10_c} \) clipped to [0,100],  
    where \(w_c\) are category weights; \(p10_c, p50_c, p90_c\) are national deciles used for robust scaling.  
  - **Display:** category table with local rate vs national median, plus an overall **Crime Risk** badge in the left column module.


## OTHER CONSIDERATIONS:

- **Web server** built with FastAPI for the backend API and static file serving  
- **Frontend** using modern JavaScript framework (React/Vue.js) with responsive CSS  
- **Real-time communication** via WebSocket for instant updates during analysis  
- Include a `.env.example`, and a **README** with setup instructions including:  
  - Web server configuration and port settings  
  - Frontend build process and dependencies  
  - Gmail and Brave API configuration  
  - Browser compatibility requirements  
- Include the **project structure** in the README with both backend and frontend components  
- Always use virtual environment for Python backend  
- Use python3 to create the venv, then python works inside the venv  
- **Launch command**: `python -m uvicorn main:app --reload` to start web server  
- **Access URL**: Application opens automatically in default browser at `http://localhost:8000`
