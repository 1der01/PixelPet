"""Settings window for PixelPet."""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QSlider,
    QPushButton,
    QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SettingsWindow(QWidget):
    """Window for application settings."""

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings.copy()
        self.settings_saved_callback = None
        self.pet_reset_callback = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the settings window UI."""
        self.setWindowTitle("PixelPet Settings")
        self.setFixedSize(400, 500)

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
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ECF0F1;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Always on top
        self.always_on_top_cb = QCheckBox("Always on Top")
        self.always_on_top_cb.setFont(QFont("Arial", 10))
        self.always_on_top_cb.setStyleSheet(
            """
            QCheckBox {
                color: #ECF0F1;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498DB;
                border: 2px solid #3498DB;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #34495E;
                border: 2px solid #7F8C8D;
                border-radius: 4px;
            }
        """
        )
        self.always_on_top_cb.setChecked(self.settings.get("always_on_top", True))
        layout.addWidget(self.always_on_top_cb)

        # Start with Windows
        self.start_with_windows_cb = QCheckBox("Start with Windows")
        self.start_with_windows_cb.setFont(QFont("Arial", 10))
        self.start_with_windows_cb.setStyleSheet(
            """
            QCheckBox {
                color: #ECF0F1;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498DB;
                border: 2px solid #3498DB;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #34495E;
                border: 2px solid #7F8C8D;
                border-radius: 4px;
            }
        """
        )
        self.start_with_windows_cb.setChecked(self.settings.get("start_with_windows", False))
        layout.addWidget(self.start_with_windows_cb)

        # Sound effects
        self.sound_effects_cb = QCheckBox("Sound Effects")
        self.sound_effects_cb.setFont(QFont("Arial", 10))
        self.sound_effects_cb.setStyleSheet(
            """
            QCheckBox {
                color: #ECF0F1;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498DB;
                border: 2px solid #3498DB;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #34495E;
                border: 2px solid #7F8C8D;
                border-radius: 4px;
            }
        """
        )
        self.sound_effects_cb.setChecked(self.settings.get("sound_effects", True))
        layout.addWidget(self.sound_effects_cb)

        # Notifications
        self.notifications_cb = QCheckBox("Notifications")
        self.notifications_cb.setFont(QFont("Arial", 10))
        self.notifications_cb.setStyleSheet(
            """
            QCheckBox {
                color: #ECF0F1;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498DB;
                border: 2px solid #3498DB;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #34495E;
                border: 2px solid #7F8C8D;
                border-radius: 4px;
            }
        """
        )
        self.notifications_cb.setChecked(self.settings.get("notifications", True))
        layout.addWidget(self.notifications_cb)

        # Pet transparency
        transparency_label = QLabel("Pet Transparency:")
        transparency_label.setFont(QFont("Arial", 10, QFont.Bold))
        transparency_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(transparency_label)

        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(50, 255)
        self.transparency_slider.setValue(self.settings.get("pet_transparency", 255))
        self.transparency_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 8px;
                background: #34495E;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498DB;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """
        )
        layout.addWidget(self.transparency_slider)

        # Animation intensity
        anim_label = QLabel("Animation Intensity:")
        anim_label.setFont(QFont("Arial", 10, QFont.Bold))
        anim_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(anim_label)

        self.anim_slider = QSlider(Qt.Horizontal)
        self.anim_slider.setRange(0, 200)
        self.anim_slider.setValue(int(self.settings.get("animation_intensity", 1.0) * 100))
        self.anim_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 8px;
                background: #34495E;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498DB;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """
        )
        layout.addWidget(self.anim_slider)

        # Reset Pet button
        layout.addSpacing(20)
        reset_btn = QPushButton("Reset Pet")
        reset_btn.setFont(QFont("Arial", 10, QFont.Bold))
        reset_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """
        )
        reset_btn.clicked.connect(self.reset_pet)
        layout.addWidget(reset_btn)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        save_btn.setFont(QFont("Arial", 10, QFont.Bold))
        save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """
        )
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Arial", 10))
        cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """
        )
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        container.setLayout(layout)

        # Set as main widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def save_settings(self):
        """Save the settings."""
        self.settings["always_on_top"] = self.always_on_top_cb.isChecked()
        self.settings["start_with_windows"] = self.start_with_windows_cb.isChecked()
        self.settings["sound_effects"] = self.sound_effects_cb.isChecked()
        self.settings["notifications"] = self.notifications_cb.isChecked()
        self.settings["pet_transparency"] = self.transparency_slider.value()
        self.settings["animation_intensity"] = self.anim_slider.value() / 100.0

        if self.settings_saved_callback:
            self.settings_saved_callback(self.settings)

        self.close()

    def set_settings_saved_callback(self, callback):
        """Set callback for settings saved."""
        self.settings_saved_callback = callback

    def set_pet_reset_callback(self, callback):
        """Set callback for pet reset."""
        self.pet_reset_callback = callback

    def reset_pet(self):
        """Reset the pet with confirmation."""
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            "Reset Pet",
            "Are you sure you want to reset your pet? This cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            if self.pet_reset_callback:
                self.pet_reset_callback()
            self.close()
