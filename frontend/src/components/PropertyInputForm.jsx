import React, { useState, useEffect } from 'react';
import { Calculator } from 'lucide-react';

const PropertyInputForm = ({ onSubmit, loading, parsedData }) => {
  const [formData, setFormData] = useState({
    address: '',
    postal_code: '',
    price: '',
    surface: '',
    rooms: '',
    bedrooms: '',
    floor: '',
    dpe: '',
    down_payment: '',
    loan_amount: '',
    annual_rate: '0.03',
    loan_term: '20',
    monthly_rent: ''
  });

  // Auto-fill form when parsed data is received
  useEffect(() => {
    if (parsedData) {
      setFormData(prev => ({
        ...prev,
        address: parsedData.address || parsedData.city || prev.address,
        postal_code: parsedData.postal_code || prev.postal_code,
        price: parsedData.price ? String(parsedData.price) : prev.price,
        surface: parsedData.surface ? String(parsedData.surface) : prev.surface,
        rooms: parsedData.rooms ? String(parsedData.rooms) : prev.rooms,
        bedrooms: parsedData.bedrooms ? String(parsedData.bedrooms) : prev.bedrooms,
        floor: parsedData.floor !== undefined ? String(parsedData.floor) : prev.floor,
        dpe: parsedData.dpe || prev.dpe,
        down_payment: parsedData.down_payment ? String(parsedData.down_payment) : prev.down_payment,
        loan_amount: parsedData.loan_amount ? String(parsedData.loan_amount) : prev.loan_amount,
        annual_rate: parsedData.annual_rate ? String(parsedData.annual_rate) : prev.annual_rate,
        loan_term: parsedData.loan_term ? String(parsedData.loan_term) : prev.loan_term,
        monthly_rent: parsedData.monthly_rent ? String(parsedData.monthly_rent) : prev.monthly_rent
      }));
    }
  }, [parsedData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert string values to numbers
    const data = {
      address: formData.address,
      postal_code: formData.postal_code,
      price: parseFloat(formData.price),
      surface: parseFloat(formData.surface),
      rooms: parseInt(formData.rooms),
      bedrooms: parseInt(formData.bedrooms),
      floor: formData.floor ? parseInt(formData.floor) : undefined,
      dpe: formData.dpe || undefined,
      down_payment: parseFloat(formData.down_payment),
      loan_amount: parseFloat(formData.loan_amount),
      annual_rate: parseFloat(formData.annual_rate),
      loan_term: parseInt(formData.loan_term),
      monthly_rent: parseFloat(formData.monthly_rent)
    };

    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Property Info */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Location
        </label>
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
          placeholder="Amiraux-Simplon-Poissonniers"
          className="input text-sm"
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Postal Code
          </label>
          <input
            type="text"
            name="postal_code"
            value={formData.postal_code}
            onChange={handleChange}
            placeholder="75018"
            pattern="[0-9]{5}"
            title="5-digit postal code"
            className="input text-sm"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Price (€)
          </label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            placeholder="500000"
            className="input text-sm"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Surface (m²)
          </label>
          <input
            type="number"
            name="surface"
            value={formData.surface}
            onChange={handleChange}
            placeholder="50"
            step="0.1"
            className="input text-sm"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Rooms
          </label>
          <input
            type="number"
            name="rooms"
            value={formData.rooms}
            onChange={handleChange}
            placeholder="2"
            className="input text-sm"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Bedrooms
          </label>
          <input
            type="number"
            name="bedrooms"
            value={formData.bedrooms}
            onChange={handleChange}
            placeholder="1"
            className="input text-sm"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Floor
          </label>
          <input
            type="number"
            name="floor"
            value={formData.floor}
            onChange={handleChange}
            placeholder="3"
            className="input text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            DPE
          </label>
          <select
            name="dpe"
            value={formData.dpe}
            onChange={handleChange}
            className="input text-sm"
          >
            <option value="">-</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
            <option value="E">E</option>
            <option value="F">F</option>
            <option value="G">G</option>
          </select>
        </div>
      </div>

      {/* Financial Info */}
      <div className="pt-4 border-t border-gray-200">
        <h3 className="text-sm font-semibold text-gray-900 mb-3">Financing</h3>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Down Payment (€)
            </label>
            <input
              type="number"
              name="down_payment"
              value={formData.down_payment}
              onChange={handleChange}
              placeholder="100000"
              className="input text-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Loan Amount (€)
            </label>
            <input
              type="number"
              name="loan_amount"
              value={formData.loan_amount}
              onChange={handleChange}
              placeholder="400000"
              className="input text-sm"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 mt-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Interest Rate
            </label>
            <input
              type="number"
              name="annual_rate"
              value={formData.annual_rate}
              onChange={handleChange}
              placeholder="0.03"
              step="0.001"
              className="input text-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Term (years)
            </label>
            <input
              type="number"
              name="loan_term"
              value={formData.loan_term}
              onChange={handleChange}
              placeholder="20"
              className="input text-sm"
              required
            />
          </div>
        </div>

        <div className="mt-3">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Expected Monthly Rent (€)
          </label>
          <input
            type="number"
            name="monthly_rent"
            value={formData.monthly_rent}
            onChange={handleChange}
            placeholder="2000"
            className="input text-sm"
            required
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full btn-primary flex items-center justify-center space-x-2"
      >
        <Calculator className="w-4 h-4" />
        <span>{loading ? 'Analyzing...' : 'Analyze Property'}</span>
      </button>
    </form>
  );
};

export default PropertyInputForm;