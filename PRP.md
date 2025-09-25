# Project Requirements and Planning (PRP)
## Real Estate Deal Evaluator

### 📋 Project Overview

**Project Name:** Real Estate Deal Evaluator  
**Primary Goal:** Create an AI-powered real estate investment analysis tool that provides rapid, data-driven buy/pass verdicts using deterministic mathematical models.  
**Target Market:** French real estate investors, particularly focused on Paris market regulations.  
**Timeline:** Multi-phase development approach  
**Technology Stack:** Python FastAPI Backend, React/Vue.js Frontend, Pydantic-AI, WebSocket, Gmail API, Brave Search API  
**Deployment:** Web application accessible via browser at `http://localhost:8000`

---

## 🎯 Core Requirements

### 1. Primary Deal Evaluator Agent (Pydantic-AI)
**Objective:** Deliver 60-second Buy/Pass verdict using deterministic mathematics

#### Key Features:
- **Unified Verdict System:** Green/Amber/Red badges based on:
  - DSCR (Debt Service Coverage Ratio)
  - IRR (Internal Rate of Return)
  - TMC (Total Monthly Cost) vs rent comparison
  - Compliance with encadrement des loyers and DPE
- **Legal Rent Verification:** Paris encadrement compliance checking
- **Now-cast Valuation:** DVF-based property valuation with market adjustments
- **Capital Market Comparison:** ETFs, bonds, stocks alternative analysis
- **Analytics Visualization:** Cash-flow graphs and year-by-year tables

### 2. Research Sub-Agent
**Objective:** Automated data gathering and normalization

#### Capabilities:
- **Listing Data Parsing:** Address, price, surface, rooms from user input and PDFs
- **DVF Comparables:** Automated comparable property fetching
- **Zone Tendue Verification:** Rent cap compliance checking
- **Environmental Risk Assessment:** Géorisques integration for:
  - Natural risks (flood, seismicity, clay shrink-swell, radon)
  - Technological risks (ICPE sites, pipelines, soil pollution)
- **Pydantic Data Validation:** Type-safe payload preparation

### 3. Negotiation Email Sub-Agent
**Objective:** Automated negotiation email drafting

#### Features:
- **Gmail Integration:** Draft creation (never auto-send)
- **Comprehensive Analysis Package:**
  - Comparables table
  - Legal rent status
  - DSCR/IRR snapshots
  - Capital markets alternatives
  - Clear price/terms recommendations

### 4. Web Application Frontend
**Objective:** Modern, responsive browser-based interface

#### Features:
- **Interactive Dashboard:** Real-time property evaluation with live updates
- **3-Column Responsive Layout:** Optimized for desktop and tablet viewing
- **Real-time Communication:** WebSocket integration for instant analysis updates
- **Export Capabilities:** PDF reports and CSV data export
- **File Upload:** Drag-and-drop for listing PDFs and documents
- **Visualization:** Interactive charts and graphs using D3.js/Chart.js

### 5. Command Line Interface (CLI) - Secondary
**Objective:** Power user and automation interface

#### Commands:
- `evaluate` → Complete verdict with analytics
- `research` → Due diligence notes and risk assessment
- `negotiate --draft` → Gmail draft creation
- `serve` → Launch web application server

---

## 🏗️ Technical Architecture

### Core Components

#### 1. Web Application Backend (FastAPI)
```
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── routes/           # API endpoints
│   │   ├── websocket.py      # Real-time communication
│   │   └── middleware.py     # CORS, authentication
│   └── static/           # Static file serving
```

#### 2. Frontend Application (React/Vue.js)
```
├── frontend/
│   ├── src/
│   │   ├── components/       # React/Vue components
│   │   ├── pages/           # Main application pages
│   │   ├── services/        # API communication
│   │   ├── hooks/           # Custom hooks/composables
│   │   └── utils/           # Frontend utilities
│   ├── public/
│   └── package.json
```

