import axios from 'axios';

// Automatically determine API URL based on current hostname
// This allows the app to work from any domain without configuration
const getApiBaseUrl = () => {
    // If VITE_API_URL is explicitly set (and not empty), use it
    if (import.meta.env.VITE_API_URL) {
        console.log('Using configured API URL:', import.meta.env.VITE_API_URL);
        return import.meta.env.VITE_API_URL;
    }

    // Otherwise, use the same host and port 5000
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;

    // If accessing via localhost, use localhost:5000
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:5000/api';
    }

    // Construct URL using the same protocol and hostname, but port 5000
    const apiUrl = `${protocol}//${hostname}:5000/api`;
    console.log('Auto-detected API URL:', apiUrl);
    return apiUrl;
};

const API_BASE_URL = getApiBaseUrl();

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    login: (credentials) => api.post('/auth/login', credentials),
};

// Areas API
export const areasAPI = {
    getAll: (params) => api.get('/areas', { params }),
    getById: (id) => api.get(`/areas/${id}`),
    create: (data) => api.post('/areas', data),
    update: (id, data) => api.put(`/areas/${id}`, data),
    delete: (id) => api.delete(`/areas/${id}`),
};

// Customers API
export const customersAPI = {
    getAll: (params) => api.get('/customers', { params }),
    getById: (id) => api.get(`/customers/${id}`),
    create: (data) => api.post('/customers', data),
    update: (id, data) => api.put(`/customers/${id}`, data),
    delete: (id) => api.delete(`/customers/${id}`),
};

// Reservations API
export const reservationsAPI = {
    getAll: (params) => api.get('/reservations', { params }),
    getById: (id) => api.get(`/reservations/${id}`),
    create: (data) => api.post('/reservations', data),
    update: (id, data) => api.put(`/reservations/${id}`, data),
    delete: (id) => api.delete(`/reservations/${id}`),
};

// Analytics API
export const analyticsAPI = {
    getSummary: (params) => api.get('/analytics/summary', { params }),
    getAttempts: (params) => api.get('/analytics/attempts', { params }),
    getAttemptById: (id) => api.get(`/analytics/attempts/${id}`),
};

export default api;
