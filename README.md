
# 🏀 Basketball Video Analysis

## 📄 Description
A computer vision system for basketball analytics that detects and tracks players, ball possession, and court keypoints using YOLO and optical flow. This tool analyzes game footage to identify teams, track ball movement, and generate statistical insights.

## ✨ Features
- **Player & Ball Detection**: Uses fine-tuned YOLO models tracking.
- **Team Assignment**: Automatically classifies players into teams based on jersey color.
- **Possession Tracking**: Calculates ball possession percentages for each team.
- **Court Keypoints**: Detects standard court lines and key zones.
- **Automated Reporting**: Generates annotated video outputs and analysis summaries.

## 🚀 Installation & Usage
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Models**:
   Download the YOLO weights (`.pt` files) from the links provided in the original project documentation (or train your own) and place them in the `models/` directory.

4. **Run the Analysis**:
   ```bash
   python main.py
   ```

## 🛠 Tech Stack
- **Languages**: Python
- **Libraries**: OpenCV, PyTorch, Ultralytics (YOLO), Supervision, Pandas, NumPy
- **Tools**: Roboflow (Dataset Management)

## 🤝 Contributing
Contributions are welcome! Please feel free to verify the `LICENSE` file for more details.# Basketball-Analytics-Estimation-Using-Object-Segmentation-
Basketball game analysis tool using deep learning for object detection, player tracking, and team assignment.
