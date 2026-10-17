import supervision as sv

class CourtKeypointDrawer:
    """
    A drawer class responsible for drawing court keypoints on a sequence of frames.

    Attributes:
        keypoint_color (str): Hex color value for the keypoints.
    """
    def __init__(self):
        self.keypoint_color = '#ff2c2c'

    def draw(self, frames, court_keypoints):
        """
        Draws court keypoints on a given list of frames.

        Args:
            frames (list): A list of frames (as NumPy arrays or image objects) on which to draw.
            court_keypoints (list): A corresponding list of lists where each sub-list contains
                the (x, y) coordinates of court keypoints for that frame.

        Returns:
            list: A list of frames with keypoints drawn on them.
        """
        # Check if we have valid inputs
        if not frames or not court_keypoints:
            print("Warning: No frames or court keypoints to draw")
            return frames
            
        # Make sure keypoints match the number of frames
        if len(frames) > len(court_keypoints):
            print(f"Warning: More frames ({len(frames)}) than keypoints ({len(court_keypoints)}). Using available keypoints.")
            max_frames = len(court_keypoints)
        else:
            max_frames = len(frames)
            
        vertex_annotator = sv.VertexAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            radius=8)
        
        vertex_label_annotator = sv.VertexLabelAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            text_color=sv.Color.WHITE,
            text_scale=0.5,
            text_thickness=1
        )
        
        # Process frames in-place to save memory
        for index in range(max_frames):
            # Skip empty frames
            if frames[index] is None:
                continue
                
            # Get keypoints for this frame
            try:
                keypoints = court_keypoints[index]
                if keypoints is None or len(keypoints) == 0:
                    continue
                    
                # Draw dots directly on the frame (modifies frame in-place)
                vertex_annotator.annotate(
                    scene=frames[index],
                    key_points=keypoints)
                    
                # Draw labels (modifies frame in-place)
                # Convert PyTorch tensor to numpy array if needed
                try:
                    keypoints_numpy = keypoints.cpu().numpy()
                except AttributeError:
                    # Already numpy array or similar format
                    keypoints_numpy = keypoints
                    
                vertex_label_annotator.annotate(
                    scene=frames[index],
                    key_points=keypoints_numpy)
            except Exception as e:
                print(f"Error processing frame {index}: {e}")
                continue

        return frames