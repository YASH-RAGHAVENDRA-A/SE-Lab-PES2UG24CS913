import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    SUDDEN_DEATH_SECONDS = 45.0
    BASE_COMPUTER_COOLDOWN = 180
    MIN_PANIC_COOLDOWN = 70

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rope = Rope(width, height)

        self.player = Puller(
            90,
            height // 2,
            (50, 120, 220),
            "PLAYER (A/D)"
        )

        self.computer = Puller(
            width - 90,
            height // 2,
            (220, 80, 50),
            "COMPUTER"
        )

        # Stores the last key that actually produced a pull.
        # This replaces the old lock-based input design.
        self.last_key = None

        self.winner = None
        self.game_state = "PLAYING"

        # Computer AI settings
        self.computer_pull_cooldown = self.BASE_COMPUTER_COOLDOWN
        self.last_computer_pull = pygame.time.get_ticks()

        # Timer
        self.match_start_time = pygame.time.get_ticks()
        self.elapsed_seconds = 0.0
        self.sudden_death = False

        # AI panic state
        self.panic_mode = False

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)
        self.font_timer = pygame.font.SysFont(None, 32)

    @staticmethod
    def _clamp(value, low, high):
        return max(low, min(high, value))

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        # ---------------------------------------------------------
        # TASK 1: Alternating A/D input
        # ---------------------------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):

                # Accept only a different key from the previous
                # successful pull.
                if event.key != self.last_key:

                    # TASK 4: Double pull distance during sudden death
                    pull_multiplier = 2.0 if self.sudden_death else 1.0

                    self.rope.pull_left(pull_multiplier)

                    self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # ---------------------------------------------------------
        # TASK 4: Match timer
        # ---------------------------------------------------------
        self.elapsed_seconds = (
            now - self.match_start_time
        ) / 1000.0

        if self.elapsed_seconds >= self.SUDDEN_DEATH_SECONDS:
            self.sudden_death = True

        # Update rope animation/momentum decay
        self.rope.update()

        # ---------------------------------------------------------
        # TASK 2: Dynamic AI panic surge
        # ---------------------------------------------------------

        total_range = (
            self.rope.right_win_x -
            self.rope.left_win_x
        )

        # 0 = center
        # 1 = player's winning boundary
        player_threat = (
            self.rope.right_win_x -
            self.rope.marker_x
        ) / total_range

        player_threat = self._clamp(
            player_threat,
            0.0,
            1.0
        )

        # Panic starts when player has travelled 65%
        # of the distance toward the winning boundary.
        panic_start = 0.65

        self.panic_mode = player_threat >= panic_start

        if self.panic_mode:

            panic_ratio = (
                player_threat - panic_start
            ) / (1.0 - panic_start)

            # Reduce the computer cooldown as danger increases.
            self.computer_pull_cooldown = int(
                self.BASE_COMPUTER_COOLDOWN
                -
                (
                    self.BASE_COMPUTER_COOLDOWN
                    - self.MIN_PANIC_COOLDOWN
                )
                * panic_ratio
            )

            # Increase computer pulling strength.
            base_strength = random.uniform(0.9, 1.2)
            panic_bonus = 0.5 * panic_ratio

            computer_strength = (
                base_strength +
                panic_bonus
            )

        else:

            self.computer_pull_cooldown = (
                self.BASE_COMPUTER_COOLDOWN
            )

            computer_strength = (
                random.uniform(0.7, 1.2)
            )

        # ---------------------------------------------------------
        # TASK 4: Sudden Death doubles computer pull
        # ---------------------------------------------------------

        if self.sudden_death:
            computer_strength *= 2.0

        # Perform computer pull when cooldown expires
        if (
            now - self.last_computer_pull
            >= self.computer_pull_cooldown
        ):

            self.rope.pull_right(
                computer_strength
            )

            self.last_computer_pull = now

        # ---------------------------------------------------------
        # Check winner
        # ---------------------------------------------------------

        result = self.rope.check_winner()

        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()

        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        now = pygame.time.get_ticks()

        self.last_computer_pull = now

        self.match_start_time = now
        self.elapsed_seconds = 0.0

        self.sudden_death = False
        self.panic_mode = False

        self.computer_pull_cooldown = (
            self.BASE_COMPUTER_COOLDOWN
        )

    def render(self, screen):
        screen.fill((30, 32, 36))

        # Mud area
        mud_rect = pygame.Rect(
            self.width // 2 - 120,
            self.height // 2 - 80,
            240,
            160
        )

        pygame.draw.rect(
            screen,
            (45, 38, 30),
            mud_rect,
            border_radius=12
        )

        self.rope.render(screen)

        # ---------------------------------------------------------
        # TASK 3: Puller leaning animation
        # ---------------------------------------------------------

        normalized_velocity = self._clamp(
            self.rope.velocity /
            self.rope.pull_step,
            -1.0,
            1.0
        )

        if normalized_velocity < 0:

            # Player is pulling left.
            player_lean = (
                18.0 * normalized_velocity
            )

            computer_lean = (
                8.0 * normalized_velocity
            )

        elif normalized_velocity > 0:

            # Computer is pulling right.
            player_lean = (
                8.0 * normalized_velocity
            )

            computer_lean = (
                18.0 * normalized_velocity
            )

        else:

            player_lean = 0.0
            computer_lean = 0.0

        self.player.render(
            screen,
            player_lean
        )

        self.computer.render(
            screen,
            computer_lean
        )

        # Instructions
        inst_text = (
            "Alternate [A] and [D] to pull | "
            "Reach the green/red boundary to win"
        )

        inst_surf = self.font_small.render(
            inst_text,
            True,
            (210, 210, 210)
        )

        screen.blit(
            inst_surf,
            (
                self.width // 2
                - inst_surf.get_width() // 2,
                20
            )
        )

        # ---------------------------------------------------------
        # TASK 4: Timer display
        # ---------------------------------------------------------

        timer_text = (
            f"Time: {self.elapsed_seconds:05.1f}s"
        )

        if self.sudden_death:

            timer_text += (
                "  |  SUDDEN DEATH x2"
            )

        elif self.panic_mode:

            timer_text += (
                "  |  PANIC SURGE"
            )

        timer_surf = self.font_timer.render(
            timer_text,
            True,
            (255, 220, 120)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2
                - timer_surf.get_width() // 2,
                55
            )
        )

        # ---------------------------------------------------------
        # Game Over overlay
        # ---------------------------------------------------------

        if self.game_state == "GAME_OVER":

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 180)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            win_text = (
                f"{self.winner} WINS!"
            )

            color = (
                (80, 220, 80)
                if self.winner == "PLAYER"
                else (240, 80, 80)
            )

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2
                    - text_surf.get_width() // 2,
                    self.height // 2 - 50
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )