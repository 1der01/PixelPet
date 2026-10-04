"""Default data and constants for PixelPet."""


DEFAULT_SETTINGS = {
    "always_on_top": True,
    "start_with_windows": False,
    "sound_effects": True,
    "notifications": True,
    "pet_transparency": 255,
    "animation_intensity": 1.0,
}

DEFAULT_PET = {
    "name": "Mochi",
    "species": "Cat",
    "personality": None,  # Will be randomly assigned
    "stats": {
        "hunger": 70,
        "energy": 50,
        "happiness": 80,
        "cleanliness": 60,
    },
    "progression": {
        "level": 1,
        "experience": 0,
        "inventory": [],
        "achievements": [],
    },
    "age": 0,
}
