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
├── requirements.txt
└── frontend/								 # Home to all the frontend code
		├── src/
		│   ├── lib/
		│   │   ├── assets/
		│   │   │   └── heroPic.png
		│   │   │
		│   │   ├── components/
		│   │   │   ├── Navbar.svelte
		│   │   │   └── ThemeToggle.svelte
		│   │   │
		│   │   ├── vitest-examples/
		│   │   │
		│   │   └── index.ts
		│   │
		│   ├── routes/
		│   │   ├── upload/
		│   │   │   ├── clip/
		│   │   │   │   └── +page.svelte
		│   │   │   │
		│   │   │   └── frame/
		│   │   │       └── +page.svelte
		│   │   │
		│   │   ├── +layout.svelte
		│   │   └── +page.svelte
		│   │
		│   ├── app.html
		│   ├── app.d.ts
		│   └── app.css
		│
		├── static/
		│
		├── .svelte-kit/
		├── .vscode/
		├── node_modules/
		│
		├── .gitignore
		├── .npmrc
		├── .prettierignore
		├── .prettierrc
		├── eslint.config.js
		├── package.json
		├── package-lock.json
		├── README.md
		├── svelte.config.js
		├── tsconfig.json
		└── vite.config.ts

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

**3. Install frontend dependencies**

```bash
cd frontend
npm install
```

**4. (Optional) Build your own reference embeddings**

If you want to add your own games, create a `referenceGames/` folder next to `app/` and populate it with screenshots:

```
referenceGames/
└── Your_Game/
    ├── screenshot1.png
    ├── screenshot2.png
    └── ...
```

Then delete the `refEmbed.pkl` in the cachedEmbeddings folder to generate new embeddings based on your data. New embeddings are generated on running `main.py`

More screenshots per game = better accuracy. Aim for at least 10-20 varied screenshots covering different scenes, HUDs, and moments.

---

## Usage — CLI

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

- Videos longer than **3 minutes** are automatically capped at the first 3 minutes.
- You can choose the duration you want by changing the parameters of `videoToFrame` function in the `main.py`
- If no frame clears the similarity threshold, the clip is reported as **Unknown Game**.
- Enter `q` to quit.
- Supports command line arguments. Order: 
 	```sh
  python main.py (video_clip_path) (startTime) (endTime)
	```

---

## Usage — Backend (FastAPI)

Run from inside the `backend/` directory:

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Endpoints

#### `POST /upload/clip`

Detect the game in a video clip.

**Form fields:**

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | File | Yes | — | Video file (.mp4, .mov, .avi) |
| `startTime` | String | No | `00:00` | Start time in MM:SS format |
| `endTime` | String | No | None | End time in MM:SS format |

**Response:**

```json
{
  "id": "98a0683c-9ad5-40d9-bbb4-b6fe1d5d7c70",
  "prediction": "Elden_Ring",
  "confidences": [["Elden_Ring", 100.0]],
  "frames": [
    "/frames/98a0683c-.../frame_0003_medium.jpg",
    "/frames/98a0683c-.../frame_0010_medium.jpg",
    "/frames/98a0683c-.../frame_0028_medium.jpg"
  ]
}
```

#### `POST /upload/frame` (in works)

Detect the game in a single screenshot.

**Form fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | File | Yes | Image file (.png, .jpg, .jpeg) |

**Response:**

```json
{
  "prediction": "Valorant",
  "confidence": 0.91
}
```

#### `GET /frames/{id}/{filename}`

Retrieve an extracted frame image by ID and filename. Used by the frontend to display influential frames after a clip detection.

---

## Usage — Web UI

Run the backend and frontend simultaneously:

```bash
# Terminal 1 — backend
cd backend
uvicorn main:app --reload

# Terminal 2 — frontend
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

- Upload a video clip or a screenshot via the upload pages.
- The detected game, confidence breakdown, and most influential frames are shown on the results page. *(In works)*

---

## Requirements

- Python 3.12
- Node.js 18+
- torch
- open-clip-torch
- opencv-python
- Pillow
- fastapi
- uvicorn
- python-multipart

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend && npm install
```

---

## Future Plans

- [*] Support for single image/screenshot detection (not just video)
- [*] Confidence score display in output
- [ ] Results page with full confidence breakdown and frame viewer
- [ ] Detection history page with past predictions
- [ ] Deduplication — reuse results for previously seen clips
- [ ] Event detection within clips (kills, deaths, aces, explosions, etc.)
- [ ] Expand shipped reference library with more games
