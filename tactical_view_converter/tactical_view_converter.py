import numpy as np
import cv2
from copy import deepcopy
from .homography import Homography
from utils import get_foot_position, measure_distance


class TacticalViewConverter:
    """Maps players from the camera view onto a top-down court image.

    `key_points` are the court reference points in tactical-view pixels, in the
    same order as the keypoint model's output.
    """

    def __init__(self, court_image_path):
        self.court_image_path = court_image_path
        self.width = 300
        self.height = 161

        self.actual_width_in_meters = 28
        self.actual_height_in_meters = 15

        def x(metres):
            return int((metres / self.actual_width_in_meters) * self.width)

        def y(metres):
            return int((metres / self.actual_height_in_meters) * self.height)

        free_throw_x = 5.79
        self.key_points = [
            # left baseline, top to bottom
            (0, 0),
            (0, y(0.91)),
            (0, y(5.18)),
            (0, y(10)),
            (0, y(14.1)),
            (0, self.height),

            # half-court line
            (self.width // 2, self.height),
            (self.width // 2, 0),

            # left free-throw line
            (x(free_throw_x), y(5.18)),
            (x(free_throw_x), y(10)),

            # right baseline, bottom to top
            (self.width, self.height),
            (self.width, y(14.1)),
            (self.width, y(10)),
            (self.width, y(5.18)),
            (self.width, y(0.91)),
            (self.width, 0),

            # right free-throw line
            (x(self.actual_width_in_meters - free_throw_x), y(5.18)),
            (x(self.actual_width_in_meters - free_throw_x), y(10)),
        ]

    def validate_keypoints(self, keypoints_list):
        """Zero out detected keypoints whose spacing doesn't match the real court.

        For each detected point, compare its distance ratio to two other detected
        points against the same ratio on the tactical court. Points that are off
        by more than 80% are treated as misdetections. Returns a copy; the input
        is left untouched.
        """
        keypoints_list = deepcopy(keypoints_list)

        for frame_idx, frame_keypoints in enumerate(keypoints_list):
            frame_keypoints = frame_keypoints.xy.tolist()[0]

            # The model reports undetected points as (0, 0).
            detected_indices = [i for i, kp in enumerate(frame_keypoints) if kp[0] > 0 and kp[1] > 0]
            if len(detected_indices) < 3:
                continue

            invalid_keypoints = []
            for i in detected_indices:
                other_indices = [idx for idx in detected_indices if idx != i and idx not in invalid_keypoints]
                if len(other_indices) < 2:
                    continue
                j, k = other_indices[0], other_indices[1]

                d_ij = measure_distance(frame_keypoints[i], frame_keypoints[j])
                d_ik = measure_distance(frame_keypoints[i], frame_keypoints[k])
                t_ij = measure_distance(self.key_points[i], self.key_points[j])
                t_ik = measure_distance(self.key_points[i], self.key_points[k])

                if t_ij > 0 and t_ik > 0:
                    prop_detected = d_ij / d_ik if d_ik > 0 else float('inf')
                    prop_tactical = t_ij / t_ik
                    error = abs((prop_detected - prop_tactical) / prop_tactical)

                    if error > 0.8:
                        keypoints_list[frame_idx].xy[0][i] *= 0
                        keypoints_list[frame_idx].xyn[0][i] *= 0
                        invalid_keypoints.append(i)

        return keypoints_list

    def transform_players_to_tactical_view(self, keypoints_list, player_tracks):
        """Return one dict per frame mapping player_id -> (x, y) on the tactical court.

        Frames with fewer than 4 good keypoints can't be mapped and come back
        empty, as do players who land outside the court.
        """
        tactical_player_positions = []

        for frame_keypoints, frame_tracks in zip(keypoints_list, player_tracks):
            tactical_positions = {}
            frame_keypoints = frame_keypoints.xy.tolist()[0]

            valid_indices = [i for i, kp in enumerate(frame_keypoints) if kp[0] > 0 and kp[1] > 0]
            if len(valid_indices) < 4:
                tactical_player_positions.append(tactical_positions)
                continue

            source_points = np.array([frame_keypoints[i] for i in valid_indices], dtype=np.float32)
            target_points = np.array([self.key_points[i] for i in valid_indices], dtype=np.float32)

            try:
                homography = Homography(source_points, target_points)

                for player_id, player_data in frame_tracks.items():
                    foot = np.array([get_foot_position(player_data["bbox"])])
                    tx, ty = homography.transform_points(foot)[0]

                    if 0 <= tx <= self.width and 0 <= ty <= self.height:
                        tactical_positions[player_id] = [float(tx), float(ty)]
            except (ValueError, cv2.error):
                # Degenerate keypoints; leave this frame without positions.
                pass

            tactical_player_positions.append(tactical_positions)

        return tactical_player_positions
