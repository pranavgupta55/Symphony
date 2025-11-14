/**
 * Zustand Store for Analysis State Management
 */
import { create } from 'zustand';

const useAnalysisStore = create((set, get) => ({
  // Current analysis state
  currentJobId: null,
  analysisStatus: null,
  analysisResults: null,
  error: null,
  isLoading: false,
  progress: 0,

  // Jobs history
  jobs: [],

  // Actions
  setCurrentJob: (jobId) => set({ currentJobId: jobId }),

  setAnalysisStatus: (status) => set({ analysisStatus: status, progress: status.progress || 0 }),

  setAnalysisResults: (results) => set({ analysisResults: results }),

  setError: (error) => set({ error, isLoading: false }),

  setLoading: (isLoading) => set({ isLoading }),

  clearError: () => set({ error: null }),

  resetAnalysis: () =>
    set({
      currentJobId: null,
      analysisStatus: null,
      analysisResults: null,
      error: null,
      isLoading: false,
      progress: 0,
    }),

  setJobs: (jobs) => set({ jobs }),

  addJob: (job) => set((state) => ({ jobs: [job, ...state.jobs] })),

  removeJob: (jobId) =>
    set((state) => ({
      jobs: state.jobs.filter((job) => job.id !== jobId),
    })),

  // Selectors
  getCurrentJob: () => {
    const state = get();
    return state.jobs.find((job) => job.id === state.currentJobId);
  },
}));

export default useAnalysisStore;
