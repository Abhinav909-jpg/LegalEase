import React, { useState } from 'react'
import { Search, Compass, MessageSquare, ShieldCheck, CheckCircle2, Award, FileText, ArrowRight, BookOpen, ExternalLink, Globe2, Sparkles } from 'lucide-react'
import SchemeCard from '../components/SchemeCard'

export default function Home({ onNavigate, onSelectScheme, allSchemes }) {
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearchSubmit = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      onNavigate('dashboard', searchQuery)
    }
  }

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-brand-50/80 via-white to-slate-50 pt-12 pb-20 border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          {/* Trust Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-100 text-brand-800 text-xs font-semibold mb-6 shadow-sm border border-brand-200">
            <ShieldCheck className="w-4 h-4 text-brand-600" />
            <span>Strictly Grounded in Official Government Documents & Guidelines</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
            Discover Government Schemes <br className="hidden sm:inline" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 to-indigo-600">
              You're Actually Eligible For.
            </span>
          </h1>

          <p className="mt-5 text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
            LegalEase uses verified PDF guidelines from the National Scholarship Portal, Ministry of Education, and State Welfare departments. No guesswork, no fabricated deadlines—only genuine RAG and deterministic eligibility verification.
          </p>

          {/* Search Box */}
          <form onSubmit={handleSearchSubmit} className="mt-8 max-w-xl mx-auto">
            <div className="flex items-center bg-white p-2 rounded-2xl shadow-lg shadow-brand-500/10 border border-slate-200 focus-within:border-brand-500 focus-within:ring-4 focus-within:ring-brand-100 transition-all">
              <Search className="w-5 h-5 text-slate-400 ml-3 mr-2 shrink-0" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search schemes: e.g. Punjab SC scholarship, Class 12, college grant..."
                className="w-full text-xs sm:text-sm text-slate-800 focus:outline-none placeholder:text-slate-400"
              />
              <button
                type="submit"
                className="px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold rounded-xl transition-colors shrink-0 shadow"
              >
                Find Schemes
              </button>
            </div>
          </form>

          {/* Quick CTA Actions */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <button
              onClick={() => onNavigate('eligibility')}
              className="inline-flex items-center gap-2 px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white text-xs sm:text-sm font-bold rounded-xl shadow-md transition-all hover:-translate-y-0.5"
            >
              <Compass className="w-4 h-4" />
              <span>Check Eligibility Wizard</span>
            </button>

            <button
              onClick={() => onNavigate('assistant')}
              className="inline-flex items-center gap-2 px-6 py-3 bg-white hover:bg-slate-50 text-slate-700 text-xs sm:text-sm font-bold rounded-xl border border-slate-300 shadow-sm transition-all hover:-translate-y-0.5"
            >
              <MessageSquare className="w-4 h-4 text-brand-600" />
              <span>Ask AI Navigator (English / हिंदी / ਪੰਜਾਬੀ)</span>
            </button>
          </div>

          {/* Official Verification Highlights */}
          <div className="mt-12 pt-8 border-t border-slate-200/80 flex flex-wrap items-center justify-center gap-6 sm:gap-12 text-xs text-slate-500 font-medium">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              National Scholarship Portal (NSP)
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Ministry of Education (PM-USP)
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Dept of Social Justice Punjab
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Ministry of Social Justice & Empowerment
            </span>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            How LegalEase Works
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 mt-2">
            A production-grade architecture combining deterministic rules with retrieval-augmented generation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative group hover:border-brand-300 transition-all">
            <div className="w-12 h-12 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center font-bold text-lg mb-4">
              1
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">Ingestion & FAISS Retrieval</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Official PDF guidelines are parsed with Unstructured, chunked with CharacterTextSplitter, embedded with Hugging Face MiniLM, indexed in FAISS, and reranked with Cross-Encoder.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative group hover:border-brand-300 transition-all">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-lg mb-4">
              2
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">Deterministic Matching</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Your age, state, education, and family income are evaluated strictly by deterministic algorithms—explaining matches, non-matches, and missing documents without guessing.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative group hover:border-brand-300 transition-all">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-lg mb-4">
              3
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">Citations & Direct Apply</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Every factual answer cites the exact document title and page number. Direct links take you straight to authentic government portals to submit your application.
            </p>
          </div>
        </div>
      </section>

      {/* Featured Verified Schemes */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-end justify-between gap-4 mb-8">
          <div>
            <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              Featured Official Schemes & Scholarships
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Active schemes with verified guidelines in the LegalEase knowledge base
            </p>
          </div>

          <button
            onClick={() => onNavigate('dashboard')}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 hover:text-brand-800"
          >
            <span>View All Schemes</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          {allSchemes.slice(0, 4).map((scheme) => (
            <SchemeCard
              key={scheme.id}
              scheme={scheme}
              onSelect={onSelectScheme}
            />
          ))}
        </div>
      </section>

      {/* Multilingual Support Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-brand-900 via-indigo-950 to-slate-900 rounded-3xl p-8 sm:p-12 text-white relative overflow-hidden">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-brand-200 text-xs font-semibold mb-4">
              <Globe2 className="w-4 h-4" />
              <span>Multi-language Accessibility</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold leading-snug">
              Explore in English, हिन्दी, or ਪੰਜਾਬੀ.
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 mt-3 leading-relaxed">
              Language should never be a barrier to securing your constitutional and educational rights. LegalEase supports queries and generates grounded answers in native Indic scripts.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <button
                onClick={() => onNavigate('assistant')}
                className="px-5 py-2.5 bg-brand-500 hover:bg-brand-600 text-white text-xs font-bold rounded-xl shadow transition-colors"
              >
                Try AI Assistant Now
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
