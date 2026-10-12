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
    QFileDialog,
    QComboBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SettingsWindow(QWidget):
    """Window for application settings."""

    def __init__(self, settings, save_manager=None, parent=None):
        super().__init__(parent)
        self.settings = settings.copy()
        self.save_manager = save_manager
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

        # Room theme
        room_theme_label = QLabel("Room Theme:")
        room_theme_label.setFont(QFont("Arial", 10, QFont.Bold))
        room_theme_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(room_theme_label)

        self.room_theme_combo = QComboBox()
        self.room_theme_combo.addItems(["Cozy", "Garden", "Space", "Neon"])
        self.room_theme_combo.setCurrentText(self.settings.get("room_theme", "Cozy"))
        self.room_theme_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #34495E;
                color: #ECF0F1;
                border: 1px solid #7F8C8D;
                border-radius: 6px;
                padding: 8px;
            }
            """
        )
        layout.addWidget(self.room_theme_combo)

        # Furniture selection
        room_furniture_label = QLabel("Room Furniture:")
        room_furniture_label.setFont(QFont("Arial", 10, QFont.Bold))
        room_furniture_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(room_furniture_label)

        self.room_furniture_checks = {}
        furniture_options = ["Bed", "Plant", "Toy Box", "Lamp"]
        furniture_row = QHBoxLayout()
        for index, item in enumerate(furniture_options):
            checkbox = QCheckBox(item)
            checkbox.setStyleSheet(
                """
                QCheckBox {
                    color: #ECF0F1;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
                QCheckBox::indicator:checked {
                    background-color: #3498DB;
                    border: 2px solid #3498DB;
                    border-radius: 3px;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #34495E;
                    border: 2px solid #7F8C8D;
                    border-radius: 3px;
                }
                """
            )
            self.room_furniture_checks[item] = checkbox
            furniture_row.addWidget(checkbox)
            if index == 1:
                layout.addLayout(furniture_row)
                furniture_row = QHBoxLayout()
        if furniture_row.count() > 0:
            layout.addLayout(furniture_row)

        current_furniture = self.settings.get("room_furniture", ["Bed", "Plant"])
        for item, checkbox in self.room_furniture_checks.items():
            checkbox.setChecked(item in current_furniture)

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

        # Save management buttons
        layout.addSpacing(20)

        backup_row = QHBoxLayout()
        backup_btn = QPushButton("Backup Save")
        backup_btn.setFont(QFont("Arial", 10, QFont.Bold))
        backup_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #8E44AD;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7D3C98;
            }
        """
        )
        backup_btn.clicked.connect(self.backup_save)
        backup_row.addWidget(backup_btn)

        restore_btn = QPushButton("Restore Backup")
        restore_btn.setFont(QFont("Arial", 10, QFont.Bold))
        restore_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D68910;
            }
        """
        )
        restore_btn.clicked.connect(self.restore_latest_backup)
        backup_row.addWidget(restore_btn)
        layout.addLayout(backup_row)

        export_row = QHBoxLayout()
        export_btn = QPushButton("Export Save")
        export_btn.setFont(QFont("Arial", 10, QFont.Bold))
        export_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #16A085;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #138D75;
            }
        """
        )
        export_btn.clicked.connect(self.export_save)
        export_row.addWidget(export_btn)

        import_btn = QPushButton("Import Save")
        import_btn.setFont(QFont("Arial", 10, QFont.Bold))
        import_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2E86DE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #246BB3;
            }
        """
        )
        import_btn.clicked.connect(self.import_save)
        export_row.addWidget(import_btn)
        layout.addLayout(export_row)

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
        self.settings["room_theme"] = self.room_theme_combo.currentText()
        self.settings["room_furniture"] = [
            item for item, checkbox in self.room_furniture_checks.items() if checkbox.isChecked()
        ] or ["Bed"]
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

    def backup_save(self):
        """Create a backup of the current pet save."""
        if self.save_manager is None:
            QMessageBox.warning(self, "Backup unavailable", "No save manager is configured.")
            return

        backup_path = self.save_manager.backup_pet_save()
        if backup_path:
            QMessageBox.information(self, "Backup created", f"Backup saved to:\n{backup_path}")
        else:
            QMessageBox.warning(self, "Backup failed", "Could not create a save backup.")

    def restore_latest_backup(self):
        """Restore the latest backup for the pet save."""
        if self.save_manager is None:
            QMessageBox.warning(self, "Restore unavailable", "No save manager is configured.")
            return

        latest_backup = self.save_manager.get_latest_backup(self.save_manager.save_file)
        if latest_backup is None:
            QMessageBox.warning(self, "No backup found", "There is no saved backup to restore.")
            return

        reply = QMessageBox.question(
            self,
            "Restore backup",
            f"Restore from {latest_backup}? This will overwrite your current pet save.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            if self.save_manager.restore_pet_backup(latest_backup):
                QMessageBox.information(self, "Backup restored", "Your pet save has been restored.")
            else:
                QMessageBox.warning(self, "Restore failed", "Could not restore the backup file.")

    def export_save(self):
        """Export the current pet save to a chosen JSON file."""
        if self.save_manager is None:
            QMessageBox.warning(self, "Export unavailable", "No save manager is configured.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PixelPet save",
            "pixelpet-save.json",
            "JSON Files (*.json)",
        )

        if not path:
            return

        export_path = self.save_manager.export_save(path, save_type="pet")
        if export_path:
            QMessageBox.information(self, "Save exported", f"Pet save exported to:\n{export_path}")
        else:
            QMessageBox.warning(self, "Export failed", "Could not export the pet save.")

    def import_save(self):
        """Import a pet save from a chosen JSON file."""
        if self.save_manager is None:
            QMessageBox.warning(self, "Import unavailable", "No save manager is configured.")
            return

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import PixelPet save",
            "",
            "JSON Files (*.json)",
        )

        if not path:
            return

        if self.save_manager.import_save(path, save_type="pet"):
            QMessageBox.information(self, "Save imported", "Your pet save was imported successfully.")
        else:
            QMessageBox.warning(self, "Import failed", "The selected file is not a valid PixelPet save.")

    def reset_pet(self):
        """Reset the pet with confirmation."""
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
