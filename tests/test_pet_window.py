import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from pixelpet.core.pet import Pet
from pixelpet.ui.pet_window import PetWindow


class PetWindowAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = PetWindow(Pet(name="Mochi", species="Cat"), {})
        self.callback = Mock()
        self.window.set_interaction_callback(self.callback)

    def tearDown(self):
        self.window.close()

    def test_pet_window_is_keyboard_focusable_and_has_accessible_instructions(self):
        self.assertEqual(self.window.focusPolicy(), Qt.StrongFocus)
        self.assertEqual(self.window.accessibleName(), "Mochi, Cat, Happy")
        self.assertIn("Space or Enter", self.window.accessibleDescription())

    def test_space_and_enter_open_interaction_menu(self):
        for key in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            with self.subTest(key=key):
                event = QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier)
                QApplication.sendEvent(self.window, event)
                self.assertTrue(event.isAccepted())

        self.assertEqual(self.callback.call_count, 3)
        self.callback.assert_called_with("menu", None)

    def test_game_update_uses_elapsed_time_since_previous_tick(self):
        self.window._last_game_update = 100
        with patch("pixelpet.ui.pet_window.time.time", return_value=163):
            with patch.object(self.window.pet, "update", return_value=None) as update:
                self.window.update_game()

        update.assert_called_once_with(63)

    def test_game_update_ignores_negative_elapsed_time(self):
        self.window._last_game_update = 100
        with patch("pixelpet.ui.pet_window.time.time", return_value=90):
            with patch.object(self.window.pet, "update", return_value=None) as update:
                self.window.update_game()

        update.assert_called_once_with(0.0)
        self.assertEqual(self.window._last_game_update, 90)

    def test_game_update_skips_display_and_tray_refresh_when_state_is_unchanged(self):
        with patch.object(self.window, "update_pet_display") as update_display:
            self.window.update_game()

        update_display.assert_not_called()
        self.callback.assert_not_called()

    def test_game_update_refreshes_display_and_tray_when_mood_changes(self):
        def change_mood(_elapsed):
            self.window.pet.mood = "Hungry"

        with patch.object(self.window.pet, "update", side_effect=change_mood):
            with patch.object(self.window, "update_pet_display") as update_display:
                self.window.update_game()

        update_display.assert_called_once_with()
        self.callback.assert_called_once_with("update_tray", None)

    def test_game_update_refreshes_display_when_sleep_state_changes(self):
        def put_pet_to_sleep(_elapsed):
            self.window.pet.is_sleeping = True

        with patch.object(self.window.pet, "update", side_effect=put_pet_to_sleep):
            with patch.object(self.window, "update_pet_display") as update_display:
                self.window.update_game()

        update_display.assert_called_once_with()
        self.callback.assert_not_called()


if __name__ == "__main__":
    unittest.main()
