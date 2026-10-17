# Basketball Video Analytics

**Basketball Video Analytics is my computer-vision project for analyzing basketball game footage.** It processes a video to detect and track players and the ball, assign players to teams, estimate ball possession, identify passes and interceptions, calculate player speed and distance, and generate an annotated video with a top-down tactical court view.

The project is maintained in this repository by **Manish Maurya**.

## Project background and attribution

This repository is my project version of a basketball analytics pipeline, built by adapting and extending the open-source work in [abdullahtarek/basketball_analysis](https://github.com/abdullahtarek/basketball_analysis).

The upstream repository is an important source for the pipeline implementation, training notebooks, and pretrained model workflow. Those inherited components should be credited to the original project; this repository organizes and documents the project under my own GitHub repository. Please consult the upstream repository and its license for the original work's attribution and usage terms.

## Features

- **Player and ball detection:** Uses fine-tuned Ultralytics YOLO models.
- **Player tracking:** Uses ByteTrack through the `supervision` library to maintain player IDs across frames.
- **Team assignment:** Uses a zero-shot Fashion-CLIP model to group players by jersey appearance.
- **Ball possession:** Estimates which player is in possession of the ball.
- **Passes and interceptions:** Tracks changes in possession to estimate passes between teammates and interceptions by the opposing team.
- **Tactical court view:** Detects court keypoints and uses a homography to project player positions onto a top-down court.
- **Speed and distance:** Estimates player movement in km/h and metres using the court mapping.
- **Annotated output:** Combines detections, tracks, possession information, events, movement statistics, and the tactical view in an output video.

## Requirements

- Python 3.11 is recommended (the Docker image uses Python 3.11).
- Dependencies listed in [`requirements.txt`](requirements.txt).
- Three model weight files in a `models/` directory:
  - `models/player_detector.pt`
  - `models/ball_detector_model.pt`
  - `models/court_keypoint_detector.pt`
- An input basketball video supported by OpenCV.

The model weights are not included in this repository by default. Follow the model-training and download guidance in the [upstream project's README](https://github.com/abdullahtarek/basketball_analysis#-training-the-models), or train models using the notebooks in `training_notebooks/`. Make sure you have permission to use any downloaded weights and datasets.

## Run locally

Clone the repository and install its dependencies:

```bash
git clone https://github.com/Manishmaurya89/Basketball-Analytics-Estimation-Using-Object-Segmentation-.git
cd Basketball-Analytics-Estimation-Using-Object-Segmentation-

python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Place the three model files listed above in `models/`, then run:

```bash
python main.py path/to/game.mp4 --output_video output_videos/output_video.avi
```

The annotated video is written to `output_videos/output_video.avi` unless you specify another path. You can see all command-line options with:

```bash
python main.py --help
```

## Run with Docker

Place the model files in `models/` before building the image:

```bash
docker build -t basketball-analytics .
docker run --rm \
  -v "$(pwd)/input_videos:/app/input_videos" \
  -v "$(pwd)/output_videos:/app/output_videos" \
  basketball-analytics input_videos/game.mp4 \
  --output_video output_videos/output_video.avi
```

The output video will be available in the local `output_videos/` directory.

## How the pipeline works

```text
Input video
    |
    v
YOLO detection: players, ball, and court keypoints
    |
    v
ByteTrack player tracking
    |
    v
Fashion-CLIP team assignment
    |
    v
Ball possession estimation
    |
    +--> Pass and interception estimates
    |
    v
Court homography and top-down player positions
    |
    v
Speed and distance estimates
    |
    v
Annotated video with tactical view and statistics
```

The current possession logic estimates possession from the ball's proximity to player bounding boxes. Passes and interceptions are inferred from changes in possession and team assignment; they are estimates, not guaranteed ground-truth event labels.

## Court and movement measurements

The tactical view uses the court image at `images/basketball_court.png`.

<p align="center">
  <img src="images/basketball_court.png" width="600" alt="Top-down basketball court used for the tactical view">
</p>

The movement calculation uses a nominal court size of **28 m × 15 m**. The keypoint mapping and this court-size assumption affect the accuracy of speed and distance estimates.

<p align="center">
  <img src="images/basketball-court-dimensions.png" width="600" alt="Basketball court dimensions in metres">
</p>

Court diagrams are credited to [The Hoops Geek](https://www.thehoopsgeek.com/basketball-court-dimensions/).

## Repository structure

```text
├── main.py                          Runs the complete pipeline
├── configs/                         Model and output paths
├── trackers/                        Player and ball detection/tracking
├── team_assigner/                   Team assignment
├── ball_aquisition/                 Ball-possession estimation
├── pass_and_interception_detector/  Pass and interception estimates
├── court_keypoint_detector/         Court keypoint detection
├── tactical_view_converter/         Homography and top-down projection
├── speed_and_distance_calculator/   Player speed and distance estimates
├── drawers/                         Video overlays and annotations
├── utils/                           Video I/O, bounding boxes, and caching
├── training_notebooks/              Model-training notebooks
├── images/                          Court images and reference diagrams
├── stubs/                           Cached intermediate results
├── Dockerfile
└── requirements.txt
```

## Technology stack

Python, Ultralytics YOLO, ByteTrack (`supervision`), Fashion-CLIP, Hugging Face Transformers, OpenCV, PyTorch, Pandas, and NumPy. The training workflow uses datasets managed through Roboflow.

## Limitations

- Detection and tracking quality depends on video quality, camera angle, occlusion, and the trained weights.
- Team assignment based on jersey appearance may be unreliable when teams wear similar colors.
- Possession, passes, and interceptions are inferred heuristically and should be validated against manually labeled footage before being used for formal performance evaluation.
- Speed and distance are estimates that depend on court-keypoint accuracy and the homography calibration.

## Credits

- **Upstream basketball analytics implementation and training workflow:** [abdullahtarek/basketball_analysis](https://github.com/abdullahtarek/basketball_analysis).
- **Court dimensions reference:** [The Hoops Geek](https://www.thehoopsgeek.com/basketball-court-dimensions/).
- **Project repository and maintenance:** [Manish Maurya](https://github.com/Manishmaurya89).

Please check the relevant upstream licenses and dataset/model terms before redistributing inherited code, weights, or data.

## Contact

Questions: manish.maurya0408@gmail.com
