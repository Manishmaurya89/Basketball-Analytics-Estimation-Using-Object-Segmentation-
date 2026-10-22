from ultralytics import YOLO
from utils import read_stub, save_stub


class CourtKeypointDetector:
    """Finds the 18 court reference points (see TacticalViewConverter.key_points) with a YOLO pose model."""

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def get_court_keypoints(self, frames, read_from_stub=False, stub_path=None, batch_size=20):
        """Return the YOLO keypoints object for each frame."""
        court_keypoints = read_stub(read_from_stub, stub_path)
        if court_keypoints is not None and len(court_keypoints) == len(frames):
            return court_keypoints

        court_keypoints = []
        for i in range(0, len(frames), batch_size):
            for detection in self.model.predict(frames[i:i + batch_size], conf=0.5):
                court_keypoints.append(detection.keypoints)

        save_stub(stub_path, court_keypoints)
        return court_keypoints
