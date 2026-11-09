"""Interaction menu for PixelPet."""
from functools import partial

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QGraphicsOpacityEffect,
)
from PySide6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont


class InteractionMenu(QWidget):
    """Popup menu for pet interactions."""

    def __init__(self, pet, parent=None):
        super().__init__(parent)
        self.pet = pet
        self.action_callback = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the interaction menu UI."""
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create main container
        container = QFrame()
        container.setObjectName("careMenuCard")
        container.setStyleSheet(
            """
            QFrame#careMenuCard {
                background-color: #F6F3EE;
                border: 1px solid #DDD4E8;
                border-radius: 16px;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        # Title
        title = QLabel(f"Care for {self.pet.name}")
        title.setObjectName("careMenuTitle")
        title.setAccessibleName("Care menu")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color: #302B3A;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Choose an action")
        subtitle.setStyleSheet("color: #71687B; font-size: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Action buttons
        self.action_buttons = []
        buttons = [
            ("Feed", "🍖", self.pet.feed, f"Feed {self.pet.name}"),
            ("Pet", "✋", self.pet.pet, f"Pet {self.pet.name}"),
            ("Play", "🎾", self.pet.play, f"Play with {self.pet.name}"),
            ("Clean", "🧹", self.pet.clean, f"Clean {self.pet.name}"),
            ("Sleep", "😴", self.pet.sleep, f"Put {self.pet.name} to sleep"),
        ]

        for text, icon, action, accessible_name in buttons:
            btn = self.create_button(
                f"{icon} {text}", accessible_name, "careActionButton"
            )
            btn.clicked.connect(partial(self.perform_action, action))
            layout.addWidget(btn)
            self.action_buttons.append(btn)

        separator = QFrame()
        separator.setObjectName("menuSeparator")
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #DED7E7;")
        layout.addWidget(separator)

        status_button = self.create_button(
            "📊 My Pet", f"{self.pet.name}'s status", "utilityButton"
        )
        status_button.clicked.connect(
            lambda: self.action_callback and self.action_callback("status", None)
        )
        layout.addWidget(status_button)

        game_button = self.create_button(
            "🍪 Catch Treats", "Play Catch Treats", "utilityButton"
        )
        game_button.clicked.connect(
            lambda: self.action_callback and self.action_callback("treat_game", None)
        )
        layout.addWidget(game_button)

        container.setLayout(layout)

        # Set as main widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

        # Set size
        self.setFixedSize(228, 430)

    @staticmethod
    def create_button(text, accessible_name=None, object_name="careActionButton"):
        """Create a consistently styled interaction button."""
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setAccessibleName(accessible_name or text)
        button.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        button.setStyleSheet(
            """
            QPushButton#careActionButton {
                background-color: #FFFFFF;
                color: #393243;
                border: 1px solid #DED7E7;
                border-radius: 9px;
                padding: 8px 10px;
                min-width: 158px;
            }
            QPushButton#careActionButton:hover {
                background-color: #EEE8F8;
                border-color: #B5A4D7;
            }
            QPushButton#careActionButton:focus {
                border: 2px solid #7352B8;
            }
            QPushButton#careActionButton:pressed {
                background-color: #DED4F0;
            }
            QPushButton#utilityButton {
                background-color: #7352B8;
                color: #FFFFFF;
                border: 1px solid #60429F;
                border-radius: 9px;
                padding: 8px 10px;
                min-width: 158px;
            }
            QPushButton#utilityButton:hover {
                background-color: #60429F;
            }
            QPushButton#utilityButton:focus {
                border: 2px solid #302B3A;
            }
            QPushButton#utilityButton:pressed {
                background-color: #513B83;
            }
        """
        )
        return button

    def perform_action(self, action):
        """Perform an action on the pet."""
        result_data = action()
        self.hide()

        if self.action_callback:
            # Handle both old (string) and new (tuple) return values
            if isinstance(result_data, tuple):
                result, sound_name, leveled_up = result_data
                self.action_callback("action", {
                    "result": result,
                    "sound": sound_name,
                    "leveled_up": leveled_up
                })
            else:
                # Backward compatibility
                self.action_callback("action", {"result": result_data})

    def show_at_position(self, pos):
        """Show menu at specified position."""
        self.move(pos)
        self.show()
        if self.action_buttons:
            self.action_buttons[0].setFocus()

    def set_action_callback(self, callback):
        """Set callback for action events."""
        self.action_callback = callback


class SpeechBubble(QWidget):
    """Speech bubble for pet dialogue with animations and smart positioning."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.fade_animation = None
        self.hide_timer = None

    def setup_ui(self):
        """Setup the speech bubble UI."""
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create bubble with better styling
        self.bubble = QFrame()
        self.bubble.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 250);
                border-radius: 20px;
                border: 2px solid rgba(100, 100, 100, 0.2);
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel()
        self.label.setFont(QFont("Segoe UI", 10))
        self.label.setStyleSheet(
            """
            QLabel {
                color: #2C3E50;
                background-color: transparent;
            }
        """
        )
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.bubble.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.bubble)
        self.setLayout(main_layout)

        # Setup opacity effect for fade animations
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

    def calculate_position(self, pet_pos, pet_size):
        """Calculate smart position for speech bubble avoiding screen edges."""
        from PySide6.QtWidgets import QApplication

        pet_center = pet_pos + QPoint(pet_size.width() // 2, pet_size.height() // 2)
        screen = QApplication.screenAt(pet_center)
        if not screen:
            screen = QApplication.primaryScreen()

        if not screen:
            return pet_pos + QPoint(0, -self.height() - 20)

        screen_geometry = screen.availableGeometry()
        margin = 10
        bubble_width = self.width()
        bubble_height = self.height()
        x = pet_center.x() - bubble_width // 2
        y = pet_pos.y() - bubble_height - 20

        if y < screen_geometry.top() + margin:
            y = pet_pos.y() + pet_size.height() + 20

        x = max(
            screen_geometry.left() + margin,
            min(x, screen_geometry.right() - bubble_width - margin + 1),
        )
        y = max(
            screen_geometry.top() + margin,
            min(y, screen_geometry.bottom() - bubble_height - margin + 1),
        )

        return QPoint(x, y)

    def show_message(self, message, pet_pos, pet_size=None):
        """Show a message with fade-in animation at smart position."""
        # Cancel any existing hide timer
        if self.hide_timer:
            self.hide_timer.stop()

        # Set message and calculate size
        self.label.setText(message)
        text_width = max(
            self.label.fontMetrics().horizontalAdvance(line)
            for line in message.splitlines() or [""]
        )
        bubble_width = max(200, min(350, text_width + 40))
        label_width = bubble_width - 48
        self.label.setFixedWidth(label_width)
        label_height = max(1, self.label.heightForWidth(label_width))
        self.label.setFixedHeight(label_height)
        self.bubble.layout().invalidate()
        self.layout().invalidate()
        self.bubble.adjustSize()
        self.setFixedSize(self.bubble.sizeHint())

        # Calculate smart position
        if pet_size:
            pos = self.calculate_position(pet_pos, pet_size)
        else:
            pos = pet_pos + QPoint(0, -self.height() - 20)

        self.move(pos)

        # Fade in animation
        self.fade_in()

        # Auto-hide after 5 seconds
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.fade_out)
        self.hide_timer.start(5000)

    def fade_in(self):
        """Fade in the speech bubble."""
        self.show()
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.start()

    def fade_out(self):
        """Fade out the speech bubble."""
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()

    def hide_message(self):
        """Hide the speech bubble immediately with fade out."""
        if self.hide_timer:
            self.hide_timer.stop()
        self.fade_out()
