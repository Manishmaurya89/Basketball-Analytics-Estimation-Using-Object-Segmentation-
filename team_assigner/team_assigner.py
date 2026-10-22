from PIL import Image
import cv2
from transformers import CLIPProcessor, CLIPModel
from utils import read_stub, save_stub


class TeamAssigner:
    """Splits players into two teams by asking Fashion-CLIP which jersey description fits better.

    Change the two class names to match the jerseys in your video.
    """

    def __init__(self, team_1_class_name="white shirt", team_2_class_name="dark blue shirt"):
        self.player_team_dict = {}
        self.team_1_class_name = team_1_class_name
        self.team_2_class_name = team_2_class_name

    def load_model(self):
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

    def get_player_color(self, frame, bbox):
        """Return whichever team class name CLIP thinks matches the player crop."""
        crop = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
        image = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))

        classes = [self.team_1_class_name, self.team_2_class_name]
        inputs = self.processor(text=classes, images=image, return_tensors="pt", padding=True)
        probs = self.model(**inputs).logits_per_image.softmax(dim=1)
        return classes[probs.argmax(dim=1)[0]]

    def get_player_team(self, frame, player_bbox, player_id):
        """Return 1 or 2, reusing the earlier answer for a player we have already classified."""
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        team_id = 1 if self.get_player_color(frame, player_bbox) == self.team_1_class_name else 2
        self.player_team_dict[player_id] = team_id
        return team_id

    def get_player_teams_across_frames(self, video_frames, player_tracks, read_from_stub=False, stub_path=None):
        """Return one dict per frame mapping player_id -> team (1 or 2)."""
        player_assignment = read_stub(read_from_stub, stub_path)
        if player_assignment is not None and len(player_assignment) == len(video_frames):
            return player_assignment

        self.load_model()

        player_assignment = []
        for frame_num, player_track in enumerate(player_tracks):
            # Re-classify everyone every 50 frames so one bad crop doesn't stick for the whole video.
            if frame_num % 50 == 0:
                self.player_team_dict = {}

            player_assignment.append({
                player_id: self.get_player_team(video_frames[frame_num], track['bbox'], player_id)
                for player_id, track in player_track.items()
            })

        save_stub(stub_path, player_assignment)
        return player_assignment
