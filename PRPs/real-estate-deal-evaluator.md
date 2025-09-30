name: "Real Estate Deal Evaluator - Full-Stack AI Agent System"
description: |
  Comprehensive PRP for building a complete real estate investment analysis platform
  with PydanticAI agents, FastAPI backend, and React frontend.

---

## Goal
Build a complete real estate deal evaluation system with:
- **Primary Deal Evaluator Agent** that returns 60-second Buy/Pass verdicts using deterministic financial math
- **Research Sub-Agent** for listing data, DVF comps, legal rent checks, and environmental risk analysis
- **Negotiation Email Sub-Agent** for drafting Gmail negotiations
- **Modern Web Application** with real-time updates, interactive dashboard, and responsive 3-column layout
- **CLI Interface** for power users and automation

## Why
- **Business Value**: Enables rapid, data-driven real estate investment decisions in the Paris market
- **User Impact**: Transforms hours of manual research into 60-second automated analysis
- **Integration**: Combines multiple data sources (DVF, Géorisques, Paris rent control API, crime data) into unified insights
- **Problems Solved**:
  - Eliminates guesswork in property valuation and investment strategy
  - Automates compliance checking (Paris encadrement des loyers, DPE)
  - Provides capital comparison (real estate vs ETFs/bonds/stocks)
  - Generates professional negotiation emails with data-backed arguments

## What
A full-stack application with PydanticAI agents providing financial analysis, risk assessment, and negotiation support.

### Success Criteria
- [ ] Primary agent returns verdicts in <60 seconds with accurate DSCR, IRR, TMC calculations
- [ ] Research agent successfully parses listings, fetches DVF data, checks rent caps, retrieves environmental risks
- [ ] Negotiation agent creates Gmail drafts with comps, legal-rent status, and clear asks
- [ ] Web UI displays real-time results in 3-column layout with interactive charts
- [ ] CLI provides `evaluate`, `research`, and `negotiate` commands
- [ ] All financial calculations are deterministic (no AI heuristics in math)
- [ ] Strategy fit scores (0-100) for 5 profiles: Owner-occupier, Location nue, LMNP, Colocation, Value-Add
- [ ] Integration tests pass with real API calls (mocked for CI/CD)
- [ ] Unit tests achieve >80% coverage

---

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Core Technologies

- url: https://ai.pydantic.dev/agents/
  why: Agent creation patterns, tools, structured outputs, dependencies
  critical: |
    - Use @agent.tool for context-aware tools with RunContext[DepsType]
    - Use @agent.tool_plain for simple tools without dependencies
    - Agents are reusable like FastAPI apps
    - Default output is string, only use result_type for structured output

- url: https://ai.pydantic.dev/tools/
  why: Tool decorator patterns and registration methods
  critical: |
    - Tools enable models to perform actions and retrieve information
    - Function parameters automatically extracted for tool schema
    - Use docstrings for parameter descriptions

- url: https://fastapi.tiangolo.com/advanced/websockets/
  why: WebSocket implementation for real-time updates
  critical: |
    - Native WebSocket support in FastAPI
    - Use async/await for WebSocket handlers
    - Maintain WebSocket connections for live updates

- url: https://testdriven.io/blog/fastapi-postgres-websockets/
  why: Real-time dashboard patterns with FastAPI and WebSockets (July 2025)
  critical: Stream live data updates from backend to frontend

- url: https://www.chartjs.org/chartjs-chart-financial/
  why: Financial chart library for cash-flow visualization

- url: https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/api/
  why: Paris rent control (encadrement des loyers) API
  critical: |
    - Updated annually on July 1st
    - Returns reference rent, ceiling rent, by neighborhood, rooms, construction period
    - Data in EUR/m² of living space

- url: https://www.georisques.gouv.fr/doc-api
  why: Environmental and technological risks API
  critical: |
    - Natural risks: flood, groundwater, seismicity, clay, radon
    - Technological risks: ICPE, pipelines, soil pollution
    - Requires address or commune-level queries

- url: https://www.data.gouv.fr/dataservices/api-dvf-trouvez-les-valeurs-de-ventes-et-encore/
  why: DVF (Demandes de Valeurs Foncières) property transaction data
  critical: |
    - All real estate sales in France (except Alsace-Moselle, Mayotte) since 2014
    - Updated every 6 months (April, October)
    - Geolocated transactions with property types and sale amounts

- url: https://developers.google.com/workspace/gmail/api/guides/drafts
  why: Gmail API for creating draft emails
  critical: |
    - Use drafts.create() method with base64url-encoded MIME messages
    - Requires OAuth 2.0 authentication
    - Messages must be RFC 2822 compliant

- url: https://api.search.brave.com/app/documentation
  why: Brave Search API documentation
  critical: |
    - Free tier: 2,000 requests/month
    - Rate limiting: Handle 429 responses
    - Endpoint: https://api.search.brave.com/res/v1/web/search

