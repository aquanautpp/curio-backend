import { API_BASE_URL } from '../config/api.js';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Métodos da sua API
  async getUsers() {
    return this.request('/users');
  }

  async getStudents() {
    return this.request('/students');
  }

  async getStudentData(studentId) {
    return this.request(`/ai/simple/dashboard-data/${studentId}`);
  }
}

export default new ApiClient();
