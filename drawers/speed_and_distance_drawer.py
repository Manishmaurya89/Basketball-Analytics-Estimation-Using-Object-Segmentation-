import cv2


class SpeedAndDistanceDrawer:
    """Writes each player's current speed and total distance under their feet."""

    def draw(self, video_frames, player_tracks, player_distances_per_frame, player_speed_per_frame):
        output_video_frames = []
        total_distances = {}

        for frame, frame_tracks, frame_distances, frame_speeds in zip(
            video_frames, player_tracks, player_distances_per_frame, player_speed_per_frame
        ):
            output_frame = frame.copy()

            for player_id, distance in frame_distances.items():
                total_distances[player_id] = total_distances.get(player_id, 0) + distance

            for player_id, track in frame_tracks.items():
                x1, y1, x2, y2 = track['bbox']
                x = int((x1 + x2) / 2)
                y = int(y2) + 40

                speed = frame_speeds.get(player_id)
                distance = total_distances.get(player_id)
                if speed is not None:
                    cv2.putText(output_frame, f"{speed:.2f} km/h", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                if distance is not None:
                    cv2.putText(output_frame, f"{distance:.2f} m", (x, y + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            output_video_frames.append(output_frame)

        return output_video_frames