# Reference Implementation Patterns

- file: use-cases/pydantic-ai/examples/main_agent_reference/research_agent.py
  why: Sub-agent pattern with tool invocation of other agents
  critical: |
    - Line 59-91: @agent.tool decorator with RunContext
    - Line 150-154: Invoking email_agent.run() from research agent tool
    - Line 42-48: ResearchAgentDependencies dataclass pattern

- file: use-cases/pydantic-ai/examples/main_agent_reference/tools.py
  why: Pure tool functions that can be imported and used by agents
  critical: |
    - Lines 18-121: search_web_tool as pure async function
    - Lines 45-46: API key validation pattern
    - Lines 72-92: Error handling with httpx (429, 401, etc.)

- file: use-cases/pydantic-ai/examples/main_agent_reference/settings.py
  why: Environment configuration with pydantic-settings and python-dotenv
  critical: |
    - Lines 11-12: load_dotenv() at module level
    - Lines 15-58: Settings class with ConfigDict and Field validators
    - Lines 51-58: Fallback for testing with dummy values

- file: use-cases/pydantic-ai/examples/main_agent_reference/models.py
  why: Pydantic models for data validation and API responses
  critical: |
    - Lines 17-33: BraveSearchResult with Field descriptions
    - Lines 89-94: ChatMessage with timestamp and tools_used
    - Use json_schema_extra for examples

- file: use-cases/pydantic-ai/examples/main_agent_reference/cli.py
  why: Streaming CLI with rich console and real-time tool visibility
  critical: |
    - Lines 44-76: Streaming agent execution with node iteration
    - Lines 74-136: Tool call event handling and display
    - Lines 26-152: Stream agent interaction pattern
```

### Current Codebase Tree

```bash
real-estate-deal-evaluator/
├── backend/
│   ├── agents/           # PydanticAI agents (empty - to be created)
│   ├── api/              # FastAPI routes and WebSocket handlers
│   ├── calculations/     # Financial math modules
│   ├── integrations/     # External API clients (DVF, Géorisques, etc.)
│   ├── models/           # Pydantic models and database schemas
│   ├── parsers/          # HTML/PDF parsers for listings and risks
│   ├── ui/               # Backend UI helpers
│   └── utils/            # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client services
│   │   ├── styles/       # CSS/styling
│   │   └── utils/        # Frontend utilities
│   ├── public/           # Static assets
│   └── dist/             # Build output
├── examples/             # Example PDFs (listing_1.pdf, env_risks_1.pdf, etc.)
├── tests/                # Pytest test files
├── use-cases/            # Reference implementations
│   └── pydantic-ai/examples/main_agent_reference/  # MIRROR THIS STRUCTURE
├── CLAUDE.md             # Global rules (MUST FOLLOW)
├── INITIAL.md            # Feature requirements
└── PRPs/                 # This file

Key files in use-cases/pydantic-ai/examples/main_agent_reference/:
- agent.py, tools.py, models.py, settings.py, cli.py, providers.py
- tests/test_agent.py, tests/conftest.py, tests/test_integration.py
```

### Desired Codebase Tree with New Files

```bash
backend/
├── agents/
│   ├── __init__.py
│   ├── deal_evaluator/
│   │   ├── __init__.py
│   │   ├── agent.py          # Primary agent - 60-second verdicts
│   │   ├── tools.py          # Invokes research & negotiation agents
│   │   ├── prompts.py        # System prompts
│   │   └── models.py         # Verdict, StrategyFit, etc.
│   ├── research/
│   │   ├── __init__.py
│   │   ├── agent.py          # Research sub-agent
│   │   ├── tools.py          # DVF, Géorisques, rent caps, listing parse
│   │   ├── prompts.py
│   │   └── models.py         # ListingData, DVFComp, RiskSummary
│   ├── negotiation/
│   │   ├── __init__.py
│   │   ├── agent.py          # Negotiation email sub-agent
│   │   ├── tools.py          # Gmail draft creation
│   │   ├── prompts.py
│   │   └── models.py         # EmailDraft, NegotiationPack
│   ├── dependencies.py       # Shared dependency dataclasses
│   ├── settings.py           # Environment config (mimic main_agent_reference)
│   └── providers.py          # LLM provider setup
├── calculations/
│   ├── __init__.py
│   ├── financial.py          # NOI, DSCR, IRR, NPV, Cap Rate, CoC
│   ├── mortgage.py           # Amortization schedule, monthly payment
│   ├── taxes.py              # LMNP, location nue, régime réel
│   ├── valuation.py          # Now-cast value, DVF median, adjustments
│   └── strategy_fit.py       # 0-100 scores for 5 profiles
├── integrations/
│   ├── __init__.py
│   ├── brave.py              # Brave Search API client
│   ├── gmail.py              # Gmail API client
│   ├── dvf.py                # DVF API client
│   ├── georisques.py         # Géorisques API client
│   ├── paris_rent.py         # Paris encadrement API client
│   └── crime_data.py         # French crime data API
├── parsers/
│   ├── __init__.py
│   ├── listing.py            # HTML/PDF listing parser (playwright)
│   └── risks.py              # Géorisques HTML parser
├── models/
│   ├── __init__.py
│   ├── property.py           # Property, Listing, Address
│   ├── financial.py          # FinancialInputs, CashFlow, Verdict
│   ├── legal.py              # LegalRentCheck, Compliance
│   └── risks.py              # EnvironmentalRisk, CrimeRisk
├── api/
│   ├── __init__.py
│   ├── main.py               # FastAPI app, CORS, static files
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── evaluate.py       # POST /api/evaluate
│   │   ├── research.py       # POST /api/research
│   │   ├── negotiate.py      # POST /api/negotiate
│   │   └── websocket.py      # WebSocket /ws for real-time updates
│   └── schemas.py            # Request/response schemas
├── cli/
│   ├── __init__.py
│   └── main.py               # CLI with typer: evaluate, research, negotiate
├── .env.example              # Environment variables template
└── main.py                   # Entry point: uvicorn main:app --reload

