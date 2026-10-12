"""Main pet window for PixelPet."""
import math
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPolygonF


class PetCanvas(QWidget):
    """Draw the pet as a colorful, animated desktop character."""

    BODY_COLORS = {
        "Cat": "#F2A76F",
        "Dog": "#C58A55",
        "Blob": "#A88AF2",
        "Frog": "#63C982",
        "Robot": "#94A9C2",
    }

    def __init__(self, pet, parent=None):
        super().__init__(parent)
        self.pet = pet
        self.anim_time = 0.0
        self.blink = False
        self.reaction = None
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        center_x = width / 2
        bob = math.sin(self.anim_time * 2.4) * 3
        if self.reaction in ("play", "game", "level_up"):
            bob += abs(math.sin(self.anim_time * 8)) * 8
        center_y = height * 0.54 + bob
        body_color = QColor(self.BODY_COLORS.get(self.pet.species, "#F2A76F"))
        outline = QColor("#493B55")
        breathe = 1.0 + math.sin(self.anim_time * 1.5) * 0.025
        painter.translate(QPointF(center_x, center_y))
        painter.scale(breathe, breathe)
        painter.translate(QPointF(-center_x, -center_y))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(35, 31, 52, 38))
        painter.drawEllipse(QPointF(center_x, height - 17), 43, 8)

        painter.setPen(QPen(outline, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(body_color))
        if self.pet.species == "Robot":
            painter.drawRoundedRect(
                int(center_x - 44), int(center_y - 42), 88, 82, 18, 18
            )
            painter.setBrush(QColor("#D5E0EC"))
            painter.drawRoundedRect(
                int(center_x - 33), int(center_y - 30), 66, 48, 12, 12
            )
        else:
            if self.pet.species in ("Cat", "Frog"):
                ear_y = center_y - 33
                painter.setBrush(QBrush(body_color))
                painter.drawPolygon(
                    QPolygonF(
                        [
                            QPointF(center_x - 42, ear_y + 8),
                            QPointF(center_x - 35, ear_y - 29),
                            QPointF(center_x - 10, ear_y + 1),
                        ]
                    )
                )
                painter.drawPolygon(
                    QPolygonF(
                        [
                            QPointF(center_x + 42, ear_y + 8),
                            QPointF(center_x + 35, ear_y - 29),
                            QPointF(center_x + 10, ear_y + 1),
                        ]
                    )
                )
            elif self.pet.species == "Dog":
                painter.setBrush(QColor("#936342"))
                painter.drawEllipse(
                    QPointF(center_x - 40, center_y - 22), 13, 25
                )
                painter.drawEllipse(
                    QPointF(center_x + 40, center_y - 22), 13, 25
                )
            painter.setBrush(QBrush(body_color))
            painter.drawEllipse(
                QPointF(center_x, center_y), 46, 43
            )

        if self.pet.species == "Robot":
            painter.setPen(QPen(QColor("#493B55"), 3, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(
                QPointF(center_x, center_y - 44),
                QPointF(center_x, center_y - 54),
            )
            painter.setBrush(QColor("#FFCE67"))
            painter.drawEllipse(QPointF(center_x, center_y - 57), 5, 5)

        happy = self.pet.mood in ("Happy", "Excited")
        sleepy = self.pet.is_sleeping or self.pet.mood == "Sleepy"
        eye_color = QColor("#382E43")
        painter.setPen(QPen(eye_color, 4, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(QBrush(eye_color))
        if self.blink or sleepy:
            painter.drawLine(
                QPointF(center_x - 17, center_y - 4),
                QPointF(center_x - 9, center_y - 4),
            )
            painter.drawLine(
                QPointF(center_x + 9, center_y - 4),
                QPointF(center_x + 17, center_y - 4),
            )
        else:
            painter.drawEllipse(QPointF(center_x - 13, center_y - 5), 3, 5)
            painter.drawEllipse(QPointF(center_x + 13, center_y - 5), 3, 5)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#F28391"))
        painter.drawEllipse(QPointF(center_x - 27, center_y + 7), 7, 4)
        painter.drawEllipse(QPointF(center_x + 27, center_y + 7), 7, 4)

        painter.setPen(QPen(eye_color, 3, Qt.SolidLine, Qt.RoundCap))
        if self.pet.mood in ("Sad", "Angry"):
            painter.drawArc(
                int(center_x - 8), int(center_y + 13), 16, 10, 0, 180 * 16
            )
        elif happy or self.reaction in ("feed", "pet", "clean"):
            painter.drawArc(
                int(center_x - 7), int(center_y + 8), 14, 11, 180 * 16, 180 * 16
            )
        else:
            painter.drawLine(
                QPointF(center_x - 5, center_y + 15),
                QPointF(center_x + 5, center_y + 15),
            )

        if self.reaction in ("feed", "pet", "clean", "game", "level_up"):
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#FFD166"))
            for x_offset, y_offset, radius in ((-42, -48, 4), (40, -55, 3), (48, -28, 3)):
                painter.drawEllipse(
                    QPointF(center_x + x_offset, center_y + y_offset), radius, radius
                )

        painter.setPen(QColor("#493B55"))
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        painter.drawText(
            0, height - 2, width, 18, Qt.AlignHCenter | Qt.AlignTop, self.pet.name
        )
        painter.end()
        _event.accept()


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
        self.reaction_timer = QTimer(self)
        self.reaction_timer.setSingleShot(True)
        self.reaction_timer.timeout.connect(self.clear_reaction)

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

        self.pet_canvas = PetCanvas(self.pet, self)
        layout.addWidget(self.pet_canvas)

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
        self.pet_canvas.anim_time = self.anim_time * intensity

        # Blinking animation
        self.blink_timer += 1
        if self.blink_timer > 50:  # Blink every ~5 seconds
            self.blink_timer = 0
            self.is_blinking = True
            # Short blink duration
            QTimer.singleShot(150, self.end_blink)

        self.pet_canvas.blink = self.is_blinking
        self.pet_canvas.update()

    def update_pet_display(self):
        """Update the pet's visual display."""
        self.setWindowTitle(f"{self.pet.name} - {self.pet.mood}")
        self.pet_canvas.update()

    def show_reaction(self, action):
        """Play a short, visible reaction to a care action or reward."""
        self.pet_canvas.reaction = action
        self.pet_canvas.update()
        self.reaction_timer.start(1400)

    def clear_reaction(self):
        self.pet_canvas.reaction = None
        self.pet_canvas.update()

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
        event.accept()

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

    def end_blink(self):
        """End blinking effect."""
        self.is_blinking = False
        self.pet_canvas.blink = False
        self.pet_canvas.update()
