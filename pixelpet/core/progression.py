"""Progression system for PixelPet."""


class Progression:
    """Manages pet level, experience, and unlocks."""

    def __init__(self, level=1, experience=0, inventory=None, achievements=None):
        self.level = level
        self.experience = experience
        self.inventory = inventory or []
        self.achievements = achievements or []

    def to_dict(self):
        """Convert progression to dictionary for saving."""
        return {
            "level": self.level,
            "experience": self.experience,
            "inventory": self.inventory,
            "achievements": self.achievements,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Progression from dictionary."""
        return cls(
            level=data.get("level", 1),
            experience=data.get("experience", 0),
            inventory=data.get("inventory", []),
            achievements=data.get("achievements", []),
        )

    def add_experience(self, amount):
        """Add experience and check for level up."""
        self.experience += amount
        leveled_up = False
        while self.experience >= self.xp_for_next_level():
            self.experience -= self.xp_for_next_level()
            self.level += 1
            leveled_up = True
            self.check_unlocks()
        return leveled_up

    def xp_for_next_level(self):
        """Calculate XP needed for next level."""
        return self.level * 100

    def check_unlocks(self):
        """Check for new unlocks based on level."""
        unlocks = {
            2: "Hat",
            3: "Bow",
            5: "Glasses",
            7: "Crown",
            10: "Tiny backpack",
        }
        for level, item in unlocks.items():
            if self.level >= level and item not in self.inventory:
                self.inventory.append(item)

    def reset(self):
        """Reset progression to starting values."""
        self.level = 1
        self.experience = 0
        self.inventory = []
        self.achievements = []
