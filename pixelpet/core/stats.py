"""Stats system for PixelPet."""


class Stats:
    """Manages the pet's four main stats: hunger, energy, happiness, cleanliness."""

    def __init__(self, hunger=70, energy=50, happiness=80, cleanliness=60):
        self.hunger = max(0, min(100, hunger))
        self.energy = max(0, min(100, energy))
        self.happiness = max(0, min(100, happiness))
        self.cleanliness = max(0, min(100, cleanliness))

    def to_dict(self):
        """Convert stats to dictionary for saving."""
        return {
            "hunger": self.hunger,
            "energy": self.energy,
            "happiness": self.happiness,
            "cleanliness": self.cleanliness,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Stats from dictionary."""
        return cls(
            hunger=data.get("hunger", 70),
            energy=data.get("energy", 50),
            happiness=data.get("happiness", 80),
            cleanliness=data.get("cleanliness", 60),
        )

    def modify(self, hunger=0, energy=0, happiness=0, cleanliness=0):
        """Modify stats by given amounts."""
        self.hunger = max(0, min(100, self.hunger + hunger))
        self.energy = max(0, min(100, self.energy + energy))
        self.happiness = max(0, min(100, self.happiness + happiness))
        self.cleanliness = max(0, min(100, self.cleanliness + cleanliness))

    def decay(self):
        """Gradually decrease stats over time."""
        self.modify(hunger=-2, energy=-1, happiness=-1, cleanliness=-1)

    def get_average(self):
        """Get the average of all stats."""
        return (self.hunger + self.energy + self.happiness + self.cleanliness) / 4

    def is_critical(self):
        """Check if any stat is critically low (below 20)."""
        return any(
            stat < 20
            for stat in [self.hunger, self.energy, self.happiness, self.cleanliness]
        )
