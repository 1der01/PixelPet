import unittest

from pixelpet.data import DEFAULT_SETTINGS, SettingsManager


class SettingsManagerTests(unittest.TestCase):
    def test_normalize_fills_defaults_and_preserves_valid_values(self):
        settings = SettingsManager.normalize(
            {
                "always_on_top": False,
                "start_with_windows": True,
                "room_theme": "Garden",
                "room_furniture": ["Plant", "Bed", "Plant"],
                "pet_transparency": 120,
                "animation_intensity": 1.5,
            }
        )

        self.assertFalse(settings["always_on_top"])
        self.assertTrue(settings["start_with_windows"])
        self.assertEqual(settings["room_theme"], "Garden")
        self.assertEqual(settings["room_furniture"], ["Plant", "Bed"])
        self.assertEqual(settings["pet_transparency"], 120)
        self.assertEqual(settings["animation_intensity"], 1.5)
        self.assertEqual(settings["sound_effects"], DEFAULT_SETTINGS["sound_effects"])

    def test_normalize_replaces_invalid_values_and_clamps_transparency(self):
        settings = SettingsManager.normalize(
            {
                "always_on_top": "false",
                "room_theme": "Unknown",
                "room_furniture": ["Unknown"],
                "pet_transparency": 999,
                "animation_intensity": "invalid",
            }
        )

        self.assertEqual(settings["always_on_top"], DEFAULT_SETTINGS["always_on_top"])
        self.assertEqual(settings["room_theme"], DEFAULT_SETTINGS["room_theme"])
        self.assertEqual(settings["room_furniture"], DEFAULT_SETTINGS["room_furniture"])
        self.assertEqual(settings["pet_transparency"], 255)
        self.assertEqual(
            settings["animation_intensity"], DEFAULT_SETTINGS["animation_intensity"]
        )


if __name__ == "__main__":
    unittest.main()
