import React, { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Assistant from './pages/Assistant'
import EligibilityForm from './components/EligibilityForm'
import SchemeModal from './components/SchemeModal'
import DocumentUploadModal from './components/DocumentUploadModal'
import { fetchSchemes } from './services/api'
import { ShieldCheck, Heart, ExternalLink, HelpCircle } from 'lucide-react'

export default function App() {
  const [activePage, setActivePage] = useState('home')
  const [selectedScheme, setSelectedScheme] = useState(null)
  const [isUploadOpen, setIsUploadOpen] = useState(false)
  const [allSchemes, setAllSchemes] = useState([])
  const [dashboardSearch, setDashboardSearch] = useState('')
  const [bookmarkedIds, setBookmarkedIds] = useState(() => {
    try {
      const saved = localStorage.getItem('legaleease_bookmarks')
      return saved ? JSON.parse(saved) : ['pm-usp-csss', 'punjab-post-matric-sc']
    } catch {
      return ['pm-usp-csss', 'punjab-post-matric-sc']
    }
  })

  // Load schemes from API or grounded catalog
  const loadSchemes = () => {
    fetchSchemes()
      .then(data => {
        if (Array.isArray(data)) setAllSchemes(data)
      })
      .catch(err => console.error('Failed to load schemes:', err))
  }

  useEffect(() => {
    loadSchemes()
  }, [])

  const handleToggleBookmark = (id) => {
    setBookmarkedIds(prev => {
      const next = prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
      try {
        localStorage.setItem('schemesathi_bookmarks', JSON.stringify(next))
      } catch (e) {
        console.error(e)
      }
      return next
    })
  }

  const handleNavigate = (page, searchStr = '') => {
    setActivePage(page)
    if (searchStr) {
      setDashboardSearch(searchStr)
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 font-sans text-slate-800">
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        onOpenUpload={() => setIsUploadOpen(true)}
      />

      <main className="flex-1">
        {activePage === 'home' && (
          <Home
            onNavigate={handleNavigate}
            onSelectScheme={setSelectedScheme}
            allSchemes={allSchemes}
          />
        )}

        {activePage === 'dashboard' && (
          <Dashboard
            allSchemes={allSchemes}
            onSelectScheme={setSelectedScheme}
            onNavigate={handleNavigate}
            bookmarkedIds={bookmarkedIds}
            onToggleBookmark={handleToggleBookmark}
            initialSearch={dashboardSearch}
          />
        )}

        {activePage === 'assistant' && (
          <Assistant onOpenUpload={() => setIsUploadOpen(true)} />
        )}

        {activePage === 'eligibility' && (
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-6">
              <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                Deterministic Eligibility Engine
              </h1>
              <p className="text-xs sm:text-sm text-slate-500 mt-1">
                Enter your genuine profile information to see exact criteria matching with zero hallucination.
              </p>
            </div>
            <EligibilityForm onSchemeClick={setSelectedScheme} />
          </div>
        )}
      </main>

      {/* Scheme Details Modal */}
      {selectedScheme && (
        <SchemeModal
          scheme={selectedScheme}
          onClose={() => setSelectedScheme(null)}
        />
      )}

      {/* Document Upload Modal */}
      <DocumentUploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={() => {
          loadSchemes()
        }}
      />

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-auto py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 text-xs text-slate-500">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center font-bold">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <span className="font-bold text-slate-900">LegaleEase</span> — AI Government Scheme & Scholarship Navigator
                <p className="text-[11px] text-slate-400">Strictly grounded in official notifications from NSP & Ministry portals.</p>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-6 text-xs">
              <a
                href="https://scholarships.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-brand-600 flex items-center gap-1"
              >
                <span>National Scholarship Portal</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              <a
                href="https://scholarships.punjab.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-brand-600 flex items-center gap-1"
              >
                <span>Punjab Dr. Ambedkar Portal</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              <a
                href="https://yet.nta.ac.in"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-brand-600 flex items-center gap-1"
              >
                <span>PM-YASASVI Portal</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-400">
            <p>
              © 2024 LegaleEase. Built for Indian citizens and students with authentic RAG architecture.
            </p>
            <p className="flex items-center gap-1">
              Deterministic Matching • Multilingual MiniLM • Qdrant Vector DB • Cross-Encoder Reranking
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