frontend/src/
├── components/
│   ├── LeftColumn/
│   │   ├── ChatInterface.jsx
│   │   ├── PropertyInput.jsx
│   │   └── FileUpload.jsx
│   ├── MiddleColumn/
│   │   ├── Dashboard.jsx
│   │   ├── FinancialMetrics.jsx
│   │   ├── CashFlowChart.jsx     # Chart.js or react-financial-charts
│   │   ├── CashFlowTable.jsx
│   │   └── RiskWidgets.jsx
│   ├── RightColumn/
│   │   ├── VerdictPanel.jsx      # Price verdict badges
│   │   ├── LegalRentCheck.jsx
│   │   └── StrategyFitCards.jsx
│   └── Layout/
│       └── ThreeColumnLayout.jsx
├── services/
│   ├── api.js                    # Axios/fetch client
│   └── websocket.js              # WebSocket connection manager
├── hooks/
│   ├── useWebSocket.js
│   └── useEvaluation.js
└── App.jsx                       # Main app with router

tests/
├── backend/
│   ├── agents/
│   │   ├── test_deal_evaluator.py
│   │   ├── test_research.py
│   │   └── test_negotiation.py
│   ├── calculations/
│   │   ├── test_financial.py
│   │   ├── test_mortgage.py
│   │   ├── test_taxes.py
│   │   ├── test_valuation.py
│   │   └── test_strategy_fit.py
│   ├── integrations/
│   │   ├── test_brave.py
│   │   ├── test_gmail.py
│   │   ├── test_dvf.py
│   │   ├── test_georisques.py
│   │   └── test_paris_rent.py
│   ├── parsers/
│   │   ├── test_listing.py
│   │   └── test_risks.py
│   └── api/
│       ├── test_routes.py
│       └── test_websocket.py
└── conftest.py                   # Pytest fixtures
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: PydanticAI Patterns
# 1. DON'T use result_type unless structured output is needed - default to string
# Example from main_agent_reference:
research_agent = Agent(
    get_llm_model(),
    deps_type=ResearchAgentDependencies,  # NO result_type!
    system_prompt=SYSTEM_PROMPT
)

# 2. Tool context access with RunContext[DepsType]
@agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str
) -> List[Dict[str, Any]]:
    return await search_web_tool(
        api_key=ctx.deps.brave_api_key,  # Access deps via ctx.deps
        query=query
    )

# 3. Sub-agent invocation from tool - pass usage for token tracking
@research_agent.tool
async def create_email_draft(
    ctx: RunContext[ResearchAgentDependencies],
    recipient: str,
    subject: str
) -> Dict[str, Any]:
    email_deps = EmailAgentDependencies(...)
    result = await email_agent.run(
        prompt,
        deps=email_deps,
        usage=ctx.usage  # CRITICAL: Pass usage for tracking
    )
    return {"success": True, "agent_response": result.data}

# CRITICAL: FastAPI + WebSocket
# 1. WebSocket connections must be async
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process and send updates
            await websocket.send_json({"status": "processing"})
    except WebSocketDisconnect:
        pass

# 2. Broadcast to multiple clients - maintain connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

# CRITICAL: Financial Calculations
# 1. IRR requires numpy-financial or scipy
import numpy_financial as npf
irr = npf.irr(cash_flows)  # cash_flows = [CF0, CF1, ..., CFn]

# 2. Monthly mortgage payment formula
def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    return principal * (monthly_rate / (1 - (1 + monthly_rate) ** -num_payments))

# 3. DSCR = NOI / ADS (must be > 1.0 for positive cash flow)
dscr = noi / annual_debt_service
if dscr < 1.0:
    # Cash flow negative - property loses money

