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


if __name__ == "__main__":
    unittest.main()
