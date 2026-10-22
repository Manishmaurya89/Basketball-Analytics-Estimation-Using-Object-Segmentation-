import cv2
import os

# Every frame is held in memory, so long videos are subsampled down to about this many.
MAX_FRAMES = 1000


def read_video(video_path):
    """Read the video into a list of BGR frames. Returns None if it cannot be opened."""
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return None

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video info: {frame_count} frames, {width}x{height} resolution, {fps} fps")

    subsample_rate = max(1, frame_count // MAX_FRAMES)
    print(f"Keeping 1 out of every {subsample_rate} frames")

    frames = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % subsample_rate == 0:
            frames.append(frame)
        frame_idx += 1
        if frame_idx % 100 == 0:
            print(f"Read {frame_idx}/{frame_count} frames...")

    cap.release()
    print(f"Read {len(frames)} frames from video")
    return frames


def save_video(output_video_frames, output_video_path):
    """Write the frames as an XVID video at 24 fps, creating the folder if needed."""
    output_dir = os.path.dirname(os.path.abspath(output_video_path))
    os.makedirs(output_dir, exist_ok=True)

    if not output_video_frames:
        raise ValueError(f"No frames to save to {output_video_path}")

    height, width = output_video_frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (width, height))
    if not out.isOpened():
        out.release()
        raise RuntimeError(
            f"Could not create output video at {output_video_path}. "
            "Check the output path and video codec support."
        )

    try:
        for frame in output_video_frames:
            if frame.shape[:2] != (height, width):
                raise ValueError("All output video frames must have the same dimensions.")
            out.write(frame)
    finally:
        out.release()
