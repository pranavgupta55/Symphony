/**
 * API Client for Symphony AI Backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload and analyze earnings call
 */
export const analyzeEarningsCall = async (audioFile, charts, companyName, companyContext) => {
  const formData = new FormData();
  formData.append('audio', audioFile);

  if (charts && charts.length > 0) {
    charts.forEach((chart) => {
      formData.append('charts', chart);
    });
  }

  if (companyName) {
    formData.append('company_name', companyName);
  }

  if (companyContext) {
    formData.append('company_context', companyContext);
  }

  const response = await apiClient.post('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Get job status
 */
export const getJobStatus = async (jobId) => {
  const response = await apiClient.get(`/api/status/${jobId}`);
  return response.data;
};

/**
 * Get analysis results
 */
export const getResults = async (jobId) => {
  const response = await apiClient.get(`/api/results/${jobId}`);
  return response.data;
};

/**
 * Get all jobs
 */
export const getJobs = async (limit = 20, offset = 0) => {
  const response = await apiClient.get('/api/jobs', {
    params: { limit, offset },
  });
  return response.data;
};

/**
 * Delete a job
 */
export const deleteJob = async (jobId) => {
  const response = await apiClient.delete(`/api/jobs/${jobId}`);
  return response.data;
};

/**
 * Get audio file URL
 */
export const getAudioUrl = (jobId) => {
  return `${API_BASE_URL}/api/audio/${jobId}`;
};

/**
 * Poll job status until completion
 */
export const pollJobStatus = async (jobId, onProgress) => {
  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        const status = await getJobStatus(jobId);

        if (onProgress) {
          onProgress(status);
        }

        if (status.status === 'completed') {
          clearInterval(interval);
          const results = await getResults(jobId);
          resolve(results);
        } else if (status.status === 'failed') {
          clearInterval(interval);
          reject(new Error(status.error_message || 'Analysis failed'));
        }
      } catch (error) {
        clearInterval(interval);
        reject(error);
      }
    }, 2000); // Poll every 2 seconds
  });
};

export default {
  analyzeEarningsCall,
  getJobStatus,
  getResults,
  getJobs,
  deleteJob,
  getAudioUrl,
  pollJobStatus,
};
