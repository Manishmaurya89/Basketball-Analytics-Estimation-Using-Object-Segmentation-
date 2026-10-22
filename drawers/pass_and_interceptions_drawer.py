import cv2


class PassInterceptionDrawer:
    """Shows running pass and interception counts per team in a box at the bottom left."""

    def get_stats(self, passes, interceptions):
        """Count events in per-frame lists where 1 or 2 is the team and -1 means nothing happened.

        Returns (team1_passes, team2_passes, team1_interceptions, team2_interceptions).
        """
        return (
            passes.count(1),
            passes.count(2),
            interceptions.count(1),
            interceptions.count(2),
        )

    def draw(self, video_frames, passes, interceptions):
        return [self.draw_frame(frame, frame_num, passes, interceptions) for frame_num, frame in enumerate(video_frames)]

    def draw_frame(self, frame, frame_num, passes, interceptions):
        font_scale = 0.7
        font_thickness = 2

        frame_height, frame_width = frame.shape[:2]
        rect_x1 = int(frame_width * 0.16)
        rect_y1 = int(frame_height * 0.75)
        rect_x2 = int(frame_width * 0.55)
        rect_y2 = int(frame_height * 0.90)
        text_x = int(frame_width * 0.19)
        text_y1 = int(frame_height * 0.80)
        text_y2 = int(frame_height * 0.88)

        # Semi-transparent white box behind the text.
        overlay = frame.copy()
        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), -1)
        alpha = 0.8
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        team1_passes, team2_passes, team1_interceptions, team2_interceptions = self.get_stats(
            passes[:frame_num + 1],
            interceptions[:frame_num + 1],
        )

        cv2.putText(
            frame,
            f"Team 1 - Passes: {team1_passes} Interceptions: {team1_interceptions}",
            (text_x, text_y1),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (0, 0, 0),
            font_thickness,
        )
        cv2.putText(
            frame,
            f"Team 2 - Passes: {team2_passes} Interceptions: {team2_interceptions}",
            (text_x, text_y2),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (0, 0, 0),
            font_thickness,
        )

        return frame
