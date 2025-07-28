const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.MODE === 'production' 
    ? 'https://curio-backend-1.onrender.com/api'
    : 'http://localhost:5000/api'
  );

export { API_BASE_URL };
