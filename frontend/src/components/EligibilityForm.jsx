import React, { useState } from 'react'
import { CheckCircle2, XCircle, AlertCircle, HelpCircle, ArrowRight, ArrowLeft, RefreshCw, Loader2, ShieldAlert, Award, FileText, ExternalLink } from 'lucide-react'
import { checkEligibility } from '../services/api'

const INDIAN_STATES = [
  "All India",
  "Punjab",
  "Delhi",
  "Haryana",
  "Uttar Pradesh",
  "Rajasthan",
  "Himachal Pradesh",
  "Maharashtra",
  "Madhya Pradesh",
  "Bihar",
  "West Bengal",
  "Karnataka",
  "Tamil Nadu",
  "Kerala",
  "Gujarat",
  "Other State / UT"
]

const EDUCATION_LEVELS = [
  "Class 8",
  "Class 9",
  "Class 10",
  "Class 11",
  "Class 12",
  "Class 12 Passed",
  "Diploma / Polytechnic",
  "Undergraduate (BA, BSc, BTech, BCom)",
  "Postgraduate (MA, MSc, MTech, MBA)",
  "PhD / Doctoral"
]

const CATEGORIES = [
  "General",
  "SC (Scheduled Caste)",
  "ST (Scheduled Tribe)",
  "OBC (Other Backward Classes)",
  "EBC (Economically Backward Class)",
  "DNT (De-Notified Tribes)"
]

