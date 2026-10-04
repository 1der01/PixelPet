# PixelPet

A cute virtual desktop pet built with Python and PySide6 that lives on your Windows desktop. PixelPet reacts to user interactions, changes mood over time, performs idle animations, and generates random events. It's designed to feel like a fun, polished indie desktop companion rather than a basic programming demo.

![PixelPet](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Interactive Pet Care**: Feed, pet, play, clean, and put your pet to sleep
- **Dynamic Mood System**: Your pet's expression and behavior change based on its stats
- **Personality System**: Each pet has a unique personality that influences dialogue and behavior
- **Random Events**: Surprise events keep the experience fresh and engaging
- **Progression System**: Level up your pet through interactions and unlock cosmetic items
- **Transparent Floating Window**: The pet lives in a frameless, transparent window on your desktop
- **System Tray Integration**: Minimize to tray, view status, and access settings
- **Auto-Save**: Your pet's state is automatically saved locally
- **Lightweight Activity Detection**: Pet reacts to your computer activity (privacy-friendly)

## Screenshots

*Coming soon - Add screenshots of the pet window, interaction menu, and settings*

## Technology Stack

- **Python 3.8+**: Core application logic
- **PySide6**: Qt-based GUI framework for Windows desktop integration
- **JSON**: Local save data persistence
- **QTimer**: Event timing and game loop
- **Qt Animations**: Smooth UI transitions

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10 or higher (for system tray and desktop integration)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pixelpet.git
cd pixelpet
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## How to Run

Simply run the main script:
```bash
python main.py
```

On first launch, you'll be prompted to create your pet:
- Choose a name for your pet
- Select a species (Cat, Dog, Blob, Frog, or Robot)
- A personality will be randomly assigned

After creation, your pet will appear on your desktop. Double-click the pet to open the interaction menu, or right-click the system tray icon for options.

## Project Structure

```
pixelpet/
├── main.py                 # Application entry point
├── ui/                     # UI components
│   ├── pet_window.py       # Main floating pet window
│   ├── interaction_menu.py # Interaction menu and speech bubbles
│   ├── setup_window.py     # Pet creation/setup window
│   └── settings_window.py  # Settings dialog
├── core/                   # Game logic
│   ├── pet.py              # Main pet class
│   ├── stats.py            # Stat management (hunger, energy, happiness, cleanliness)
│   ├── mood.py             # Mood calculation system
│   ├── progression.py      # Level and progression system
│   ├── events.py           # Random event system
│   └── activity_monitor.py # User activity detection
├── data/                   # Data management
│   ├── save_manager.py     # JSON save/load functionality
│   └── default_data.py     # Default settings and constants
├── assets/                 # Art and sound assets
│   ├── pets/               # Pet sprites/art
│   ├── icons/              # UI icons
│   └── sounds/             # Sound effects
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How the Pet System Works

### Stats

Your pet has four main stats, each ranging from 0-100:

- **Hunger**: Decreases over time. Feed your pet to increase it.
- **Energy**: Decreases over time and with activities. Put your pet to sleep to restore it.
- **Happiness**: Increases with interactions. Decreases if neglected.
- **Cleanliness**: Decreases over time. Clean your pet to maintain it.

Stats gradually decay over time but the game is designed to be forgiving, not punishing.

### Mood

The pet's mood is calculated based on its current stats:
- Low hunger → Hungry
- Low energy → Sleepy
- Low cleanliness → Dirty
- Low happiness → Sad or Angry
- High happiness + high energy → Excited
- Good overall stats → Happy

The pet's ASCII art expression changes based on its mood.

### Personalities

Each pet has a randomly assigned personality that influences dialogue and behavior:
- **Lazy**: Relaxed, prefers napping
- **Energetic**: Always ready for action
- **Shy**: Quiet and gentle
- **Playful**: Loves games and fun
- **Chaotic**: Unpredictable and quirky
- **Curious**: Interested in everything
- **Grumpy**: A bit cantankerous

### Progression

Interactions grant experience points:
- Feed: +5 XP
- Pet: +2 XP
- Play: +10 XP
- Clean: +5 XP

Level up to unlock cosmetic items like hats, bows, glasses, and more!

### Random Events

Every few minutes, random events may occur:
- Pet gets hungry
- Pet falls asleep
- Pet asks for attention
- Pet finds an item
- Pet gets bored
- Pet starts dancing
- Pet complains about your screen time
- And more!

Events are shown in speech bubbles with personality-specific dialogue.

## Privacy Considerations

PixelPet includes lightweight activity detection to react to user behavior:

**What it does:**
- Detects when you become idle (no input for 5+ minutes)
- Detects when you become active again
- These detections are purely local and used for pet reactions

**What it does NOT do:**
- Capture screenshots
- Record keystrokes
- Collect personal data
- Send data to external servers
- Access files on your computer

All data is stored locally in JSON format in your user's home directory (`.pixelpet` folder).

## Settings

Access settings via the system tray menu:

- **Always on Top**: Keep the pet window above other windows
- **Start with Windows**: Launch PixelPet automatically on startup
- **Sound Effects**: Enable/disable sound effects
- **Notifications**: Enable/disable event notifications
- **Pet Transparency**: Adjust the pet window's opacity
- **Animation Intensity**: Control animation speed/intensity
- **Reset Pet**: Start fresh with a new pet (with confirmation)

## Future Improvements

Potential features for future versions:

- [ ] More species and pet variations
- [ ] Additional personalities
- [ ] More cosmetic items and customization
- [ ] Pet-to-pet interactions (multiple pets)
- [ ] Mini-games for earning XP
- [ ] Weather and time-of-day effects
- [ ] More complex event chains
- [ ] Sound effects and music
- [ ] Achievement system
- [ ] Mac and Linux support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by classic virtual pet games like Tamagotchi
- Built with PySide6/Qt for robust Windows desktop integration
- Designed as a portfolio project demonstrating clean architecture and polished UX

---

Made with ❤️ by [Your Name]
