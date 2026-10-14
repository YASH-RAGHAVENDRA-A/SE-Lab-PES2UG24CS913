import math
import pygame


class Rope:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.center_y = screen_height // 2

        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180

        self.pull_step = 12

        # Animation state
        self.velocity = 0.0
        self.tension = 0.0

    def pull_left(self, strength=1.0):
        distance = self.pull_step * strength

        self.marker_x -= distance

        # Negative = movement towards the player
        self.velocity = -distance

        # Increase rope tension
        self.tension = min(
            1.0,
            self.tension + 0.35
        )

    def pull_right(self, strength=1.0):
        distance = self.pull_step * strength

        self.marker_x += distance

        # Positive = movement towards computer
        self.velocity = distance

        # Increase rope tension
        self.tension = min(
            1.0,
            self.tension + 0.35
        )

    def update(self):
        """
        Gradually reduce rope momentum and tension
        so that the animation settles after each pull.
        """

        # Reduce momentum gradually
        self.velocity *= 0.86

        # Reduce rope tension gradually
        self.tension *= 0.92

        if abs(self.velocity) < 0.05:
            self.velocity = 0.0

        if self.tension < 0.02:
            self.tension = 0.0

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"

        if self.marker_x >= self.right_win_x:
            return "COMPUTER"

        return None

    def reset(self):
        self.marker_x = float(
            self.screen_width // 2
        )

        self.velocity = 0.0
        self.tension = 0.0

    def render(self, surface):

        start_x = 60
        end_x = self.screen_width - 60

        current_time = (
            pygame.time.get_ticks() / 1000.0
        )

        points = []

        # More points = smoother rope animation
        segments = max(
            2,
            (end_x - start_x) // 10
        )

        for i in range(segments + 1):

            x = (
                start_x
                + (end_x - start_x)
                * i
                / segments
            )

            # Position from 0 to 1
            position = i / segments

            # Animation strongest near the middle
            envelope = math.sin(
                math.pi * position
            )

            # Rope sag increases with tension
            sag = (
                8.0
                * self.tension
                * envelope
            )

            # Rope vibration increases with tension
            vibration = (
                math.sin(
                    x * 0.16
                    + current_time * 18.0
                )
                * (
                    1.5
                    + 4.5 * self.tension
                )
                * envelope
            )

            y = (
                self.center_y
                + sag
                + vibration
            )

            points.append(
                (
                    int(x),
                    int(y)
                )
            )

        # Draw dynamic rope
        pygame.draw.lines(
            surface,
            (180, 140, 90),
            False,
            points,
            10
        )

        # Player winning boundary
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (
                self.left_win_x,
                self.center_y - 40
            ),
            (
                self.left_win_x,
                self.center_y + 40
            ),
            4
        )

        # Computer winning boundary
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (
                self.right_win_x,
                self.center_y - 40
            ),
            (
                self.right_win_x,
                self.center_y + 40
            ),
            4
        )

        # Center boundary
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (
                self.screen_width // 2,
                self.center_y - 20
            ),
            (
                self.screen_width // 2,
                self.center_y + 20
            ),
            2
        )

        # Red center flag
        flag_rect = pygame.Rect(
            int(self.marker_x) - 12,
            self.center_y - 24,
            24,
            48
        )

        pygame.draw.rect(
            surface,
            (230, 40, 40),
            flag_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            flag_rect,
            width=2,
            border_radius=4
        )