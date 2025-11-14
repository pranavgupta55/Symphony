# CLAUDE.md - Symphony AI Development Guide

## Project Overview

**Symphony AI** is a multi-modal market intelligence fusion platform for real-time financial earnings call analysis. The platform combines audio, video, text, and chart data through advanced AI to extract vocal biomarkers, detect CEO confidence and stress patterns, and provide comprehensive financial insights.

### Current Status
⚠️ **SPECIFICATION PHASE** - This repository currently contains the technical specification only. No implementation code exists yet. See `paper.pdf` for the complete 28-page technical specification.

### Key Capabilities (Planned)
- Real-time multi-modal analysis of financial earnings calls
- Vocal biomarker extraction (pitch, energy, MFCCs, prosodic features)
- CEO confidence and stress pattern detection
- Claude API integration with 1M token context window
- 90% cost savings through prompt caching
- 250-500ms end-to-end latency
- Chart-statement verification and inconsistency detection

---

## Technical Architecture

### Core Components

1. **Audio Processing Pipeline**
   - 16kHz mono audio with PyAudio streaming (64ms latency)
   - WhisperStreaming for transcription (3.3s lag)
   - librosa for paralinguistic feature extraction (MFCCs, pitch, prosody, jitter, shimmer)

2. **Text Analysis Engine**
   - FinBERT financial sentiment models (74.88% accuracy with audio)
   - Linguistic feature extraction
   - Forced alignment for transcript synchronization
   - Hierarchical discourse analysis (Q&A vs prepared statements)

3. **Multi-Modal Fusion Module**
   - Hybrid fusion architecture (early + late fusion)
   - Cross-modal attention mechanisms
   - Inconsistency detection between verbal statements and charts
   - Synchronized buffers across modalities (100ms tolerance)

4. **Claude API Integration Layer**
   - Server-Sent Events (SSE) streaming
   - Extended thinking mode (32K token budget)
   - Prompt caching ($15/day → $1.70/day savings)
   - 1M token context windows
   - Vision API for chart analysis
   - MCP protocol for financial data

5. **Data Storage Architecture**
   - PostgreSQL: metadata and relational data
   - S3/CloudFlare R2: audio/video assets with lifecycle policies
   - Vector databases (Pinecone): semantic search
   - Redis: hot data caching and session management
   - 7-year historical data retention

### Technology Stack

#### Backend
- **FastAPI** with async support (2-3x throughput vs Flask)
- **Python 3.9+** for audio and ML pipelines
- **Node.js with Bun.js** for real-time services
- **Docker + Kubernetes** for orchestration (100+ concurrent streams)

#### Frontend
- **Next.js 15** App Router with native streaming
- **React 18.3** with Server Components
- **Zustand** for state management (3KB bundle)
- **shadcn/ui** component library (Radix UI primitives)
- **Wavesurfer.js** for interactive audio waveforms
- **Recharts** for financial visualizations

#### Machine Learning
- **PyTorch 2.1** with torch.compile optimization
- **HuggingFace Transformers 4.35** for pre-trained models
- **faster-whisper** for 4-5x transcription speedup
- **scikit-learn** for classical ML algorithms
- **MLflow** for experiment tracking

---

## Project Structure (Planned)

```
symphony/
├── backend/
│   ├── audio_service/          # Audio processing microservice
│   │   ├── capture.py          # PyAudio streaming
│   │   ├── features.py         # MFCC, pitch, prosody extraction
│   │   ├── vad.py              # Voice Activity Detection
│   │   └── whisper_stream.py  # Real-time transcription
│   ├── text_service/           # Text analysis microservice
│   │   ├── sentiment.py        # FinBERT integration
│   │   ├── linguistic.py       # Feature extraction
│   │   └── alignment.py        # Forced alignment
│   ├── fusion_service/         # Multi-modal fusion
│   │   ├── attention.py        # Cross-modal attention
│   │   ├── synchronizer.py    # Temporal sync
│   │   └── inconsistency.py   # Chart-statement verification
│   ├── claude_service/         # Claude API integration
│   │   ├── client.py           # API client with caching
│   │   ├── streaming.py        # SSE implementation
│   │   └── mcp_connector.py   # Financial data MCP
│   └── api/                    # FastAPI gateway
│       ├── main.py
│       ├── routes.py
│       └── models.py
├── frontend/
│   ├── app/                    # Next.js 15 App Router
│   │   ├── api/                # API routes
│   │   ├── components/         # React components
│   │   └── page.tsx
│   ├── lib/
│   │   ├── store.ts            # Zustand state management
│   │   └── hooks.ts            # Custom hooks (useSSEStream)
│   └── components/
│       ├── AudioPlayer.tsx     # Wavesurfer.js integration
│       ├── TranscriptView.tsx  # Synchronized transcript
│       └── SentimentChart.tsx  # Recharts visualizations
├── ml/
│   ├── models/                 # ML model definitions
│   ├── training/               # Training scripts
│   └── inference/              # Inference pipelines
├── infra/
│   ├── docker/                 # Dockerfiles
│   ├── k8s/                    # Kubernetes manifests
│   └── terraform/              # Infrastructure as Code
├── tests/
│   ├── unit/
│   ├── integration/
│   └── performance/
├── docs/
│   ├── api/                    # API documentation
│   └── architecture/           # Architecture diagrams
├── .gitignore
├── LICENSE
├── README.md
├── CLAUDE.md                   # This file
└── paper.pdf                   # Technical specification
```

