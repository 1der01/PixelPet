"""Settings normalization for PixelPet."""

from .default_data import DEFAULT_SETTINGS


class SettingsManager:
    """Normalize persisted and user-provided application settings."""

    ROOM_THEME_OPTIONS = ("Cozy", "Garden", "Space", "Neon")
    ROOM_FURNITURE_OPTIONS = ("Bed", "Plant", "Toy Box", "Lamp")

    @classmethod
    def normalize(cls, settings):
        """Return a validated settings dictionary with defaults for invalid values."""
        settings = settings if isinstance(settings, dict) else {}
        normalized = DEFAULT_SETTINGS.copy()
        normalized.update(settings)

        for key in (
            "always_on_top",
            "start_with_windows",
            "sound_effects",
            "notifications",
        ):
            if not isinstance(normalized.get(key), bool):
                normalized[key] = DEFAULT_SETTINGS[key]

        if normalized.get("room_theme") not in cls.ROOM_THEME_OPTIONS:
            normalized["room_theme"] = DEFAULT_SETTINGS["room_theme"]

        furniture = normalized.get("room_furniture")
        if not isinstance(furniture, list):
            furniture = DEFAULT_SETTINGS["room_furniture"]
        normalized["room_furniture"] = list(
            dict.fromkeys(
                item for item in furniture if item in cls.ROOM_FURNITURE_OPTIONS
            )
        ) or list(DEFAULT_SETTINGS["room_furniture"])

        try:
            transparency = int(normalized.get("pet_transparency"))
        except (TypeError, ValueError, OverflowError):
            transparency = DEFAULT_SETTINGS["pet_transparency"]
        normalized["pet_transparency"] = max(50, min(255, transparency))

        try:
            intensity = float(normalized.get("animation_intensity"))
        except (TypeError, ValueError, OverflowError):
            intensity = DEFAULT_SETTINGS["animation_intensity"]
        if not 0 <= intensity <= 2:
            intensity = DEFAULT_SETTINGS["animation_intensity"]
        normalized["animation_intensity"] = intensity

        return normalized
