"""Settings window for PixelPet."""
import copy
import os

from pixelpet.data import SettingsManager

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
    QScrollArea,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SettingsWindow(QWidget):
    """Window for application settings."""

    ROOM_THEME_OPTIONS = ["Cozy", "Garden", "Space", "Neon"]
    ROOM_FURNITURE_OPTIONS = ["Bed", "Plant", "Toy Box", "Lamp"]
    DEFAULT_ROOM_FURNITURE = ["Bed", "Plant"]
    CHECKBOX_STYLE = """
        QCheckBox {
            color: #ECF0F1;
        }
        QCheckBox:disabled {
            color: #7F8C8D;
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
    CHECKBOX_FURNITURE_STYLE = """
        QCheckBox {
            color: #ECF0F1;
        }
        QCheckBox:disabled {
            color: #7F8C8D;
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
    COMBOBOX_STYLE = """
        QComboBox {
            background-color: #34495E;
            color: #ECF0F1;
            border: 1px solid #7F8C8D;
            border-radius: 6px;
            padding: 8px;
        }
    """
    SLIDER_STYLE = """
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

    def __init__(self, settings, save_manager=None, pet=None, parent=None):
        super().__init__(parent)
        self.settings = SettingsManager.normalize(settings)
        self.save_manager = save_manager
        self.pet = pet
        self.settings_saved_callback = None
        self.pet_reset_callback = None
        self.pet_save_changed_callback = None
        self.setup_ui()

    @staticmethod
    def _create_checkbox(label_text, checked=False):
        """Create a themed checkbox."""
        checkbox = QCheckBox(label_text)
        checkbox.setFont(QFont("Arial", 10))
        checkbox.setStyleSheet(SettingsWindow.CHECKBOX_STYLE)
        checkbox.setChecked(checked)
        return checkbox

    @staticmethod
    def _create_button(label_text, background_color, hover_color, callback=None):
        """Create a themed button."""
        button = QPushButton(label_text)
        button.setFont(QFont("Arial", 10, QFont.Bold))
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            """
        )
        if callback is not None:
            button.clicked.connect(callback)
        return button

    def _get_available_furniture(self):
        """Return the room furniture that is currently unlocked."""
        if self.pet is not None and hasattr(self.pet, "progression"):
            try:
                return self.pet.progression.get_available_room_furniture()
            except (AttributeError, TypeError):
                pass
        return list(self.DEFAULT_ROOM_FURNITURE)

    def _sanitize_room_furniture(self, furniture):
        """Validate furniture selections and keep only valid unlocked items."""
        available = self._get_available_furniture()
        if self.pet is not None and hasattr(self.pet, "progression"):
            try:
                return self.pet.progression.sanitize_room_furniture(furniture)
            except (AttributeError, TypeError):
                pass

        cleaned = []
        seen = set()
        for item in furniture or []:
            if item in available and item not in seen:
                cleaned.append(item)
                seen.add(item)
        if not cleaned:
            return available[:1] if available else ["Bed"]
        return cleaned

    def setup_ui(self):
        """Setup the settings window UI."""
        self.setWindowTitle("PixelPet Settings")
        self.resize(400, 500)
        self.setMinimumSize(360, 400)

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

        title = QLabel("Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ECF0F1;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.always_on_top_cb = self._create_checkbox(
            "Always on Top", self.settings.get("always_on_top", True)
        )
        layout.addWidget(self.always_on_top_cb)

        self.start_with_windows_cb = self._create_checkbox(
            "Start with Windows", self.settings.get("start_with_windows", False)
        )
        self.start_with_windows_cb.setEnabled(os.name == "nt")
        if os.name != "nt":
            self.start_with_windows_cb.setToolTip(
                "Automatic startup is only supported on Windows."
            )
        layout.addWidget(self.start_with_windows_cb)

        self.sound_effects_cb = self._create_checkbox(
            "Sound Effects", self.settings.get("sound_effects", True)
        )
        layout.addWidget(self.sound_effects_cb)

        self.notifications_cb = self._create_checkbox(
            "Event Notifications", self.settings.get("notifications", True)
        )
        self.notifications_cb.setToolTip(
            "Show speech bubbles and reactions for random pet events."
        )
        layout.addWidget(self.notifications_cb)

        room_theme_label = QLabel("Room Theme:")
        room_theme_label.setFont(QFont("Arial", 10, QFont.Bold))
        room_theme_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(room_theme_label)

        self.room_theme_combo = QComboBox()
        self.room_theme_combo.addItems(SettingsManager.ROOM_THEME_OPTIONS)
        current_theme = self.settings.get("room_theme", "Cozy")
        if current_theme in SettingsManager.ROOM_THEME_OPTIONS:
            self.room_theme_combo.setCurrentText(current_theme)
        else:
            self.room_theme_combo.setCurrentText("Cozy")
        self.room_theme_combo.setStyleSheet(self.COMBOBOX_STYLE)
        layout.addWidget(self.room_theme_combo)

        room_furniture_label = QLabel("Room Furniture:")
        room_furniture_label.setFont(QFont("Arial", 10, QFont.Bold))
        room_furniture_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(room_furniture_label)

        self.room_furniture_checks = {}
        available_furniture = self._get_available_furniture()
        furniture_row = QHBoxLayout()
        for index, item in enumerate(SettingsManager.ROOM_FURNITURE_OPTIONS):
            checkbox = QCheckBox(item)
            checkbox.setEnabled(item in available_furniture)
            checkbox.setToolTip(
                "Unlocked" if item in available_furniture else self._get_furniture_unlock_tooltip(item)
            )
            checkbox.setStyleSheet(self.CHECKBOX_FURNITURE_STYLE)
            self.room_furniture_checks[item] = checkbox
            furniture_row.addWidget(checkbox)
            if index == 1:
                layout.addLayout(furniture_row)
                furniture_row = QHBoxLayout()
        if furniture_row.count() > 0:
            layout.addLayout(furniture_row)

        current_furniture = self._sanitize_room_furniture(
            self.settings.get("room_furniture", available_furniture)
        )
        for item, checkbox in self.room_furniture_checks.items():
            checkbox.setChecked(item in current_furniture)

        transparency_label = QLabel("Pet Transparency:")
        transparency_label.setFont(QFont("Arial", 10, QFont.Bold))
        transparency_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(transparency_label)

        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(50, 255)
        self.transparency_slider.setValue(int(self.settings.get("pet_transparency", 255)))
        self.transparency_slider.setStyleSheet(self.SLIDER_STYLE)
        layout.addWidget(self.transparency_slider)

        anim_label = QLabel("Animation Intensity:")
        anim_label.setFont(QFont("Arial", 10, QFont.Bold))
        anim_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(anim_label)

        self.anim_slider = QSlider(Qt.Horizontal)
        self.anim_slider.setRange(0, 200)
        self.anim_slider.setValue(int(float(self.settings.get("animation_intensity", 1.0)) * 100))
        self.anim_slider.setStyleSheet(self.SLIDER_STYLE)
        layout.addWidget(self.anim_slider)

        layout.addSpacing(20)

        backup_row = QHBoxLayout()
        backup_btn = self._create_button("Backup Save", "#8E44AD", "#7D3C98")
        backup_btn.clicked.connect(self.backup_save)
        backup_row.addWidget(backup_btn)

        restore_btn = self._create_button("Restore Backup", "#F39C12", "#D68910")
        restore_btn.clicked.connect(self.restore_latest_backup)
        backup_row.addWidget(restore_btn)
        layout.addLayout(backup_row)

        export_row = QHBoxLayout()
        export_btn = self._create_button("Export Save", "#16A085", "#138D75")
        export_btn.clicked.connect(self.export_save)
        export_row.addWidget(export_btn)

        import_btn = self._create_button("Import Save", "#2E86DE", "#246BB3")
        import_btn.clicked.connect(self.import_save)
        export_row.addWidget(import_btn)
        layout.addLayout(export_row)

        reset_btn = self._create_button("Reset Pet", "#E74C3C", "#C0392B")
        reset_btn.clicked.connect(self.reset_pet)
        layout.addWidget(reset_btn)

        layout.addStretch()

        button_layout = QHBoxLayout()
        save_btn = self._create_button("Save", "#27AE60", "#229954")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)

        cancel_btn = self._create_button("Cancel", "#E74C3C", "#C0392B")
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        container.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def _get_furniture_unlock_tooltip(self, item):
        """Return the tooltip text for a locked furniture item."""
        if self.pet is None or not hasattr(self.pet, "progression"):
            return "Locked"

        unlock_level = next(
            (
                level
                for level, items in sorted(self.pet.progression.ROOM_FURNITURE_UNLOCKS.items())
                if item in items
            ),
            None,
        )
        return f"Unlock at level {unlock_level}." if unlock_level is not None else "Locked"

    def save_settings(self):
        """Save the settings after validating entries."""
        theme = self.room_theme_combo.currentText()
        if theme not in SettingsManager.ROOM_THEME_OPTIONS:
            theme = SettingsManager.normalize({})["room_theme"]

        available_furniture = self._get_available_furniture()
        selected_furniture = [
            item
            for item, checkbox in self.room_furniture_checks.items()
            if checkbox.isChecked() and item in available_furniture
        ]

        self.settings = SettingsManager.normalize(
            {
                "always_on_top": self.always_on_top_cb.isChecked(),
                "start_with_windows": self.start_with_windows_cb.isChecked(),
                "sound_effects": self.sound_effects_cb.isChecked(),
                "notifications": self.notifications_cb.isChecked(),
                "room_theme": theme,
                "room_furniture": self._sanitize_room_furniture(selected_furniture),
                "pet_transparency": int(self.transparency_slider.value()),
                "animation_intensity": self.anim_slider.value() / 100.0,
            }
        )

        if self.settings_saved_callback:
            self.settings_saved_callback(self.settings)

        self.close()

    def set_settings_saved_callback(self, callback):
        """Set callback for settings saved."""
        self.settings_saved_callback = callback

    def set_pet_reset_callback(self, callback):
        """Set callback for pet reset."""
        self.pet_reset_callback = callback

    def set_pet_save_changed_callback(self, callback):
        """Set callback for a successful pet save import or restore."""
        self.pet_save_changed_callback = callback

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
                if self.pet_save_changed_callback and not self.pet_save_changed_callback():
                    QMessageBox.warning(
                        self,
                        "Restore failed",
                        "The backup was restored, but the pet could not be reloaded.",
                    )
                    return
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
            if self.pet_save_changed_callback and not self.pet_save_changed_callback():
                QMessageBox.warning(
                    self,
                    "Import failed",
                    "The save was imported, but the pet could not be reloaded.",
                )
                return
            QMessageBox.information(self, "Save imported", "Your pet save was imported successfully.")
        else:
            QMessageBox.warning(
                self,
                "Import failed",
                "The selected file is not a valid PixelPet save.",
            )

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