---

## Development Workflow

### Phase 1: MVP Foundation (Weeks 1-4)

**Week 1: Audio Pipeline**
- Set up Python 3.9+ environment
- Implement PyAudio audio capture (16kHz, 1024 buffer)
- Extract MFCCs using librosa
- Deploy basic FastAPI server

**Week 2: Transcription & Text Analysis**
- Integrate faster-whisper for transcription
- Implement prosodic feature extraction (pitch, energy, speech rate)
- Integrate FinBERT for sentiment analysis
- Create transcript preprocessing pipeline

**Week 3: Early Fusion & API**
- Implement early fusion (audio + text features)
- Train baseline sentiment classifier
- Develop FastAPI endpoints (`POST /analyze`)
- Build simple Streamlit UI for testing

**Week 4: Integration & Demo**
- Create demo dataset (10-20 earnings calls)
- Integration testing
- Optimize for <5 minutes per call
- Prepare demonstration

**MVP Success Criteria:**
- Process one earnings call in <5 minutes
- 60%+ sentiment classification accuracy
- API response time <2 seconds
- End-to-end functionality demonstrated

### Phase 2: Advanced Features (Weeks 5-12)
- Cross-modal attention fusion architecture
- Speaker diarization (pyannote.audio)
- Voice quality metrics (jitter, shimmer, HNR)
- Claude API integration with caching
- Vision API for chart analysis
- Next.js frontend with SSE streaming

### Phase 3: Production Deployment (Weeks 13-16)
- Kubernetes cluster setup
- Docker containerization
- CI/CD with GitHub Actions
- Monitoring (Prometheus, Grafana)
- Security audit & penetration testing

### Phase 4: Scale & Optimize (Months 5-6)
- Advanced deception detection
- Comparative analysis across quarters
- Custom fine-tuned models
- Scale to 1000+ concurrent users

---

## Key Development Conventions

### Code Style
- **Python**: PEP 8, type hints (Python 3.9+), docstrings for all public functions
- **TypeScript**: Strict mode, ESLint with Airbnb config
- **Naming**: snake_case (Python), camelCase (TypeScript/JavaScript)

### Git Workflow
- **Main branch**: `main` (protected, production-ready)
- **Development**: Create feature branches `feature/description`
- **Commits**: Conventional commits format
  - `feat: add audio feature extraction`
  - `fix: resolve synchronization bug`
  - `docs: update API documentation`

### Testing Requirements
- **Unit tests**: 80%+ code coverage
- **Integration tests**: End-to-end pipeline validation
- **Performance tests**: Latency <500ms, throughput benchmarks
- **Run tests before commits**: `pytest` (Python), `jest` (TypeScript)

### API Design
- **REST principles**: Resource-based URLs
- **Versioning**: `/api/v1/`
- **Error handling**: Standard HTTP status codes + JSON error messages
- **Authentication**: JWT tokens for API access
- **Rate limiting**: 1000 requests/hour per API key

### Documentation
- **API docs**: OpenAPI/Swagger specification
- **Code comments**: Explain "why", not "what"
- **Architecture docs**: Mermaid diagrams in markdown
- **Update CLAUDE.md**: When making architectural changes

---

## Claude API Integration Best Practices

