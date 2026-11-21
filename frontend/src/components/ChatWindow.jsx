import React, { useState, useRef, useEffect } from 'react'
import { Send, Globe, Bot, User, Sparkles, AlertCircle, RefreshCw, Loader2, ShieldCheck, ChevronRight, Mic, MicOff } from 'lucide-react'
import SourceCitation from './SourceCitation'
import { sendChatMessage } from '../services/api'

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: "Namaste! I am **LegalEase**, your official AI Government Scheme & Scholarship Navigator.\n\nI answer your questions strictly using verified guidelines from the **National Scholarship Portal (NSP)**, **Ministry of Education**, and **State Welfare Departments**.\n\nEvery factual answer includes **document citations and page numbers**. What scheme or scholarship would you like to explore today?",
      citations: [
        {
          document_name: "PM_USP_Central_Sector_Scholarship_Guidelines.pdf",
          page_number: 1,
          scheme_name: "PM-USP Central Sector Scholarship",
          source_url: "https://scholarships.gov.in",
          snippet: "Financial assistance to meritorious students from economically weaker families pursuing higher education."
        }
      ],
      suggested_follow_ups: [
        "What is the parental income limit for Central Sector Scholarship?",
        "What are the requirements for Post Matric Scholarship for SC in Punjab?",
        "How do I apply for the PM-YASASVI scholarship scheme?"
      ],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ])

  const [input, setInput] = useState('')
  const [language, setLanguage] = useState('en') // 'en', 'hi', 'pa'
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [isListening, setIsListening] = useState(false)
  const [speechError, setSpeechError] = useState(null)
  const recognitionRef = useRef(null)
  const messagesEndRef = useRef(null)

  // Web Speech API Voice-to-Text Initialization
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return

    const recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = true

    // Map selected language to regional speech locale
    if (language === 'hi') {
      recognition.lang = 'hi-IN'
    } else if (language === 'pa') {
      recognition.lang = 'pa-IN'
    } else {
      recognition.lang = 'en-IN'
    }

    recognition.onstart = () => {
      setIsListening(true)
      setSpeechError(null)
    }

    recognition.onresult = (event) => {
      let interimTranscript = ''
      let finalTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript
        } else {
          interimTranscript += event.results[i][0].transcript
        }
      }

      const spoken = finalTranscript || interimTranscript
      if (spoken) {
        setInput(spoken)
      }
    }

    recognition.onerror = (event) => {
      console.warn('Speech recognition error:', event.error)
      if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
        setSpeechError('Microphone permission was denied. Click the lock/tune icon in your address bar to Allow Microphone.')
      } else if (event.error === 'network') {
        setSpeechError('Speech recognition network error: If using Brave, enable Google Speech Services in settings, or try using Chrome/Edge with an active internet connection.')
      } else if (event.error === 'no-speech') {
        // Silent timeout when user doesn't speak, do not alarm
      } else if (event.error === 'aborted') {
        // User stopped listening
      } else {
        setSpeechError(`Voice input notice: ${event.error}`)
      }
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      try {
        recognition.abort()
      } catch (e) {}
    }
  }, [language])

  const toggleListening = async () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      setSpeechError('Voice input is not supported in this browser. Please use Google Chrome, Edge, or Safari.')
      return
    }

    if (isListening) {
      try {
        recognitionRef.current?.stop()
      } catch (e) {}
      setIsListening(false)
    } else {
      setSpeechError(null)
      try {
        // Pre-check / request mic permission explicitly
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            stream.getTracks().forEach(track => track.stop())
          } catch (micErr) {
            if (micErr.name === 'NotAllowedError' || micErr.name === 'PermissionDeniedError') {
              setSpeechError('Microphone permission was denied. Please allow microphone permissions in your browser URL bar.')
              return
            }
          }
        }
        recognitionRef.current?.start()
      } catch (err) {
        console.warn('Could not start recognition:', err)
        try {
          recognitionRef.current?.abort()
          recognitionRef.current?.start()
        } catch (e) {
          setSpeechError('Could not connect to microphone. Please check browser permissions.')
        }
      }
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const handleSend = async (queryText = null) => {
    const textToSend = queryText || input
    if (!textToSend.trim() || loading) return

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: textToSend.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    setMessages(prev => [...prev, userMessage])
    if (!queryText) setInput('')
    setLoading(true)
    setError(null)

    try {
      const data = await sendChatMessage(textToSend.trim(), language)

      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        citations: data.citations || [],
        confidence: data.confidence,
        suggested_follow_ups: data.suggested_follow_ups || [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err.message || 'Error communicating with LegalEase server.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-[750px] bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Chat Header */}
      <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-600 text-white flex items-center justify-center shadow-sm">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-slate-900 text-sm">LegalEase Assistant</h3>
              <span className="flex items-center gap-1 bg-emerald-100 text-emerald-800 text-[10px] font-semibold px-2 py-0.5 rounded-full">
                <ShieldCheck className="w-3 h-3 text-emerald-600" />
                Grounded RAG
              </span>
            </div>
            <p className="text-[11px] text-slate-500">Official Government Verified Information Only</p>
          </div>
        </div>

        {/* Language Selection Buttons */}
        <div className="flex items-center bg-slate-200/70 p-1 rounded-xl text-xs font-semibold">
          <button
            onClick={() => setLanguage('en')}
            className={`px-3 py-1 rounded-lg transition-all ${
              language === 'en'
                ? 'bg-white text-brand-700 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            English
          </button>
          <button
            onClick={() => setLanguage('hi')}
            className={`px-3 py-1 rounded-lg transition-all ${
              language === 'hi'
                ? 'bg-white text-brand-700 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            हिंदी
          </button>
          <button
            onClick={() => setLanguage('pa')}
            className={`px-3 py-1 rounded-lg transition-all ${
              language === 'pa'
                ? 'bg-white text-brand-700 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            ਪੰਜਾਬੀ
          </button>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center shrink-0 mt-1">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div className={`max-w-[85%] sm:max-w-[75%] flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-brand-600 text-white rounded-tr-none shadow-sm'
                    : 'bg-slate-50 text-slate-800 border border-slate-200/80 rounded-tl-none shadow-sm'
                }`}
              >
                {/* Message text with basic markdown formatting */}
                <div className="space-y-2 whitespace-pre-wrap">
                  {msg.content}
                </div>

                {/* Source Citations Section */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-slate-200/80">
                    <div className="flex items-center gap-1 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">
                      <ShieldCheck className="w-3.5 h-3.5 text-brand-600" />
                      <span>Verified Source Citations ({msg.citations.length})</span>
                    </div>
                    <div className="space-y-1.5">
                      {msg.citations.map((c, idx) => (
                        <SourceCitation key={idx} citation={c} index={idx} />
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Timestamp */}
              <span className="text-[10px] text-slate-400 mt-1 px-1">
                {msg.timestamp}
              </span>

              {/* Follow-up suggestions */}
              {msg.suggested_follow_ups && msg.suggested_follow_ups.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2.5">
                  {msg.suggested_follow_ups.map((q, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSend(q)}
                      className="inline-flex items-center gap-1 text-[11px] bg-slate-100 hover:bg-brand-50 text-slate-600 hover:text-brand-700 border border-slate-200 hover:border-brand-300 px-3 py-1.5 rounded-full transition-all text-left"
                    >
                      <Sparkles className="w-3 h-3 text-brand-500 shrink-0" />
                      <span>{q}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-slate-800 text-white flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {/* Loading state */}
        {loading && (
          <div className="flex gap-3.5 justify-start">
            <div className="w-8 h-8 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center shrink-0 mt-1">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-slate-50 border border-slate-200 rounded-2xl rounded-tl-none p-4 max-w-[70%]">
              <div className="flex items-center gap-2 text-xs font-medium text-slate-600">
                <Loader2 className="w-4 h-4 text-brand-600 animate-spin" />
                <span>Searching official guidelines & retrieving verified citations...</span>
              </div>
              <div className="mt-2 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                <div className="h-full bg-brand-500 rounded-full animate-pulse w-3/4"></div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-500 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="p-4 bg-slate-50 border-t border-slate-200">
        {/* Active Speech Recognition Banner */}
        {isListening && (
          <div className="flex items-center justify-between gap-2 mb-2.5 px-3.5 py-2 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 shadow-sm animate-pulse">
            <div className="flex items-center gap-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-600"></span>
              </span>
              <span className="font-semibold">
                {language === 'hi'
                  ? 'सुन रहे हैं... कृपया छात्रवृत्ति या योजना के बारे में बोलें'
                  : language === 'pa'
                  ? 'ਸੁਣ ਰਹੇ ਹਾਂ... ਕਿਰਪਾ ਕਰਕੇ ਸਕੀਮ ਜਾਂ ਸਕਾਲਰਸ਼ਿਪ ਬਾਰੇ ਬੋਲੋ'
                  : 'Listening... Speak your scholarship or scheme question now'}
              </span>
            </div>
            <button
              type="button"
              onClick={toggleListening}
              className="text-xs font-bold text-rose-600 hover:text-rose-800 bg-rose-100 hover:bg-rose-200 px-2.5 py-0.5 rounded-md transition-colors"
            >
              Stop
            </button>
          </div>
        )}

        {speechError && (
          <div className="flex items-center justify-between gap-2 mb-2.5 px-3 py-1.5 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800">
            <span>{speechError}</span>
            <button onClick={() => setSpeechError(null)} className="text-amber-600 hover:text-amber-800 font-bold ml-2">×</button>
          </div>
        )}

        <div className="flex items-end gap-2 bg-white rounded-xl border border-slate-300 focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-200 p-2 transition-all">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              language === 'hi'
                ? "सरकारी छात्रवृत्ति या योजना के बारे में पूछें या माइक दबाकर बोलें..."
                : language === 'pa'
                ? "ਸਰਕਾਰੀ ਸਕੀਮ ਜਾਂ ਸਕਾਲਰਸ਼ਿਪ ਬਾਰੇ ਪੁੱਛੋ ਜਾਂ ਮਾਈਕ ਦਬਾ ਕੇ ਬੋਲੋ..."
                : "Ask about eligibility, documents, or deadlines (or click mic to speak)..."
            }
            rows={1}
            className="flex-1 resize-none text-xs sm:text-sm px-2 py-1.5 focus:outline-none text-slate-800 placeholder:text-slate-400 max-h-32"
          />

          {/* Voice to Text Button */}
          <button
            type="button"
            onClick={toggleListening}
            disabled={loading}
            className={`p-2.5 rounded-lg transition-all shrink-0 ${
              isListening
                ? 'bg-rose-600 text-white animate-pulse shadow-md shadow-rose-200 ring-2 ring-rose-400'
                : 'text-slate-500 hover:text-brand-600 hover:bg-slate-100'
            }`}
            title={isListening ? "Listening... Click to stop" : "Speak query (Voice-to-Text)"}
          >
            {isListening ? (
              <MicOff className="w-4 h-4 text-white" />
            ) : (
              <Mic className="w-4 h-4" />
            )}
          </button>

          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
            className="p-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 disabled:opacity-40 text-white transition-colors shrink-0 shadow-sm"
            title="Send Message"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 px-1">
          <span className="flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-brand-600" />
            Grounded in official Ministry guidelines & NSP regulations
          </span>
          <span className="hidden sm:inline">Press Enter to send</span>
        </div>
      </div>
    </div>
  )
}
