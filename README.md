# 🏀 Basketball Video Analytics

An **AI-powered video analytics system** that detects and tracks players, the ball, and court elements in basketball footage using YOLOv8 and DeepSORT. Built for both amateur and professional team performance analysis.

---

##  Features

- 🎯 **Player & Ball Detection** — fine-tuned YOLOv8 model with **95%+ detection accuracy**
- 🏃 **Multi-object Tracking** — DeepSORT maintains consistent player IDs across frames
- 👕 **Team Assignment** — automatically classifies players into teams based on jersey colour
- 🏀 **Ball Possession & Pass Detection** — identifies passes, interceptions, and possession sequences
- 🌡️ **Player Heatmaps** — visual overlay showing court coverage and movement patterns
- 📈 **Ball Trajectories** — traces ball path across frames
- 📊 **Team Statistics** — real-time stats panel per team


---

##  Tech Stack

| Component | Technology |
|---|---|
| Object Detection | YOLOv8 (Ultralytics) |
| Multi-object Tracking | DeepSORT |
| Computer Vision | OpenCV |
| Deep Learning | PyTorch |
| Data Processing | Pandas · NumPy |
| Dataset Management | Roboflow |

---

## Getting Started

### Option A — Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/Manishmaurya89/Basketball-Analytics-Estimation-Using-Object-Segmentation-.git
cd Basketball-Analytics-Estimation-Using-Object-Segmentation-

# Build and run
docker build -t basketball-analytics .
docker run --gpus all -v $(pwd)/videos:/app/videos basketball-analytics
```

### Option B — Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis on a video file
python main.py --input videos/match.mp4 --output output/result.mp4
```

---

## 📁 Project Structure

```
Basketball-Analytics/
├── github_upload/
│   ├── main.py               # Pipeline entry point
│   ├── tracker.py            # DeepSORT integration
│   ├── team_assigner.py      # Jersey colour-based team classification
│   ├── possession.py         # Ball possession & pass detection logic
│   ├── heatmap.py            # Player heatmap generation
│   ├── utils.py              # Helpers & visualisation
│   └── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🔧 How It Works

```
Input Video
     ↓
YOLOv8 — detect players, ball, court keypoints (95%+ accuracy)
     ↓
DeepSORT — assign consistent IDs to each player across frames
     ↓
Team Assigner — jersey colour clustering → Team A / Team B
     ↓
Possession Engine — ball proximity → possession %, passes, interceptions
     ↓
Overlay Renderer — heatmaps, trajectories, stats panel
     ↓
Annotated Output Video + Statistics Report
```

---

## Sample Output

-  Player bounding boxes with team colour and ID
-  Ball bounding box with trajectory trail
-  Heatmap overlay per player
- Scoreboard panel: possession %, passes, interceptions per team

---

## Contact

For questions: **manish.maurya0408@gmail.com**

---

##  License

MIT License — free to use and modify.