### Prompt Caching (90% Cost Reduction)
```python
# Cache static context (historical financial data)
system=[
    {"type": "text", "text": "You are a financial analyst..."},
    {
        "type": "text",
        "text": large_financial_dataset,  # 100K+ tokens
        "cache_control": {"type": "ephemeral"}
    }
]
```

**Caching Guidelines:**
- Minimum 1,024 tokens for Sonnet/Opus
- Maximum 4 cache breakpoints per request
- Hierarchical caching: tools → system → messages
- 5-minute TTL (standard) or 1-hour (extended with header)

### Extended Thinking Mode
```python
thinking={"type": "enabled", "budget_tokens": 16000}
```

**Use cases:**
- Complex financial modeling
- Multi-variable analysis
- Strategic planning with interconnected decisions
- Deep reasoning for earnings analysis

### 1M Token Context Window
```python
# Requires header: anthropic-beta: context-1m-2025-08-07
# Premium pricing for >200K tokens
```

**Optimization:**
- Keep under 200K for standard pricing when possible
- Selective context loading (only relevant data)
- Compress non-critical historical context
- Use Files API for large dataset uploads

### Streaming with SSE
```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Why SSE over WebSocket:**
- Unidirectional streaming (perfect for AI responses)
- Serverless compatible (Vercel, AWS Lambda)
- Automatic reconnection
- Works through firewalls/proxies
- Simpler implementation

### Vision API for Charts
```python
# Support: JPEG, PNG, GIF, WebP
# Max: 100 images/request (20 on claude.ai)
# Optimal: 1.15 megapixels
# Cost: ~$0.004/image with Sonnet
```

---

## Performance Targets

### Latency Requirements
- **End-to-end**: <500ms for real-time streaming
- **Audio buffer**: 32-64ms (PyAudio)
- **Feature extraction**: 300ms per minute of audio
- **Whisper transcription**: 0.15 RTF on GPU (6.6x realtime)
- **Claude API first token**: 200-500ms
- **Claude streaming**: 20-50 tokens/second

### Throughput Targets
- **Concurrent calls**: 100+ with horizontal scaling
- **API capacity**: 1000 requests/second
- **Uptime**: 99.9% (43 minutes downtime/month)
- **95th percentile response**: <2 seconds

### Resource Requirements
- **Audio processing node**: 4 CPU cores, 16GB RAM
- **Whisper node**: 1 GPU (T4+), 5GB memory for large-v2
- **API server**: 8 CPU cores, 32GB RAM
- **Storage**: 100GB SSD per processing node

---

## Audio Analysis Implementation Details

### Feature Extraction
**MFCCs (Mel-Frequency Cepstral Coefficients)**
```python
import librosa
mfcc = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=20, n_fft=2048, hop_length=512)
```
- 13-20 coefficients
- 2048 n_fft, 512 hop_length
- Processing: 50ms per minute of audio

**Pitch Tracking**
```python
f0, voiced_flag, voiced_probs = librosa.pyin(audio, fmin=65, fmax=400, sr=16000)
```
- 65-400 Hz range (human speech)
- More robust than piptrack for speech
- Extract: mean, std, range, coefficient of variation

**Voice Quality Indicators**
- **Jitter**: Pitch period variability (mean absolute diff / mean F0)
- **Shimmer**: Amplitude variability
- **HNR**: Harmonics-to-noise ratio (HPSS separation)
- **ZCR**: Zero-crossing rate

### Vocal Stress Detection
**Validated Acoustic Correlates:**
- F0 increase of 10-20 Hz under stress (most reliable)
- F1/F2 formant decrease >50 Hz (vocal tract tension)
- Increased RMS energy during arousal
- Higher F0 variability
- Decreased HNR (more aperiodic energy)

**Important:** Commercial Voice Stress Analysis achieves only 50% accuracy. Use speaker-specific baselines!

### Confidence Scoring Model
Multi-factor approach (weighted):
1. **F0 stability** (25%): Lower coefficient of variation = higher confidence
2. **Energy consistency** (20%)
3. **Optimal speech rate** (15%): ~155 WPM ideal
4. **Low hesitation rate** (20%): Filled pauses, silent pauses
5. **Appropriate pitch range** (10%): 100-150 Hz
6. **Voice quality HNR** (10%)

**Scoring:**
- >0.7: High confidence
- 0.4-0.7: Medium confidence
- <0.4: Low confidence

---

## Security & Compliance

### API Key Management
- Store in environment variables (never commit)
- Rotate quarterly or after suspected compromise
- Least privilege access for service accounts
- Separate keys for dev/staging/production

### Data Protection
- Encrypt audio files at rest (AES-256)
- TLS 1.3 for all network communication
- Anonymize PII in logs
- SOC 2 Type II compliance for enterprise

### Access Control
- Role-based access control (RBAC): read-only, analyst, admin
- Multi-factor authentication for production
- Log all data access for audit trails
- IP whitelisting for sensitive endpoints

---

## Monitoring & Observability

### Key Metrics
- Requests per second, error rates by endpoint
- 50th, 95th, 99th percentile latencies
- Model prediction confidence distributions (drift detection)
- Audio processing queue depth (capacity indicator)
- Cache hit rates (cost optimization)

### Alerting Thresholds
- API error rate >5% for 5 minutes
- Audio processing lag >10 minutes
- Claude API rate limit >80% of quota
- Database connection pool exhaustion
- Disk space >85% capacity

### Distributed Tracing
- OpenTelemetry for request tracing
- Correlation IDs across all requests
- Service dependency visualization (Grafana)

---

## Testing Strategy

### Unit Tests
- All feature extraction functions with sample audio
- Data preprocessing and normalization
- Error handling for edge cases (corrupted audio, empty transcripts)
- 80%+ code coverage
- Run time: <5 minutes for CI/CD

### Integration Tests
- End-to-end pipeline (audio → analysis)
- API endpoints with realistic payloads
- Database transactions and rollbacks
- External API integrations (Claude, financial data)
- Run daily on staging

### Performance Tests
- Load test: 1000 concurrent requests
- Stress test: 100 simultaneous calls
- Memory usage under sustained load
- Auto-scaling trigger validation
- Run weekly on production-like infrastructure

### Behavioral Tests
- Model stability across demographics (gender, accent)
- Fairness metrics for protected attributes
- Model explanation consistency
- Graceful degradation when features missing
- Quarterly bias audits

---

## Cost Optimization

### Claude API Savings
**Prompt Caching:** $15/day → $1.70/day (88.7% savings)
- Cache write: 1.25x base ($3.75/M for Sonnet 4.5)
- Cache read: 0.1x base ($0.30/M)
- 5-minute TTL (standard), 1-hour extended

**Batch API:** 50% discount on input + output
- Process historical earnings calls
- Up to 10,000 requests or 32MB per batch
- 24-hour processing window
- Combined with caching: up to 95% total savings

**Context Management:**
- Keep under 200K tokens for standard pricing
- Structured JSON output (reduces tokens vs prose)
- Summarize old context beyond 100K tokens

### Infrastructure Optimization
- Spot instances for batch processing (60-70% savings)
- Auto-scaling based on demand
- S3 Intelligent-Tiering for storage
- Reserved instances for baseline capacity (40% savings)
- Cost allocation tags for tracking

---

## Data Sources & Integration

### Earnings Call Providers
- **AlphaStreet**: Real-time and historical transcripts
- **S&P Capital IQ Transcripts**: 10-year history, comprehensive coverage
- **FactSet Transcripts**: Structured data with speaker identification
- **Bloomberg Terminal**: API access with audio/transcript

### Financial Data APIs
- **FactSet API**: Fundamentals, estimates, ownership data
- **S&P Capital IQ API**: Company info, financials, OAuth 2.0
- **Morningstar Direct**: Equity research, fund performance

### MCP (Model Context Protocol) Connectors
```python
from mcp import Server, Tool

