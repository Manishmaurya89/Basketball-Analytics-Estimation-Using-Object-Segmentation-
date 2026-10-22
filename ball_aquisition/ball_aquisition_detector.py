from utils.bbox_utils import measure_distance, get_center_of_bbox


class BallAquisitionDetector:
    """Works out which player has the ball in each frame.

    A player whose box covers most of the ball wins outright. Otherwise the
    nearest player within `possession_threshold` pixels gets it. Either way
    they need to keep it for `min_frames` frames in a row before it counts.
    """

    def __init__(self):
        self.possession_threshold = 50
        self.min_frames = 11
        self.containment_threshold = 0.8

    def get_key_basketball_player_assignment_points(self, player_bbox, ball_center):
        """Points on the player's box to measure the ball against.

        Using the edges and corners instead of just the centre means a ball
        held out to the side still counts as close.
        """
        ball_x, ball_y = ball_center
        x1, y1, x2, y2 = player_bbox
        width = x2 - x1
        height = y2 - y1

        points = []
        # Closest points on the box edges level with the ball.
        if y1 < ball_y < y2:
            points += [(x1, ball_y), (x2, ball_y)]
        if x1 < ball_x < x2:
            points += [(ball_x, y1), (ball_x, y2)]

        points += [
            (x1 + width // 2, y1),
            (x2, y1),
            (x1, y1),
            (x2, y1 + height // 2),
            (x1, y1 + height // 2),
            (x1 + width // 2, y1 + height // 2),
            (x2, y2),
            (x1, y2),
            (x1 + width // 2, y2),
            (x1 + width // 2, y1 + height // 3),
        ]
        return points

    def calculate_ball_containment_ratio(self, player_bbox, ball_bbox):
        """Fraction of the ball's box that lies inside the player's box (0 to 1)."""
        px1, py1, px2, py2 = player_bbox
        bx1, by1, bx2, by2 = ball_bbox

        ix1, iy1 = max(px1, bx1), max(py1, by1)
        ix2, iy2 = min(px2, bx2), min(py2, by2)
        if ix2 < ix1 or iy2 < iy1:
            return 0.0

        intersection_area = (ix2 - ix1) * (iy2 - iy1)
        ball_area = (bx2 - bx1) * (by2 - by1)
        return intersection_area / ball_area

    def find_minimum_distance_to_ball(self, ball_center, player_bbox):
        key_points = self.get_key_basketball_player_assignment_points(player_bbox, ball_center)
        return min(measure_distance(ball_center, point) for point in key_points)

    def find_best_candidate_for_possession(self, ball_center, player_tracks_frame, ball_bbox):
        """Return the player_id most likely holding the ball in this frame, or -1."""
        high_containment_players = []
        other_players = []

        for player_id, player_info in player_tracks_frame.items():
            player_bbox = player_info.get('bbox', [])
            if not player_bbox:
                continue

            containment = self.calculate_ball_containment_ratio(player_bbox, ball_bbox)
            min_distance = self.find_minimum_distance_to_ball(ball_center, player_bbox)

            if containment > self.containment_threshold:
                high_containment_players.append((player_id, min_distance))
            else:
                other_players.append((player_id, min_distance))

        if high_containment_players:
            return max(high_containment_players, key=lambda x: x[1])[0]

        if other_players:
            player_id, distance = min(other_players, key=lambda x: x[1])
            if distance < self.possession_threshold:
                return player_id

        return -1

    def detect_ball_possession(self, player_tracks, ball_tracks):
        """Return a list with the player_id holding the ball in each frame, or -1 for nobody."""
        num_frames = len(ball_tracks)
        possession_list = [-1] * num_frames
        consecutive_frames = {}

        for frame_num in range(num_frames):
            ball_bbox = ball_tracks[frame_num].get(1, {}).get('bbox', [])
            if not ball_bbox:
                continue

            best_player_id = self.find_best_candidate_for_possession(
                get_center_of_bbox(ball_bbox),
                player_tracks[frame_num],
                ball_bbox,
            )

            if best_player_id == -1:
                consecutive_frames = {}
                continue

            # Only the current candidate's streak is kept; anyone else starts over.
            consecutive_frames = {best_player_id: consecutive_frames.get(best_player_id, 0) + 1}
            if consecutive_frames[best_player_id] >= self.min_frames:
                possession_list[frame_num] = best_player_id

        return possession_list
