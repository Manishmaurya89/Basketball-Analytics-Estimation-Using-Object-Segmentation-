from utils import measure_distance


class SpeedAndDistanceCalculator:
    """Converts tactical-view pixel positions into metres moved and km/h."""

    def __init__(self, width_in_pixels, height_in_pixels, width_in_meters, height_in_meters):
        self.width_in_pixels = width_in_pixels
        self.height_in_pixels = height_in_pixels
        self.width_in_meters = width_in_meters
        self.height_in_meters = height_in_meters

    def calculate_distance(self, tactical_player_positions):
        """Return one dict per frame with the metres each player moved since they were last seen."""
        last_positions = {}
        output_distances = []

        for frame_positions in tactical_player_positions:
            frame_distances = {}
            for player_id, position in frame_positions.items():
                if player_id in last_positions:
                    frame_distances[player_id] = self.calculate_meter_distance(last_positions[player_id], position)
                last_positions[player_id] = position
            output_distances.append(frame_distances)

        return output_distances

    def calculate_meter_distance(self, previous_pixel_position, current_pixel_position):
        x_scale = self.width_in_meters / self.width_in_pixels
        y_scale = self.height_in_meters / self.height_in_pixels

        previous = (previous_pixel_position[0] * x_scale, previous_pixel_position[1] * y_scale)
        current = (current_pixel_position[0] * x_scale, current_pixel_position[1] * y_scale)

        # Empirical scale factor, not derived from the court size.
        return measure_distance(current, previous) * 0.4

    def calculate_speed(self, distances, fps=30, window_size=5):
        """Return one dict per frame mapping player_id -> speed in km/h.

        Speed is averaged over the last `window_size * 3` frames, and stays 0
        until the player has at least `window_size` distance readings in that window.
        """
        speeds = []

        for frame_idx in range(len(distances)):
            frame_speeds = {}
            start_frame = max(0, frame_idx - window_size * 3 + 1)

            for player_id in distances[frame_idx]:
                total_distance = 0
                frames_present = 0
                seen_before = False

                for i in range(start_frame, frame_idx + 1):
                    if player_id in distances[i]:
                        # The first reading in the window has no earlier frame to pair with.
                        if seen_before:
                            total_distance += distances[i][player_id]
                            frames_present += 1
                        seen_before = True

                if frames_present >= window_size:
                    hours = frames_present / fps / 3600
                    frame_speeds[player_id] = (total_distance / 1000) / hours
                else:
                    frame_speeds[player_id] = 0

            speeds.append(frame_speeds)

        return speeds