# CRITICAL: API Rate Limits
# 1. Brave Search: 2,000/month free tier, handle 429
if response.status_code == 429:
    raise Exception("Rate limit exceeded. Check your Brave API quota.")

# 2. DVF API: No strict limits but batch requests for comps
# 3. Géorisques: Public API, be respectful with request frequency
# 4. Gmail API: 100 quota units per send, 5 per draft create

# CRITICAL: Parser Gotcha - Use Playwright MCP for HTML parsing
# The examples show PDFs but actual data is in HTML
# Use Playwright to fetch and parse listing pages
from playwright.async_api import async_playwright
async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto(listing_url)
    # Extract data from HTML

# CRITICAL: Paris Rent Control
# 1. Data updated July 1st annually - cache but refresh yearly
# 2. Query by: quartier_id, number_rooms, construction_period, furnished/unfurnished
# 3. Returns: loyer_reference, loyer_majore (ceiling), in EUR/m²
# 4. Legal max = (ceiling * surface) + complément_de_loyer (if justified)

# CRITICAL: Environment Variables with python-dotenv
# MUST call load_dotenv() at module level before Settings instantiation
from dotenv import load_dotenv
load_dotenv()  # Load .env file

# Then create Settings
from pydantic_settings import BaseSettings
settings = Settings()

# CRITICAL: Testing with PydanticAI
# Use TestModel for fast validation without API calls
from pydantic_ai.models.test import TestModel
test_agent = agent.override(model=TestModel())

# Use FunctionModel for custom test behavior
from pydantic_ai.models.function import FunctionModel
def custom_call_function(messages, info):
    return "Test response"
test_model = FunctionModel(custom_call_function)

# CRITICAL: Async/Sync Mixing
# PydanticAI tools can be async or sync, but prefer async for I/O
# Don't mix: use asyncio.run() for sync contexts calling async code
import asyncio
result = asyncio.run(agent.run("query", deps=deps))
```

---

## Implementation Blueprint

### Data Models and Structure

Create core Pydantic models for type safety and consistency:

```python
# backend/models/property.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Address(BaseModel):
    """Property address."""
    street: str
    city: str = "Paris"
    postal_code: str = Field(..., pattern=r"^\d{5}$")
    quartier: Optional[str] = None

class Property(BaseModel):
    """Property details."""
    address: Address
    price: float = Field(..., gt=0)
    surface: float = Field(..., gt=0, description="Living surface in m²")
    rooms: int = Field(..., ge=1)
    bedrooms: int = Field(..., ge=0)
    construction_year: Optional[int] = None
    dpe: Optional[str] = Field(None, pattern=r"^[A-G]$")
    furnished: bool = False

# backend/models/financial.py
class FinancialInputs(BaseModel):
    """User financial inputs for analysis."""
    down_payment: float = Field(..., ge=0)
    loan_amount: float = Field(..., ge=0)
    annual_interest_rate: float = Field(..., ge=0, le=1)
    loan_term_years: int = Field(..., ge=1, le=30)
    monthly_rent: Optional[float] = Field(None, ge=0)
    vacancy_rate: float = Field(0.05, ge=0, le=1)
    operating_expenses: float = Field(..., ge=0)
    holding_period_years: int = Field(10, ge=1, le=30)

class CashFlow(BaseModel):
    """Annual cash flow breakdown."""
    year: int
    rental_income: float
    vacancy_loss: float
    operating_expenses: float
    debt_service: float
    pre_tax_cash_flow: float
    taxes: float
    after_tax_cash_flow: float
    cumulative_cash_flow: float

class Verdict(BaseModel):
    """60-second verdict output."""
    buy_pass: str = Field(..., description="BUY or PASS")
    dscr: float = Field(..., description="Debt Service Coverage Ratio")
    irr: float = Field(..., description="Internal Rate of Return")
    tmc: float = Field(..., description="Total Monthly Cost")
    price_verdict: str = Field(..., description="Under-priced / Average / Overpriced")
    legal_rent_status: str = Field(..., description="Conformant – Low / High / Non-conformant")
    strategy_fits: List[StrategyFit]
    cash_flows: List[CashFlow]
    environmental_risk_summary: str
    crime_risk_score: float = Field(..., ge=0, le=100)

class StrategyFit(BaseModel):
    """Strategy fit score (0-100) with reasons."""
    strategy: str = Field(..., description="Owner-occupier / Location nue / LMNP / Colocation / Value-Add")
    score: float = Field(..., ge=0, le=100)
    reasons: List[str]
    pros: List[str]
    cons: List[str]
```

### List of Tasks to Complete (Ordered)

```yaml
Task 1: Environment Setup
MODIFY .env.example:
  - ADD all required API keys: LLM_API_KEY, BRAVE_API_KEY, GMAIL_CREDENTIALS_PATH, etc.
  - ADD database connection if using SQLAlchemy

