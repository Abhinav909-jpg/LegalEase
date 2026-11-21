import React, { useState, useEffect } from 'react'
import { FileText, ShieldCheck, UploadCloud, Info, CheckCircle2, ExternalLink } from 'lucide-react'
import ChatWindow from '../components/ChatWindow'
import { fetchDocuments } from '../services/api'

export default function Assistant({ onOpenUpload }) {
  const [documents, setDocuments] = useState([])

  useEffect(() => {
    fetchDocuments()
      .then(data => {
        if (Array.isArray(data)) setDocuments(data)
      })
      .catch(err => console.error('Failed to load documents:', err))
  }, [])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Left Info & Knowledge Base Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Grounding Notice Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
            <div className="flex items-center gap-2 text-brand-700 text-xs font-bold uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Grounded Guarantee</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              LegalEase never fabricates criteria. All responses are verified against official government PDFs using Unstructured, CharacterTextSplitter, Hugging Face Embeddings, FAISS similarity search, and Cross-Encoder reranking.
            </p>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
              <span>Embeddings:</span>
              <span className="font-semibold text-slate-700">Hugging Face MiniLM</span>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-500">
              <span>Reranker:</span>
              <span className="font-semibold text-slate-700">Cross-Encoder</span>
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-500">
              <span>Vector DB:</span>
              <span className="font-semibold text-slate-700">FAISS</span>
            </div>
          </div>

          {/* Official Document Repository Explorer */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-brand-600" />
                Indexed Guidelines ({documents.length})
              </h4>
            </div>

            <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
              {documents.length === 0 ? (
                <div className="text-[11px] text-slate-400">Loading document index...</div>
              ) : (
                documents.map((doc, idx) => (
                  <div key={idx} className="bg-slate-50 border border-slate-200/80 rounded-xl p-2.5 text-xs">
                    <div className="font-medium text-slate-800 text-[11px] leading-snug line-clamp-2" title={doc.document_name}>
                      {doc.document_name}
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1.5">
                      <span>Verified: {doc.last_verified || '2024'}</span>
                      <span className="text-emerald-700 font-semibold bg-emerald-50 px-1.5 py-0.2 rounded">Indexed</span>
                    </div>
                  </div>
                ))
              )}
            </div>

            <button
              onClick={onOpenUpload}
              className="mt-4 w-full flex items-center justify-center gap-2 py-2 px-3 bg-brand-50 hover:bg-brand-100 text-brand-700 text-xs font-semibold rounded-xl border border-brand-200 transition-colors"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Add Official PDF</span>
            </button>
          </div>

          {/* Multilingual Tip */}
          <div className="bg-indigo-50/70 border border-indigo-100 rounded-2xl p-4 text-xs text-indigo-950 space-y-2">
            <div className="font-bold flex items-center gap-1.5 text-indigo-900">
              <Info className="w-4 h-4 text-indigo-600" />
              Language Assistance
            </div>
            <p className="text-[11px] text-indigo-800 leading-relaxed">
              Use the top-right language buttons in the chat window to switch between English, Hindi, and Punjabi at any time.
            </p>
          </div>
        </div>

        {/* Main Chat Interface */}
        <div className="lg:col-span-3">
          <ChatWindow />
        </div>
      </div>
    </div>
  )
}
