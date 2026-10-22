import cv2


class TacticalViewDrawer:
    """Overlays the top-down court in the top-left corner with players as team-coloured dots."""

    def __init__(self, team_1_color=[255, 245, 238], team_2_color=[128, 0, 0]):
        self.start_x = 20
        self.start_y = 40
        self.team_1_color = team_1_color
        self.team_2_color = team_2_color

    def draw(self,
             video_frames,
             court_image_path,
             width,
             height,
             tactical_court_keypoints,
             tactical_player_positions=None,
             player_assignment=None,
             ball_acquisition=None):
        court_image = cv2.imread(court_image_path)
        court_image = cv2.resize(court_image, (width, height))

        x1, y1 = self.start_x, self.start_y
        x2, y2 = self.start_x + width, self.start_y + height
        player_radius = 8

        output_video_frames = []
        for frame_idx, frame in enumerate(video_frames):
            frame = frame.copy()

            alpha = 0.6
            overlay = frame[y1:y2, x1:x2].copy()
            cv2.addWeighted(court_image, alpha, overlay, 1 - alpha, 0, frame[y1:y2, x1:x2])

            for keypoint_index, (x, y) in enumerate(tactical_court_keypoints):
                x += self.start_x
                y += self.start_y
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                cv2.putText(frame, str(keypoint_index), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if tactical_player_positions and player_assignment and frame_idx < len(tactical_player_positions):
                frame_positions = tactical_player_positions[frame_idx]
                teams = player_assignment[frame_idx] if frame_idx < len(player_assignment) else {}
                player_with_ball = ball_acquisition[frame_idx] if ball_acquisition and frame_idx < len(ball_acquisition) else -1

                for player_id, position in frame_positions.items():
                    color = self.team_1_color if teams.get(player_id, 1) == 1 else self.team_2_color
                    x = int(position[0]) + self.start_x
                    y = int(position[1]) + self.start_y
                    cv2.circle(frame, (x, y), player_radius, color, -1)

                    if player_id == player_with_ball:
                        cv2.circle(frame, (x, y), player_radius + 3, (0, 0, 255), 2)

            output_video_frames.append(frame)

        return output_video_frames