CREATE backend/agents/settings.py:
  - MIRROR pattern from: use-cases/pydantic-ai/examples/main_agent_reference/settings.py
  - INCLUDE: load_dotenv() at module level
  - DEFINE Settings class with all API keys
  - ADD field validators for non-empty keys

CREATE backend/agents/providers.py:
  - DEFINE get_llm_model() function
  - SUPPORT multiple providers (OpenAI, Anthropic)
  - USE settings.py for configuration

Task 2: Financial Calculations Module
CREATE backend/calculations/financial.py:
  - IMPLEMENT noi_calculation(gmi, vcl, oe) -> float
  - IMPLEMENT cap_rate(noi, price) -> float
  - IMPLEMENT cash_on_cash(annual_cash_flow, initial_cash) -> float
  - INCLUDE comprehensive docstrings with formulas

CREATE backend/calculations/mortgage.py:
  - IMPLEMENT monthly_payment(principal, rate, years) -> float
  - IMPLEMENT amortization_schedule(principal, rate, years) -> List[Dict]
  - USE formula: M = P × (i / (1 - (1 + i)^-n))

CREATE backend/calculations/taxes.py:
  - IMPLEMENT lmnp_micro_bic_tax(gross_rent, abatement_rate, marginal_rate) -> float
  - IMPLEMENT location_nue_micro_foncier_tax(gross_rent, flat_abatement, rate) -> float
  - IMPLEMENT after_tax_margin(pre_tax_cf, income_tax, social_charges) -> float

CREATE backend/calculations/irr_npv.py:
  - IMPLEMENT irr_calculation(cash_flows: List[float]) -> float
  - USE numpy-financial: npf.irr(cash_flows)
  - IMPLEMENT npv_calculation(cash_flows, discount_rate) -> float
  - HANDLE edge cases: all positive/negative flows

CREATE backend/calculations/valuation.py:
  - IMPLEMENT nowcast_value(dvf_median, market_delta, listing_delta) -> float
  - IMPLEMENT price_verdict(property_price, nowcast_value) -> str
  - RETURN: "Under-priced" if < 95%, "Average" if 95-105%, "Overpriced" if > 105%

CREATE backend/calculations/strategy_fit.py:
  - IMPLEMENT calculate_fit_scores(property, financials, legal_status) -> List[StrategyFit]
  - DEFINE weights for each strategy profile
  - COMPUTE normalized scores based on DSCR, IRR, TMC, bedrooms, discount
  - SORT by score descending

Task 3: External API Integration Clients
CREATE backend/integrations/brave.py:
  - MIRROR: use-cases/pydantic-ai/examples/main_agent_reference/tools.py lines 18-121
  - IMPLEMENT search_web(api_key, query, count) -> List[Dict]
  - HANDLE rate limits (429), auth errors (401)
  - USE httpx.AsyncClient for async requests

CREATE backend/integrations/dvf.py:
  - IMPLEMENT fetch_dvf_comps(address, radius_km, min_date) -> List[Dict]
  - QUERY: https://api.gouv.fr/les-api/api-donnees-foncieres
  - PARSE: property type, sale date, price, surface
  - CALCULATE: median price/m² for comps

CREATE backend/integrations/georisques.py:
  - IMPLEMENT fetch_environmental_risks(postal_code, address) -> Dict
  - QUERY: https://www.georisques.gouv.fr/doc-api
  - RETURN: {natural_risks: [...], technological_risks: [...], address_level_flags: [...]}
  - PARSE: flood, groundwater, seismicity, clay, radon, ICPE, pipelines

CREATE backend/integrations/paris_rent.py:
  - IMPLEMENT fetch_rent_cap(quartier, rooms, construction_period, furnished) -> Dict
  - QUERY: https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/api/
  - RETURN: {reference_rent_eur_m2: float, ceiling_rent_eur_m2: float}
  - CACHE: Data updated July 1st - cache for 1 year

CREATE backend/integrations/crime_data.py:
  - IMPLEMENT fetch_crime_stats(postal_code) -> Dict
  - QUERY: French open data for crime rates
  - COMPUTE: normalized crime score 0-100 using percentile scaling
  - RETURN: {score: float, categories: {burglary: float, theft: float, ...}}

CREATE backend/integrations/gmail.py:
  - IMPLEMENT create_draft(credentials_path, token_path, to, subject, body) -> str
  - USE: google-auth, google-api-python-client
  - CREATE: MIME message, base64url encode
  - CALL: service.users().drafts().create(userId='me', body={...})
  - RETURN: draft_id

Task 4: Parsers for Listings and Risk Reports
CREATE backend/parsers/listing.py:
  - IMPLEMENT parse_listing_html(url: str) -> Property
  - USE: Playwright MCP server for fetching HTML
  - EXTRACT: address, price, surface, rooms, bedrooms, DPE
  - HANDLE: Missing fields with Optional types
  - RAISE: ParseError if critical fields missing

