from .utils import draw_traingle

class BallTracksDrawer:
    """
    A drawer class responsible for drawing ball tracks on video frames.

    Attributes:
        ball_pointer_color (tuple): The color used to draw the ball pointers (in BGR format).
    """

    def __init__(self):
        """
        Initialize the BallTracksDrawer instance with default settings.
        """
        self.ball_pointer_color = (0, 255, 0)

    def draw(self, video_frames, tracks):
        """
        Draws ball pointers on each video frame based on provided tracking information.

        Args:
            video_frames (list): A list of video frames (as NumPy arrays or image objects).
            tracks (list): A list of dictionaries where each dictionary contains ball information
                for the corresponding frame.

        Returns:
            list: A list of processed video frames with drawn ball pointers.
        """
        # We'll modify the frames in-place to save memory
        # The caller has already made copies if needed
        output_video_frames = video_frames
        
        # Make sure we have valid tracks to process
        if not tracks or len(tracks) == 0:
            print("Warning: No ball tracks to draw")
            return output_video_frames
            
        # Make sure tracks match the number of frames
        if len(video_frames) > len(tracks):
            print(f"Warning: More frames ({len(video_frames)}) than ball tracks ({len(tracks)}). Using available tracks.")
            max_frames = len(tracks)
        else:
            max_frames = len(video_frames)
            
        for frame_num in range(max_frames):
            # Skip empty frames
            if video_frames[frame_num] is None:
                continue
                
            ball_dict = tracks[frame_num]
            if not ball_dict:  # Skip if no balls in this frame
                continue
                
            # Draw ball (directly on the frame, no copying)
            for _, ball in ball_dict.items():
                if ball["bbox"] is None:
                    continue
                # Apply drawing directly to the frame, no need to reassign
                draw_traingle(video_frames[frame_num], ball["bbox"], self.ball_pointer_color)
            
        return output_video_frames