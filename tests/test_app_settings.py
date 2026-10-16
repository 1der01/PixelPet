import unittest
from unittest.mock import Mock, patch

from pixelpet.main import PixelPetApp


class EventNotificationTests(unittest.TestCase):
    @staticmethod
    def make_app(notifications_enabled):
        app = Mock()
        app.settings = {"notifications": notifications_enabled}
        app.pet_window = Mock()
        app.speech_bubble = Mock()
        app.sound_system = Mock()
        return app

    def test_disabled_notifications_suppress_event_alerts(self):
        app = self.make_app(False)

        PixelPetApp.handle_interaction(app, "event", {"message": "Hello!"})

        app.speech_bubble.show_message.assert_not_called()
        app.pet_window.show_reaction.assert_not_called()
        app.sound_system.play.assert_not_called()

    def test_enabled_notifications_show_event_alerts(self):
        app = self.make_app(True)
        app.pet_window.pos.return_value = "position"
        app.pet_window.size.return_value = "size"

        PixelPetApp.handle_interaction(app, "event", {"message": "Hello!"})

        app.speech_bubble.show_message.assert_called_once_with(
            "Hello!", "position", "size"
        )
        app.pet_window.show_reaction.assert_called_once_with("event")
        app.sound_system.play.assert_called_once_with("event")

    @staticmethod
    def make_settings_app():
        app = Mock()
        app.settings = {
            "start_with_windows": False,
            "sound_effects": True,
            "room_theme": "Cozy",
            "room_furniture": ["Bed"],
        }
        app.pet.progression.sanitize_room_furniture.return_value = ["Bed"]
        return app

    def test_saving_startup_preference_registers_pixelpet(self):
        app = self.make_settings_app()
        new_settings = dict(app.settings, start_with_windows=True)

        with patch("pixelpet.main.StartupManager.set_enabled") as set_enabled:
            PixelPetApp.update_settings(app, new_settings)

        set_enabled.assert_called_once_with(True)
        app.save_manager.save_settings.assert_called_once_with(new_settings)

    def test_startup_registration_failure_preserves_previous_setting(self):
        app = self.make_settings_app()
        new_settings = dict(app.settings, start_with_windows=True)

        with (
            patch(
                "pixelpet.main.StartupManager.set_enabled",
                side_effect=OSError("registry unavailable"),
            ),
            patch("pixelpet.main.QMessageBox.warning") as warning,
        ):
            PixelPetApp.update_settings(app, new_settings)

        self.assertFalse(app.settings["start_with_windows"])
        app.save_manager.save_settings.assert_called_once()
        warning.assert_called_once()


if __name__ == "__main__":
    unittest.main()
