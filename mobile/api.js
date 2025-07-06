import axios from 'axios';

const API_BASE_URL = 'http://YOUR_FASTAPI_SERVER_URL'; // Replace with your FastAPI URL

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export default api;
