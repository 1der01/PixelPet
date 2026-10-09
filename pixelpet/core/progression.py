"""Progression system for PixelPet."""


class Progression:
    """Manages pet level, experience, unlocks, affection, and care goals."""

    DEFAULT_GOALS = {
        "feed": {"title": "Feed your pet", "target": 2},
        "pet": {"title": "Give attention", "target": 3},
        "play": {"title": "Play together", "target": 2},
        "clean": {"title": "Keep them tidy", "target": 2},
    }

    def __init__(
        self,
        level=1,
        experience=0,
        inventory=None,
        achievements=None,
        affection=0,
        care_streak=0,
        goals=None,
    ):
        self.level = level
        self.experience = experience
        self.inventory = inventory or []
        self.achievements = achievements or []
        self.affection = affection
        self.care_streak = care_streak
        self.goals = goals or {
            goal_id: {"title": data["title"], "target": data["target"], "progress": 0}
            for goal_id, data in self.DEFAULT_GOALS.items()
        }

    def to_dict(self):
        """Convert progression to dictionary for saving."""
        return {
            "level": self.level,
            "experience": self.experience,
            "inventory": self.inventory,
            "achievements": self.achievements,
            "affection": self.affection,
            "care_streak": self.care_streak,
            "goals": self.goals,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Progression from dictionary."""
        goals_data = data.get("goals")
        goals = goals_data or {
            goal_id: {"title": info["title"], "target": info["target"], "progress": 0}
            for goal_id, info in cls.DEFAULT_GOALS.items()
        }
        return cls(
            level=data.get("level", 1),
            experience=data.get("experience", 0),
            inventory=data.get("inventory", []),
            achievements=data.get("achievements", []),
            affection=data.get("affection", 0),
            care_streak=data.get("care_streak", 0),
            goals=goals,
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

    def record_care_action(self, action_name, amount=1):
        """Update affection, streak, and daily goals after a care action."""
        self.affection += amount
        self.care_streak += 1

        if action_name in self.goals:
            goal = self.goals[action_name]
            goal["progress"] = min(goal["target"], goal["progress"] + 1)

        if self.affection >= self.level * 25:
            self.achievements.append("Loyal companion") if "Loyal companion" not in self.achievements else None

    def get_goal_status(self):
        """Return current goal progress in a UI-friendly structure."""
        summary = []
        for action_name, goal in self.goals.items():
            summary.append(
                {
                    "id": action_name,
                    "title": goal["title"],
                    "progress": goal["progress"],
                    "target": goal["target"],
                    "complete": goal["progress"] >= goal["target"],
                }
            )
        return summary

    def reset(self):
        """Reset progression to starting values."""
        self.level = 1
        self.experience = 0
        self.inventory = []
        self.achievements = []
        self.affection = 0
        self.care_streak = 0
        self.goals = {
            goal_id: {"title": data["title"], "target": data["target"], "progress": 0}
            for goal_id, data in self.DEFAULT_GOALS.items()
        }
