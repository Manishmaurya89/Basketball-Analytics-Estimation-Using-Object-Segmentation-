from ultralytics import YOLO
import supervision as sv
from utils import read_stub, save_stub


class PlayerTracker:
    """Detects players with YOLO and keeps their IDs stable across frames with ByteTrack."""

    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames, batch_size=20):
        detections = []
        for i in range(0, len(frames), batch_size):
            detections += self.model.predict(frames[i:i + batch_size], conf=0.5)
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        """Return one dict per frame mapping track_id -> {"bbox": [x1, y1, x2, y2]}."""
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None and len(tracks) == len(frames):
            return tracks

        tracks = []
        for detection in self.detect_frames(frames):
            player_class_id = {name: cls_id for cls_id, name in detection.names.items()}['Player']
            detections = self.tracker.update_with_detections(sv.Detections.from_ultralytics(detection))

            frame_tracks = {}
            for bbox, _, _, cls_id, track_id, *_ in detections:
                if cls_id == player_class_id:
                    frame_tracks[track_id] = {"bbox": bbox.tolist()}
            tracks.append(frame_tracks)

        save_stub(stub_path, tracks)
        return tracks
