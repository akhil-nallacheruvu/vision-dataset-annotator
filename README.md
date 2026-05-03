# Visual Dataset Annotation Pipeline

A web-based tool for auto-annotating image datasets using Google's Gemini Vision API. Designed to accelerate dataset creation for training vision transformers and vision-language models (VLMs). Supports single and batch image upload, exports to JSONL, CSV, and COCO JSON formats.

**Live Demo:** https://visual-analysis-pipeline.streamlit.app/

---

## Features

- Single and batch image upload with progress tracking
- Generates four annotation types per image: dense captions, object labels, scene/lighting metadata, and VQA pairs
- Exports to JSONL (VLM fine-tuning), CSV (general purpose), and COCO JSON (object detection pipelines)
- Modal-based API key authentication with live connection validation
- Model selector with three Gemini free-tier options, with graceful rate limit error handling
- Running dataset preview and one-click ZIP download of all export formats

## Annotation Output

Each image is annotated with the following fields:

| Field | Description |
|---|---|
| `dense_caption` | Detailed 2-4 sentence description covering objects, spatial relationships, lighting, and context — suitable for VLM training |
| `objects` | List of all identifiable objects in the image |
| `scene` | Scene type (e.g. indoor, outdoor, aerial, medical) |
| `lighting` | Lighting conditions (e.g. natural daylight, low light, overcast) |
| `vqa_pairs` | 3 question-answer pairs per image for visual question answering datasets |
| `confidence_notes` | Model uncertainty flags for downstream filtering |

## Export Formats

| Format | Use Case |
|---|---|
| JSONL | VLM fine-tuning (e.g. LLaVA, InstructBLIP) |
| CSV | General purpose dataset management |
| COCO JSON | Object detection pipelines |
| ZIP | All three formats bundled |

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
3. Choose between single image or batch upload mode
4. Select a Gemini model and click **Annotate Image** or **Annotate All**
5. Download the generated dataset as JSONL, CSV, COCO JSON, or ZIP from the sidebar

## Output Format

```json
{
  "dense_caption": "A wildlife camera trap image showing two elephants at a watering hole at dusk, with dense vegetation in the background and soft golden light.",
  "objects": ["elephant", "water", "vegetation", "mud"],
  "scene": "outdoor",
  "lighting": "golden hour",
  "vqa_pairs": [
    {"question": "How many elephants are visible?", "answer": "Two"},
    {"question": "What time of day does this appear to be?", "answer": "Dusk or golden hour"},
    {"question": "What are the elephants doing?", "answer": "Drinking or standing at a watering hole"}
  ],
  "confidence_notes": "Species confirmed as elephant; exact subspecies uncertain"
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
