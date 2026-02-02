import cv2
class FrameNumberDrawer:
    def __init__(self):
        self.text_color = (0, 255, 0)  # Green color for frame numbers
        self.text_position = (10, 30)  # Top left corner
        self.font_scale = 1
        self.thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw(self, frames):
        """
        Draws frame numbers directly on the input frames to save memory.
        
        Args:
            frames (list): List of video frames to annotate with frame numbers
            
        Returns:
            list: The same list of frames, modified in-place with frame numbers
        """
        # Check if frames exist
        if not frames:
            print("Warning: No frames to add frame numbers to")
            return frames
            
        # Process each frame in-place
        for i in range(len(frames)):
            if frames[i] is None:
                continue
                
            # Draw text directly on the frame (modifies the frame in-place)
            cv2.putText(
                frames[i],
                str(i), 
                self.text_position, 
                self.font, 
                self.font_scale, 
                self.text_color, 
                self.thickness
            )
            
        return frames