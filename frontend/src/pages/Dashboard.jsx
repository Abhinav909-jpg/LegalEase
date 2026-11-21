import React, { useState } from 'react'
import { Search, Filter, Bookmark, BookOpen, FileCheck, CheckCircle2, ChevronRight, Clock, ShieldCheck, ArrowRight } from 'lucide-react'
import SchemeCard from '../components/SchemeCard'

const STATES_FILTER = ["All", "Punjab", "All India"]
const CATEGORIES_FILTER = ["All", "General", "SC", "OBC", "EBC", "DNT", "School Students"]

export default function Dashboard({ 
  allSchemes, 
  onSelectScheme, 
  onNavigate,
  bookmarkedIds,
  onToggleBookmark,
  initialSearch = ''
}) {
  const [search, setSearch] = useState(initialSearch)
  const [selectedState, setSelectedState] = useState('All')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [tab, setTab] = useState('all') // 'all' or 'saved'

  // Application tracker step mock
  const [activeStage, setActiveStage] = useState(2)

  const STAGES = [
    { num: 1, title: "Eligibility Evaluation", desc: "Run LegalEase deterministic engine to confirm conditions." },
    { num: 2, title: "Document Preparation", desc: "Gather Tehsildar income certificate, caste certificate, marksheet." },
    { num: 3, title: "Portal Registration", desc: "Complete NSP OTR or Dr. Ambedkar Portal enrollment." },
    { num: 4, title: "Institution Verification", desc: "College/School Nodal Officer (INO) certifies admission." },
    { num: 5, title: "DBT Direct Sanction", desc: "Direct disbursement to your Aadhaar-linked bank account." }
  ]

  const filteredSchemes = allSchemes.filter(s => {
    if (tab === 'saved' && !bookmarkedIds.includes(s.id)) {
      return false
    }

    if (search.trim()) {
      const q = search.toLowerCase()
      const matchName = s.name.toLowerCase().includes(q)
      const matchMin = s.ministry.toLowerCase().includes(q)
      const matchTags = s.tags?.some(t => t.toLowerCase().includes(q))
      if (!matchName && !matchMin && !matchTags) return false
    }

    if (selectedState !== 'All') {
      const isPunjab = selectedState === 'Punjab' && (s.name.includes('Punjab') || s.tags?.includes('Punjab'))
      const isAllIndia = selectedState === 'All India' && s.tags?.includes('All India')
      if (!isPunjab && !isAllIndia) return false
    }

    if (selectedCategory !== 'All') {
      const catMatch = s.tags?.some(t => t.toLowerCase().includes(selectedCategory.toLowerCase()))
      if (!catMatch) return false
    }

    return true
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Welcome & Overview Header */}
      <div className="bg-gradient-to-r from-brand-900 to-indigo-900 rounded-2xl p-6 sm:p-8 text-white relative overflow-hidden">
        <div className="relative z-10 max-w-3xl">
          <div className="flex items-center gap-2 text-brand-200 text-xs font-semibold mb-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>National Verified Directory</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Scheme Discovery & Application Center
          </h1>
          <p className="text-xs sm:text-sm text-brand-100 mt-2 leading-relaxed">
            Browse official guidelines, track your application milestones, and access primary government application portals directly.
          </p>
        </div>

        {/* Quick Stats Grid */}
        <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center sm:text-left">
          <div>
            <span className="text-brand-300 text-xs">Total Active Schemes</span>
            <div className="text-xl font-bold mt-0.5">{allSchemes.length} Verified</div>
          </div>
          <div>
            <span className="text-brand-300 text-xs">Knowledge Base Docs</span>
            <div className="text-xl font-bold mt-0.5">4 Official PDFs</div>
          </div>
          <div>
            <span className="text-brand-300 text-xs">Saved Bookmarks</span>
            <div className="text-xl font-bold mt-0.5">{bookmarkedIds.length} Schemes</div>
          </div>
          <div>
            <span className="text-brand-300 text-xs">Disbursement Mode</span>
            <div className="text-xl font-bold mt-0.5 text-emerald-300">100% DBT Direct</div>
          </div>
        </div>
      </div>

      {/* Application Progress Tracker Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
          <div>
            <h3 className="text-base font-bold text-slate-900">Official Scholarship Application Roadmap</h3>
            <p className="text-xs text-slate-500">Standard standard operating procedure across NSP and State Portals</p>
          </div>
          <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-3 py-1 rounded-full border border-brand-200">
            Interactive Roadmap
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
          {STAGES.map((st) => {
            const isCompleted = st.num < activeStage
            const isCurrent = st.num === activeStage

            return (
              <div 
                key={st.num}
                onClick={() => setActiveStage(st.num)}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                  isCurrent 
                    ? 'border-brand-500 bg-brand-50/60 ring-2 ring-brand-200' 
                    : isCompleted
                    ? 'border-emerald-300 bg-emerald-50/40'
                    : 'border-slate-200 bg-slate-50/60 hover:bg-slate-100'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center ${
                    isCurrent
                      ? 'bg-brand-600 text-white'
                      : isCompleted
                      ? 'bg-emerald-600 text-white'
                      : 'bg-slate-200 text-slate-600'
                  }`}>
                    {isCompleted ? <CheckCircle2 className="w-4 h-4" /> : st.num}
                  </span>
                  <span className="text-[10px] font-semibold uppercase text-slate-400">
                    Stage {st.num}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-slate-900 leading-snug">{st.title}</h4>
                <p className="text-[11px] text-slate-500 mt-1 leading-relaxed line-clamp-2">
                  {st.desc}
                </p>
              </div>
            )
          })}
        </div>
      </div>

      {/* Discovery Filters & Search */}
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          {/* Tabs */}
          <div className="flex items-center bg-slate-200/80 p-1 rounded-xl text-xs font-bold">
            <button
              onClick={() => setTab('all')}
              className={`px-4 py-1.5 rounded-lg transition-all ${
                tab === 'all'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Official Schemes ({allSchemes.length})
            </button>
            <button
              onClick={() => setTab('saved')}
              className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg transition-all ${
                tab === 'saved'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Bookmark className="w-3.5 h-3.5" />
              <span>Saved Schemes ({bookmarkedIds.length})</span>
            </button>
          </div>

          {/* Search box */}
          <div className="relative w-full sm:w-72">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search scheme name, ministry..."
              className="w-full text-xs pl-9 pr-3.5 py-2 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 bg-white"
            />
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
          <span className="font-semibold text-slate-500 flex items-center gap-1 mr-1">
            <Filter className="w-3.5 h-3.5" />
            State:
          </span>
          {STATES_FILTER.map(st => (
            <button
              key={st}
              onClick={() => setSelectedState(st)}
              className={`px-3 py-1 rounded-full text-xs transition-colors ${
                selectedState === st
                  ? 'bg-brand-600 text-white font-semibold shadow-sm'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              {st}
            </button>
          ))}

          <span className="font-semibold text-slate-500 flex items-center gap-1 ml-4 mr-1">
            Category:
          </span>
          {CATEGORIES_FILTER.map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-full text-xs transition-colors ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Schemes Grid */}
        {filteredSchemes.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-lg mx-auto">
            <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h4 className="text-base font-bold text-slate-800">No matching schemes found</h4>
            <p className="text-xs text-slate-500 mt-1">
              Try adjusting your search query, state, or category filters.
            </p>
            <button
              onClick={() => {
                setSearch('')
                setSelectedState('All')
                setSelectedCategory('All')
                setTab('all')
              }}
              className="mt-4 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg"
            >
              Clear All Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
            {filteredSchemes.map((scheme) => (
              <SchemeCard
                key={scheme.id}
                scheme={scheme}
                onSelect={onSelectScheme}
                isBookmarked={bookmarkedIds.includes(scheme.id)}
                onToggleBookmark={onToggleBookmark}
              />
            ))}
          </div>
        )}
      </div>

      {/* Quick Prompts for Assistant */}
      <div className="bg-slate-100/70 rounded-2xl p-6 border border-slate-200">
        <h4 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
          <Clock className="w-4 h-4 text-brand-600" />
          Commonly Asked Citizen Questions
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <button
            onClick={() => onNavigate('assistant', 'What are the required documents for Punjab Post Matric Scholarship?')}
            className="p-3 bg-white hover:bg-brand-50 border border-slate-200 rounded-xl text-left font-medium text-slate-700 hover:text-brand-700 transition-colors"
          >
            "What documents are needed for Punjab Post Matric Scholarship?"
          </button>
          <button
            onClick={() => onNavigate('assistant', 'What is the income ceiling for Central Sector Scholarship CSSS?')}
            className="p-3 bg-white hover:bg-brand-50 border border-slate-200 rounded-xl text-left font-medium text-slate-700 hover:text-brand-700 transition-colors"
          >
            "What is the income ceiling for PM-USP Central Sector Scholarship?"
          </button>
          <button
            onClick={() => onNavigate('assistant', 'Can private school students apply for National Means-cum-Merit Scholarship?')}
            className="p-3 bg-white hover:bg-brand-50 border border-slate-200 rounded-xl text-left font-medium text-slate-700 hover:text-brand-700 transition-colors"
          >
            "Can private school students apply for NMMSS scholarship?"
          </button>
        </div>
      </div>
    </div>
  )
}
