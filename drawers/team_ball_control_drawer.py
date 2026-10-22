import cv2
import numpy as np


class TeamBallControlDrawer:
    """Shows each team's share of ball possession so far in a box at the bottom right."""

    def get_team_ball_control(self, player_assignment, ball_aquisition):
        """Return an array with the team holding the ball in each frame: 1, 2, or -1 for nobody."""
        team_ball_control = []
        for teams, player_with_ball in zip(player_assignment, ball_aquisition):
            if player_with_ball == -1 or player_with_ball not in teams:
                team_ball_control.append(-1)
            elif teams[player_with_ball] == 1:
                team_ball_control.append(1)
            else:
                team_ball_control.append(2)
        return np.array(team_ball_control)

    def draw(self, video_frames, player_assignment, ball_aquisition):
        team_ball_control = self.get_team_ball_control(player_assignment, ball_aquisition)

        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            if frame_num == 0:
                continue
            output_video_frames.append(self.draw_frame(frame, frame_num, team_ball_control))
        return output_video_frames

    def draw_frame(self, frame, frame_num, team_ball_control):
        font_scale = 0.7
        font_thickness = 2

        frame_height, frame_width = frame.shape[:2]
        rect_x1 = int(frame_width * 0.60)
        rect_y1 = int(frame_height * 0.75)
        rect_x2 = int(frame_width * 0.99)
        rect_y2 = int(frame_height * 0.90)
        text_x = int(frame_width * 0.63)
        text_y1 = int(frame_height * 0.80)
        text_y2 = int(frame_height * 0.88)

        # Semi-transparent white box behind the text.
        overlay = frame.copy()
        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), -1)
        alpha = 0.8
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Share of frames so far, including frames where nobody had the ball.
        so_far = team_ball_control[:frame_num + 1]
        team_1 = np.count_nonzero(so_far == 1) / len(so_far)
        team_2 = np.count_nonzero(so_far == 2) / len(so_far)

        cv2.putText(frame, f"Team 1 Ball Control: {team_1 * 100:.2f}%", (text_x, text_y1),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)
        cv2.putText(frame, f"Team 2 Ball Control: {team_2 * 100:.2f}%", (text_x, text_y2),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)

        return frame
