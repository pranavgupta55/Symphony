# 🎬 Symphony AI - Demo Guide

This guide will help you set up and run a demo of Symphony AI for showcasing its capabilities.

---

## 📋 Pre-Demo Checklist

### 1. API Keys Setup

Ensure you have both API keys configured in `backend/.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...  # Your actual Anthropic key
OPENAI_API_KEY=sk-...         # Your actual OpenAI key
```

**Getting API Keys:**
- **Anthropic Claude**: https://console.anthropic.com/
- **OpenAI**: https://platform.openai.com/api-keys

### 2. Install Dependencies

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

## 🚀 Running the Demo

### Step 1: Start Backend

In terminal 1:
```bash
./start-backend.sh
# OR manually:
cd backend && source venv/bin/activate && python -m app.main
```

Wait for: `🎵 Symphony AI started successfully!`

### Step 2: Start Frontend

In terminal 2:
```bash
./start-frontend.sh
# OR manually:
cd frontend && npm run dev
```

Frontend will open at: http://localhost:5173

---

## 🎯 Demo Flow

### Option 1: Use Your Own Audio (Recommended)

1. **Find an Earnings Call Recording**:
   - YouTube: Search for "earnings call" + company name
   - Company IR websites often have recordings
   - Download as MP3 or WAV (< 100MB)

2. **Optional: Prepare Charts**:
   - Screenshot quarterly earnings slides
   - Financial charts from earnings presentations
   - Save as PNG or JPG

### Option 2: Generate Sample Audio

If you don't have real audio, you can use text-to-speech:

**Using macOS `say` command:**
```bash
say -v Alex -o sample-earnings-call.m4a -f sample-script.txt
```

**Sample Script (save as `sample-script.txt`):**
```
Thank you for joining Tesla's Q4 2024 earnings call. I'm Elon Musk, CEO.

We had a fantastic quarter with record deliveries of 485,000 vehicles.
Revenue reached 25.2 billion dollars, up 3 percent year over year.

Our automotive gross margin improved to 18.9 percent, excluding credits.
This demonstrates the strength of our cost reduction initiatives.

Looking ahead, we expect vehicle deliveries to grow approximately 20 to 30 percent in 2025.

Now I'll hand it over to our CFO for the financial details.

Thank you, Elon. Operating expenses increased by 8 percent to 2.8 billion dollars.

Free cash flow for the quarter was 2.1 billion dollars, bringing our total cash to 29.1 billion.

We're confident in our ability to execute on our growth plans.

Now we'll take questions from analysts.
```

---

## 🎭 Presenting the Demo

### 1. Introduction (1-2 minutes)

"Symphony AI is a multi-modal financial analysis platform that analyzes earnings calls using three distinct approaches:

1. **Vocal Biomarkers**: We extract audio features like pitch, energy, and voice quality to detect confidence and stress
2. **FinBERT Sentiment**: A financial-tuned NLP model analyzes the sentiment and tone of statements
3. **Chart Analysis**: Using Claude's vision capabilities, we verify that charts match verbal claims

All three modalities are fused together, and Claude AI generates comprehensive investment insights."

### 2. Upload & Analysis (3-5 minutes)

**Show the Upload Interface:**
1. Drag and drop the audio file
2. Optionally upload 1-2 financial charts
3. Enter company name (e.g., "Tesla Inc.")
4. Add context: "Q4 2024 earnings call for electric vehicle manufacturer"
5. Click "Analyze Earnings Call"

**During Processing (30-60 seconds):**
Point out the progress indicator showing:
- Audio Transcription ✓
- Vocal Feature Extraction ✓
- Sentiment Analysis ✓
- Chart Analysis ✓
- Multi-Modal Fusion ✓
- AI Analysis Generation ✓

### 3. Results Walkthrough (5-7 minutes)

**Overview Tab:**
- Point out the summary cards: Confidence, Sentiment, Risk Level
- Explain the Confidence Timeline chart
- Highlight any discrepancies found