export default function EligibilityForm({ onSchemeClick }) {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    age: '',
    state: 'Punjab',
    gender: 'Female',
    education: 'Undergraduate (BA, BSc, BTech, BCom)',
    category: 'SC (Scheduled Caste)',
    school_type: 'Government',
    board_percentile: '82',
    family_income: '200000',
    other_scholarships: false,
    disability_status: false
  })

  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [activeFilter, setActiveFilter] = useState('ALL') // 'ALL', 'ELIGIBLE', 'POTENTIALLY_ELIGIBLE', 'INELIGIBLE'
  const [expandedScheme, setExpandedScheme] = useState(null)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleEvaluate = async () => {
    setLoading(true)
    setError(null)

    // Parse clean category string e.g. "SC" from "SC (Scheduled Caste)"
    let cleanCategory = formData.category
    if (cleanCategory.includes('(')) {
      cleanCategory = cleanCategory.split('(')[0].trim()
    }

    const payload = {
      age: formData.age ? parseInt(formData.age, 10) : null,
      state: formData.state,
      gender: formData.gender,
      education: formData.education,
      category: cleanCategory,
      school_type: formData.school_type,
      board_percentile: formData.board_percentile ? parseFloat(formData.board_percentile) : null,
      family_income: formData.family_income ? parseFloat(formData.family_income) : null,
      other_scholarships: formData.other_scholarships,
      disability_status: formData.disability_status
    }

    try {
      const data = await checkEligibility(payload)
      setResults(data)
      setStep(4) // Move to results step
    } catch (err) {
      setError(err.message || 'Error occurred during eligibility evaluation.')
    } finally {
      setLoading(false)
    }
  }

  const filteredResults = results?.results.filter(r => {
    if (activeFilter === 'ALL') return true
    return r.match_status === activeFilter
  }) || []

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Wizard Progress Header */}
      <div className="bg-slate-50 border-b border-slate-200 px-6 py-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold text-brand-700 uppercase tracking-wider">
            Deterministic Eligibility Checker
          </span>
          <span className="text-xs font-medium text-slate-500">
            {step <= 3 ? `Step ${step} of 3` : 'Evaluation Results'}
          </span>
        </div>

        {/* Progress bar */}
        <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-brand-600 transition-all duration-300"
            style={{ width: `${step === 4 ? 100 : (step / 3) * 100}%` }}
          />
        </div>
      </div>

      <div className="p-6">
        {error && (
          <div className="mb-6 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-500 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Step 1: Personal & State */}
        {step === 1 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div>
              <h3 className="text-base font-bold text-slate-900">Personal & Domicile Information</h3>
              <p className="text-xs text-slate-500 mt-0.5">Eligibility criteria strictly depend on state residence and demographic norms.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  State of Domicile / Residence *
                </label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs font-medium"
                >
                  {INDIAN_STATES.map((st, i) => (
                    <option key={i} value={st}>{st}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  Age (Years)
                </label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  placeholder="e.g. 19"
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  Gender
                </label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs font-medium"
                >
                  <option value="Female">Female (50% Quota in Central Sector)</option>
                  <option value="Male">Male</option>
                  <option value="Transgender">Transgender</option>
                </select>
              </div>

              <div className="flex items-center pt-6">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    name="disability_status"
                    checked={formData.disability_status}
                    onChange={handleChange}
                    className="w-4 h-4 text-brand-600 rounded border-slate-300 focus:ring-brand-500"
                  />
                  <span className="text-xs text-slate-700 font-medium">
                    Person with Benchmark Disability (PwD)
                  </span>
                </label>
              </div>
            </div>

            <div className="flex justify-end pt-4">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors"
              >
                <span>Continue to Academic Info</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Academic & Category */}
        {step === 2 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div>
              <h3 className="text-base font-bold text-slate-900">Academic Level & Social Category</h3>
              <p className="text-xs text-slate-500 mt-0.5">Government scholarships are reserved or tiered based on educational stage and social category.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  Current Course / Education Stage *
                </label>
                <select
                  name="education"
                  value={formData.education}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs font-medium"
                >
                  {EDUCATION_LEVELS.map((ed, i) => (
                    <option key={i} value={ed}>{ed}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  Social Category (Caste / Community) *
                </label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs font-medium"
                >
                  {CATEGORIES.map((cat, i) => (
                    <option key={i} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  Class 12 Board Percentile (If passed)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="board_percentile"
                  value={formData.board_percentile}
                  onChange={handleChange}
                  placeholder="e.g. 84.5"
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs"
                />
                <span className="text-[10px] text-slate-400 mt-1 block">
                  Required &gt; 80th percentile for Central Sector (PM-USP)
                </span>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  School / Institution Type
                </label>
                <select
                  name="school_type"
                  value={formData.school_type}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs font-medium"
                >
                  <option value="Government">Government Institution</option>
                  <option value="Govt-Aided">Government-Aided Institution</option>
                  <option value="Private Recognized">Private Recognized College / School</option>
                  <option value="Kendriya Vidyalaya">Kendriya Vidyalaya / JNV</option>
                </select>
              </div>
            </div>

            <div className="flex justify-between pt-4">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>

              <button
                type="button"
                onClick={() => setStep(3)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors"
              >
                <span>Continue to Financial Info</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Financial & Income */}
        {step === 3 && (
          <div className="space-y-5 animate-in fade-in duration-150">
            <div>
              <h3 className="text-base font-bold text-slate-900">Family Income & Financial Norms</h3>
              <p className="text-xs text-slate-500 mt-0.5">Every government scholarship has strict ceiling limits verified by Tehsildar certificates.</p>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  Gross Annual Parental / Family Income (in ₹ INR) *
                </label>
                <div className="relative">
                  <span className="absolute left-3.5 top-2.5 font-bold text-slate-400">₹</span>
                  <input
                    type="number"
                    name="family_income"
                    value={formData.family_income}
                    onChange={handleChange}
                    placeholder="e.g. 250000"
                    className="w-full pl-8 pr-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 text-xs font-semibold text-slate-800"
                  />
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {[150000, 250000, 350000, 450000, 800000].map((inc) => (
                    <button
                      key={inc}
                      type="button"
                      onClick={() => setFormData(p => ({ ...p, family_income: inc.toString() }))}
                      className="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-600 text-[11px]"
                    >
                      ₹{(inc / 100000).toFixed(1)} Lakh
                    </button>
                  ))}
                </div>
              </div>

              <div className="bg-amber-50 border border-amber-200 rounded-xl p-3.5">
                <label className="flex items-start gap-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    name="other_scholarships"
                    checked={formData.other_scholarships}
                    onChange={handleChange}
                    className="w-4 h-4 text-amber-600 rounded border-amber-300 focus:ring-amber-500 mt-0.5"
                  />
                  <div className="text-xs text-amber-900">
                    <span className="font-semibold">I already receive another government scholarship or fee concession</span>
                    <p className="text-[11px] text-amber-700 mt-0.5">
                      Note: Most central schemes (like CSSS) disallow double-benefiting across government schemes.
                    </p>
                  </div>
                </label>
              </div>
            </div>

            <div className="flex justify-between pt-4">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>

              <button
                type="button"
                onClick={handleEvaluate}
                disabled={loading}
                className="inline-flex items-center gap-2 px-7 py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                <span>{loading ? 'Evaluating Rules...' : 'Run Deterministic Evaluation'}</span>
              </button>
            </div>
          </div>
        )}

        {/* Step 4: Results Display */}
        {step === 4 && results && (
          <div className="space-y-6 animate-in fade-in duration-200">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-200">
              <div>
                <h3 className="text-lg font-bold text-slate-900">Eligibility Analysis Results</h3>
                <p className="text-xs text-slate-500">Evaluated against structured official government guidelines</p>
              </div>

              <button
                onClick={() => setStep(1)}
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-600 hover:text-brand-800 bg-brand-50 px-3 py-1.5 rounded-lg"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Edit Profile Information</span>
              </button>
            </div>

            {/* Summary Counters */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div 
                onClick={() => setActiveFilter('ALL')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                  activeFilter === 'ALL' ? 'border-brand-500 bg-brand-50/50 ring-2 ring-brand-100' : 'border-slate-200 bg-white hover:bg-slate-50'
                }`}
              >
                <span className="text-xs font-medium text-slate-500">Total Evaluated</span>
                <div className="text-xl font-bold text-slate-900 mt-1">{results.total_evaluated}</div>
              </div>

              <div 
                onClick={() => setActiveFilter('ELIGIBLE')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                  activeFilter === 'ELIGIBLE' ? 'border-emerald-500 bg-emerald-50/50 ring-2 ring-emerald-100' : 'border-slate-200 bg-white hover:bg-slate-50'
                }`}
              >
                <span className="text-xs font-medium text-emerald-700">100% Eligible</span>
                <div className="text-xl font-bold text-emerald-700 mt-1">{results.eligible_count}</div>
              </div>

              <div 
                onClick={() => setActiveFilter('POTENTIALLY_ELIGIBLE')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                  activeFilter === 'POTENTIALLY_ELIGIBLE' ? 'border-amber-500 bg-amber-50/50 ring-2 ring-amber-100' : 'border-slate-200 bg-white hover:bg-slate-50'
                }`}
              >
                <span className="text-xs font-medium text-amber-700">Potentially Eligible</span>
                <div className="text-xl font-bold text-amber-700 mt-1">{results.potentially_eligible_count}</div>
              </div>

              <div 
                onClick={() => setActiveFilter('INELIGIBLE')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                  activeFilter === 'INELIGIBLE' ? 'border-rose-500 bg-rose-50/50 ring-2 ring-rose-100' : 'border-slate-200 bg-white hover:bg-slate-50'
                }`}
              >
                <span className="text-xs font-medium text-rose-700">Ineligible</span>
                <div className="text-xl font-bold text-rose-700 mt-1">{results.ineligible_count}</div>
              </div>
            </div>

            {/* Schemes List with Accordion Details */}
            <div className="space-y-4">
              {filteredResults.map((scheme) => {
                const isExpanded = expandedScheme === scheme.scheme_id

                return (
                  <div 
                    key={scheme.scheme_id} 
                    className="border border-slate-200 rounded-xl overflow-hidden shadow-sm hover:border-slate-300 transition-all bg-white"
                  >
                    <div 
                      onClick={() => setExpandedScheme(isExpanded ? null : scheme.scheme_id)}
                      className="p-4 cursor-pointer flex flex-wrap items-center justify-between gap-3 bg-slate-50/50 hover:bg-slate-50"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                            scheme.match_status === 'ELIGIBLE' 
                              ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                              : scheme.match_status === 'POTENTIALLY_ELIGIBLE'
                              ? 'bg-amber-100 text-amber-800 border-amber-300'
                              : 'bg-rose-100 text-rose-800 border-rose-300'
                          }`}>
                            {scheme.match_status.replace('_', ' ')} ({scheme.match_percentage}%)
                          </span>
                          <span className="text-[11px] text-slate-500">{scheme.ministry_or_dept}</span>
                        </div>
                        <h4 className="text-sm font-bold text-slate-900">{scheme.scheme_name}</h4>
                        <p className="text-xs text-slate-600">{scheme.award_summary}</p>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="text-xs font-semibold text-brand-600">
                          {isExpanded ? 'Hide Criteria Details' : 'View Criteria Breakdown'}
                        </span>
                      </div>
                    </div>

                    {/* Detailed Condition Breakdown */}
                    {isExpanded && (
                      <div className="p-5 border-t border-slate-200 bg-white space-y-4 text-xs">
                        {/* Matched Conditions */}
                        {scheme.matched_conditions.length > 0 && (
                          <div>
                            <h5 className="font-bold text-emerald-800 mb-2 flex items-center gap-1.5">
                              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                              Matched Criteria ({scheme.matched_conditions.length})
                            </h5>
                            <div className="space-y-1.5 pl-5">
                              {scheme.matched_conditions.map((c, i) => (
                                <div key={i} className="text-slate-700">
                                  <strong>{c.criterion_description}:</strong> {c.explanation}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Failed Conditions */}
                        {scheme.failed_conditions.length > 0 && (
                          <div>
                            <h5 className="font-bold text-rose-800 mb-2 flex items-center gap-1.5">
                              <XCircle className="w-4 h-4 text-rose-600" />
                              Non-Matching Criteria ({scheme.failed_conditions.length})
                            </h5>
                            <div className="space-y-1.5 pl-5">
                              {scheme.failed_conditions.map((c, i) => (
                                <div key={i} className="text-rose-700">
                                  <strong>{c.criterion_description}:</strong> {c.explanation}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Unknown Conditions & Missing Questions */}
                        {scheme.unknown_conditions.length > 0 && (
                          <div className="bg-amber-50/70 p-3 rounded-lg border border-amber-200">
                            <h5 className="font-bold text-amber-900 mb-2 flex items-center gap-1.5">
                              <HelpCircle className="w-4 h-4 text-amber-600" />
                              Missing Information Needed:
                            </h5>
                            <ul className="list-disc list-inside space-y-1 text-amber-800">
                              {scheme.missing_information_questions.map((q, i) => (
                                <li key={i}>{q}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Official Document Citation Footer */}
                        <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-500">
                          <span className="flex items-center gap-1">
                            <FileText className="w-3.5 h-3.5 text-brand-600" />
                            Official Source: <code className="font-mono bg-slate-100 px-1 py-0.5 rounded text-slate-700">{scheme.official_source_doc}</code>
                          </span>

                          <a
                            href={scheme.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 font-semibold text-brand-600 hover:underline"
                          >
                            <span>Open Official Application Portal</span>
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>

            {/* Official Legal Disclaimer */}
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-500 leading-relaxed flex items-start gap-2.5">
              <ShieldAlert className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-700">Official Disclaimer:</strong> {results.results[0]?.disclaimer}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
