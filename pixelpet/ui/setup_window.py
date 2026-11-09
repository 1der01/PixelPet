"""Setup window for creating a new pet."""
from pixelpet.core.pet import Pet

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
        self.setFixedSize(440, 500)
        self.setObjectName("setupWindow")
        self.setStyleSheet(
            """
            QWidget#setupWindow {
                background-color: #F6F3EE;
            }
            QFrame#setupCard {
                background-color: #FFFFFF;
                border: 1px solid #E5DFD7;
                border-radius: 18px;
            }
            QLabel#setupTitle {
                color: #302B3A;
                font-size: 23px;
                font-weight: 700;
            }
            QLabel#setupSubtitle, QLabel#setupHint {
                color: #71687B;
            }
            QLabel#setupFieldLabel {
                color: #51465F;
                font-size: 12px;
                font-weight: 700;
            }
            QLineEdit#petNameInput, QComboBox#petSpeciesCombo {
                background-color: #FBFAFD;
                border: 1px solid #CFC6D9;
                border-radius: 9px;
                color: #302B3A;
                padding: 10px;
                min-height: 22px;
            }
            QLineEdit#petNameInput:focus, QComboBox#petSpeciesCombo:focus {
                border: 2px solid #7352B8;
            }
            QFrame#personalityNote {
                background-color: #F1ECF8;
                border: 1px solid #E2D9F0;
                border-radius: 10px;
            }
            QLabel#setupHint {
                background: transparent;
                border: none;
                padding: 8px;
            }
            QPushButton#createPetButton {
                background-color: #7352B8;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 700;
                padding: 12px;
            }
            QPushButton#createPetButton:hover {
                background-color: #60429F;
            }
            QPushButton#createPetButton:focus {
                border: 2px solid #302B3A;
            }
            QPushButton#createPetButton:pressed {
                background-color: #513B83;
            }
            """
        )

        # Create main container
        container = QFrame()
        container.setObjectName("setupCard")

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(12)

        # Title
        title = QLabel("Create Your PixelPet")
        title.setObjectName("setupTitle")
        title.setFont(QFont("Segoe UI", 21, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Let's create your new companion!")
        subtitle.setObjectName("setupSubtitle")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Name input
        name_label = QLabel("Pet Name:")
        name_label.setObjectName("setupFieldLabel")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setObjectName("petNameInput")
        self.name_input.setAccessibleName("Pet name")
        self.name_input.setPlaceholderText("Enter a name...")
        self.name_input.setText("Mochi")
        name_label.setBuddy(self.name_input)
        layout.addWidget(self.name_input)

        # Species selection
        species_label = QLabel("Species:")
        species_label.setObjectName("setupFieldLabel")
        species_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(species_label)

        self.species_combo = QComboBox()
        self.species_combo.setObjectName("petSpeciesCombo")
        self.species_combo.setAccessibleName("Pet species")
        self.species_combo.addItems(["Cat", "Dog", "Blob", "Frog", "Robot"])
        species_label.setBuddy(self.species_combo)
        layout.addWidget(self.species_combo)

        # Personality info
        info_card = QFrame()
        info_card.setObjectName("personalityNote")
        info_layout = QHBoxLayout(info_card)
        info_layout.setContentsMargins(8, 3, 8, 3)
        info_label = QLabel("A unique personality will be chosen for your pet.")
        info_label.setObjectName("setupHint")
        info_label.setFont(QFont("Segoe UI", 9))
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)
        layout.addWidget(info_card)

        layout.addStretch()

        # Create button
        create_btn = QPushButton("Create Pet")
        create_btn.setObjectName("createPetButton")
        create_btn.setAccessibleName("Create pet")
        create_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        create_btn.clicked.connect(self.create_pet)
        layout.addWidget(create_btn)

        container.setLayout(layout)

        # Set as main widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def create_pet(self):
        """Create the pet with sanitized user input."""
        name = Pet.normalize_name(self.name_input.text())
        species = Pet.normalize_species(self.species_combo.currentText())

        if self.setup_complete_callback:
            self.setup_complete_callback({"name": name, "species": species})

        self.close()

    def set_setup_complete_callback(self, callback):
        """Set callback for setup completion."""
        self.setup_complete_callback = callback
