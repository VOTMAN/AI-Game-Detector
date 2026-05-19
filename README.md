# AI Game Detector

Detects which video game is being played in a video clip using AI-powered image embeddings. Drop in a clip, get the game name.

Currently supports **CS2, Elden Ring, Hollow Knight, and Valorant**, with pre-built embeddings shipped directly in the repo.

---

## How It Works

The detector uses **OpenCLIP (ViT-B-32)** to convert images into semantic embeddings — vector representations that capture visual meaning. These are compared against a library of reference screenshots to find the closest match.

### Detection Flow

```
Video Clip
    │
    ▼
Extract a frame every 2 seconds           (video.py)
    │
    ▼
For each frame:
  → Generate embedding via OpenCLIP       (embeddings.py)
  → Compare against reference library
  → Pick best game for that frame         (detector.py)
    │
    ▼
Majority vote across all frames           (main.py)
    │
    ▼
Final Prediction: "Game Name"
```

### Two-Level Voting

Detection runs at two levels for robustness:

- **Frame level** (`detector.py`) — For each frame, the top 5 most similar reference images are found. Similarity scores are accumulated per game and the highest-scoring game wins that frame.
- **Video level** (`main.py`) — Each frame casts one vote. The game with the most frame-level wins is the final prediction.

This means a single ambiguous frame (menu screen, cutscene, black screen) won't throw off the result — it gets outvoted by consistent gameplay frames.

### Embedding Cache

Pre-built embeddings for all supported games are shipped in `cachedEmbeddings/refEmbed.pkl`. The app loads this automatically on startup — no build step needed.

---

## Project Structure

```
.
├── app/
│   ├── main.py              # Entry point
│   ├── detector.py          # Frame-level game detection
│   ├── embeddings.py        # OpenCLIP model + embedding functions
│   ├── video.py             # Video frame extraction
│   └── utils.py             # Embedding cache helpers
├── cachedEmbeddings/
│   └── refEmbed.pkl         # Pre-built embeddings (shipped with repo)
├── videoClips/              # Put your test clips here
├── extractedFrames/         # Auto-generated during detection
└── requirements.txt
```

---

## Setup

**1. Clone the repo and create a virtual environment**
```bash
git clone <repo-url>
cd aipro
python -m venv myenv
source myenv/bin/activate       # Windows: myenv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. (Optional) Build your own reference embeddings**

If you want to add your own games, create a `referenceGames/` folder next to `app/` and populate it with screenshots:

```
referenceGames/
└── Your_Game/
    ├── screenshot1.png
    ├── screenshot2.png
    └── ...
```

Then run this once from inside `app/` to build and cache the embeddings:

```python
from embeddings import buildReferenceEmbeddings
from utils import cacheEmbeddings

referenceEmbeddings, _ = buildReferenceEmbeddings("../referenceGames")
cacheEmbeddings(referenceEmbeddings)
```

This overwrites `cachedEmbeddings/refEmbed.pkl` with your new embeddings. More screenshots per game = better accuracy. Aim for at least 10-20 varied screenshots covering different scenes, HUDs, and moments.

---

## Usage

Run from inside the `app/` directory:

```bash
cd app
python main.py
```

You'll be prompted to enter a video path:

```
=== AI Game Detector ===

Enter video path (or q to quit): ../videoClips/Valorant.mp4

Extracting frames...
Selected Duration: 118.0
Extraction Complete

Detected Game: Valorant
```

- Videos longer than **2 minutes** are automatically capped at the first 2 minutes.
- If no frame clears the similarity threshold, the clip is reported as **Unknown Game**.
- Enter `q` to quit.

---

## Requirements

- Python 3.12
- torch
- open-clip-torch
- opencv-python
- Pillow

Install all via:
```bash
pip install -r requirements.txt
```

---

## Future Plans

- [ ] Web frontend for drag-and-drop video upload
- [ ] Expand shipped reference library with more games
- [ ] Support for single image/screenshot detection (not just video)
- [ ] Confidence score display in output
- [ ] Auto-download reference packs for popular games
