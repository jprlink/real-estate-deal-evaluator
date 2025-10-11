import React, { useState } from 'react';
import Header from './components/Header';
import LeftPanel from './components/LeftPanel';
import MiddlePanel from './components/MiddlePanel';
import RightPanel from './components/RightPanel';
import { evaluateProperty } from './services/api';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

function App() {
  const [propertyData, setPropertyData] = useState(null);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [parsedData, setParsedData] = useState(null);
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Bonjour! I\'m your AI real estate analyst. Tell me about a property you\'d like to evaluate anywhere in France.',
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
        content: 'I can help you analyze properties anywhere in France. Please fill out the property details form on the left to get started.',
        timestamp: new Date()
      }]);
    }, 1000);
  };

  const handleParsedData = (data) => {
    setParsedData(data);
  };

  const handleExportReport = () => {
    if (!evaluationResult || !propertyData) {
      alert('Please analyze a property before exporting the report.');
      return;
    }

    // Create PDF document
    const doc = new jsPDF();
    let yPos = 20;

    // Helper function to check if we need a new page
    const checkPageBreak = (neededSpace) => {
      if (yPos + neededSpace > 280) {
        doc.addPage();
        yPos = 20;
        return true;
      }
      return false;
    };

    // Title
    doc.setFontSize(18);
    doc.setFont(undefined, 'bold');
    doc.text('France Real Estate Investment Analysis Report', 105, yPos, { align: 'center' });
    yPos += 8;
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');
    doc.text(`Generated: ${new Date().toLocaleString()}`, 105, yPos, { align: 'center' });
    yPos += 15;

    // Property Details Section
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('PROPERTY DETAILS', 14, yPos);
    yPos += 7;
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');

    const propertyDetails = [
      ['Address', propertyData.address],
      ['Postal Code', propertyData.postal_code],
      ...(evaluationResult.city ? [['Location', evaluationResult.city]] : []),
      ['Price', `€${propertyData.price.toLocaleString()}`],
      ['Surface', `${propertyData.surface} m²`],
      ['Price per m²', `€${evaluationResult.metrics.price_per_m2.toFixed(0)}`],
      ['Rooms', propertyData.rooms.toString()],
      ['Bedrooms', propertyData.bedrooms.toString()],
      ...(propertyData.dpe ? [['DPE', propertyData.dpe]] : [])
    ];

    doc.autoTable({
      startY: yPos,
      head: [],
      body: propertyDetails,
      theme: 'grid',
      headStyles: { fillColor: [14, 165, 233] },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 60 }, 1: { cellWidth: 120 } },
      margin: { left: 14 }
    });
    yPos = doc.lastAutoTable.finalY + 10;

    // Financing Section
    checkPageBreak(60);
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('FINANCING', 14, yPos);
    yPos += 7;
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');

    const financingDetails = [
      ['Down Payment', `€${propertyData.down_payment.toLocaleString()}`],
      ['Loan Amount', `€${propertyData.loan_amount.toLocaleString()}`],
      ['Interest Rate', `${(propertyData.annual_rate * 100).toFixed(2)}%`],
      ['Loan Term', `${propertyData.loan_term} years`],
      ['Monthly Mortgage Payment', `€${evaluationResult.metrics.monthly_payment.toFixed(0)}`],
      ['LTV Ratio', `${(evaluationResult.metrics.ltv * 100).toFixed(0)}%`],
      ...(propertyData.renovation_costs && propertyData.renovation_costs > 0 ? [['Renovation Costs', `€${propertyData.renovation_costs.toLocaleString()}`]] : [])
    ];

    doc.autoTable({
      startY: yPos,
      body: financingDetails,
      theme: 'grid',
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 60 }, 1: { cellWidth: 120 } },
      margin: { left: 14 }
    });
    yPos = doc.lastAutoTable.finalY + 10;

    // Investment Analysis Section
    checkPageBreak(60);
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('INVESTMENT ANALYSIS', 14, yPos);
    yPos += 7;

    const verdictColor = evaluationResult.verdict === 'BUY' ? [34, 197, 94] :
                         evaluationResult.verdict === 'CAUTION' ? [234, 179, 8] : [239, 68, 68];

    doc.autoTable({
      startY: yPos,
      body: [
        ['Investment Verdict', evaluationResult.verdict],
        ['Price Verdict', evaluationResult.price_verdict],
        ['Legal Rent Status', evaluationResult.legal_rent_status]
      ],
      theme: 'grid',
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 60 }, 1: { cellWidth: 120 } },
      margin: { left: 14 },
      didParseCell: (data) => {
        if (data.row.index === 0 && data.column.index === 1) {
          data.cell.styles.textColor = verdictColor;
          data.cell.styles.fontStyle = 'bold';
        }
      }
    });
    yPos = doc.lastAutoTable.finalY + 10;

    // Financial Metrics Section
    checkPageBreak(80);
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('FINANCIAL METRICS', 14, yPos);
    yPos += 7;

    const metricsData = [
      ['Monthly Rent', `€${propertyData.monthly_rent.toLocaleString()}`],
      ['NOI (Annual)', `€${evaluationResult.metrics.noi.toFixed(0)}`],
      ['DSCR', evaluationResult.metrics.dscr.toFixed(2)],
      ['Cap Rate', `${(evaluationResult.metrics.cap_rate * 100).toFixed(2)}%`],
      ['Cash-on-Cash Return', `${(evaluationResult.metrics.cash_on_cash * 100).toFixed(2)}%`],
      ['IRR', `${(evaluationResult.metrics.irr * 100).toFixed(2)}%`],
      ...(evaluationResult.metrics.appreciation_rate_display ? [['Property Appreciation', evaluationResult.metrics.appreciation_rate_display]] : [])
    ];

    doc.autoTable({
      startY: yPos,
      body: metricsData,
      theme: 'grid',
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 60 }, 1: { cellWidth: 120 } },
      margin: { left: 14 }
    });
    yPos = doc.lastAutoTable.finalY + 10;

    // Rent Band Information
    if (evaluationResult.rent_band) {
      checkPageBreak(60);
      const rb = evaluationResult.rent_band;
      doc.setFontSize(14);
      doc.setFont(undefined, 'bold');
      doc.text('RENT ANALYSIS', 14, yPos);
      yPos += 7;

      doc.autoTable({
        startY: yPos,
        body: [
          ['Type', rb.is_estimate ? 'Market Estimate' : 'Legal Rent Control'],
          ['Property Rent per m²', `€${rb.property_rent_per_m2.toFixed(2)}`],
          [`${rb.is_estimate ? 'Typical' : 'Legal'} Min`, `€${rb.min_rent.toFixed(2)}/m²`],
          ['Median', `€${rb.median_rent.toFixed(2)}/m²`],
          [`${rb.is_estimate ? 'Typical' : 'Legal'} Max`, `€${rb.max_rent.toFixed(2)}/m²`],
          ['Compliant', rb.is_compliant ? 'Yes' : 'No']
        ],
        theme: 'grid',
        columnStyles: { 0: { fontStyle: 'bold', cellWidth: 60 }, 1: { cellWidth: 120 } },
        margin: { left: 14 }
      });
      yPos = doc.lastAutoTable.finalY + 10;
    }

    // Strategy Fits
    if (evaluationResult.strategy_fits && evaluationResult.strategy_fits.length > 0) {
      checkPageBreak(80);
      doc.setFontSize(14);
      doc.setFont(undefined, 'bold');
      doc.text('TOP INVESTMENT STRATEGIES', 14, yPos);
      yPos += 7;

      evaluationResult.strategy_fits.forEach((strategy, index) => {
        checkPageBreak(25);
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.text(`${index + 1}. ${strategy.strategy} (Score: ${strategy.score.toFixed(0)})`, 14, yPos);
        yPos += 5;
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text(`Pros: ${strategy.pros.join('; ')}`, 20, yPos, { maxWidth: 170 });
        yPos += 5;
        doc.text(`Cons: ${strategy.cons.join('; ')}`, 20, yPos, { maxWidth: 170 });
        yPos += 8;
      });
    }

    // Costs at Purchase Section
    const year0 = evaluationResult.cash_flow_projections?.find(cf => cf.year === 0);
    if (year0) {
      checkPageBreak(60);
      doc.setFontSize(14);
      doc.setFont(undefined, 'bold');
      doc.text('COSTS AT PURCHASE', 14, yPos);
      yPos += 7;

      const purchaseCosts = [
        ['Down Payment', `€${propertyData.down_payment.toLocaleString()}`],
        ...(propertyData.renovation_costs > 0 ? [['Renovation Costs', `€${propertyData.renovation_costs.toLocaleString()}`]] : []),
        ['Notary Fees (7.5%)', `€${Math.round(propertyData.price * 0.075).toLocaleString()}`],
        ['Total Cash Required', `€${Math.abs(year0.cash_flow).toLocaleString()}`]
      ];

      doc.autoTable({
        startY: yPos,
        body: purchaseCosts,
        theme: 'grid',
        columnStyles: { 0: { fontStyle: 'bold', cellWidth: 60 }, 1: { cellWidth: 120 } },
        margin: { left: 14 }
      });
      yPos = doc.lastAutoTable.finalY + 10;
    }

    // Cash Flow Projections (excluding Year 0)
    const displayCashFlow = evaluationResult.cash_flow_projections?.filter(cf => cf.year !== 0) || [];
    if (displayCashFlow.length > 0) {
      doc.addPage();
      yPos = 20;
      doc.setFontSize(14);
      doc.setFont(undefined, 'bold');
      doc.text(`CASH FLOW PROJECTION (${propertyData.projection_years} YEARS)`, 14, yPos);
      yPos += 5;
      doc.setFontSize(8);
      doc.setFont(undefined, 'italic');
      doc.text('Assumptions: 5% vacancy rate, 25% operating expenses, 7.5% notary fees', 14, yPos);
      yPos += 7;

      const cashFlowData = displayCashFlow.map(cf => [
        cf.year,
        `€${Math.round(cf.rental_income).toLocaleString()}`,
        `€${Math.round(cf.vacancy_loss).toLocaleString()}`,
        `€${Math.round(cf.operating_expenses).toLocaleString()}`,
        `€${Math.round(cf.mortgage_payment).toLocaleString()}`,
        `€${Math.round(cf.cash_flow).toLocaleString()}`,
        `€${Math.round(cf.cumulative_cash_flow).toLocaleString()}`,
        `€${Math.round(cf.property_value).toLocaleString()}`
      ]);

      doc.autoTable({
        startY: yPos,
        head: [['Year', 'Gross Rent', 'Vacancy', 'OpEx', 'Mortgage', 'Cash Flow', 'Cumul. CF', 'Prop. Value']],
        body: cashFlowData,
        theme: 'striped',
        headStyles: { fillColor: [14, 165, 233], fontSize: 7 },
        bodyStyles: { fontSize: 7 },
        columnStyles: {
          0: { cellWidth: 18, halign: 'center' },
          1: { cellWidth: 22, halign: 'right' },
          2: { cellWidth: 20, halign: 'right' },
          3: { cellWidth: 20, halign: 'right' },
          4: { cellWidth: 22, halign: 'right' },
          5: { cellWidth: 22, halign: 'right' },
          6: { cellWidth: 25, halign: 'right' },
          7: { cellWidth: 28, halign: 'right' }
        },
        margin: { left: 14, right: 14 }
      });
      yPos = doc.lastAutoTable.finalY + 10;
    }

    // Summary
    checkPageBreak(40);
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('SUMMARY', 14, yPos);
    yPos += 7;
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');
    const summaryLines = doc.splitTextToSize(evaluationResult.summary, 180);
    doc.text(summaryLines, 14, yPos);
    yPos += summaryLines.length * 5 + 5;

    // Data Sources
    if (evaluationResult.appreciation_source) {
      checkPageBreak(30);
      doc.setFontSize(12);
      doc.setFont(undefined, 'bold');
      doc.text('DATA SOURCES', 14, yPos);
      yPos += 6;
      doc.setFontSize(9);
      doc.setFont(undefined, 'normal');
      const sourceLines = doc.splitTextToSize(evaluationResult.appreciation_source, 180);
      doc.text(sourceLines, 14, yPos);
    }

    // Save PDF
    doc.save(`property-analysis-${propertyData.postal_code}-${Date.now()}.pdf`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onExportReport={handleExportReport} hasData={!!evaluationResult} />

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