@server.tool()
async def get_company_fundamentals(ticker: str, metrics: list[str]) -> dict:
    """Retrieve company fundamentals from FactSet"""
    # Implementation
```

---

## Deployment Configuration

### Docker Containerization
- Separate containers per microservice
- Multi-stage builds (minimize image size)
- Layer caching for faster rebuilds

### Kubernetes Configuration
- 3 replicas minimum per service (high availability)
- Horizontal pod autoscaling (CPU 70% threshold + custom metrics)
- Resource requests/limits to prevent exhaustion
- Readiness/liveness probes for health checking
- Kubernetes secrets for sensitive config

### Cloud Infrastructure (AWS Example)
- **EKS**: Kubernetes orchestration
- **S3**: Audio/video storage with lifecycle policies
- **RDS PostgreSQL**: Metadata (multi-AZ)
- **ElastiCache Redis**: Caching and sessions
- **CloudFront**: CDN for global delivery
- **ALB**: Application Load Balancer

---

## AI Assistant Guidelines

### When Working on This Project

1. **Always reference the technical specification** in `paper.pdf` for implementation details

2. **Start with MVP features** before advanced functionality:
   - Audio capture and basic feature extraction
   - Whisper transcription
   - Simple sentiment analysis
   - Basic API endpoint

3. **Follow the phased implementation roadmap**:
   - Phase 1 (Weeks 1-4): MVP Foundation
   - Phase 2 (Weeks 5-12): Advanced Features
   - Phase 3 (Weeks 13-16): Production Deployment
   - Phase 4 (Months 5-6): Scale & Optimize

4. **Prioritize real-time performance**:
   - Keep latency under 500ms
   - Use streaming where possible
   - Implement proper buffering and chunking

5. **Optimize Claude API costs**:
   - Always use prompt caching for repeated context
   - Use batch API for historical analysis
   - Structure prompts for JSON output

6. **Write production-ready code**:
   - Type hints and docstrings
   - Error handling with graceful degradation
   - Comprehensive logging with correlation IDs
   - Unit tests for all new functions

7. **Consider multi-modal synchronization**:
   - Maintain 100ms tolerance across modalities
   - Implement forced alignment for accuracy
   - Use timestamps for all data streams

8. **Security first**:
   - Never commit API keys or secrets
   - Encrypt sensitive data at rest
   - Use TLS for all network communication
   - Implement proper access control

### When Implementing New Features

1. **Create a design document** outlining:
   - Problem statement
   - Proposed solution
   - Performance implications
   - Testing strategy

2. **Update this CLAUDE.md** when making architectural changes

3. **Add tests** before marking feature as complete:
   - Unit tests (80%+ coverage)
   - Integration tests
   - Performance benchmarks

4. **Document APIs** using OpenAPI/Swagger specifications

### Common Pitfalls to Avoid

❌ **Don't** skip the MVP phase and jump to advanced features
❌ **Don't** ignore latency requirements (500ms target)
❌ **Don't** forget prompt caching (wastes 90% of API costs)
❌ **Don't** process audio synchronously (blocks the pipeline)
❌ **Don't** neglect error handling (multi-modal systems are complex)
❌ **Don't** commit secrets or API keys to version control
❌ **Don't** use WebSocket when SSE is sufficient
❌ **Don't** over-engineer before validating core functionality

---

## Quick Start Commands

### Development Environment Setup
```bash
# Python environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Node.js frontend
cd frontend
npm install
npm run dev

