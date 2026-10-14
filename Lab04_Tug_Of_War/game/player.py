import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label

        self.font = pygame.font.SysFont(
            None,
            24
        )

    def render(self, surface, lean=0.0):

        # Limit the amount of leaning
        lean = max(
            -18.0,
            min(18.0, lean)
        )

        center_x = int(self.x)

        # Feet remain fixed while upper body leans
        top_x = int(
            self.x + lean
        )

        top_y = self.y - 35
        bottom_y = self.y + 35

        # Body
        body_points = [
            (
                top_x - 20,
                top_y
            ),
            (
                top_x + 20,
                top_y
            ),
            (
                center_x + 20,
                bottom_y
            ),
            (
                center_x - 20,
                bottom_y
            )
        ]

        pygame.draw.polygon(
            surface,
            self.color,
            body_points
        )

        # Head also follows the lean
        head_x = int(
            self.x + lean * 1.15
        )

        pygame.draw.circle(
            surface,
            (240, 210, 180),
            (
                head_x,
                self.y - 50
            ),
            16
        )

        # Feet / anchor
        pygame.draw.line(
            surface,
            (30, 30, 30),
            (
                center_x - 24,
                bottom_y
            ),
            (
                center_x + 24,
                bottom_y
            ),
            6
        )

        # Label
        label_surface = self.font.render(
            self.label,
            True,
            (240, 240, 240)
        )

        surface.blit(
            label_surface,
            (
                self.x
                - label_surface.get_width() // 2,
                self.y + 45
            )
        )