#### 3. Agent Framework (Pydantic-AI)
```
├── agents/
│   ├── deal_evaluator.py      # Primary agent
│   ├── research_agent.py      # Data gathering
│   └── negotiation_agent.py   # Email drafting
```

#### 4. Financial Calculation Engine
```
├── calculations/
│   ├── metrics.py             # DSCR, IRR, NOI, etc.
│   ├── tax_calculations.py    # LMNP, Location nue regimes
│   ├── cash_flow.py          # TMC, cash flow projections
│   └── strategy_fit.py       # Investment strategy scoring
```

#### 5. Data Integration Layer
```
├── integrations/
│   ├── dvf_client.py         # Property value data
│   ├── georisques_client.py  # Environmental risks
│   ├── crime_data_client.py  # Crime statistics
│   ├── brave_search.py       # Web search
│   └── gmail_client.py       # Email integration
```

#### 6. Parsers and Validators
```
├── parsers/
│   ├── listing_parser.py     # PDF/HTML listing extraction
│   ├── risk_parser.py        # Environmental risk parsing
│   └── rent_cap_parser.py    # Legal rent validation
```

#### 7. User Interfaces
```
├── ui/
│   ├── cli.py               # Command line interface
│   └── components.py        # Shared UI components
```

---

## 📊 Financial Formulas & Calculations

### Key Metrics Implementation

#### Revenue Calculations
- **GMI (Gross Monthly Income)** = Monthly Rent + Other Property Income
- **VCL (Vacancy & Credit Loss)** = GMI × Vacancy Rate
- **NOI (Net Operating Income)** = (GMI − VCL) × 12 − Annual OE

#### Debt Service & Coverage
- **ADS (Annual Debt Service)** = 12 × Monthly Mortgage Payment
- **Monthly Mortgage**: M = P × [i / (1 - (1 + i)^-n)]
- **DSCR** = NOI ÷ ADS

#### Investment Returns
- **Cap Rate** = NOI ÷ Purchase Price
- **CoC Return** = Annual Pre-Tax Cash Flow ÷ Initial Cash Invested
- **IRR**: Solve 0 = Σ[CFt / (1+r)^t]
- **NPV** = Σ[CFt / (1+k)^t]

#### Strategy-Specific Calculations
- **TMC** = Principal + Interest + Monthly OE + Insurance + Management − Tax Effects
- **Strategy Fit Score** = Σ(wi × si^norm)
- **Price-to-Rent Ratio** = Purchase Price ÷ Annual Rent

---

## 🎨 User Experience Design

### Web Application Layout (3-Column Responsive Design)

#### Left Column: Input & Interaction Panel
- **AI Chatbot Interface** (top section)
  - Conversation history with agents
  - Natural language property queries
  - Real-time response indicators
- **Property Input Forms** (middle section)
  - Address autocomplete with validation
  - Price, surface, rooms with smart defaults
  - Loan parameters with sliders and inputs
  - File upload area for listing PDFs
- **Quick Actions** (bottom section)
  - "Analyze Property" primary button
  - "Export Report" secondary button
  - Settings and preferences

#### Middle Column: Interactive Analytics Dashboard
- **Financial Metrics Cards** (top section)
  - DSCR, IRR, Cap Rate with color coding
  - Tooltips explaining each metric
  - Real-time updates as inputs change
- **Interactive Visualizations** (middle section)
  - **Cash Flow Charts**: D3.js interactive graphs
  - **Comparison Charts**: Property vs alternatives
  - **Trend Analysis**: Market data over time
- **Detailed Tables** (bottom section)
  - Year-by-year cash flow breakdown
  - Expandable/collapsible sections
  - Export to CSV functionality
- **Risk Assessment Widgets**
  - Environmental risk summary cards
  - Crime statistics with local comparisons

#### Right Column: Verdict & Strategy Dashboard
- **Primary Verdicts** (top section)
  - **Property Price Verdict**: Color-coded badges (Green/Amber/Red)
  - **Legal Rent Check**: Compliance status with details
  - **Overall Recommendation**: Buy/Pass with confidence score
