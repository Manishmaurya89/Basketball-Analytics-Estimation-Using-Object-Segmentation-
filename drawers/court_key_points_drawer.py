import supervision as sv


class CourtKeypointDrawer:
    """Draws the detected court keypoints and their index numbers. Draws on the frames in place."""

    def __init__(self):
        self.keypoint_color = '#ff2c2c'

    def draw(self, frames, court_keypoints):
        if not frames or not court_keypoints:
            print("Warning: No frames or court keypoints to draw")
            return frames

        if len(frames) > len(court_keypoints):
            print(f"Warning: More frames ({len(frames)}) than keypoints ({len(court_keypoints)}). Using available keypoints.")

        vertex_annotator = sv.VertexAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            radius=8,
        )
        vertex_label_annotator = sv.VertexLabelAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            text_color=sv.Color.WHITE,
            text_scale=0.5,
            text_thickness=1,
        )

        for index, (frame, keypoints) in enumerate(zip(frames, court_keypoints)):
            if frame is None:
                continue
            try:
                if keypoints is None or len(keypoints) == 0:
                    continue
                vertex_annotator.annotate(scene=frame, key_points=keypoints)

                # The label annotator wants numpy, but YOLO gives us a torch-backed object.
                try:
                    keypoints_numpy = keypoints.cpu().numpy()
                except AttributeError:
                    keypoints_numpy = keypoints
                vertex_label_annotator.annotate(scene=frame, key_points=keypoints_numpy)
            except Exception as e:
                print(f"Error processing frame {index}: {e}")

        return frames
