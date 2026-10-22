from .utils import draw_triangle


class BallTracksDrawer:
    """Marks the ball with a green pointer. Draws on the frames in place."""

    def __init__(self):
        self.ball_pointer_color = (0, 255, 0)

    def draw(self, video_frames, tracks):
        if not tracks:
            print("Warning: No ball tracks to draw")
            return video_frames

        if len(video_frames) > len(tracks):
            print(f"Warning: More frames ({len(video_frames)}) than ball tracks ({len(tracks)}). Using available tracks.")

        for frame, ball_dict in zip(video_frames, tracks):
            if frame is None:
                continue
            for ball in ball_dict.values():
                if ball["bbox"] is not None:
                    draw_triangle(frame, ball["bbox"], self.ball_pointer_color)

        return video_frames
