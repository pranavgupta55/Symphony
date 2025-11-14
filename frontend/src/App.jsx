/**
 * Symphony AI - Main Application Component
 * Updated with React Router for multi-page navigation
 */
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ReportHub } from './pages/ReportHub'
import { ReportInputPage } from './pages/ReportInputPage'
import { ReportAnalysisPage } from './pages/ReportAnalysisPage'

function App() {
  return (
    <Router>
      <Routes>
        {/* Redirect root to hub */}
        <Route path="/" element={<Navigate to="/hub" replace />} />

        {/* Main hub/dashboard */}
        <Route path="/hub" element={<ReportHub />} />

        {/* New report input */}
        <Route path="/new-report" element={<ReportInputPage />} />

        {/* Analysis page (both loading and display) */}
        <Route path="/analysis/:id" element={<ReportAnalysisPage />} />

        {/* Catch all - redirect to hub */}
        <Route path="*" element={<Navigate to="/hub" replace />} />
      </Routes>
    </Router>
  )
}

export default App
