import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QComboBox, QScrollArea, QMessageBox

from pixelpet.core.pet import Pet
from pixelpet.ui.settings_window import SettingsWindow


class SettingsWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.initial_settings = {
            "always_on_top": True,
            "start_with_windows": False,
            "sound_effects": True,
            "notifications": True,
            "room_theme": "Cozy",
            "room_furniture": ["Bed", "Plant"],
            "pet_transparency": 255,
            "animation_intensity": 1.0,
        }
        self.window = SettingsWindow(
            self.initial_settings,
            pet=Pet(name="Mochi", species="Cat"),
        )
        self.saved_settings = None
        self.window.set_settings_saved_callback(self._save_settings)

    def tearDown(self):
        self.window.close()

    def _save_settings(self, settings):
        self.saved_settings = settings

    def test_save_settings_persists_controls_and_calls_callback(self):
        self.window.always_on_top_cb.setChecked(False)
        self.window.start_with_windows_cb.setChecked(True)
        self.window.sound_effects_cb.setChecked(False)
        self.window.notifications_cb.setChecked(False)
        self.window.room_theme_combo.setCurrentText("Garden")
        self.window.room_furniture_checks["Bed"].setChecked(False)
        self.window.room_furniture_checks["Plant"].setChecked(True)
        self.window.transparency_slider.setValue(137)
        self.window.anim_slider.setValue(175)

        self.window.save_settings()

        self.assertEqual(
            self.saved_settings,
            {
                "always_on_top": False,
                "start_with_windows": True,
                "sound_effects": False,
                "notifications": False,
                "room_theme": "Garden",
                "room_furniture": ["Plant"],
                "pet_transparency": 137,
                "animation_intensity": 1.75,
            },
        )
        self.assertIs(self.saved_settings, self.window.settings)
        self.assertEqual(self.initial_settings["room_theme"], "Cozy")
        self.assertEqual(self.initial_settings["room_furniture"], ["Bed", "Plant"])

    def test_save_settings_discards_locked_furniture_and_keeps_a_default(self):
        self.window.room_furniture_checks["Bed"].setChecked(False)
        self.window.room_furniture_checks["Plant"].setChecked(False)
        self.window.room_furniture_checks["Toy Box"].setChecked(True)

        self.window.save_settings()

        self.assertEqual(self.saved_settings["room_furniture"], ["Bed"])

    def test_settings_content_is_scrollable(self):
        self.assertIsNotNone(self.window.findChild(QScrollArea))

    def test_settings_window_has_grouped_light_theme_and_accessible_controls(self):
        self.assertIn("QFrame#settingsCard", self.window.styleSheet())
        self.assertIn("QLabel#settingsSection", self.window.styleSheet())
        self.assertEqual(self.window.room_theme_combo.accessibleName(), "Room theme")
        self.assertEqual(
            self.window.transparency_slider.accessibleName(), "Pet transparency"
        )
        self.assertIsNotNone(self.window.findChild(QComboBox, "roomThemeCombo"))

    def test_successful_import_notifies_pet_reload_callback(self):
        callback = unittest.mock.Mock(return_value=True)
        self.window.set_pet_save_changed_callback(callback)
        self.window.save_manager = unittest.mock.Mock()
        self.window.save_manager.import_save.return_value = True

        with (
            patch("pixelpet.ui.settings_window.QFileDialog.getOpenFileName", return_value=("save.json", "")),
            patch.object(QMessageBox, "information"),
        ):
            self.window.import_save()

        callback.assert_called_once_with()

    def test_successful_restore_notifies_pet_reload_callback(self):
        callback = unittest.mock.Mock(return_value=True)
        self.window.set_pet_save_changed_callback(callback)
        self.window.save_manager = unittest.mock.Mock()
        self.window.save_manager.get_latest_backup.return_value = "backup.bak"
        self.window.save_manager.restore_pet_backup.return_value = True

        with (
            patch.object(QMessageBox, "question", return_value=QMessageBox.Yes),
            patch.object(QMessageBox, "information"),
        ):
            self.window.restore_latest_backup()

        callback.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