CREATE backend/parsers/risks.py:
  - IMPLEMENT parse_georisques_html(html: str) -> Dict
  - EXTRACT: risk categories, status, address vs commune level
  - RETURN: Structured dict matching EnvironmentalRisk model

Task 5: Research Agent with Tools
CREATE backend/agents/research/models.py:
  - DEFINE: ListingData, DVFComp, RiskSummary, ResearchResult models
  - USE: Pydantic with Field descriptions

CREATE backend/agents/research/tools.py:
  - IMPLEMENT: search_listings(query, max_results) -> List[Dict]
  - IMPLEMENT: fetch_dvf_comps_tool(address, radius) -> List[DVFComp]
  - IMPLEMENT: check_rent_cap_tool(address, property) -> Dict
  - IMPLEMENT: fetch_env_risks_tool(address) -> RiskSummary
  - ALL pure async functions (no ctx parameter)

CREATE backend/agents/research/prompts.py:
  - DEFINE: RESEARCH_SYSTEM_PROMPT with instructions
  - INCLUDE: "Normalize listing facts, fetch DVF comps, check zone tendue, prepare typed payloads"

CREATE backend/agents/research/agent.py:
  - IMPORT: Agent, RunContext from pydantic_ai
  - DEFINE: ResearchAgentDependencies dataclass
  - CREATE: research_agent = Agent(get_llm_model(), deps_type=..., system_prompt=...)
  - REGISTER: @research_agent.tool decorators for each tool in tools.py
  - INJECT: API keys from ctx.deps into pure tool functions

Task 6: Negotiation Agent with Gmail Tool
CREATE backend/agents/negotiation/models.py:
  - DEFINE: EmailDraft, NegotiationPack models

CREATE backend/agents/negotiation/tools.py:
  - IMPLEMENT: create_gmail_draft_tool(credentials, token, to, subject, body) -> str
  - CALL: backend/integrations/gmail.py create_draft()

CREATE backend/agents/negotiation/prompts.py:
  - DEFINE: NEGOTIATION_SYSTEM_PROMPT
  - INCLUDE: "Draft professional email with comps, legal-rent status, DSCR/IRR, capital alternative, clear ask"

CREATE backend/agents/negotiation/agent.py:
  - DEFINE: NegotiationAgentDependencies
  - CREATE: negotiation_agent with @agent.tool for create_gmail_draft

Task 7: Primary Deal Evaluator Agent
CREATE backend/agents/deal_evaluator/models.py:
  - DEFINE: Verdict, StrategyFit, EvaluationResult models
  - INCLUDE: All verdict fields from INITIAL.md

CREATE backend/agents/deal_evaluator/tools.py:
  - IMPLEMENT: invoke_research_agent(ctx, property_details) -> ResearchResult
  - IMPLEMENT: invoke_negotiation_agent(ctx, research_data, verdict) -> str
  - CALL: research_agent.run(prompt, deps=..., usage=ctx.usage)
  - CALL: negotiation_agent.run(prompt, deps=..., usage=ctx.usage)

CREATE backend/agents/deal_evaluator/prompts.py:
  - DEFINE: EVALUATOR_SYSTEM_PROMPT
  - INCLUDE: "Return 60-second Buy/Pass verdict using deterministic math. No AI heuristics in calculations."

CREATE backend/agents/deal_evaluator/agent.py:
  - DEFINE: DealEvaluatorDependencies
  - CREATE: deal_evaluator_agent with tools
  - COMPUTE: All financial metrics using backend/calculations modules
  - RETURN: Verdict with unified badges (green/amber/red)

Task 8: FastAPI Backend with WebSocket
CREATE backend/api/main.py:
  - SETUP: FastAPI app with CORS middleware
  - MOUNT: static files for frontend
  - INCLUDE: routers from routes/

CREATE backend/api/routes/evaluate.py:
  - DEFINE: POST /api/evaluate endpoint
  - ACCEPT: EvaluationRequest (property + financial inputs)
  - CALL: deal_evaluator_agent.run()
  - RETURN: Verdict JSON

CREATE backend/api/routes/research.py:
  - DEFINE: POST /api/research endpoint
  - CALL: research_agent.run()
  - RETURN: ResearchResult JSON

CREATE backend/api/routes/negotiate.py:
  - DEFINE: POST /api/negotiate endpoint
  - CALL: negotiation_agent.run()
  - RETURN: EmailDraft JSON

CREATE backend/api/routes/websocket.py:
  - DEFINE: WebSocket /ws endpoint
  - IMPLEMENT: ConnectionManager for broadcast
  - STREAM: Real-time evaluation progress updates
  - SEND: JSON messages with status, progress percentage, current step