- **Strategy Fit Analysis** (middle section)
  - Top 3 investment strategies as interactive cards
  - Hover for detailed pros/cons
  - Click to explore strategy-specific metrics
- **Action Items** (bottom section)
  - Negotiation suggestions
  - Next steps recommendations
  - Market alerts and notifications

---

## 🔧 Development Phases

### Phase 1: Foundation & Backend (Weeks 1-4)
**Priority:** Core calculation engine and FastAPI backend

#### Deliverables:
- [ ] Project structure setup with virtual environment
- [ ] FastAPI backend with basic API endpoints
- [ ] Financial calculation engine (metrics.py)
- [ ] Basic Pydantic models for property data
- [ ] WebSocket setup for real-time communication
- [ ] CLI foundation with `evaluate` and `serve` commands
- [ ] Unit tests for financial formulas and API endpoints

#### Success Criteria:
- All financial formulas working correctly
- FastAPI server running on localhost:8000
- Basic API endpoints returning JSON responses
- WebSocket connection established
- Comprehensive test coverage for calculations

### Phase 2: Data Integration & API Enhancement (Weeks 5-7)
**Priority:** External data sources and backend API completion

#### Deliverables:
- [ ] DVF API integration for comparables
- [ ] Géorisques environmental risk parsing
- [ ] Crime data integration
- [ ] PDF/HTML listing parsers with file upload API
- [ ] Paris rent cap validation system
- [ ] RESTful API endpoints for all data sources
- [ ] API documentation with OpenAPI/Swagger

#### Success Criteria:
- Automated data fetching from all sources via API
- File upload working for PDF processing
- Reliable parsing of listing documents
- Environmental and crime risk assessment via API
- Complete API documentation available

### Phase 3: AI Agents & WebSocket Integration (Weeks 8-10)
**Priority:** Pydantic-AI agent implementation with real-time communication

#### Deliverables:
- [ ] Primary Deal Evaluator agent with WebSocket integration
- [ ] Research Sub-Agent with Brave Search
- [ ] Negotiation Email Sub-Agent
- [ ] Agent orchestration and communication
- [ ] Gmail API integration
- [ ] Real-time progress updates via WebSocket
- [ ] Agent status monitoring and error handling

#### Success Criteria:
- End-to-end automated evaluation workflow
- Real-time agent communication via WebSocket
- Research agent providing comprehensive data
- Email drafting with complete analysis
- Live progress indicators for long-running tasks

### Phase 4: Frontend Development (Weeks 11-14)
**Priority:** React/Vue.js frontend with responsive design

#### Deliverables:
- [ ] Frontend project setup (React/Vue.js + Vite/Webpack)
- [ ] 3-column responsive layout implementation
- [ ] Interactive forms with validation and auto-complete
- [ ] Real-time WebSocket integration for live updates
- [ ] D3.js/Chart.js interactive visualizations
- [ ] File upload component with drag-and-drop
- [ ] Chatbot interface with conversation history
- [ ] Export functionality (PDF reports, CSV data)
- [ ] Mobile-responsive design adaptations
- [ ] Enhanced CLI with all commands (secondary priority)

#### Success Criteria:
- Fully functional web application accessible in browser
- Responsive design working on desktop, tablet, and mobile
- Real-time updates working smoothly
- Interactive charts and visualizations
- Intuitive user experience with clear navigation

### Phase 5: Integration, Testing & Polish (Weeks 15-16)
**Priority:** End-to-end testing, optimization, and deployment preparation

#### Deliverables:
- [ ] Frontend-backend integration testing
- [ ] Cross-browser compatibility testing
- [ ] Performance optimization (frontend and backend)
- [ ] Security review and HTTPS setup
- [ ] User acceptance testing with real scenarios
- [ ] Production build optimization
- [ ] Deployment documentation and scripts
- [ ] Example data and interactive tutorials
- [ ] Error monitoring and logging setup

#### Success Criteria:
- Production-ready web application
- Sub-60-second evaluation performance maintained
- Cross-browser compatibility confirmed
- Secure HTTPS deployment ready
- Complete documentation with examples
- Monitoring and error tracking in place

