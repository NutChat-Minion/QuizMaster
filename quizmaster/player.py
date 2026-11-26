from dataclasses import dataclass


@dataclass
class Player:
    """Represent a player and track their quiz score."""

    name: str
    score: int = 0

    def __post_init__(self):
        """Validate and normalize player information."""

        if not isinstance(self.name, str):
            raise TypeError("Player name must be a string.")

        self.name = self.name.strip()

        if not self.name:
            raise ValueError("Player name cannot be empty.")

        if not isinstance(self.score, int) or isinstance(self.score, bool):
            raise ValueError("Score must be an integer.")

        if self.score < 0:
            raise ValueError("Score cannot be negative.")

    def add_points(self, points: int) -> None:
        """Add points to the player's current score."""

        if not isinstance(points, int) or isinstance(points, bool):
            raise ValueError("Points must be an integer.")

        if points < 0:
            raise ValueError("Points cannot be negative.")

        self.score += points

    def reset_score(self) -> None:
        """Reset the player's score to zero."""

        self.score = 0

    def __str__(self) -> str:
        """Return a readable representation of the player."""

        return f"{self.name}: {self.score} points"