**Transcript Tab:**
- Show color-coded sentiment (green/yellow/red)
- Point out speaker identification (CEO, CFO, Analyst)
- Explain how timing is tracked

**Confidence Analysis Tab:**
- Show the vocal confidence chart over time
- Explain stress indicators (jitter, pitch variation, etc.)
- Discuss what low confidence might mean

**AI Analysis Tab:**
- Read the Executive Summary
- Review Risk Indicators
- Highlight any Red Flags
- Discuss the Overall Recommendation

**Download Results:**
- Show the JSON export functionality

### 4. Key Differentiators (1-2 minutes)

"What makes Symphony AI unique:

1. **Vocal Lie Detection**: Competitors only analyze text - we analyze HOW something is said, not just WHAT is said
2. **Cross-Modal Verification**: We catch when charts don't match verbal statements
3. **Financial-Specific Models**: FinBERT is trained on financial data, not general text
4. **Comprehensive AI Synthesis**: Claude combines all signals into actionable insights"

---

## 💡 Demo Tips

### Do's ✅
- Test the entire flow beforehand
- Have API keys loaded and tested
- Use a real earnings call if possible (more impressive)
- Prepare 2-3 talking points about each analysis section
- Have the paper.pdf ready to show technical details

### Don'ts ❌
- Don't use copyrighted music as "test audio"
- Don't use audio longer than 10-15 minutes (takes too long)
- Don't skip the "why this matters" explanation
- Don't forget to mention this works locally (no cloud deployment needed for demo)

---

## 🐛 Troubleshooting

### "API Error: Invalid API Key"
- Check `backend/.env` has correct keys
- Ensure keys don't have quotes around them
- Verify keys are active in respective consoles

### "Model download error" (FinBERT)
- First run downloads ~400MB model from HuggingFace
- Ensure internet connection
- May take 2-3 minutes on first startup

### "CORS Error" in Browser
- Backend must be running on port 8000
- Frontend must be on port 5173
- Check browser console for exact error

### Audio Upload Fails
- Check file size < 100MB
- Ensure format is MP3, WAV, or M4A
- Try converting with: `ffmpeg -i input.mp4 -vn output.mp3`

---

## 📊 Expected Results

For a typical 10-minute earnings call:

**Processing Time:**
- Transcription: ~5-10 seconds
- Feature Extraction: ~3 seconds
- Sentiment Analysis: ~2 seconds
- Chart Analysis: ~5-10 seconds per chart
- AI Analysis: ~10-15 seconds
- **Total: 30-60 seconds**

**Output:**
- 20-40 transcript segments
- Confidence timeline with 10-15 data points
- 3-5 risk indicators
- 3-5 opportunities
- Comprehensive AI summary (200-400 words)

---

## 🎥 Recording the Demo

If creating a video:

1. Use screen recording software (OBS, QuickTime, etc.)
2. Record at 1920x1080 minimum
3. Use a good microphone for narration
4. Show terminal output for authenticity
5. Include a before/after comparison
6. Keep total demo under 5 minutes

---

## 🎉 Post-Demo Q&A

**Common Questions:**

**Q: How accurate is the deception detection?**
A: Vocal biomarkers are indicators, not proof. We combine multiple signals (audio, text, charts) to flag areas requiring human review. Our cross-modal verification catches inconsistencies competitors miss.

**Q: What companies can this analyze?**
A: Any company with public earnings calls. Works across industries - tech, finance, retail, energy, etc.

**Q: Can it analyze live calls?**
A: Current demo is batch processing. The architecture supports real-time streaming (mentioned in paper.pdf roadmap).

**Q: How does this compare to Bloomberg/FactSet?**
A: Those focus on data aggregation. We provide unique vocal analysis and cross-modal verification they don't offer.

---

**Good luck with your demo! 🚀**

For technical questions, refer to [paper.pdf](paper.pdf)
