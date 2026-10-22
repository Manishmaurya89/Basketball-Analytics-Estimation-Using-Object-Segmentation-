class PassAndInterceptionDetector:
    """Turns per-frame ball possession into pass and interception events.

    Both methods return a list with one entry per frame: the team (1 or 2) that
    made the pass or interception on that frame, or -1 if nothing happened.
    """

    def _possession_changes(self, ball_acquisition, player_assignment):
        """Yield (frame, previous_team, new_team) each time the ball moves to a different player.

        Frames where nobody has the ball are skipped over, so a loose ball
        between two players still counts as one change of hands.
        """
        prev_holder = -1
        prev_frame = -1

        for frame in range(1, len(ball_acquisition)):
            if ball_acquisition[frame - 1] != -1:
                prev_holder = ball_acquisition[frame - 1]
                prev_frame = frame - 1

            current_holder = ball_acquisition[frame]
            if prev_holder != -1 and current_holder != -1 and prev_holder != current_holder:
                yield (
                    frame,
                    player_assignment[prev_frame].get(prev_holder, -1),
                    player_assignment[frame].get(current_holder, -1),
                )

    def detect_passes(self, ball_acquisition, player_assignment):
        passes = [-1] * len(ball_acquisition)
        for frame, prev_team, new_team in self._possession_changes(ball_acquisition, player_assignment):
            if prev_team != -1 and prev_team == new_team:
                passes[frame] = prev_team
        return passes

    def detect_interceptions(self, ball_acquisition, player_assignment):
        interceptions = [-1] * len(ball_acquisition)
        for frame, prev_team, new_team in self._possession_changes(ball_acquisition, player_assignment):
            if prev_team != -1 and new_team != -1 and prev_team != new_team:
                interceptions[frame] = new_team
        return interceptions
