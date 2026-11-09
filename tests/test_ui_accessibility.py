import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QFrame, QPushButton

from pixelpet.core.pet import Pet
from pixelpet.ui.fun_windows import PetStatusWindow, TreatCatchWindow
from pixelpet.ui.interaction_menu import InteractionMenu


class PetUiAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def tearDown(self):
        for window in getattr(self, "windows", []):
            window.close()

    def create_window(self, window_type):
        if not hasattr(self, "windows"):
            self.windows = []
        window = window_type(Pet(name="Mochi", species="Cat"))
        self.windows.append(window)
        return window

    def test_interaction_menu_buttons_have_descriptive_accessible_names(self):
        menu = self.create_window(InteractionMenu)

        self.assertEqual(
            [button.accessibleName() for button in menu.action_buttons],
            [
                "Feed Mochi",
                "Pet Mochi",
                "Play with Mochi",
                "Clean Mochi",
                "Put Mochi to sleep",
            ],
        )
        self.assertEqual(menu.size().width(), 228)
        self.assertIsNotNone(menu.findChild(QFrame, "careMenuCard"))
        self.assertIsNotNone(menu.findChild(QFrame, "menuSeparator"))
        self.assertEqual(
            [button.objectName() for button in menu.findChildren(QPushButton)],
            ["careActionButton"] * 5 + ["utilityButton"] * 2,
        )
        self.assertIn(
            "QPushButton#careActionButton:focus",
            menu.action_buttons[0].styleSheet(),
        )

    def test_status_progress_bars_and_accessory_selector_are_named(self):
        window = self.create_window(PetStatusWindow)

        self.assertIn("QFrame#statusCard", window.styleSheet())
        self.assertEqual(
            [
                card.objectName()
                for card in window.findChildren(QFrame)
                if card.objectName() == "statusCard"
            ],
            ["statusCard", "statusCard"],
        )
        self.assertEqual(window.xp_bar.objectName(), "experienceBar")
        self.assertEqual(
            {
                stat_id: bar.accessibleName()
                for stat_id, bar in window.stat_bars.items()
            },
            {
                "hunger": "Hunger",
                "energy": "Energy",
                "happiness": "Happiness",
                "cleanliness": "Cleanliness",
            },
        )
        self.assertEqual(window.xp_bar.accessibleName(), "Experience")
        self.assertEqual(
            window.accessory_selector.accessibleName(), "Equipped accessory"
        )
        self.assertIsNotNone(window.accessory_label.buddy())

    def test_treat_game_exposes_keyboard_instructions_and_control_names(self):
        window = self.create_window(TreatCatchWindow)

        self.assertEqual(window.size().width(), 480)
        self.assertEqual(window.treat_button.objectName(), "treatButton")
        self.assertEqual(window.playfield.objectName(), "treatPlayfield")
        self.assertIn("QFrame#treatPlayfield", window.styleSheet())
        self.assertIn("QPushButton#treatButton:focus", window.styleSheet())
        self.assertEqual(window.treat_button.accessibleName(), "Catch treat")
        self.assertIn("Space or Enter", window.treat_button.accessibleDescription())
        self.assertEqual(window.score_label.accessibleName(), "Treats caught")
        self.assertEqual(window.timer_label.accessibleName(), "Time remaining")


if __name__ == "__main__":
    unittest.main()
