# 🏀 Basketball Video Analytics

A computer vision pipeline that analyses basketball game footage. It detects and tracks players and the ball, splits
players into teams, and works out ball possession, passes, interceptions and each player's speed and distance on a
top-down view of the court.

## Credits

This project is built on [abdullahtarek/basketball_analysis](https://github.com/abdullahtarek/basketball_analysis).
The pipeline code, training notebooks and pretrained model weights come from that repository.

---

## Features

- **Player and ball detection** with fine-tuned Ultralytics YOLO models
- **Player tracking** with ByteTrack (from the `supervision` library), so each player keeps the same ID across frames
- **Team assignment** with a zero-shot Fashion-CLIP model that labels each player's shirt ("white shirt" or "dark blue shirt")
- **Ball possession, passes and interceptions** per team
- **Court keypoint detection** and a homography that maps players onto a top-down tactical view
- **Speed and distance** for every player, in km/h and metres
- **Annotated output video** with all of the above drawn on each frame

---

## Tech Stack

| Component | Technology |
|---|---|
| Object and keypoint detection | Ultralytics YOLO |
| Multi-object tracking | ByteTrack (`supervision`) |
| Team assignment | Fashion-CLIP (Hugging Face Transformers) |
| Computer vision | OpenCV |
| Deep learning | PyTorch |
| Data processing | Pandas · NumPy |
| Dataset management | Roboflow |

---

## Getting Started

All code is in the `github_upload/` folder.

### 1. Get the models

The pipeline needs three model files in `github_upload/models/`:

- `player_detector.pt`
- `ball_detector_model.pt`
- `court_keypoint_detector.pt`

Download the pretrained weights from the links in the
[original project's README](https://github.com/abdullahtarek/basketball_analysis#-training-the-models), or train
your own with the notebooks in `github_upload/training_notebooks/`.

### 2a. Run with Python

```bash
git clone https://github.com/Manishmaurya89/Basketball-Analytics-Estimation-Using-Object-Segmentation-.git
cd Basketball-Analytics-Estimation-Using-Object-Segmentation-/github_upload

pip install -r requirements.txt
python main.py path/to/game.mp4 --output_video output_videos/output_video.avi
```

### 2b. Run with Docker

Put the model files in `github_upload/models/` first, so they are copied into the image.

```bash
cd Basketball-Analytics-Estimation-Using-Object-Segmentation-/github_upload
docker build -t basketball-analytics .
docker run \
  -v "$(pwd)/input_videos:/app/input_videos" \
  -v "$(pwd)/output_videos:/app/output_videos" \
  basketball-analytics input_videos/game.mp4
```

The output video is saved to `output_videos/output_video.avi`.

> `main.py` caches detection results in `stubs/`. A cached result is only reused when its frame count matches the
> input video, so a new video is always processed from scratch.

---

## 📁 Project Structure

```
github_upload/
├── main.py                          pipeline entry point
├── configs/                         model and output paths
├── trackers/                        player and ball detection + ByteTrack tracking
├── team_assigner/                   Fashion-CLIP team assignment
├── ball_aquisition/                 which player has the ball
├── pass_and_interception_detector/  passes and interceptions
├── court_keypoint_detector/         court keypoints
├── tactical_view_converter/         homography to the top-down court view
├── speed_and_distance_calculator/   player speed and distance
├── drawers/                         draws tracks, stats and the tactical view on each frame
├── utils/                           video reading/writing, bounding boxes, stub caching
├── training_notebooks/              notebooks to train the three YOLO models
├── stubs/                           cached results for the sample video
├── Dockerfile
└── requirements.txt
```

---

## 🔧 How It Works

```
Input video
     ↓
YOLO: detect players, the ball and court keypoints
     ↓
ByteTrack: give each player a consistent ID across frames
     ↓
Fashion-CLIP: classify each player's shirt into Team 1 or Team 2
     ↓
Possession: a player has the ball when it sits inside or close to their box; changes between
            teammates are passes, changes to the other team are interceptions
     ↓
Homography: map player positions onto a top-down court, then compute speed and distance
     ↓
Annotated output video
```

---

## Contact

For questions: **manish.maurya0408@gmail.com**
