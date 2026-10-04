"""Interaction menu for PixelPet."""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt, QPoint, QTimer
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
        container.setStyleSheet(
            """
            QFrame {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel(f"What would you like to do with {self.pet.name}?")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Action buttons
        buttons = [
            ("Feed", "🍖", self.pet.feed),
            ("Pet", "✋", self.pet.pet),
            ("Play", "🎾", self.pet.play),
            ("Clean", "🧹", self.pet.clean),
            ("Sleep", "😴", self.pet.sleep),
        ]

        for text, icon, action in buttons:
            btn = QPushButton(f"{icon} {text}")
            btn.setFont(QFont("Arial", 9))
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 8px;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """
            )
            btn.clicked.connect(lambda checked, a=action: self.perform_action(a))
            layout.addWidget(btn)

        container.setLayout(layout)

        # Set as main widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

        # Set size
        self.setFixedSize(180, 280)

    def perform_action(self, action):
        """Perform an action on the pet."""
        result = action()
        self.hide()

        if self.action_callback:
            self.action_callback("action", {"result": result})

    def show_at_position(self, pos):
        """Show menu at specified position."""
        self.move(pos)
        self.show()

    def set_action_callback(self, callback):
        """Set callback for action events."""
        self.action_callback = callback


class SpeechBubble(QWidget):
    """Speech bubble for pet dialogue."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup the speech bubble UI."""
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create bubble
        self.bubble = QFrame()
        self.bubble.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 240);
                border-radius: 15px;
                border: 2px solid rgba(0, 0, 0, 0.1);
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        self.label = QLabel()
        self.label.setFont(QFont("Arial", 9))
        self.label.setStyleSheet("color: #333;")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.bubble.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.bubble)
        self.setLayout(main_layout)

        self.setFixedSize(200, 80)

    def show_message(self, message, pos):
        """Show a message at the specified position."""
        self.label.setText(message)
        self.move(pos)
        self.show()

        # Auto-hide after 5 seconds
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.hide)
        self.hide_timer.start(5000)
