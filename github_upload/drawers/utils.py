"""
A utility module providing functions for drawing shapes on video frames.

This module includes functions to draw triangles and ellipses on frames, which can be used
to represent various annotations such as player positions or ball locations in sports analysis.
"""

import cv2 
import numpy as np
import sys 
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width, get_foot_position

def draw_traingle(frame, bbox, color):
    """
    Draws a filled triangle on the given frame at the specified bounding box location.
    Modifies the frame in-place.

    Args:
        frame (numpy.ndarray): The frame on which to draw the triangle.
        bbox (tuple): A tuple representing the bounding box (x, y, width, height).
        color (tuple): The color of the triangle in BGR format.

    Returns:
        numpy.ndarray: Reference to the same frame that was passed in, for convenience.
    """
    try:
        y = int(bbox[1])
        x, _ = get_center_of_bbox(bbox)

        triangle_points = np.array([
            [x, y],
            [x-10, y-20],
            [x+10, y-20],
        ], dtype=np.int32)  # Ensure int32 type to avoid conversion warnings
        
        cv2.drawContours(frame, [triangle_points], 0, color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points], 0, (0, 0, 0), 2)
    except Exception as e:
        print(f"Error drawing triangle: {e}")
        
    return frame

def draw_ellipse(frame, bbox, color, track_id=None):
    """
    Draws an ellipse and an optional rectangle with a track ID on the given frame at the specified bounding box location.
    Modifies the frame in-place.

    Args:
        frame (numpy.ndarray): The frame on which to draw the ellipse.
        bbox (tuple): A tuple representing the bounding box (x, y, width, height).
        color (tuple): The color of the ellipse in BGR format.
        track_id (int, optional): The track ID to display inside a rectangle. Defaults to None.

    Returns:
        numpy.ndarray: Reference to the same frame that was passed in, for convenience.
    """
    try:
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        width = get_bbox_width(bbox)

        # Draw the ellipse (in-place operation)
        cv2.ellipse(
            frame,
            center=(x_center, y2),
            axes=(int(width), int(0.35*width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4
        )

        # Draw track ID if provided
        if track_id is not None:
            rectangle_width = 40
            rectangle_height = 20
            x1_rect = x_center - rectangle_width//2
            x2_rect = x_center + rectangle_width//2
            y1_rect = (y2 - rectangle_height//2) + 15
            y2_rect = (y2 + rectangle_height//2) + 15

            # Draw ID rectangle (in-place operation)
            cv2.rectangle(
                frame,
                (int(x1_rect), int(y1_rect)),
                (int(x2_rect), int(y2_rect)),
                color,
                cv2.FILLED
            )
            
            # Adjust text position for larger numbers
            x1_text = x1_rect + 12
            if track_id > 99:
                x1_text -= 10
            
            # Draw ID text (in-place operation)
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text), int(y1_rect+15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )
    except Exception as e:
        print(f"Error drawing ellipse: {e}")
    
    return frame