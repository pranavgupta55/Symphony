# 🎵 Symphony AI

**Multi-Modal Financial Analysis Platform for Earnings Calls**

Symphony AI combines audio biomarker extraction, financial sentiment analysis, and chart verification to provide comprehensive insights into earnings calls. Detect deception, assess confidence, and uncover hidden risks using cutting-edge AI.

---

## ✨ Key Features

### 🎤 Vocal Biomarker Analysis
- **MFCC Extraction**: 13-20 Mel-frequency cepstral coefficients
- **Pitch Tracking**: F0 extraction using pyin algorithm
- **Voice Quality**: Jitter, shimmer, and HNR measurements
- **Confidence Detection**: Real-time confidence scoring from vocal patterns
- **Stress Indicators**: Automatic detection of hesitation and nervousness

### 📊 Financial Sentiment Analysis
- **FinBERT Model**: State-of-the-art financial sentiment classifier (74.88% accuracy)
- **Speaker Diarization**: Separate CEO, CFO, and analyst segments
- **Discourse Analysis**: Distinguish prepared statements from Q&A
- **Topic Extraction**: Identify key financial themes and metrics

### 📈 Chart Analysis
- **Claude Vision API**: Analyze financial charts and graphs
- **Data Extraction**: Pull key numbers and trends from visuals
- **Inconsistency Detection**: Compare verbal statements with chart data
- **Cross-Modal Verification**: Flag discrepancies between speech and visuals

### 🤖 AI-Powered Insights
- **Claude 3.5 Sonnet**: Advanced reasoning with extended thinking mode
- **Multi-Modal Fusion**: Combine audio, text, and visual data
- **Risk Assessment**: Comprehensive risk level calculation
- **Executive Summary**: Clear, actionable investment insights

---

## 🏗️ Architecture

```
Symphony AI
├── Backend (FastAPI)
│   ├── Audio Processing (Whisper + librosa)
│   ├── Feature Extraction (MFCCs, pitch, prosodic features)
│   ├── Sentiment Analysis (FinBERT)
│   ├── Chart Analysis (Claude Vision)
│   ├── Multi-Modal Fusion
│   └── Claude AI Integration
│
├── Frontend (React + Vite)
│   ├── Upload Interface
│   ├── Confidence Timeline (Recharts)
│   ├── Transcript Viewer
│   └── Results Dashboard
│
└── ML Models
    ├── FinBERT (HuggingFace)
    ├── Whisper (OpenAI)
    └── Claude 3.5 Sonnet (Anthropic)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **API Keys**:
  - [Anthropic API Key](https://console.anthropic.com/)
  - [OpenAI API Key](https://platform.openai.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/symphony-ai.git
cd Symphony
```

### 2. Configure API Keys

Edit `backend/.env` and add your API keys:

```bash
ANTHROPIC_API_KEY=your-anthropic-key-here
OPENAI_API_KEY=your-openai-key-here
```

### 3. Start the Backend

```bash
# Option 1: Use the startup script
./start-backend.sh

# Option 2: Manual setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

The backend will start at `http://localhost:8000`

### 4. Start the Frontend

In a **new terminal**:

```bash
# Option 1: Use the startup script
./start-frontend.sh

# Option 2: Manual setup
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:5173`

### 5. Open Your Browser

Navigate to `http://localhost:5173` and start analyzing earnings calls!

---

## 📖 Usage Guide

### Analyzing an Earnings Call

1. **Upload Audio**: Drag and drop or select an earnings call audio file (MP3, WAV, M4A)
2. **Add Charts (Optional)**: Upload financial charts or graphs (PNG, JPG)
3. **Provide Context (Optional)**: Enter company name and additional context
4. **Analyze**: Click "Analyze Earnings Call" and wait for processing

### Understanding Results

#### Overview Tab
- **Confidence Timeline**: Visual representation of executive confidence over time
- **Key Insights**: Automatically extracted insights from multi-modal fusion
- **Discrepancies**: Cross-modal inconsistencies flagged by the system

#### Transcript Tab
- **Color-Coded Segments**: Green (positive), Yellow (neutral), Red (negative)
- **Speaker Labels**: CEO, CFO, Analyst identification
- **Timestamps**: Precise timing for each segment

#### Confidence Analysis Tab
- **Vocal Confidence Chart**: Line graph showing confidence scores
- **Stress Indicators**: Detected vocal stress patterns with descriptions

#### AI Analysis Tab
- **Executive Summary**: 2-3 paragraph overview
- **Risk Indicators**: Specific risks identified
- **Opportunities**: Positive signals and growth areas
- **Red Flags**: Critical concerns requiring attention
- **Confidence Assessment**: Management credibility evaluation
- **Overall Recommendation**: Bullish/Bearish/Neutral perspective

---

## 🛠️ Development

### Project Structure

```
Symphony/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Configuration
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   │       ├── audio_transcription.py
│   │       ├── audio_features.py
│   │       ├── sentiment_analysis.py
│   │       ├── chart_analysis.py
│   │       ├── fusion.py
│   │       ├── claude_integration.py
│   │       └── orchestrator.py
│   ├── uploads/              # Uploaded files
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── components/       # React components
│   │   ├── store/            # Zustand state management
│   │   └── App.jsx
│   ├── package.json
│   └── .env
│
├── data/                     # Sample data
├── ml_models/                # Model utilities
└── README.md
```

### API Endpoints

- `POST /api/analyze` - Upload and analyze earnings call
- `GET /api/status/{job_id}` - Check processing status
- `GET /api/results/{job_id}` - Retrieve analysis results
- `GET /api/jobs` - List all jobs
- `DELETE /api/jobs/{job_id}` - Delete a job
- `GET /api/audio/{job_id}` - Download audio file

### Adding New Features

1. **Backend Service**: Add to `backend/app/services/`
2. **Frontend Component**: Add to `frontend/src/components/`
3. **Update Orchestrator**: Modify `backend/app/services/orchestrator.py`
4. **Update UI**: Modify `frontend/src/App.jsx` or relevant component

---

## 📊 Performance

- **Transcription**: ~3-5 seconds for 10-minute audio (Whisper API)
- **Feature Extraction**: ~2-3 seconds (librosa)
- **Sentiment Analysis**: ~1-2 seconds (FinBERT on CPU)
- **Chart Analysis**: ~5-10 seconds per chart (Claude Vision)
- **AI Analysis**: ~10-15 seconds (Claude 3.5 with thinking)

**Total Processing Time**: ~30-60 seconds for a complete 10-minute earnings call

---

## 🎯 Use Cases

1. **Investment Research**: Analyze management credibility before making investment decisions
2. **Due Diligence**: Detect red flags in acquisitions or partnerships
3. **Compliance**: Monitor for misleading statements or misrepresentations
4. **Financial Journalism**: Uncover hidden insights in earnings calls
5. **Academic Research**: Study vocal patterns in financial communications

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI Whisper**: State-of-the-art speech recognition
- **Anthropic Claude**: Advanced AI reasoning and vision
- **FinBERT**: Financial sentiment analysis (ProsusAI)
- **librosa**: Audio analysis library
- **FastAPI**: Modern Python web framework
- **React + Vite**: Fast frontend development

---

## 📞 Support

For questions, issues, or feature requests, please refer to the [paper.pdf](paper.pdf) for technical details.

---

**Built with ❤️ by the Symphony AI Team**

*Detect deception. Uncover truth. Invest confidently.*