# Docker development
docker-compose up --build

# Run tests
pytest tests/
npm test
```

### Production Deployment
```bash
# Build Docker images
docker build -t symphony-audio:latest ./backend/audio_service
docker build -t symphony-frontend:latest ./frontend

# Deploy to Kubernetes
kubectl apply -f infra/k8s/

# Check deployment
kubectl get pods -n symphony
kubectl logs -f <pod-name> -n symphony
```

---

## Resources

### Documentation
- **Technical Specification**: `paper.pdf` (28 pages, comprehensive)
- **Claude API Docs**: https://docs.anthropic.com
- **Whisper Streaming**: https://github.com/ufal/whisper_streaming
- **librosa Documentation**: https://librosa.org/doc/latest/
- **Next.js 15 Docs**: https://nextjs.org/docs

### Key Papers & Research
- Vocal stress analysis research (Nature, IEEE Xplore, PubMed)
- Multi-modal fusion architectures (arXiv)
- Financial sentiment analysis (FinBERT, ScienceDirect)

### Community & Support
- GitHub Issues: Report bugs and request features
- Development Team: Cross-functional team (audio, NLP, ML, backend, frontend)

---

## License

MIT License - Copyright (c) 2025 Pranav Gupta

See `LICENSE` file for full details.

---

## Changelog

### 2025-01-14 - Initial Specification
- Created comprehensive technical specification (paper.pdf)
- Defined architecture and technology stack
- Established phased implementation roadmap
- Created CLAUDE.md for AI assistant guidance

---

**Last Updated**: 2025-01-14
**Document Version**: 1.0.0
**Status**: Specification Phase - No implementation yet

For questions or clarifications, refer to the detailed technical specification in `paper.pdf`.
