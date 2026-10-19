"""Main Pet class for PixelPet."""
import random
import re
import time
from .stats import Stats
from .mood import MoodSystem
from .progression import Progression
from .events import EventSystem
from .activity_monitor import ActivityMonitor


class Pet:
    """Main pet class managing all pet systems."""

    STAT_DECAY_INTERVAL = 30 * 60
    SPECIES = ["Cat", "Dog", "Blob", "Frog", "Robot"]
    PERSONALITIES = ["Lazy", "Energetic", "Shy", "Playful", "Chaotic", "Curious", "Grumpy"]
    FAVORITE_FOODS = {
        "Cat": "Fish",
        "Dog": "Bones",
        "Blob": "Anything",
        "Frog": "Flies",
        "Robot": "Electricity",
    }
    MAX_NAME_LENGTH = 24

    @classmethod
    def normalize_name(cls, name):
        """Normalize user-facing pet names to a safe, readable format."""
        if not isinstance(name, str):
            return "Mochi"

        cleaned = " ".join(name.strip().split())
        if not cleaned:
            return "Mochi"

        cleaned = re.sub(r"[^A-Za-z0-9' -]", "", cleaned)
        cleaned = " ".join(cleaned.split())
        if not cleaned:
            return "Mochi"

        cleaned = cleaned[: cls.MAX_NAME_LENGTH].rstrip()
        if not cleaned:
            return "Mochi"
        return cleaned

    @classmethod
    def normalize_species(cls, species):
        """Accept common species inputs and normalize them to a known species."""
        if not isinstance(species, str):
            return random.choice(cls.SPECIES)

        normalized = species.strip()
        for valid_species in cls.SPECIES:
            if normalized.lower() == valid_species.lower():
                return valid_species

        return random.choice(cls.SPECIES)

    def __init__(
        self,
        name="Mochi",
        species="Cat",
        personality=None,
        stats=None,
        progression=None,
        age=0,
        room_theme="Cozy",
        room_furniture=None,
    ):
        self.name = self.normalize_name(name)
        self.species = self.normalize_species(species)
        self.personality = personality or random.choice(self.PERSONALITIES)
        self.favorite_food = self.FAVORITE_FOODS.get(self.species, "Anything")
        self.stats = stats or Stats()
        self.progression = progression or Progression()
        self.age = age
        self.room_theme = room_theme
        self.room_furniture = room_furniture or self.progression.get_available_room_furniture()
        self.mood = MoodSystem.calculate_mood(self.stats)
        self.is_sleeping = False
        self.event_system = EventSystem()
        self.activity_monitor = ActivityMonitor()
        self.decay_timer = 0
        self.last_update = time.time()
        self.created_time = time.time()

    def to_dict(self):
        """Convert pet to dictionary for saving."""
        return {
            "name": self.name,
            "species": self.species,
            "personality": self.personality,
            "favorite_food": self.favorite_food,
            "stats": self.stats.to_dict(),
            "progression": self.progression.to_dict(),
            "age": self.age,
            "mood": self.mood,
            "is_sleeping": self.is_sleeping,
            "created_time": self.created_time,
            "room_theme": self.room_theme,
            "room_furniture": self.room_furniture,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Pet from dictionary."""
        progression = Progression.from_dict(data.get("progression", {}))
        pet = cls(
            name=data.get("name", "Mochi"),
            species=data.get("species", "Cat"),
            personality=data.get("personality"),
            stats=Stats.from_dict(data.get("stats", {})),
            progression=progression,
            age=data.get("age", 0),
            room_theme=data.get("room_theme", "Cozy"),
            room_furniture=data.get("room_furniture", progression.get_available_room_furniture()),
        )
        pet.mood = data.get("mood", MoodSystem.calculate_mood(pet.stats))
        pet.is_sleeping = data.get("is_sleeping", False)
        pet.created_time = data.get("created_time", pet.created_time)
        return pet

    def update(self, dt):
        """Update pet state."""
        self.last_update = time.time()
        self.age += dt

        # Check for user becoming active
        user_woke_up = self.activity_monitor.update()

        # Wake up if user becomes active
        if user_woke_up and self.is_sleeping:
            self.wake_up()

        # Apply one gentle decay pulse for each 30 minutes spent awake.
        if not self.is_sleeping:
            self.decay_timer += dt
            decay_periods = int(self.decay_timer // self.STAT_DECAY_INTERVAL)
            if decay_periods:
                self.stats.decay(decay_periods)
                self.decay_timer %= self.STAT_DECAY_INTERVAL

        # Update mood
        self.mood = MoodSystem.calculate_mood(self.stats)

        # Update events
        event = self.event_system.update(dt)
        if event:
            dialogue = self.event_system.get_dialogue_for_event(
                event, self.personality
            )
            return {"event": event, "dialogue": dialogue}

        return None

    def feed(self):
        """Feed the pet."""
        if self.is_sleeping:
            self.wake_up()
        self.stats.modify(hunger=15, happiness=5)
        leveled_up = self.progression.add_experience(5)
        self.progression.record_care_action("feed")
        self.mood = MoodSystem.calculate_mood(self.stats)
        self.activity_monitor.record_activity()
        result = f"You fed {self.name}! Yum!"
        if leveled_up:
            result += f" Level up! Now level {self.progression.level}!"
        return result, "feed", leveled_up

    def pet(self):
        """Pet the pet."""
        if self.is_sleeping:
            self.wake_up()
        self.stats.modify(happiness=10)
        leveled_up = self.progression.add_experience(2)
        self.progression.record_care_action("pet")
        self.mood = MoodSystem.calculate_mood(self.stats)
        self.activity_monitor.record_activity()
        result = f"You petted {self.name}! So cute!"
        if leveled_up:
            result += f" Level up! Now level {self.progression.level}!"
        return result, "pet", leveled_up

    def play(self):
        """Play with the pet."""
        if self.is_sleeping:
            self.wake_up()
        self.stats.modify(happiness=15, energy=-10)
        leveled_up = self.progression.add_experience(10)
        self.progression.record_care_action("play")
        self.mood = MoodSystem.calculate_mood(self.stats)
        self.activity_monitor.record_activity()
        result = f"You played with {self.name}! Fun!"
        if leveled_up:
            result += f" Level up! Now level {self.progression.level}!"
        return result, "play", leveled_up

    def clean(self):
        """Clean the pet."""
        if self.is_sleeping:
            self.wake_up()
        self.stats.modify(cleanliness=20, happiness=5)
        leveled_up = self.progression.add_experience(5)
        self.progression.record_care_action("clean")
        self.mood = MoodSystem.calculate_mood(self.stats)
        self.activity_monitor.record_activity()
        result = f"You cleaned {self.name}! Sparkling!"
        if leveled_up:
            result += f" Level up! Now level {self.progression.level}!"
        return result, "clean", leveled_up

    def sleep(self):
        """Put the pet to sleep."""
        self.is_sleeping = True
        self.activity_monitor.record_activity()
        return f"{self.name} is now sleeping...", "sleep", False

    def wake_up(self):
        """Wake the pet up."""
        if self.is_sleeping:
            self.stats.modify(energy=30)
            self.mood = MoodSystem.calculate_mood(self.stats)
            self.is_sleeping = False
            return f"{self.name} woke up!", "notification", False
        return f"{self.name} is already awake!", None, False

    def reset(self):
        """Reset pet to starting state."""
        self.stats = Stats()
        self.progression.reset()
        self.age = 0
        self.room_furniture = self.progression.sanitize_room_furniture(["Bed", "Plant"])
        self.mood = MoodSystem.calculate_mood(self.stats)
        self.is_sleeping = False
        self.event_system = EventSystem()
        self.created_time = time.time()

    def get_ascii_art(self):
        """Get ASCII art for the pet based on species and mood."""
        expression = MoodSystem.get_expression(self.mood)

        art = {
            "Cat": f"    /\\_/\\  \n   {expression}\n    > ^ <\n   {self.name}",
            "Dog": f"   / \\__/\n  (    )\n{expression}\n   {self.name}",
            "Blob": f"   .---.\n  /     \\\n {expression}\n  \\_____/\n {self.name}",
            "Frog": f"  ( o o )\n {expression}\n  /   \\ \n {self.name}",
            "Robot": f"  [_____]\n {expression}\n  |  |  |\n {self.name}",
        }
        return art.get(self.species, art["Cat"])

    def get_status_text(self):
        """Get formatted status text for stats."""
        return (
            f"Hunger: {'#' * (self.stats.hunger // 10)}{'-' * (10 - self.stats.hunger // 10)} {self.stats.hunger}\n"
            f"Energy: {'#' * (self.stats.energy // 10)}{'-' * (10 - self.stats.energy // 10)} {self.stats.energy}\n"
            f"Happiness: {'#' * (self.stats.happiness // 10)}{'-' * (10 - self.stats.happiness // 10)} {self.stats.happiness}\n"
            f"Cleanliness: {'#' * (self.stats.cleanliness // 10)}{'-' * (10 - self.stats.cleanliness // 10)} {self.stats.cleanliness}"
        )

    def get_priority_needs(self):
        """Return the pet's top needs in a clear order so UI can guide actions."""
        need_map = {
            "feed": ("Hungry", self.stats.hunger),
            "clean": ("Needs a bath", self.stats.cleanliness),
            "sleep": ("Sleepy", self.stats.energy),
            "pet": ("Needs attention", self.stats.happiness),
        }
        order = {"feed": 0, "clean": 1, "sleep": 2, "pet": 3}
        return [
            {"id": action, "label": label, "value": value}
            for action, (label, value) in sorted(
                need_map.items(), key=lambda item: (item[1][1], order[item[0]])
            )
        ]

    def get_need_summary(self):
        """Return a short text summary of what the pet needs right now."""
        needs = self.get_priority_needs()
        top_need = needs[0]
        return f"{self.name} needs {top_need['label'].lower()} right now."
