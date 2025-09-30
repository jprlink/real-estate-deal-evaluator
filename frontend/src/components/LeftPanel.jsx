import React, { useState, useRef, useEffect } from 'react';
import { Send, Upload, MapPin } from 'lucide-react';
import PropertyInputForm from './PropertyInputForm';
import ChatMessage from './ChatMessage';

const LeftPanel = ({ onPropertySubmit, loading, chatMessages, onChatMessage, onParsedData }) => {
  const [chatInput, setChatInput] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [urlInput, setUrlInput] = useState('');
  const [parsing, setParsing] = useState(false);
  const [parsedFormData, setParsedFormData] = useState(null);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (chatInput.trim()) {
      onChatMessage(chatInput);
      setChatInput('');
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      onChatMessage('Please upload a valid PDF file.');
      return;
    }

    setUploadedFile(file);
    setParsing(true);
    onChatMessage(`Uploading and parsing ${file.name}...`);

    try {
      const { parsePDF } = await import('../services/api');
      const result = await parsePDF(file);

      if (result.success) {
        // Auto-fill form with parsed data
        setParsedFormData(result);
        if (onParsedData) {
          onParsedData(result);
        }
        onChatMessage(`✅ Successfully parsed ${file.name}! Form fields have been auto-filled. Please review and complete any missing information.`);
      } else {
        onChatMessage(result.message || `⚠️ ${file.name} uploaded but parsing is not fully implemented yet. Please fill in the form manually.`);
      }
    } catch (error) {
      console.error('Error parsing PDF:', error);
      onChatMessage(`❌ Error parsing PDF. Please fill in the form manually.`);
    } finally {
      setParsing(false);
    }
  };

  const handleUrlParse = async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    setParsing(true);
    onChatMessage(`Fetching and parsing URL...`);

    try {
      const { parseURL } = await import('../services/api');
      const result = await parseURL(urlInput);

      if (result.success) {
        // Auto-fill form with parsed data
        setParsedFormData(result);
        if (onParsedData) {
          onParsedData(result);
        }
        onChatMessage(`✅ Successfully parsed listing! Form fields have been auto-filled. Please review and complete any missing information.`);
        setUrlInput(''); // Clear URL input after success
      } else {
        onChatMessage(result.message || `⚠️ URL fetched but parsing failed. Please fill in the form manually.`);
      }
    } catch (error) {
      console.error('Error parsing URL:', error);
      onChatMessage(`❌ Error parsing URL: ${error.message}. Please check the URL and try again.`);
    } finally {
      setParsing(false);
    }
  };

  return (
    <>
      {/* Chat Interface */}
      <div className="card flex flex-col h-[40%]">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
          <span className="badge badge-success">Online</span>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto space-y-3 mb-4">
          {chatMessages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Chat Input */}
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Ask me anything..."
            className="input text-sm"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !chatInput.trim()}
            className="btn-primary px-3"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

      {/* Property Input Form */}
      <div className="card flex-1 overflow-y-auto">
        <div className="flex items-center space-x-2 mb-4">
          <MapPin className="w-5 h-5 text-primary-600" />
          <h2 className="text-lg font-semibold text-gray-900">Property Details</h2>
        </div>

        <PropertyInputForm
          onSubmit={onPropertySubmit}
          loading={loading || parsing}
          parsedData={parsedFormData}
        />

        {/* URL Input */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Parse Listing from URL (Optional)
          </label>
          <form onSubmit={handleUrlParse} className="flex gap-2">
            <input
              type="url"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              placeholder="https://www.seloger.com/annonces/..."
              className="input text-sm flex-1"
              disabled={loading || parsing}
            />
            <button
              type="submit"
              disabled={loading || parsing || !urlInput.trim()}
              className="btn-primary px-3"
            >
              <MapPin className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* File Upload */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload Listing PDF (Optional)
          </label>
          <div className="flex items-center justify-center w-full">
            <label className="flex flex-col items-center justify-center w-full h-24 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Upload className="w-6 h-6 text-gray-400 mb-2" />
                {uploadedFile ? (
                  <p className="text-xs text-green-600 font-medium">{uploadedFile.name}</p>
                ) : (
                  <p className="text-xs text-gray-500">Click to upload or drag and drop</p>
                )}
              </div>
              <input
                type="file"
                className="hidden"
                accept=".pdf"
                onChange={handleFileUpload}
                disabled={loading || parsing}
              />
            </label>
          </div>
        </div>
      </div>
    </>
  );
};

export default LeftPanel;