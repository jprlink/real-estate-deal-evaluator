import React, { useState } from 'react';
import Header from './components/Header';
import LeftPanel from './components/LeftPanel';
import MiddlePanel from './components/MiddlePanel';
import RightPanel from './components/RightPanel';
import { evaluateProperty } from './services/api';

function App() {
  const [propertyData, setPropertyData] = useState(null);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [parsedData, setParsedData] = useState(null);
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Bonjour! I\'m your AI real estate analyst. Tell me about a property you\'d like to evaluate in Paris.',
      timestamp: new Date()
    }
  ]);

  const handlePropertySubmit = async (data) => {
    setLoading(true);
    setPropertyData(data);

    // Add user message to chat
    setChatMessages(prev => [...prev, {
      id: Date.now(),
      role: 'user',
      content: `Evaluating property at ${data.address}, €${data.price.toLocaleString()}, ${data.surface}m², ${data.rooms} rooms`,
      timestamp: new Date()
    }]);

    try {
      const result = await evaluateProperty(data);
      setEvaluationResult(result);

      // Add assistant response to chat
      setChatMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Analysis complete! DSCR: ${result.metrics.dscr.toFixed(2)}, IRR: ${(result.metrics.irr * 100).toFixed(1)}%. Verdict: ${result.verdict}`,
        timestamp: new Date()
      }]);
    } catch (err) {
      console.error('Evaluation error:', err);
      setChatMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error analyzing this property. Please check your inputs and try again.',
        timestamp: new Date()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleChatMessage = async (message) => {
    // Add user message
    setChatMessages(prev => [...prev, {
      id: Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date()
    }]);

    // Simulate AI response (replace with actual agent call)
    setTimeout(() => {
      setChatMessages(prev => [...prev, {
        id: Date.now(),
        role: 'assistant',
        content: 'I can help you analyze properties in Paris. Please fill out the property details form on the left to get started.',
        timestamp: new Date()
      }]);
    }, 1000);
  };

  const handleParsedData = (data) => {
    setParsedData(data);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
          {/* Left Panel: Chat + Input */}
          <div className="col-span-3 flex flex-col space-y-4">
            <LeftPanel
              onPropertySubmit={handlePropertySubmit}
              loading={loading}
              chatMessages={chatMessages}
              onChatMessage={handleChatMessage}
              onParsedData={handleParsedData}
            />
          </div>

          {/* Middle Panel: Analytics Dashboard */}
          <div className="col-span-6 overflow-y-auto">
            <MiddlePanel
              evaluationResult={evaluationResult}
              propertyData={propertyData}
              loading={loading}
            />
          </div>

          {/* Right Panel: Verdicts */}
          <div className="col-span-3 overflow-y-auto">
            <RightPanel
              evaluationResult={evaluationResult}
              loading={loading}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;