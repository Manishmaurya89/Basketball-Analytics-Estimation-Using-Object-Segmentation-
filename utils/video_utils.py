"""
A module for reading and writing video files.

This module provides utility functions to load video frames into memory and save
processed frames back to video files, with support for common video formats.
"""

import cv2
import os

def read_video(video_path):
    """
    Read all frames from a video file into memory.

    Args:
        video_path (str): Path to the input video file.

    Returns:
        list: List of video frames as numpy arrays.
        or None if the video could not be read.
    """
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None
        
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return None
        
    # Get video info
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Video info: {frame_count} frames, {width}x{height} resolution, {fps} fps")
    
    # Limit frame count or subsample if memory is a concern
    target_frame_count = min(frame_count, 1000)  # Limit to 1000 frames to avoid memory issues
    subsample_rate = max(1, frame_count // target_frame_count)
    
    print(f"Processing 1 out of every {subsample_rate} frames to avoid memory issues")
    
    frames = []
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Only process every nth frame to reduce memory usage
        if frame_idx % subsample_rate == 0:
            frames.append(frame)
            
        frame_idx += 1
        
        # Print progress periodically
        if frame_idx % 100 == 0:
            print(f"Processed {frame_idx}/{frame_count} frames...")
    
    cap.release()
    print(f"Successfully read {len(frames)} frames from video")
    return frames

def save_video(ouput_video_frames, output_video_path):
    """
    Save a sequence of frames as a video file.

    Creates necessary directories if they don't exist and writes frames using XVID codec.

    Args:
        ouput_video_frames (list): List of frames to save.
        output_video_path (str): Path where the video should be saved.
    """
    # Resolve the directory so paths like "output.avi" work too.
    output_dir = os.path.dirname(os.path.abspath(output_video_path))
    os.makedirs(output_dir, exist_ok=True)

    # Do not silently produce an empty or missing output file.
    if not ouput_video_frames:
        raise ValueError(f"No frames to save to {output_video_path}")

    height, width = ouput_video_frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (width, height))
    if not out.isOpened():
        out.release()
        raise RuntimeError(
            f"Could not create output video at {output_video_path}. "
            "Check the output path and video codec support."
        )

    try:
        for frame in ouput_video_frames:
            if frame.shape[:2] != (height, width):
                raise ValueError("All output video frames must have the same dimensions.")
            out.write(frame)
    finally:
        out.release()