import React from 'react'
import { X, ExternalLink, Calendar, ShieldCheck, FileCheck, Award, CheckCircle2, AlertCircle } from 'lucide-react'

export default function SchemeModal({ scheme, onClose }) {
  if (!scheme) return null

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
      <div 
        className="bg-white rounded-2xl shadow-2xl border border-slate-100 max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="p-6 bg-gradient-to-r from-brand-900 to-indigo-900 text-white relative">
          <button 
            onClick={onClose}
            className="absolute top-5 right-5 text-white/80 hover:text-white bg-white/10 hover:bg-white/20 p-1.5 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          
          <div className="flex items-center gap-2 text-brand-200 text-xs font-semibold uppercase tracking-wider mb-2">
            <ShieldCheck className="w-4 h-4" />
            <span>{scheme.ministry}</span>
          </div>

          <h2 className="text-xl sm:text-2xl font-bold leading-snug">
            {scheme.name}
          </h2>

          <div className="flex flex-wrap items-center gap-4 mt-3 text-xs text-brand-100">
            <span className="flex items-center gap-1.5 bg-white/10 px-2.5 py-1 rounded-md">
              <Award className="w-3.5 h-3.5 text-yellow-300" />
              {scheme.short_name || 'Verified Scheme'}
            </span>
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5" />
              Verified: {scheme.last_verified}
            </span>
          </div>
        </div>

        {/* Modal Scrollable Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm text-slate-700">
          {/* Benefits Summary Box */}
          <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-start gap-3">
            <Award className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-emerald-900 text-sm">Financial Award & Benefits</h4>
              <p className="text-emerald-800 text-xs mt-1 leading-relaxed">
                {scheme.benefits}
              </p>
              {scheme.quota && (
                <p className="text-emerald-700 text-[11px] mt-1 font-medium">
                  Allocation: {scheme.quota}
                </p>
              )}
            </div>
          </div>

          {/* Eligibility Requirements */}
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-3">
              <CheckCircle2 className="w-4 h-4 text-brand-600" />
              Eligibility Criteria
            </h3>
            <ul className="space-y-2 bg-slate-50 border border-slate-200/80 rounded-xl p-4">
              {scheme.eligibility?.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-500 shrink-0 mt-1.5" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Required Documents */}
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-3">
              <FileCheck className="w-4 h-4 text-indigo-600" />
              Mandatory Documents Checklist
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {scheme.required_documents?.map((doc, idx) => (
                <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-2.5 flex items-center gap-2 text-xs">
                  <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                  <span className="text-slate-800 font-medium">{doc}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Application Procedure */}
          <div>
            <h3 className="text-base font-bold text-slate-900 mb-3">
              Application Procedure
            </h3>
            <div className="space-y-2">
              {scheme.application_procedure?.map((step, idx) => (
                <div key={idx} className="bg-brand-50/50 border border-brand-100 rounded-lg p-3 text-xs text-slate-700 leading-relaxed">
                  {step}
                </div>
              ))}
            </div>
          </div>

          {/* Official Verification Notice */}
          <div className="bg-slate-100 rounded-xl p-3.5 text-xs text-slate-500 border border-slate-200">
            <p className="font-medium text-slate-600 mb-1">Source Document Traceability:</p>
            <p className="text-[11px]">
              Extracted from official government notification <code className="bg-white px-1.5 py-0.5 rounded border border-slate-300 text-slate-800 font-mono">{scheme.source_doc}</code>.
            </p>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 transition-colors"
          >
            Close
          </button>
          
          <a
            href={scheme.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow transition-all duration-150"
          >
            <span>Apply on Official Portal</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  )
}
