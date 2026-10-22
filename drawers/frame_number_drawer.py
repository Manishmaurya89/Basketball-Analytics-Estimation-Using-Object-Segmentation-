import cv2


class FrameNumberDrawer:
    """Writes the frame index in the top-left corner. Draws on the frames in place."""

    def __init__(self):
        self.text_color = (0, 255, 0)
        self.text_position = (10, 30)
        self.font_scale = 1
        self.thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw(self, frames):
        if not frames:
            print("Warning: No frames to add frame numbers to")
            return frames

        for i, frame in enumerate(frames):
            if frame is None:
                continue
            cv2.putText(frame, str(i), self.text_position, self.font,
                        self.font_scale, self.text_color, self.thickness)

        return frames
