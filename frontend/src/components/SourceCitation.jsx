import React from 'react'
import { FileText, ExternalLink, Bookmark, CheckCircle2 } from 'lucide-react'

export default function SourceCitation({ citation, index }) {
  if (!citation) return null

  const { document_name, page_number, scheme_name, source_url, snippet } = citation

  return (
    <div className="inline-flex flex-col bg-slate-50 hover:bg-brand-50/60 border border-slate-200 hover:border-brand-300 rounded-lg p-2.5 text-xs transition-all duration-150 w-full mb-2">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 font-medium text-slate-800 truncate">
          <FileText className="w-3.5 h-3.5 text-brand-600 shrink-0" />
          <span className="truncate" title={document_name}>{document_name}</span>
          <span className="bg-brand-100 text-brand-800 text-[10px] font-semibold px-1.5 py-0.5 rounded-full shrink-0">
            Page {page_number}
          </span>
        </div>
        {source_url && (
          <a
            href={source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-slate-400 hover:text-brand-600 inline-flex items-center gap-0.5 shrink-0"
            title="Open official portal"
          >
            <span className="sr-only">Official Link</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>

      {scheme_name && (
        <div className="text-[11px] text-slate-500 mt-1 font-medium truncate">
          Scheme: {scheme_name}
        </div>
      )}

      {snippet && (
        <p className="text-[11px] text-slate-600 mt-1.5 line-clamp-2 italic bg-white/70 p-1.5 rounded border border-slate-100">
          "{snippet}"
        </p>
      )}
    </div>
  )
}