Task 9: CLI Interface with Typer
CREATE backend/cli/main.py:
  - USE: typer library for CLI
  - DEFINE: evaluate(property_address, price, ...) command
  - DEFINE: research(property_address) command
  - DEFINE: negotiate(property_address, --draft) command
  - CALL: Agent.run_sync() for synchronous CLI execution
  - DISPLAY: Results with rich console formatting

Task 10: Frontend React Application
CREATE frontend/src/components/Layout/ThreeColumnLayout.jsx:
  - SETUP: 3-column grid layout (responsive)
  - LEFT: 25% width - chat + inputs
  - MIDDLE: 50% width - dashboard
  - RIGHT: 25% width - verdicts

CREATE frontend/src/components/LeftColumn/ChatInterface.jsx:
  - IMPLEMENT: Chat UI with message history
  - CONNECT: WebSocket for real-time agent responses
  - DISPLAY: Tool calls and streaming text

CREATE frontend/src/components/LeftColumn/PropertyInput.jsx:
  - IMPLEMENT: Form with address, price, surface, rooms, etc.
  - VALIDATE: Input fields
  - SUBMIT: POST /api/evaluate

CREATE frontend/src/components/MiddleColumn/Dashboard.jsx:
  - DISPLAY: Financial metrics cards (DSCR, IRR, Cap Rate, CoC, NPV)
  - INCLUDE: CashFlowChart and CashFlowTable

CREATE frontend/src/components/MiddleColumn/CashFlowChart.jsx:
  - USE: Chart.js or react-financial-charts
  - PLOT: Annual bars (income, expenses, cash flow) + cumulative line
  - ENABLE: Zoom and hover tooltips

CREATE frontend/src/components/MiddleColumn/CashFlowTable.jsx:
  - RENDER: Year-by-year table with all CashFlow fields
  - MAKE: Expandable sections

CREATE frontend/src/components/RightColumn/VerdictPanel.jsx:
  - DISPLAY: Price verdict badges (Under-priced / Average / Overpriced)
  - COLOR: Green / Amber / Red

CREATE frontend/src/components/RightColumn/LegalRentCheck.jsx:
  - DISPLAY: Legal rent status badges
  - SHOW: Reference rent, ceiling, property rent

CREATE frontend/src/components/RightColumn/StrategyFitCards.jsx:
  - RENDER: Top 3 strategy fit cards
  - SHOW: Score (0-100), pros, cons, reason codes

CREATE frontend/src/services/api.js:
  - IMPLEMENT: API client with axios/fetch
  - DEFINE: evaluateProperty(data), researchProperty(data), negotiateDraft(data)

CREATE frontend/src/services/websocket.js:
  - IMPLEMENT: WebSocket connection manager
  - HANDLE: Connection, disconnection, message parsing
  - EMIT: Events for React components

CREATE frontend/src/hooks/useWebSocket.js:
  - IMPLEMENT: Custom hook for WebSocket connection
  - MANAGE: Connection state, messages

CREATE frontend/src/hooks/useEvaluation.js:
  - IMPLEMENT: Custom hook for evaluation state
  - CALL: API and manage loading/error states

Task 11: Testing - Unit Tests
CREATE tests/backend/calculations/test_financial.py:
  - TEST: noi_calculation with expected inputs
  - TEST: cap_rate edge cases (zero price)
  - TEST: cash_on_cash with negative cash flow

CREATE tests/backend/calculations/test_irr_npv.py:
  - TEST: irr_calculation with known cash flows
  - TEST: npv_calculation with discount rate
  - TEST: Edge cases (all positive, all negative flows)

CREATE tests/backend/integrations/test_brave.py:
  - MOCK: httpx responses
  - TEST: search_web success case
  - TEST: Rate limit handling (429)
  - TEST: Auth error (401)

CREATE tests/backend/integrations/test_dvf.py:
  - MOCK: DVF API responses
  - TEST: fetch_dvf_comps returns comps
  - TEST: Median calculation

CREATE tests/backend/agents/test_deal_evaluator.py:
  - USE: TestModel from pydantic_ai.models.test
  - TEST: Agent runs with mock dependencies
  - TEST: Tool invocations
  - TEST: Verdict structure

CREATE tests/backend/agents/test_research.py:
  - USE: TestModel
  - TEST: Research agent with mocked API calls
  - TEST: Listing parsing

CREATE tests/backend/api/test_routes.py:
  - USE: FastAPI TestClient
  - TEST: POST /api/evaluate returns 200
  - TEST: POST /api/research returns 200
  - TEST: Invalid input returns 422

CREATE tests/conftest.py:
  - DEFINE: Fixtures for settings, agents, API clients
  - MOCK: External API responses

Task 12: Integration Tests
CREATE tests/backend/test_end_to_end.py:
  - TEST: Full evaluation flow (property input → verdict)
  - USE: Real agents with TestModel
  - VERIFY: All calculations match expected values

