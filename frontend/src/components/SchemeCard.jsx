import React from 'react'
import { Bookmark, BookmarkCheck, ExternalLink, ShieldCheck, ChevronRight, Award, CheckCircle2, AlertCircle } from 'lucide-react'

export default function SchemeCard({ 
  scheme, 
  onSelect, 
  isBookmarked = false, 
  onToggleBookmark,
  matchData = null 
}) {
  const { id, name, short_name, ministry, benefits, tags, source_url, last_verified } = scheme

  // Status badge logic based on matchData
  const renderMatchBadge = () => {
    if (!matchData) return null

    const { match_status, match_percentage } = matchData
    if (match_status === 'ELIGIBLE') {
      return (
        <span className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-800 text-[11px] font-bold px-2.5 py-0.5 rounded-full border border-emerald-300">
          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
          100% Eligible
        </span>
      )
    }
    if (match_status === 'POTENTIALLY_ELIGIBLE') {
      return (
        <span className="inline-flex items-center gap-1 bg-amber-100 text-amber-800 text-[11px] font-bold px-2.5 py-0.5 rounded-full border border-amber-300">
          <AlertCircle className="w-3 h-3 text-amber-600" />
          {match_percentage}% Potentially Eligible
        </span>
      )
    }
    if (match_status === 'INSUFFICIENT_DATA') {
      return (
        <span className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 text-[11px] font-bold px-2.5 py-0.5 rounded-full border border-blue-300">
          More Info Needed
        </span>
      )
    }
    return (
      <span className="inline-flex items-center gap-1 bg-rose-100 text-rose-800 text-[11px] font-bold px-2.5 py-0.5 rounded-full border border-rose-300">
        Criteria Not Met
      </span>
    )
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 hover:border-brand-300 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between overflow-hidden group">
      <div className="p-5">
        {/* Top Ministry bar & bookmark */}
        <div className="flex items-start justify-between gap-3 mb-2.5">
          <div className="flex items-center gap-1.5 text-slate-500 text-[11px] font-medium tracking-tight">
            <ShieldCheck className="w-3.5 h-3.5 text-brand-600 shrink-0" />
            <span className="truncate max-w-[240px]" title={ministry}>{ministry}</span>
          </div>

          <button
            onClick={(e) => {
              e.stopPropagation()
              onToggleBookmark && onToggleBookmark(id)
            }}
            className={`p-1.5 rounded-lg transition-colors ${
              isBookmarked 
                ? 'text-brand-600 bg-brand-50 hover:bg-brand-100' 
                : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
            }`}
            title={isBookmarked ? "Remove from saved" : "Save scheme"}
          >
            {isBookmarked ? <BookmarkCheck className="w-4 h-4 fill-brand-600" /> : <Bookmark className="w-4 h-4" />}
          </button>
        </div>

        {/* Title */}
        <h3 
          onClick={() => onSelect(scheme)}
          className="text-base font-bold text-slate-900 group-hover:text-brand-700 cursor-pointer transition-colors leading-snug line-clamp-2"
        >
          {name}
        </h3>

        {/* Match status badge */}
        <div className="mt-2.5 flex items-center gap-2">
          {renderMatchBadge()}
          {last_verified && (
            <span className="text-[11px] text-slate-600">
              Verified {last_verified}
            </span>
          )}
        </div>

        {/* Award Highlight */}
        <div className="mt-3.5 bg-slate-50 rounded-xl p-3 border border-slate-100 text-xs text-slate-700">
          <div className="flex items-start gap-2">
            <Award className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <span className="line-clamp-2 leading-relaxed font-medium">
              {benefits || scheme.award_summary}
            </span>
          </div>
        </div>

        {/* Tags */}
        {tags && tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-3">
            {tags.slice(0, 3).map((tag, idx) => (
              <span key={idx} className="bg-slate-100 text-slate-600 text-[10px] font-medium px-2 py-0.5 rounded-md">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Card Actions Footer */}
      <div className="px-5 py-3 bg-slate-50/70 border-t border-slate-100 flex items-center justify-between text-xs font-semibold">
        <button
          onClick={() => onSelect(scheme)}
          className="text-brand-600 hover:text-brand-800 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform"
        >
          <span>View Criteria & Documents</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>

        {source_url && (
          <a
            href={source_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="text-slate-400 hover:text-brand-600 p-1 rounded"
            title="Open official portal"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}
      </div>
    </div>
  )
}
