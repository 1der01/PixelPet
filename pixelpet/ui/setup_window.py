"""Setup window for creating a new pet."""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SetupWindow(QWidget):
    """Window for creating a new pet."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_complete_callback = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the setup window UI."""
        self.setWindowTitle("Create Your PixelPet")
        self.setFixedSize(400, 450)

        # Create main container
        container = QFrame()
        container.setStyleSheet(
            """
            QFrame {
                background-color: #2C3E50;
                border-radius: 15px;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Create Your PixelPet")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ECF0F1;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Let's create your new companion!")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #BDC3C7;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Name input
        name_label = QLabel("Pet Name:")
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        name_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter a name...")
        self.name_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #3498DB;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }
        """
        )
        self.name_input.setText("Mochi")
        layout.addWidget(self.name_input)

        # Species selection
        species_label = QLabel("Species:")
        species_label.setFont(QFont("Arial", 10, QFont.Bold))
        species_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(species_label)

        self.species_combo = QComboBox()
        self.species_combo.addItems(["Cat", "Dog", "Blob", "Frog", "Robot"])
        self.species_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #3498DB;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """
        )
        layout.addWidget(self.species_combo)

        # Personality info
        info_label = QLabel("Personality will be randomly assigned!")
        info_label.setFont(QFont("Arial", 9))
        info_label.setStyleSheet("color: #95A5A6;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        layout.addStretch()

        # Create button
        create_btn = QPushButton("Create Pet")
        create_btn.setFont(QFont("Arial", 12, QFont.Bold))
        create_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #21618C;
            }
        """
        )
        create_btn.clicked.connect(self.create_pet)
        layout.addWidget(create_btn)

        container.setLayout(layout)

        # Set as main widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def create_pet(self):
        """Create the pet with user input."""
        name = self.name_input.text().strip()
        if not name:
            name = "Mochi"

        species = self.species_combo.currentText()

        if self.setup_complete_callback:
            self.setup_complete_callback({"name": name, "species": species})

        self.close()

    def set_setup_complete_callback(self, callback):
        """Set callback for setup completion."""
        self.setup_complete_callback = callback
