import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const evaluateProperty = async (propertyData) => {
  try {
    const response = await api.post('/evaluate', propertyData);
    return response.data;
  } catch (error) {
    console.error('Error evaluating property:', error);
    throw error;
  }
};

export const researchProperty = async (address, postalCode) => {
  try {
    const response = await api.post('/research', { address, postal_code: postalCode });
    return response.data;
  } catch (error) {
    console.error('Error researching property:', error);
    throw error;
  }
};

export const createNegotiationDraft = async (negotiationData) => {
  try {
    const response = await api.post('/negotiate', negotiationData);
    return response.data;
  } catch (error) {
    console.error('Error creating negotiation draft:', error);
    throw error;
  }
};

export const parsePDF = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/parse/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error parsing PDF:', error);
    throw error;
  }
};

export default api;