---

## 🛠️ Technical Requirements

### Backend Dependencies
```python
# Web Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
websockets>=12.0

# Core Framework
pydantic-ai>=0.0.14
pydantic>=2.0.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0

# File Processing
PyPDF2>=3.0.0
beautifulsoup4>=4.12.0
python-multipart>=0.0.6

# APIs
google-auth>=2.22.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
gmail-api-python-client>=2.0.0

# CLI
click>=8.1.0
rich>=13.0.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0",
    "axios": "^1.6.0",
    "ws": "^8.14.0",
    "d3": "^7.8.0",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "tailwindcss": "^3.3.0",
    "@headlessui/react": "^1.7.0",
    "react-router-dom": "^6.18.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.0",
    "eslint": "^8.53.0",
    "prettier": "^3.0.0",
    "@types/d3": "^7.4.0"
  }
}
```

### Environment Configuration
```bash
# Web Server Configuration
HOST=localhost
PORT=8000
ENVIRONMENT=development
DEBUG=true

# Required API Keys
BRAVE_SEARCH_API_KEY=your_brave_api_key
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads
ALLOWED_FILE_TYPES=pdf,jpg,png,docx

# Optional Configuration
DEFAULT_DISCOUNT_RATE=0.08
DEFAULT_HOLDING_PERIOD=10
DEFAULT_VACANCY_RATE=0.05

# WebSocket Configuration
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=100
```

---

## 📁 Project Structure
```
real-estate-deal-evaluator/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt              # Python backend dependencies
├── setup.py
├── pyproject.toml
├── main.py                      # FastAPI application entry point
│
├── backend/                     # Python Backend (FastAPI)
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── evaluation.py    # Property evaluation endpoints
│   │   │   ├── research.py      # Research and data endpoints
│   │   │   ├── negotiation.py   # Email drafting endpoints
│   │   │   └── upload.py        # File upload endpoints
│   │   ├── websocket.py     # WebSocket handlers
│   │   ├── middleware.py    # CORS, auth, logging
│   │   └── dependencies.py  # Dependency injection
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── deal_evaluator.py
│   │   ├── research_agent.py
│   │   └── negotiation_agent.py
│   │
│   ├── calculations/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── tax_calculations.py
│   │   ├── cash_flow.py
│   │   └── strategy_fit.py
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── dvf_client.py
│   │   ├── georisques_client.py
│   │   ├── crime_data_client.py
│   │   ├── brave_search.py
│   │   └── gmail_client.py
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── listing_parser.py
│   │   ├── risk_parser.py
│   │   └── rent_cap_parser.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── property_models.py
│   │   ├── financial_models.py
│   │   └── risk_models.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── components.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       ├── logging.py
│       └── helpers.py
│
├── frontend/                    # React/Vue.js Frontend
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   │
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── main.tsx              # Application entry point
│   │   ├── App.tsx               # Root component
│   │   │
│   │   ├── components/           # Reusable UI components
│   │   │   ├── layout/
│   │   │   │   ├── LeftPanel.tsx
│   │   │   │   ├── MiddlePanel.tsx
│   │   │   │   └── RightPanel.tsx
│   │   │   ├── forms/
│   │   │   │   ├── PropertyForm.tsx
│   │   │   │   └── FileUpload.tsx
│   │   │   ├── charts/
│   │   │   │   ├── CashFlowChart.tsx
│   │   │   │   └── ComparisonChart.tsx
│   │   │   ├── chat/
│   │   │   │   ├── ChatBot.tsx
│   │   │   │   └── ChatMessage.tsx
│   │   │   └── ui/              # Basic UI components
│   │   │       ├── Button.tsx
│   │   │       ├── Card.tsx
│   │   │       └── Badge.tsx
│   │   │
│   │   ├── pages/                # Main application pages
│   │   │   ├── Dashboard.tsx
│   │   │   ├── PropertyAnalysis.tsx
│   │   │   └── Settings.tsx
│   │   │
│   │   ├── services/             # API communication
│   │   │   ├── api.ts
│   │   │   ├── websocket.ts
│   │   │   └── types.ts
│   │   │
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useWebSocket.ts
│   │   │   ├── usePropertyData.ts
│   │   │   └── useAnalytics.ts
│   │   │
│   │   ├── utils/                # Frontend utilities
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── constants.ts
│   │   │
│   │   └── styles/               # CSS and styling
│   │       ├── globals.css
│   │       └── components.css
│   │
│   └── dist/                     # Built frontend files
│
├── uploads/                     # File upload directory
│
├── tests/
│   ├── __init__.py
│   ├── test_api/                # API endpoint tests
│   ├── test_calculations/       # Financial calculation tests
│   ├── test_agents/            # Agent behavior tests
│   ├── test_integrations/      # External API tests
│   ├── test_parsers/           # Document parsing tests
│   ├── test_frontend/          # Frontend component tests
│   └── fixtures/               # Test data
│
├── examples/
│   ├── listing_1.pdf
│   ├── listing_2.pdf
│   ├── georisques.pdf
│   ├── env_risks_1.pdf
│   ├── env_risks_2.pdf
│   └── sample_evaluations/
│
├── docs/
│   ├── api_reference.md
│   ├── user_guide.md
│   ├── development_guide.md
│   └── deployment_guide.md
│
└── scripts/
    ├── setup_environment.py
    ├── build_frontend.py
    ├── test_apis.py
    └── deploy.py
```

