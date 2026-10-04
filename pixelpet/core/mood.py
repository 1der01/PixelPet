"""Mood system for PixelPet."""


class MoodSystem:
    """Determines the pet's mood based on its stats."""

    MOODS = [
        "Happy",
        "Normal",
        "Hungry",
        "Sleepy",
        "Sad",
        "Dirty",
        "Excited",
        "Angry",
    ]

    @staticmethod
    def calculate_mood(stats):
        """Calculate mood based on current stats."""
        if stats.hunger < 30:
            return "Hungry"
        if stats.energy < 30:
            return "Sleepy"
        if stats.cleanliness < 30:
            return "Dirty"
        if stats.happiness < 30:
            return "Sad"
        if stats.happiness > 80 and stats.energy > 70:
            return "Excited"
        if stats.happiness < 20:
            return "Angry"
        if stats.happiness > 70:
            return "Happy"
        return "Normal"

    @staticmethod
    def get_expression(mood):
        """Get ASCII art expression based on mood."""
        expressions = {
            "Happy": "( ^ _ ^ )",
            "Normal": "( o . o )",
            "Hungry": "( O . O )",
            "Sleepy": "( - . - )",
            "Sad": "( T . T )",
            "Dirty": "( @ . @ )",
            "Excited": "( > w < )",
            "Angry": "( # . # )",
        }
        return expressions.get(mood, "( o . o )")

    @staticmethod
    def get_color(mood):
        """Get color associated with mood."""
        colors = {
            "Happy": "#FFD700",
            "Normal": "#FFFFFF",
            "Hungry": "#FF6B6B",
            "Sleepy": "#9370DB",
            "Sad": "#87CEEB",
            "Dirty": "#8B4513",
            "Excited": "#FF69B4",
            "Angry": "#FF4500",
        }
        return colors.get(mood, "#FFFFFF")
