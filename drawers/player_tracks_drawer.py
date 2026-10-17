from .utils import draw_ellipse,draw_traingle

class PlayerTracksDrawer:
    """
    A class responsible for drawing player tracks and ball possession indicators on video frames.

    Attributes:
        default_player_team_id (int): Default team ID used when a player's team is not specified.
        team_1_color (list): RGB color used to represent Team 1 players.
        team_2_color (list): RGB color used to represent Team 2 players.
    """
    def __init__(self,team_1_color=[255, 245, 238],team_2_color=[128, 0, 0]):
        """
        Initialize the PlayerTracksDrawer with specified team colors.

        Args:
            team_1_color (list, optional): RGB color for Team 1. Defaults to [255, 245, 238].
            team_2_color (list, optional): RGB color for Team 2. Defaults to [128, 0, 0].
        """
        self.default_player_team_id = 1
        self.team_1_color=team_1_color
        self.team_2_color=team_2_color

    def draw(self, video_frames, tracks, player_assignment, ball_aquisition):
        """
        Draw player tracks and ball possession indicators on a list of video frames.

        Args:
            video_frames (list): A list of frames (as NumPy arrays or image objects) on which to draw.
            tracks (list): A list of dictionaries where each dictionary contains player tracking information
                for the corresponding frame.
            player_assignment (list): A list of dictionaries indicating team assignments for each player
                in the corresponding frame.
            ball_aquisition (list): A list indicating which player has possession of the ball in each frame.

        Returns:
            list: A list of frames with player tracks and ball possession indicators drawn on them.
        """
        # Check if we have valid inputs
        if not video_frames or not tracks:
            print("Warning: No frames or player tracks to draw")
            return video_frames
            
        # Make sure all data arrays match the number of frames
        num_frames = len(video_frames)
        num_tracks = len(tracks)
        num_assignments = len(player_assignment) if player_assignment else 0
        num_ball_acquisitions = len(ball_aquisition) if ball_aquisition else 0
        
        if num_frames > num_tracks:
            print(f"Warning: More frames ({num_frames}) than player tracks ({num_tracks}).")
            max_frames = num_tracks
        else:
            max_frames = num_frames
            
        # Process frames in-place
        for frame_num in range(max_frames):
            # Skip empty frames
            if video_frames[frame_num] is None:
                continue
                
            # Get player data for this frame
            try:
                player_dict = tracks[frame_num]
                if not player_dict:  # Skip if no players in this frame
                    continue
                    
                # Get team assignments and ball possession if available
                player_assignment_for_frame = player_assignment[frame_num] if frame_num < num_assignments else {}
                player_id_has_ball = ball_aquisition[frame_num] if frame_num < num_ball_acquisitions else None
                
                # Draw Players
                for track_id, player in player_dict.items():
                    if player["bbox"] is None:  # Skip if no bounding box
                        continue
                        
                    # Get team color
                    team_id = player_assignment_for_frame.get(track_id, self.default_player_team_id)
                    color = self.team_1_color if team_id == 1 else self.team_2_color
                    
                    # Draw directly on the frame (modifies in-place)
                    draw_ellipse(video_frames[frame_num], player["bbox"], color, track_id)
                    
                    # Draw ball possession indicator if this player has the ball
                    if player_id_has_ball is not None and track_id == player_id_has_ball:
                        draw_traingle(video_frames[frame_num], player["bbox"], (0, 0, 255))
                        
            except Exception as e:
                print(f"Error processing player tracks for frame {frame_num}: {e}")
                continue

        return video_frames
        
