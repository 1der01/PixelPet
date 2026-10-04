"""Main entry point for PixelPet."""
import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon, QAction

from .core import Pet
from .data import SaveManager, DEFAULT_SETTINGS
from .ui import PetWindow, InteractionMenu, SpeechBubble, SetupWindow, SettingsWindow


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
        self.tray_icon = QSystemTrayIcon()
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
            if result:
                # Show speech bubble with result
                pos = self.pet_window.pos()
                bubble_pos = pos + self.pet_window.rect().topLeft() - QPoint(0, 90)
                self.speech_bubble.show_message(result, bubble_pos)

            # Save after action
            self.save_manager.save_pet(self.pet)
            # Update tray tooltip
            self.update_tray_tooltip()

        elif event_type == "event":
            # Handle random event
            message = data.get("message", "")
            event = data.get("event", {})

            if message:
                pos = self.pet_window.pos()
                bubble_pos = pos + self.pet_window.rect().topLeft() - QPoint(0, 90)
                self.speech_bubble.show_message(message, bubble_pos)

        elif event_type == "update_tray":
            # Update tray tooltip
            self.update_tray_tooltip()

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
        self.settings_window = SettingsWindow(self.settings)
        self.settings_window.set_settings_saved_callback(self.update_settings)
        self.settings_window.set_pet_reset_callback(self.reset_pet)
        self.settings_window.show()

    def update_settings(self, new_settings):
        """Update application settings."""
        self.settings = new_settings
        self.save_manager.save_settings(self.settings)
        self.pet_window.update_settings(self.settings)

    def reset_pet(self):
        """Reset the pet to starting state."""
        self.pet.reset()
        self.save_manager.save_pet(self.pet)
        self.pet_window.update_pet_display()
        self.speech_bubble.show_message("Pet reset!", self.pet_window.pos())

    def manual_save(self):
        """Manually save pet state."""
        if self.save_manager.save_pet(self.pet):
            self.speech_bubble.show_message("Saved!", self.pet_window.pos())

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
