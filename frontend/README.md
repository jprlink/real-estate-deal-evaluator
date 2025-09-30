# Real Estate Deal Evaluator - Frontend

Modern React-based frontend for the Paris Real Estate Investment Analyzer.

## Features

- **3-Column Responsive Layout**
  - Left: AI Chat + Property Input Form
  - Middle: Analytics Dashboard with Charts
  - Right: Verdicts & Strategy Fits

- **Real-time Analysis**
  - Instant property evaluation
  - Interactive charts (Chart.js)
  - Live financial metrics

- **Modern UI/UX**
  - Tailwind CSS styling
  - Lucide React icons
  - Smooth animations and transitions

## Setup

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm start
```

Runs the app in development mode at [http://localhost:3000](http://localhost:3000).

The page will reload when you make changes.

### Build for Production

```bash
npm run build
```

Builds the app for production to the `build` folder.

## Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Project Structure

```
frontend/
├── public/             # Static files
├── src/
│   ├── components/     # React components
│   │   ├── Header.jsx
│   │   ├── LeftPanel.jsx
│   │   ├── MiddlePanel.jsx
│   │   ├── RightPanel.jsx
│   │   ├── PropertyInputForm.jsx
│   │   └── ChatMessage.jsx
│   ├── services/       # API services
│   │   └── api.js
│   ├── App.js          # Main app component
│   ├── index.js        # Entry point
│   └── index.css       # Global styles
├── package.json
└── tailwind.config.js
```

## Technologies

- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icons