---

## 🧪 Testing Strategy

### Unit Tests
- Financial calculation accuracy
- Pydantic model validation
- Individual component functionality

### Integration Tests
- API connectivity and data flow
- Agent communication and orchestration
- End-to-end evaluation workflows

### Performance Tests
- Response time under 60 seconds
- Memory usage optimization
- Concurrent request handling

### User Acceptance Tests
- Web application usability testing across browsers
- Mobile responsiveness validation
- Real-time update functionality
- File upload and processing workflows
- Export functionality testing
- CLI usability testing (secondary)
- Error handling and user feedback scenarios

---

## 🚀 Deployment Considerations

### Local Development
- Virtual environment isolation
- Environment variable management
- Development database setup

### Production Readiness
- Error logging and monitoring
- API rate limiting
- Security credential management
- Performance optimization

### Documentation Requirements
- Setup instructions with Gmail/Brave configuration
- API key management guide
- Troubleshooting documentation
- Example usage scenarios

---

## 🎯 Success Metrics

### Performance Targets
- **Response Time:** < 60 seconds for complete evaluation
- **Frontend Load Time:** < 3 seconds initial page load
- **Real-time Updates:** < 500ms WebSocket response time
- **Accuracy:** > 95% for financial calculations
- **Data Coverage:** Complete environmental and crime risk data
- **User Experience:** Intuitive web interface with responsive design
- **Cross-browser Support:** Chrome, Firefox, Safari, Edge
- **Mobile Support:** Tablet-optimized responsive design

### Quality Assurance
- **Code Coverage:** > 90% test coverage
- **Documentation:** Complete API and user documentation
- **Error Handling:** Graceful failure with informative messages
- **Security:** Secure API key and credential management

---

## 📝 Risk Assessment & Mitigation

### Technical Risks
- **API Dependencies:** Implement fallback mechanisms and caching
- **Data Quality:** Validation layers and error detection
- **Performance:** Optimize calculation algorithms and data fetching

### Business Risks
- **Regulatory Changes:** Modular design for easy updates
- **Market Data Availability:** Multiple data source integration
- **User Adoption:** Comprehensive documentation and examples

### Mitigation Strategies
- Comprehensive testing at each phase
- Modular architecture for easy updates
- Fallback mechanisms for external dependencies
- Regular security audits and updates

---

*This PRP document serves as the foundation for the Real Estate Deal Evaluator project development. It should be reviewed and updated as requirements evolve during the development process.*
