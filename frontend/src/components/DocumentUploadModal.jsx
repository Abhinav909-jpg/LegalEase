import React, { useState } from 'react'
import { X, UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react'
import { uploadDocument } from '../services/api'

export default function DocumentUploadModal({ isOpen, onClose, onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [schemeName, setSchemeName] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  if (!isOpen) return null

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0]
      if (!selected.name.toLowerCase().endsWith('.pdf')) {
        setError('Only PDF files are supported.')
        setFile(null)
        return
      }
      if (selected.size > 25 * 1024 * 1024) {
        setError('File exceeds 25 MB limit.')
        setFile(null)
        return
      }
      setFile(selected)
      setError(null)
      setResult(null)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select an official PDF file.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    if (schemeName.trim()) {
      formData.append('scheme_name', schemeName.trim())
    }

    try {
      const data = await uploadDocument(formData)

      setResult(data)
      setFile(null)
      setSchemeName('')
      onUploadSuccess && onUploadSuccess(data)
    } catch (err) {
      setError(err.message || 'Failed to upload and index document.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-100 max-w-lg w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1.5 rounded-full hover:bg-slate-100"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center">
            <UploadCloud className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Ingest Official Scheme PDF</h3>
            <p className="text-xs text-slate-500">Expand LegalEase's RAG knowledge base</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="mb-4 p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 space-y-1">
            <div className="flex items-center gap-1.5 font-bold">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>{result.message}</span>
            </div>
            <div className="text-[11px] text-emerald-700 pl-5">
              Extracted {result.pages_extracted} pages into {result.chunks_created} multilingual vector chunks in Qdrant.
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Select Official Guidelines PDF (max 25 MB)
            </label>
            <div className="border-2 border-dashed border-slate-200 hover:border-brand-400 rounded-xl p-5 text-center transition-colors bg-slate-50/50">
              <input
                type="file"
                accept=".pdf"
                id="doc-file-upload"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="doc-file-upload" className="cursor-pointer flex flex-col items-center">
                <FileText className="w-8 h-8 text-slate-400 mb-2" />
                <span className="text-xs font-semibold text-brand-600 hover:underline">
                  {file ? file.name : "Click to select a government PDF"}
                </span>
                <span className="text-[11px] text-slate-400 mt-1">
                  Supports NSP, State Welfare, Ministry notifications
                </span>
              </label>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Scheme Name (Optional)
            </label>
            <input
              type="text"
              value={schemeName}
              onChange={(e) => setSchemeName(e.target.value)}
              placeholder="e.g. National Overseas Scholarship Scheme 2024"
              className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 text-[11px] text-slate-500 leading-relaxed">
            <strong>Authenticity Guarantee:</strong> Uploaded guidelines are parsed using PyMuPDF, indexed with Multilingual Sentence Transformers, and served with verified page-level citations.
          </div>

          <div className="flex items-center justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-600 hover:text-slate-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !file}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow transition-colors"
            >
              {loading && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
              <span>{loading ? 'Ingesting & Chunking...' : 'Upload & Index'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
