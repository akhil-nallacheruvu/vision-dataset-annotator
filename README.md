# Visual Analysis Pipeline

A web-based image analysis tool that uses Google's Gemini Vision API to return structured JSON insights from any uploaded image. Built with Streamlit and the Google GenAI SDK.

**Live Demo:** _coming soon_

---

## Features

- Modal-based API key authentication with live connection validation
- Supports JPG, PNG, and WEBP image formats
- Returns structured JSON output: scene type, detected objects, dominant colors, and a natural language description
- Model selector with three Gemini free-tier options, with graceful rate limit error handling

## Models Supported

| Model | Notes |
|---|---|
| Gemini 2.5 Flash | Recommended — best balance of speed and capability |
| Gemini 2.5 Flash-Lite | Highest free-tier request limits |
| Gemini 2.5 Pro | Most capable, lower free-tier limits (5 RPM / 100 RPD) |

## Getting Started

### Prerequisites

- Python 3.10+
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

```bash
git clone https://github.com/akhil-nallacheruvu/visual-analysis-pipeline.git
cd visual-analysis-pipeline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Usage

1. On launch, a dialog will prompt for your Gemini API key
2. The key is validated with a test call before the app loads
3. Upload an image and select a model from the dropdown
4. Click **Analyze Image** to receive structured JSON output

## Output Format

```json
{
  "description": "A golden retriever running through a grassy park",
  "objects": ["dog", "grass", "trees", "sky"],
  "scene": "outdoor",
  "colors": ["green", "golden yellow", "blue"],
  "confidence_notes": "Breed identification uncertain due to motion blur"
}
```

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI and deployment
- [Google GenAI SDK](https://pypi.org/project/google-genai/) — Gemini Vision API client
- [Pillow](https://python-pillow.org/) — Image preprocessing

## Project Structure

```
visual-analysis-pipeline/
├── app.py               # Main Streamlit app
├── requirements.txt     # Dependencies
└── README.md
```
