"""Main pet window for PixelPet."""
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QMenu,
    QSystemTrayIcon,
    QPushButton,
)
from PySide6.QtCore import Qt, QTimer, QPoint, QRect
from PySide6.QtGui import QFont, QAction, QCursor, QPainter, QColor


class PetWindow(QWidget):
    """Main floating window for the pet."""

    def __init__(self, pet, settings):
        super().__init__()
        self.pet = pet
        self.settings = settings
        self.interaction_callback = None
        self.setup_ui()
        self.setup_timers()

    def setup_ui(self):
        """Setup the pet window UI."""
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set initial size
        self.setFixedSize(200, 200)

        # Create main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Pet display label
        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setFont(QFont("Courier New", 10, QFont.Bold))
        self.pet_label.setStyleSheet(
            """
            QLabel {
                color: white;
                background-color: transparent;
            }
        """
        )
        layout.addWidget(self.pet_label)

        self.setLayout(layout)

        # Update pet display
        self.update_pet_display()

    def setup_timers(self):
        """Setup update timers."""
        # Game update timer (1 second)
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(1000)

        # Animation timer (100ms for smooth animations)
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(100)

    def update_game(self):
        """Update game state."""
        # Update pet with 1 second delta time
        event_result = self.pet.update(1.0)

        # Update display
        self.update_pet_display()

        # Notify main app to update tray tooltip
        if self.interaction_callback:
            self.interaction_callback("update_tray", None)

        # Handle events
        if event_result:
            self.show_event(event_result)

    def update_animation(self):
        """Update animations."""
        # Placeholder for animation updates
        pass

    def update_pet_display(self):
        """Update the pet's visual display."""
        ascii_art = self.pet.get_ascii_art()
        self.pet_label.setText(ascii_art)

        # Update window title
        self.setWindowTitle(f"{self.pet.name} - {self.pet.mood}")

    def show_event(self, event_result):
        """Show an event with speech bubble."""
        event = event_result["event"]
        dialogue = event_result["dialogue"]

        # Create speech bubble
        if self.interaction_callback:
            self.interaction_callback("event", {"message": dialogue, "event": event})

    def mousePressEvent(self, event):
        """Handle mouse press for dragging and interactions."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        """Handle double click to show interaction menu."""
        if self.interaction_callback:
            self.interaction_callback("menu", None)

    def set_interaction_callback(self, callback):
        """Set callback for interaction events."""
        self.interaction_callback = callback

    def update_settings(self, settings):
        """Update window based on settings."""
        self.settings = settings

        if settings.get("always_on_top", True):
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowStaysOnTopHint
            )
        else:
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowStaysOnTopHint
            )

        # Update transparency
        opacity = settings.get("pet_transparency", 255) / 255.0
        self.setWindowOpacity(opacity)

        self.show()
