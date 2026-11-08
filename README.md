# PixelPet

A cute virtual desktop pet built with Python and PySide6 that lives on your Windows desktop. PixelPet reacts to user interactions, changes mood over time, performs idle animations, and generates random events. It's designed to feel like a fun, polished indie desktop companion rather than a basic programming demo.

![PixelPet](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Interactive Pet Care**: Feed, pet, play, clean, and put your pet to sleep
- **Dynamic Mood System**: Your pet's expression and behavior change based on its stats
- **Personality System**: Each pet has a unique personality that influences dialogue and behavior
- **Random Events**: Surprise events keep the experience fresh and engaging
- **Progression System**: Level up your pet through interactions and unlock cosmetic items
- **Pet Status Panel**: Review needs, XP, care goals, affection, achievements, and accessories
- **Treat Catch Mini-Game**: Catch treats for XP, with a one-time Golden Bell reward for a high score
- **Custom-Drawn Pet**: Animated pet artwork in a frameless, transparent desktop window
- **System Tray Integration**: Minimize to tray, view status, and access settings
- **Auto-Save**: Your pet's state is automatically saved locally
- **Local Activity Tracking**: Pet care interactions update a local activity timer; the app does not monitor system-wide keyboard or mouse input

## Technology Stack

- **Python 3.10+**: Core application logic
- **PySide6**: Qt-based GUI framework for Windows desktop integration
- **JSON**: Local save data persistence
- **QTimer**: Event timing and game loop
- **QPainter and QTimer**: Custom pet drawing, idle animation, and game updates

## Installation

### Prerequisites

- Python 3.10 or higher
- Windows 10 or higher (for system tray and desktop integration)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/1der01/PixelPet.git
cd PixelPet
```

2. Create and activate a virtual environment in PowerShell:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install and run PixelPet:
```bash
python -m pip install -e .
python main.py
```

### Build a portable Windows executable

Build on Windows with Python 3.10 or newer:

```powershell
python -m pip install -e ".[build]"
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PixelPet main.py
```

The standalone executable is written to `dist\PixelPet.exe`. It does not
require Python to be installed on the target computer. The GitHub Actions
workflow also builds this executable and publishes it as a downloadable
workflow artifact; it is not an installer or a signed release.

## How to Run

Simply run the main script:
```bash
python main.py
```

On first launch, you'll be prompted to create your pet:
- Choose a name for your pet
- Select a species (Cat, Dog, Blob, Frog, or Robot)
- A personality will be randomly assigned

After creation, your pet will appear on your desktop. Double-click the pet, or
focus it and press **Space** or **Enter**, to open the interaction menu. Use
**Tab** and **Enter** to navigate and choose menu actions, or right-click the
system tray icon for application options.

The interaction menu, pet stats, experience bar, and accessory selector have
screen-reader names. In the Catch Treats mini-game, focus the treat and press
**Space** or **Enter** to catch it.

## Project Structure

```
pixelpet/
├── main.py                 # Application and tray orchestration
├── ui/                     # UI components
│   ├── pet_window.py       # Main floating pet window
│   ├── interaction_menu.py # Interaction menu and speech bubbles
│   ├── fun_windows.py      # Pet status and treat mini-game
│   ├── setup_window.py     # Pet creation/setup window
│   └── settings_window.py  # Settings dialog
├── core/                   # Game logic
│   ├── pet.py              # Main pet class
│   ├── stats.py            # Stat management (hunger, energy, happiness, cleanliness)
│   ├── mood.py             # Mood calculation system
│   ├── progression.py      # Level and progression system
│   ├── events.py           # Random event system
│   ├── activity_monitor.py # In-app interaction timing
│   └── sound.py            # Sound effects and platform fallback
├── data/                   # Data management
│   ├── save_manager.py     # JSON save/load functionality
│   ├── settings_manager.py # Settings validation and defaults
│   ├── activity_service.py # Optional authenticated activity integration
│   └── startup_manager.py  # Windows startup registration
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Editable install shortcut
└── README.md              # This file
```

Pet artwork is drawn by the UI. Optional WAV sound files can be placed in
`pixelpet/assets/sounds/`; without them, PixelPet uses the platform fallback.

## How the Pet System Works

### Stats

Your pet has four main stats, each ranging from 0-100:

- **Hunger**: Decreases over time. Feed your pet to increase it.
- **Energy**: Decreases over time and with activities. Put your pet to sleep to restore it.
- **Happiness**: Increases with interactions. Decreases if neglected.
- **Cleanliness**: Decreases over time. Clean your pet to maintain it.

While awake, stats decrease gently once every 30 minutes: hunger by 2 points
and the other stats by 1 point. Sleeping pauses decay. PixelPet uses elapsed
wall-clock time while it is running, so decay catches up after the computer
sleeps or the app is suspended. Stats do not decay while the application is
closed.

### Mood

The pet's mood is calculated based on its current stats:
- Low hunger → Hungry
- Low energy → Sleepy
- Low cleanliness → Dirty
- Low happiness → Sad or Angry
- High happiness + high energy → Excited
- Good overall stats → Happy

The pet's drawn expression changes based on its mood.

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

Open the interaction menu and choose **My Pet** to view your stats, XP progress,
care goals, achievements, and unlocked accessories. Choose an owned item under
**Equipped accessory** to show it on your desktop pet; choose **None** to remove
it. Your equipped item is saved with your pet. Choose **Catch Treats** for a
20-second mini-game; each treat caught earns 2 XP, up to 20 XP per round.
Catching at least 8 treats unlocks the Golden Bell accessory once.

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

PixelPet tracks in-app care interactions locally:

**What it does:**
- Records when a care action occurs, for local game logic
- Applies stat decay while the pet is awake and PixelPet is running

**What it does NOT do:**
- Monitor system-wide keyboard or mouse input
- Capture screenshots
- Record keystrokes
- Send pet or settings data to a backend from the desktop application

Pet and settings data are stored locally in JSON files in your user's home
directory (`.pixelpet` folder). Save data does not decay while the application
is closed.

The source also includes an optional `ActivityService` integration that accepts
an authenticated Supabase-compatible client. The desktop application does not
initialize or call this service, and it has no configured backend connection.
Only an external caller that supplies a client and explicitly invokes the
service can send activity records to a backend.

## Settings

Access settings via the system tray menu:

- **Always on Top**: Keep the pet window above other windows
- **Start with Windows**: Launch PixelPet automatically on startup
- **Sound Effects**: Enable/disable sound effects
- **Event Notifications**: Show or hide random-event speech bubbles, reactions, and alert sounds
- **Pet Transparency**: Adjust the pet window's opacity
- **Animation Intensity**: Control animation speed/intensity
- **Backup Save / Restore**: Keep a local recovery point and restore from the latest snapshot
- **Export / Import Save**: Copy your pet save to another location or restore a previous JSON export
- **Reset Pet**: Start fresh with a new pet (with confirmation)

**Start with Windows** registers PixelPet for the current Windows user. This
option is unavailable on other platforms.

PixelPet keeps one timestamped backup per hour for the last 24 hours and one
per day for the preceding 30 days, in addition to the quick-access latest
backup. If the pet save is invalid, PixelPet tries to restore the newest valid
backup automatically. Save failures are reported and logged.

## Tests

Run the unit tests locally with:

```bash
python -m unittest discover -s tests -v
```

The suite covers pet behavior and decay, progression, settings, Windows startup
registration, activity-service validation, and save/import/backup recovery.
GitHub Actions runs it on Windows with Python 3.10, 3.12, and 3.14 for every
push and pull request. The workflow also builds a portable Windows executable.

## Future Improvements

Potential features for future versions:

- [ ] More species and pet variations
- [ ] Additional personalities
- [ ] More cosmetic items and customization
- [ ] Pet-to-pet interactions (multiple pets)
- [ ] Weather and time-of-day effects
- [ ] More complex event chains
- [ ] More character art, icons, and sound assets
- [ ] Expanded accessibility options, including high contrast and reduced motion
- [ ] Multi-pet support
- [ ] Additional platform support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by classic virtual pet games like Tamagotchi
- Built with PySide6/Qt for robust Windows desktop integration
- Designed as a portfolio project demonstrating clean architecture and polished UX

---
