from ultralytics import YOLO
import supervision as sv
import numpy as np
import pandas as pd
from utils import read_stub, save_stub


class BallTracker:
    """Finds the ball in each frame with YOLO and cleans up the track afterwards."""

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_frames(self, frames, batch_size=20):
        detections = []
        for i in range(0, len(frames), batch_size):
            detections += self.model.predict(frames[i:i + batch_size], conf=0.5)
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        """Return one dict per frame, {1: {"bbox": [x1, y1, x2, y2]}}, or {} when no ball was seen."""
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None and len(tracks) == len(frames):
            return tracks

        tracks = []
        for detection in self.detect_frames(frames):
            ball_class_id = {name: cls_id for cls_id, name in detection.names.items()}['Ball']

            # Only one ball can be on court, so keep the most confident box.
            chosen_bbox = None
            max_confidence = 0
            for bbox, _, confidence, cls_id, *_ in sv.Detections.from_ultralytics(detection):
                if cls_id == ball_class_id and confidence > max_confidence:
                    chosen_bbox = bbox.tolist()
                    max_confidence = confidence

            tracks.append({1: {"bbox": chosen_bbox}} if chosen_bbox is not None else {})

        save_stub(stub_path, tracks)
        return tracks

    def remove_wrong_detections(self, ball_positions, max_pixels_per_frame=25):
        """Drop detections that jump further from the last good one than the ball could move."""
        last_good_frame = -1

        for i in range(len(ball_positions)):
            current_box = ball_positions[i].get(1, {}).get('bbox', [])
            if len(current_box) == 0:
                continue

            if last_good_frame == -1:
                last_good_frame = i
                continue

            last_good_box = ball_positions[last_good_frame].get(1, {}).get('bbox', [])
            allowed = max_pixels_per_frame * (i - last_good_frame)
            jump = np.linalg.norm(np.array(last_good_box[:2]) - np.array(current_box[:2]))

            if jump > allowed:
                ball_positions[i] = {}
            else:
                last_good_frame = i

        return ball_positions

    def interpolate_ball_positions(self, ball_positions):
        """Fill frames with no ball by interpolating between the detections around them."""
        boxes = [x.get(1, {}).get('bbox', []) for x in ball_positions]
        df = pd.DataFrame(boxes, columns=['x1', 'y1', 'x2', 'y2'])
        df = df.interpolate().bfill()
        return [{1: {"bbox": box}} for box in df.to_numpy().tolist()]
