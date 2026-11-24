# LegalEase 🇮🇳 
### AI-Powered Government Scheme & Scholarship Navigator for Indian Citizens & Students

LegalEase is a full-stack, production-grade AI platform that empowers Indian citizens and students to discover potentially relevant government schemes, evaluate strict eligibility criteria deterministically, understand required documents, and access authentic application sources with verifiable citations.

Unlike generic chatbot wrappers, LegalEase features a **genuine, multi-stage Retrieval-Augmented Generation (RAG) pipeline** backed by official guidelines from the **National Scholarship Portal (NSP)**, **Ministry of Education**, and **State Welfare Departments**.

---

## 🏛️ Core RAG Architecture & Technology Stack

| Stage | Technology | Implementation Details |
|---|---|---|
| **Project Name** | **LegalEase** | Renamed and upgraded across backend and frontend |
| **PDF Extraction** | **Unstructured** | `unstructured.partition.pdf.partition_pdf` (with fast strategy and page metadata extraction) |
| **Text Splitting** | **CharacterTextSplitter** | `langchain_text_splitters.CharacterTextSplitter` (chunk size: 600, overlap: 100, separator: `\n`) |
| **Embeddings** | **Hugging Face Embeddings** | `langchain_huggingface.HuggingFaceEmbeddings` with `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| **Vector Storage** | **FAISS** | `langchain_community.vectorstores.FAISS` (persisted on-disk with automatic index reloading) |
| **Retrieval** | **FAISS Similarity Search** | `Hugging Face Embeddings → FAISS Similarity Search` (`similarity_search_with_score`) |
| **Reranking** | **Cross-Encoder** | `sentence_transformers.CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")` |
| **Answer Generation** | **Google Gemini** | Google GenAI SDK (`google-genai`) with user's Gemini API key & direct straight-answer prompt engineering |
| **Eligibility Matching** | **Deterministic Engine** | Transparent rule comparator for income, category, domicile, education, and marks |
| **Frontend UI** | **React + Vite + Tailwind** | Modern SaaS interface with multilingual toggle (English, Hindi, Punjabi) |

---

## 📁 Project Structure

```
LegalEase/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx           # Grounded conversational interface
│   │   │   ├── SchemeCard.jsx           # Scheme display card with match badges
│   │   │   ├── SourceCitation.jsx       # Page-level document citation badges
│   │   │   ├── EligibilityForm.jsx      # Multi-step deterministic matching wizard
│   │   │   ├── SchemeModal.jsx          # Comprehensive scheme breakdown modal
│   │   │   ├── DocumentUploadModal.jsx  # Knowledge base expansion upload modal
│   │   │   └── Navbar.jsx               # Navigation bar & live status
│   │   ├── pages/
│   │   │   ├── Home.jsx                 # Landing page & how it works
│   │   │   ├── Dashboard.jsx            # Scheme discovery & application roadmap
│   │   │   └── Assistant.jsx            # AI Navigator workspace & document index
│   │   ├── App.jsx                      # Main React application
│   │   ├── main.jsx                     # Vite entrypoint
│   │   └── index.css                    # Tailwind CSS definitions
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py                  # POST /api/chat
│   │   │   ├── schemes.py               # GET /api/schemes, GET /api/schemes/{id}
│   │   │   ├── eligibility.py           # POST /api/eligibility/check
│   │   │   └── documents.py             # POST /api/documents/upload, GET /api/sources/{id}
│   │   ├── rag/
│   │   │   ├── ingestion.py             # Unstructured PDF extraction & page metadata
│   │   │   ├── chunking.py              # CharacterTextSplitter text chunking
│   │   │   ├── embeddings.py            # Hugging Face Embeddings service
│   │   │   ├── retrieval.py             # FAISS vector storage & similarity search
│   │   │   ├── reranking.py             # Cross-Encoder Reranker
│   │   │   ├── generation.py            # Gemini Grounded generation with direct answers
│   │   │   ├── pipeline.py              # End-to-end RAG orchestrator
│   │   │   └── evaluation.py            # Precision, Recall & Faithfulness metrics
│   │   ├── services/
│   │   │   └── eligibility_engine.py    # Deterministic rule evaluation
│   │   ├── config.py                    # Environment & settings management
│   │   └── main.py                      # FastAPI application entrypoint
│   ├── data/
│   │   ├── raw/                         # Official Government Scheme PDFs
│   │   └── processed/faiss_index/       # FAISS on-disk vector index
│   ├── tests/
│   │   └── test_api.py                  # Automated test suite (9 tests)
│   ├── demo_terminal.py                 # Interactive terminal showcase script
│   ├── requirements.txt
│   └── .env
└── README.md
```

---

## 🚀 How to Run and Test LegalEase

### Step 1: Start the Backend (Terminal 1)
```powershell
cd D:\Code\SATWINNER\LegalEase\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Access API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

### Step 2: Start the Frontend (Terminal 2)
```powershell
cd D:\Code\SATWINNER\LegalEase\frontend
npm run dev -- --port 5173
```
- Open browser at `http://localhost:5173`

### Step 3: Run the Terminal Interactive Demo (Terminal 3)
```powershell
cd D:\Code\SATWINNER\LegalEase\backend
python demo_terminal.py
```

### Step 4: Run the Automated Unit Tests
```powershell
cd D:\Code\SATWINNER\LegalEase\backend
python -m unittest tests/test_api.py
```
*(All 9 tests verify health, scheme catalog, deterministic eligibility evaluation, FAISS retrieval, multilingual chat, and page-level citations).*

---

## 🌐 Push to GitHub & Enable GitHub Pages

The repository is configured for `Abhinav909-jpg/Sathack_winners` with automated GitHub Actions CI/CD (`.github/workflows/deploy.yml`).

### Step 1: Push Your Code to GitHub
In your terminal, run:
```powershell
cd D:\Code\SATWINNER\LegalEase
git push -u origin main
```

### Step 2: Enable GitHub Pages in 2 Clicks
1. Go to: [github.com/Abhinav909-jpg/Sathack_winners](https://github.com/Abhinav909-jpg/Sathack_winners)
2. Click **Settings** (top tab) $\rightarrow$ **Pages** (in the left sidebar).
3. Under **Build and deployment > Source**, select **GitHub Actions**.
4. That's it! GitHub Actions will build and deploy your live app at:
   **`https://abhinav909-jpg.github.io/Sathack_winners/`**

---

## ☁️ 24/7 Cloud Backend Deployment (Optional)

The frontend on GitHub Pages includes a built-in verified grounded scheme engine that functions 24/7 immediately. To connect it to your live Python FastAPI backend in the cloud:

1. Create a free account on [Render.com](https://render.com) and link your GitHub account.
2. Click **New +** $\rightarrow$ **Web Service** $\rightarrow$ Select `Sathack_winners`.
3. Configure settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable**: `GEMINI_API_KEY` = your API key
4. Once deployed, add repository variable `VITE_API_URL` with your Render URL under GitHub Repo Settings $\rightarrow$ Secrets and variables $\rightarrow$ Actions.
