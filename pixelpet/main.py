"""Main entry point for PixelPet."""
import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import QObject, QPointF, Qt
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPen, QPixmap, QPolygonF

from .core import Pet, SoundSystem
from .data import SaveManager, DEFAULT_SETTINGS
from .ui import (
    PetWindow,
    InteractionMenu,
    SpeechBubble,
    SetupWindow,
    SettingsWindow,
    PetStatusWindow,
    TreatCatchWindow,
)


class PixelPetApp(QObject):
    """Main application class for PixelPet."""

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Initialize save manager
        self.save_manager = SaveManager()

        # Load settings
        self.settings = self.save_manager.load_settings()
        if self.settings is None:
            self.settings = DEFAULT_SETTINGS.copy()

        # Initialize sound system
        self.sound_system = SoundSystem()
        self.sound_system.set_enabled(self.settings.get("sound_effects", True))

        # Load or create pet
        if self.save_manager.has_save():
            pet_data = self.save_manager.load_pet()
            if pet_data:
                self.pet = Pet.from_dict(pet_data)
                # Setup UI
                self.setup_ui()
                # Setup system tray
                self.setup_tray()
                # Start auto-save timer
                self.setup_auto_save()
            else:
                self.show_setup()
        else:
            self.show_setup()

    def setup_ui(self):
        """Setup the main UI components."""
        # Pet window
        self.pet_window = PetWindow(self.pet, self.settings)
        self.pet_window.set_interaction_callback(self.handle_interaction)
        self.pet_window.show()

        # Position window in center of screen
        screen = self.app.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            x = geometry.center().x() - self.pet_window.width() // 2
            y = geometry.center().y() - self.pet_window.height() // 2
            self.pet_window.move(x, y)

        # Interaction menu
        self.interaction_menu = InteractionMenu(self.pet)
        self.interaction_menu.set_action_callback(self.handle_interaction)

        # Speech bubble
        self.speech_bubble = SpeechBubble()

    def setup_tray(self):
        """Setup system tray icon."""
        self.tray_icon = QSystemTrayIcon(self.create_tray_icon(), self)
        self.tray_icon.setToolTip(f"PixelPet - {self.pet.name}")

        # Create tray menu
        tray_menu = QMenu()

        show_action = QAction("Show PixelPet", self)
        show_action.triggered.connect(self.show_pet)
        tray_menu.addAction(show_action)

        hide_action = QAction("Hide PixelPet", self)
        hide_action.triggered.connect(self.hide_pet)
        tray_menu.addAction(hide_action)

        tray_menu.addSeparator()

        status_action = QAction(f"Status: {self.pet.mood}", self)
        status_action.setEnabled(False)
        tray_menu.addAction(status_action)

        tray_menu.addSeparator()

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.manual_save)
        tray_menu.addAction(save_action)

        tray_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def create_tray_icon(self):
        """Draw a self-contained pet-face icon so the tray is never iconless."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("#493B55"), 3))
        painter.setBrush(QColor("#F2A76F"))
        painter.drawEllipse(9, 13, 46, 44)
        painter.setBrush(QColor("#F2A76F"))
        painter.drawPolygon(
            QPolygonF([QPointF(14, 26), QPointF(19, 4), QPointF(31, 20)])
        )
        painter.drawPolygon(
            QPolygonF([QPointF(50, 26), QPointF(45, 4), QPointF(33, 20)])
        )
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#493B55"))
        painter.drawEllipse(21, 30, 5, 8)
        painter.drawEllipse(38, 30, 5, 8)
        painter.setBrush(QColor("#F28391"))
        painter.drawEllipse(14, 40, 10, 5)
        painter.drawEllipse(40, 40, 10, 5)
        painter.end()
        return QIcon(pixmap)

    def setup_auto_save(self):
        """Setup auto-save timer."""
        from PySide6.QtCore import QTimer

        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.auto_save)
        self.save_timer.start(60000)  # Save every minute

    def show_setup(self):
        """Show setup window for new pet."""
        self.setup_window = SetupWindow()
        self.setup_window.set_setup_complete_callback(self.create_pet)
        self.setup_window.show()
        # Don't return - let the app run with just the setup window

    def create_pet(self, pet_info):
        """Create a new pet from setup info."""
        self.pet = Pet(
            name=pet_info["name"],
            species=pet_info["species"],
        )

        # Save the new pet
        self.save_manager.save_pet(self.pet)

        # Setup UI
        self.setup_ui()
        # Setup system tray
        self.setup_tray()
        # Start auto-save timer
        self.setup_auto_save()

        # Play notification sound
        self.sound_system.play("notification")

    def handle_interaction(self, event_type, data):
        """Handle interaction events from pet window."""
        if event_type == "menu":
            # Show interaction menu near pet window
            pos = self.pet_window.pos()
            menu_pos = pos + self.pet_window.rect().bottomLeft()
            self.interaction_menu.show_at_position(menu_pos)

        elif event_type == "action":
            # Handle action result
            result = data.get("result", "")
            sound_name = data.get("sound", None)
            leveled_up = data.get("leveled_up", False)
            reaction = "level_up" if leveled_up else sound_name

            if result:
                # Show speech bubble with result (pass pet position and size)
                pos = self.pet_window.pos()
                self.speech_bubble.show_message(result, pos, self.pet_window.size())

            if reaction:
                self.pet_window.show_reaction(reaction)
            self.pet_window.update_pet_display()

            # Play sound effect
            if sound_name:
                self.sound_system.play(sound_name)

            # Play level up sound if pet leveled up
            if leveled_up:
                self.sound_system.play("level_up")

            # Save after action
            self.save_manager.save_pet(self.pet)
            # Update tray tooltip
            self.update_tray_tooltip()

        elif event_type == "event":
            # Handle random event
            message = data.get("message", "")
            if message:
                # Show speech bubble with event message (pass pet position and size)
                pos = self.pet_window.pos()
                self.speech_bubble.show_message(message, pos, self.pet_window.size())
                self.pet_window.show_reaction("event")

                # Play event sound
                self.sound_system.play("event")

        elif event_type == "status":
            self.status_window = PetStatusWindow(
                self.pet, accessory_callback=self.handle_accessory_equipped
            )
            self.status_window.show()

        elif event_type == "treat_game":
            self.treat_game = TreatCatchWindow(
                self.pet, completed_callback=self.handle_treat_game_reward
            )
            self.treat_game.show()

        elif event_type == "update_tray":
            # Update tray tooltip
            self.update_tray_tooltip()

    def handle_treat_game_reward(self, reward):
        """Persist mini-game rewards and celebrate level or cosmetic unlocks."""
        self.pet_window.show_reaction(
            "level_up" if reward["leveled_up"] else "game"
        )
        self.save_manager.save_pet(self.pet)
        self.update_tray_tooltip()
        if reward["leveled_up"]:
            self.sound_system.play("level_up")
        else:
            self.sound_system.play("notification")

    def handle_accessory_equipped(self, accessory):
        """Refresh the pet after an accessory is equipped or removed."""
        self.pet_window.update_pet_display()
        self.pet_window.show_reaction("pet")
        message = (
            f"{self.pet.name} is wearing the {accessory}!"
            if accessory
            else f"{self.pet.name} is not wearing an accessory."
        )
        self.speech_bubble.show_message(
            message, self.pet_window.pos(), self.pet_window.size()
        )
        self.save_manager.save_pet(self.pet)

    def update_tray_tooltip(self):
        """Update the system tray tooltip with current pet status."""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.setToolTip(f"PixelPet - {self.pet.name} ({self.pet.mood})")

    def show_pet(self):
        """Show the pet window."""
        self.pet_window.show()

    def hide_pet(self):
        """Hide the pet window."""
        self.pet_window.hide()

    def show_settings(self):
        """Show settings window."""
        self.settings_window = SettingsWindow(
            self.settings,
            save_manager=self.save_manager,
            pet=getattr(self, "pet", None),
        )
        self.settings_window.set_settings_saved_callback(self.update_settings)
        self.settings_window.set_pet_reset_callback(self.reset_pet)
        self.settings_window.set_pet_save_changed_callback(self.reload_pet_save)
        self.settings_window.show()

    def reload_pet_save(self):
        """Reload an imported or restored pet save into the running application."""
        pet_data = self.save_manager.load_pet()
        if pet_data is None:
            return False

        try:
            pet = Pet.from_dict(pet_data)
        except (AttributeError, KeyError, TypeError, ValueError):
            return False

        self.pet = pet
        self.settings["room_theme"] = pet.room_theme
        self.settings["room_furniture"] = pet.progression.sanitize_room_furniture(
            pet.room_furniture
        )
        pet.room_furniture = self.settings["room_furniture"]
        self.save_manager.save_settings(self.settings)

        self.pet_window.pet = pet
        self.pet_window.pet_canvas.pet = pet
        self.pet_window.update_settings(self.settings)
        self.pet_window.show()
        self.pet_window.update_pet_display()

        self.interaction_menu.close()
        self.interaction_menu = InteractionMenu(pet)
        self.interaction_menu.set_action_callback(self.handle_interaction)
        self.update_tray_tooltip()
        return True

    def update_settings(self, new_settings):
        """Update application settings."""
        self.settings = new_settings
        self.save_manager.save_settings(self.settings)

        if hasattr(self, "pet"):
            self.pet.room_theme = self.settings.get("room_theme", "Cozy")
            self.pet.room_furniture = self.pet.progression.sanitize_room_furniture(
                self.settings.get("room_furniture", self.pet.progression.get_available_room_furniture())
            )
            self.save_manager.save_pet(self.pet)

        self.pet_window.update_settings(self.settings)

        # Update sound system
        self.sound_system.set_enabled(self.settings.get("sound_effects", True))

    def reset_pet(self):
        """Reset the pet to starting state."""
        self.pet.reset()
        self.save_manager.save_pet(self.pet)
        self.pet_window.update_pet_display()
        self.speech_bubble.show_message("Pet reset!", self.pet_window.pos(), self.pet_window.size())
        self.sound_system.play("notification")

    def manual_save(self):
        """Manually save pet state."""
        if self.save_manager.save_pet(self.pet):
            self.speech_bubble.show_message("Saved!", self.pet_window.pos(), self.pet_window.size())

    def auto_save(self):
        """Auto-save pet state."""
        self.save_manager.save_pet(self.pet)

    def quit(self):
        """Quit the application."""
        # Save before quitting (only if pet exists)
        if hasattr(self, 'pet'):
            self.save_manager.save_pet(self.pet)
        self.save_manager.save_settings(self.settings)
        self.app.quit()

    def run(self):
        """Run the application."""
        return self.app.exec()


def main():
    """Main entry point."""
    app = PixelPetApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