Task 13: Documentation and Final Setup
CREATE README.md:
  - INCLUDE: Setup instructions (venv, dependencies, .env)
  - INCLUDE: Project structure
  - INCLUDE: Web server launch: python -m uvicorn backend.api.main:app --reload
  - INCLUDE: CLI usage examples
  - INCLUDE: Browser access: http://localhost:8000
  - INCLUDE: Gmail and Brave API configuration

CREATE .env.example:
  - LIST: All required environment variables
  - INCLUDE: LLM_API_KEY, BRAVE_API_KEY, GMAIL_CREDENTIALS_PATH, GMAIL_TOKEN_PATH

UPDATE TASK.md:
  - MARK: All tasks completed
  - ADD: Any discovered sub-tasks
```

---

## Validation Loop

### Level 1: Syntax & Style
```bash
# Activate venv first
source venv/bin/activate  # Linux/Mac
# OR: venv\Scripts\activate  # Windows

# Run linting and type checking
ruff check backend/ --fix
mypy backend/

# Expected: No errors. If errors, READ and fix before proceeding.
```

### Level 2: Unit Tests
```bash
# Run all unit tests with coverage
pytest tests/backend/ -v --cov=backend --cov-report=term-missing

# Expected: >80% coverage, all tests pass
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Tests
```bash
# Run integration tests (requires .env with test API keys or mocks)
pytest tests/backend/test_end_to_end.py -v

# Expected: Full evaluation flow completes successfully
```

### Level 4: Manual Web UI Test
```bash
# Start backend server
python -m uvicorn backend.api.main:app --reload

# In browser, navigate to: http://localhost:8000
# Test:
# 1. Enter property details in left column
# 2. Click "Evaluate"
# 3. Verify real-time updates via WebSocket
# 4. Check verdict badges in right column
# 5. Verify cash-flow chart renders in middle column

# Expected: UI displays all results correctly
```

### Level 5: CLI Test
```bash
# Test CLI commands
python -m backend.cli.main evaluate \
  --address "10 Rue de Rivoli, 75001 Paris" \
  --price 500000 \
  --surface 50 \
  --rooms 2 \
  --down-payment 100000 \
  --loan-amount 400000 \
  --annual-rate 0.03 \
  --loan-term 20

# Expected: Prints verdict with DSCR, IRR, price verdict, legal rent status
```

### Level 6: Playwright Test (Listing Parser)
```bash
# Use Playwright MCP to test listing parser
# (Already configured from user setup: claude mcp add playwright)

# Test parsing example listing
python -c "
import asyncio
from backend.parsers.listing import parse_listing_html
result = asyncio.run(parse_listing_html('https://example-listing.com'))
print(result)
"

# Expected: Returns Property object with extracted fields
```

---

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check backend/`
- [ ] No type errors: `mypy backend/`
- [ ] Web UI launches and displays verdicts correctly
- [ ] CLI commands work (`evaluate`, `research`, `negotiate`)
- [ ] WebSocket streams real-time updates
- [ ] Agents invoke sub-agents correctly
- [ ] Financial calculations are deterministic (no AI in math)
- [ ] Strategy fit scores computed and sorted
- [ ] Gmail drafts created successfully
- [ ] Environmental risks fetched and displayed
- [ ] Paris rent control checked accurately
- [ ] DVF comps fetched and used in valuation
- [ ] Logs are informative but not verbose
- [ ] README.md includes all setup steps

---

## Anti-Patterns to Avoid
- ❌ Don't use result_type unless structured output needed (PydanticAI default is string)
- ❌ Don't skip agent testing with TestModel before using real models
- ❌ Don't hardcode API keys - always use .env with load_dotenv()
- ❌ Don't create agents without deps_type - use dataclasses for dependencies
- ❌ Don't forget to pass usage=ctx.usage when invoking sub-agents from tools
- ❌ Don't mix sync/async - use asyncio.run() for CLI, keep agents async
- ❌ Don't use AI heuristics for financial calculations - must be deterministic
- ❌ Don't create files >500 lines - split into modules
- ❌ Don't skip input validation - use Pydantic models for all inputs
- ❌ Don't ignore API rate limits - handle 429 gracefully
- ❌ Don't commit .env files to git - only commit .env.example
- ❌ Don't use echo/cat in bash for communication - output text directly

---

## PRP Confidence Score: 9/10

**Strengths:**
- Comprehensive context from official documentation (PydanticAI, FastAPI, APIs)
- Clear implementation blueprint with ordered tasks
- Reference patterns from existing codebase (main_agent_reference)
- Detailed financial formulas from INITIAL.md
- Multiple validation gates (unit, integration, manual)
- All required technologies researched (2025 updates)

**Minor Gaps:**
- Frontend implementation details are less comprehensive than backend
- Some API endpoints (crime data) may require additional research for exact URLs
- Playwright MCP integration for parsing needs testing in practice

**Overall:** This PRP provides sufficient context for one-pass implementation with high confidence. The agent should be able to build the complete system with iterative refinement using the validation loops.