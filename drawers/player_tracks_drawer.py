from .utils import draw_ellipse, draw_triangle


class PlayerTracksDrawer:
    """Draws each player's ellipse in their team colour, plus a red pointer on whoever has the ball.

    Draws on the frames in place.
    """

    def __init__(self, team_1_color=[255, 245, 238], team_2_color=[128, 0, 0]):
        self.default_player_team_id = 1
        self.team_1_color = team_1_color
        self.team_2_color = team_2_color

    def draw(self, video_frames, tracks, player_assignment, ball_aquisition):
        if not video_frames or not tracks:
            print("Warning: No frames or player tracks to draw")
            return video_frames

        if len(video_frames) > len(tracks):
            print(f"Warning: More frames ({len(video_frames)}) than player tracks ({len(tracks)}).")

        num_assignments = len(player_assignment) if player_assignment else 0
        num_ball_acquisitions = len(ball_aquisition) if ball_aquisition else 0

        for frame_num, (frame, player_dict) in enumerate(zip(video_frames, tracks)):
            if frame is None or not player_dict:
                continue

            try:
                teams = player_assignment[frame_num] if frame_num < num_assignments else {}
                player_with_ball = ball_aquisition[frame_num] if frame_num < num_ball_acquisitions else None

                for track_id, player in player_dict.items():
                    if player["bbox"] is None:
                        continue

                    team_id = teams.get(track_id, self.default_player_team_id)
                    color = self.team_1_color if team_id == 1 else self.team_2_color
                    draw_ellipse(frame, player["bbox"], color, track_id)

                    if track_id == player_with_ball:
                        draw_triangle(frame, player["bbox"], (0, 0, 255))
            except Exception as e:
                print(f"Error processing player tracks for frame {frame_num}: {e}")

        return video_frames
