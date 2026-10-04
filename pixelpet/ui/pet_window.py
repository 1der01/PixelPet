"""Main pet window for PixelPet."""
import math
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

        # Animation state
        self.anim_time = 0
        self.blink_timer = 0
        self.is_blinking = False
        self.original_pos = None
        self.is_dragging = False

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
        # Get animation intensity from settings (0.0 to 2.0)
        intensity = self.settings.get("animation_intensity", 1.0)
        if intensity <= 0:
            return

        self.anim_time += 0.1 * intensity

        # Breathing animation (subtle scale)
        breath_scale = 1.0 + (0.02 * intensity * math.sin(self.anim_time * 0.5))
        self.pet_label.setStyleSheet(
            f"""
            QLabel {{
                color: white;
                background-color: transparent;
                transform: scale({breath_scale});
            }}
        """
        )

        # Bouncing animation (subtle vertical movement)
        bounce_offset = int(3 * intensity * math.sin(self.anim_time * 0.8))
        if self.original_pos is None:
            self.original_pos = self.pos()
        new_pos = self.original_pos + QPoint(0, bounce_offset)
        self.move(new_pos)

        # Blinking animation
        self.blink_timer += 1
        if self.blink_timer > 50:  # Blink every ~5 seconds
            self.blink_timer = 0
            self.is_blinking = True
            # Short blink duration
            QTimer.singleShot(150, self.end_blink)

        # Apply blinking to expression
        if self.is_blinking:
            self.apply_blink()

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
            self.is_dragging = True
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if event.buttons() == Qt.LeftButton and self.is_dragging:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            self.original_pos = new_pos  # Update original position during drag
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.original_pos = self.pos()  # Set final position as original
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

        # Update original position for animation
        if self.original_pos is None:
            self.original_pos = self.pos()

        self.show()

    def apply_blink(self):
        """Apply blinking effect to pet expression."""
        current_art = self.pet.get_ascii_art()
        # Replace eyes with closed eyes (- -)
        blink_art = current_art.replace("( o . o )", "( - . - )")
        blink_art = blink_art.replace("( O . O )", "( - . - )")
        blink_art = blink_art.replace("( ^ _ ^ )", "( - _ - )")
        blink_art = blink_art.replace("( > w < )", "( - w - )")
        blink_art = blink_art.replace("( # . # )", "( - . - )")
        blink_art = blink_art.replace("( @ . @ )", "( - . - )")
        blink_art = blink_art.replace("( T . T )", "( - . - )")
        self.pet_label.setText(blink_art)

    def end_blink(self):
        """End blinking effect."""
        self.is_blinking = False
        self.update_pet_display()
