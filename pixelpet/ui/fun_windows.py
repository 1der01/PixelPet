"""Status and mini-game windows for PixelPet."""
import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)


class PetStatusWindow(QDialog):
    """A compact overview of pet needs and long-term progress."""

    STAT_NAMES = (
        ("hunger", "Hunger"),
        ("energy", "Energy"),
        ("happiness", "Happiness"),
        ("cleanliness", "Cleanliness"),
    )

    def __init__(self, pet, accessory_callback=None, parent=None):
        super().__init__(parent)
        self.pet = pet
        self.accessory_callback = accessory_callback
        self.setWindowTitle(f"{pet.name}'s Status")
        self.setMinimumWidth(340)

        layout = QVBoxLayout(self)
        self.heading = QLabel()
        self.heading.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.heading)

        self.stat_bars = {}
        for stat_id, label in self.STAT_NAMES:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setTextVisible(True)
            self.stat_bars[stat_id] = bar
            row.addWidget(bar)
            layout.addLayout(row)

        self.level_label = QLabel()
        self.xp_bar = QProgressBar()
        layout.addWidget(self.level_label)
        layout.addWidget(self.xp_bar)

        self.affection_label = QLabel()
        layout.addWidget(self.affection_label)

        self.section_label = QLabel("Care goals")
        self.section_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.section_label)
        self.goals_label = QLabel()
        self.goals_label.setWordWrap(True)
        layout.addWidget(self.goals_label)

        self.collection_label = QLabel()
        self.collection_label.setWordWrap(True)
        layout.addWidget(self.collection_label)

        self.accessory_label = QLabel("Equipped accessory")
        self.accessory_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.accessory_label)
        self.accessory_selector = QComboBox()
        self.accessory_selector.addItem("None")
        self.accessory_selector.currentTextChanged.connect(
            self.handle_accessory_selection
        )
        layout.addWidget(self.accessory_selector)

        self.refresh_status()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_status)
        self.refresh_timer.start(1000)

    def refresh_status(self):
        """Refresh values from the current pet state."""
        progression = self.pet.progression
        self.heading.setText(
            f"{self.pet.name} the {self.pet.species}  |  {self.pet.mood}"
            f"\n{self.pet.personality} personality"
        )
        for stat_id in self.stat_bars:
            value = getattr(self.pet.stats, stat_id)
            self.stat_bars[stat_id].setValue(value)

        required_xp = progression.xp_for_next_level()
        self.level_label.setText(f"Level {progression.level}")
        self.xp_bar.setRange(0, required_xp)
        self.xp_bar.setValue(progression.experience)
        self.xp_bar.setFormat(f"{progression.experience} / {required_xp} XP")
        self.affection_label.setText(
            f"Affection: {progression.affection}  |  Care actions: {progression.care_streak}"
        )

        goal_lines = [
            f"{goal['title']}: {goal['progress']}/{goal['target']}"
            for goal in progression.get_goal_status()
        ]
        self.goals_label.setText("\n".join(goal_lines) or "No goals yet.")

        achievements = ", ".join(progression.achievements) or "None yet"
        inventory = ", ".join(progression.inventory) or "No accessories yet"
        self.collection_label.setText(
            f"Achievements: {achievements}\nAccessories: {inventory}"
        )

        selected_item = progression.equipped_accessory or "None"
        available_items = ["None", *progression.inventory]
        current_items = [
            self.accessory_selector.itemText(index)
            for index in range(self.accessory_selector.count())
        ]
        if current_items != available_items:
            self.accessory_selector.blockSignals(True)
            self.accessory_selector.clear()
            self.accessory_selector.addItems(available_items)
            self.accessory_selector.blockSignals(False)
        if self.accessory_selector.currentText() != selected_item:
            self.accessory_selector.setCurrentText(selected_item)

    def handle_accessory_selection(self, selected_item):
        """Equip the selected owned item and notify the application."""
        item = None if selected_item == "None" else selected_item
        self.pet.progression.equip_accessory(item)
        if self.accessory_callback:
            self.accessory_callback(item)

    def closeEvent(self, event):
        self.refresh_timer.stop()
        super().closeEvent(event)


class TreatCatchWindow(QDialog):
    """A short click-the-treat mini-game with bounded, persistent rewards."""

    GAME_SECONDS = 20
    MAX_SCORE = 10

    def __init__(self, pet, completed_callback=None, parent=None):
        super().__init__(parent)
        self.pet = pet
        self.completed_callback = completed_callback
        self.remaining = self.GAME_SECONDS
        self.score = 0
        self.game_finished = False

        self.setWindowTitle(f"Catch Treats with {pet.name}!")
        self.setFixedSize(440, 300)

        layout = QVBoxLayout(self)
        self.instruction = QLabel("Click the treat before it hops away!")
        self.instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction)

        self.score_label = QLabel()
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)

        self.playfield = QFrame()
        self.playfield.setFrameShape(QFrame.StyledPanel)
        self.playfield.setStyleSheet(
            "QFrame { background-color: #EAF7FF; border: 1px solid #B7DDF2; }"
        )
        self.playfield.setFixedSize(410, 190)
        layout.addWidget(self.playfield, alignment=Qt.AlignCenter)

        self.treat_button = QPushButton("🍪 Treat")
        self.treat_button.setParent(self.playfield)
        self.treat_button.setFixedSize(90, 38)
        self.treat_button.clicked.connect(self.catch_treat)
        self.place_treat()

        self.timer_label = QLabel()
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)

        self.close_button = QPushButton("Close")
        self.close_button.setEnabled(False)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.tick)
        self.hop_timer = QTimer(self)
        self.hop_timer.timeout.connect(self.place_treat)
        self.update_labels()
        self.countdown_timer.start(1000)
        self.hop_timer.start(1400)

    def update_labels(self):
        self.score_label.setText(f"Treats caught: {self.score}/{self.MAX_SCORE}")
        self.timer_label.setText(f"Time left: {self.remaining} seconds")

    def place_treat(self):
        """Move the treat to a random position inside the playfield."""
        max_x = self.playfield.width() - self.treat_button.width()
        max_y = self.playfield.height() - self.treat_button.height()
        self.treat_button.move(random.randint(0, max_x), random.randint(0, max_y))

    def catch_treat(self):
        if self.game_finished:
            return
        self.score = min(self.MAX_SCORE, self.score + 1)
        self.update_labels()
        self.place_treat()
        if self.score >= self.MAX_SCORE:
            self.finish_game()

    def tick(self):
        self.remaining -= 1
        self.update_labels()
        if self.remaining <= 0:
            self.finish_game()

    def finish_game(self):
        if self.game_finished:
            return
        self.game_finished = True
        self.countdown_timer.stop()
        self.hop_timer.stop()
        self.treat_button.setEnabled(False)

        reward = self.pet.progression.award_treat_game(self.score)
        message = f"Game over! You caught {self.score} treats and earned {reward['experience']} XP."
        if reward["item"]:
            message += f" You unlocked the {reward['item']}!"
        self.instruction.setText(message)
        self.close_button.setEnabled(True)
        if self.completed_callback:
            self.completed_callback(reward)

    def closeEvent(self, event):
        """Stop an abandoned game without awarding an incomplete round."""
        if not self.game_finished:
            self.game_finished = True
            self.countdown_timer.stop()
            self.hop_timer.stop()
        super().closeEvent(event)
