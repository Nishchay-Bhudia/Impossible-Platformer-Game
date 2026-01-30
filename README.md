# Impossible Platformer Game 🎮

A challenging 2D platformer game built with Python and Pygame featuring traps, checkpoints, and smooth animations.

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Controls](#game-controls)
- [Game Mechanics](#game-mechanics)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## About

Impossible Platformer Game is a challenging 2D side-scrolling platformer where players navigate through obstacle-filled levels with various traps including fires, saws, spikes, and more. The game features a checkpoint system, authentication, and smooth character animations.

**Course Work Project**  
**Developer:** Nishchay Bhudia  
**Development Period:** 08/10/2024 - 21/01/2025  
**Subject:** Computer Science

## ✨ Features

- **User Authentication System** - Sign up and login functionality with CSV-based storage
- **Checkpoint System** - Save progress at strategic points throughout the level
- **Multiple Trap Types**:
  - 🔥 Fire traps
  - ⚙️ Rotating saws
  - 🔺 Spikes
  - 🧱 Block obstacles
  - 🎪 Trampolines for enhanced jumps
- **Smooth Animations** - Fluid character movements including running, jumping, double-jumping, and falling
- **Sound Effects** - Background music and sound effects for deaths, checkpoints, and game start
- **Pause Menu** - Press ESC to pause and access game options
- **Scrolling Background** - Dynamic camera that follows the player
- **Respawn System** - Automatic respawn at the last activated checkpoint

## Installation

### Prerequisites
- Python 3.x
- Pygame library

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/impossible-platformer.git
cd impossible-platformer
```

2. **Install required dependencies**
```bash
pip install pygame
```


3. **Run the game**
```bash
python main.py
```

## 🎮 How to Play

1. **Launch the game** - Run the Python script
2. **Start Screen** - Press any key to start the game
3. **Navigate** - Use arrow keys to move and jump
4. **Survive** - Avoid traps and reach checkpoints
5. **Pause** - Press ESC to access the pause menu

## 🕹️ Game Controls

| Key | Action |
|-----|--------|
| ← (Left Arrow) | Move Left |
| → (Right Arrow) | Move Right |
| ↑ (Up Arrow) | Jump / Double Jump |
| ESC | Pause Menu |

### Pause Menu Options
- **Resume** - Continue playing
- **Reset Character** - Respawn at last checkpoint
- **Reset Game** - Restart from the beginning

## 🎲 Game Mechanics

### Movement
- **Horizontal Movement**: 5 pixels per frame
- **Jump**: Press UP arrow (up to 2 jumps - double jump enabled)
- **Gravity**: Dynamic falling speed that increases over time

### Obstacles
- **Fire Traps** - Animated fire that damages on contact
- **Saw Blades** - Rotating saws that kill instantly
- **Spikes** - Ground-based hazards
- **Block Obstacles** - Solid barriers and hazards
- **Trampolines** - Launch the player high into the air

### Checkpoints
- Activate checkpoints by touching the checkpoint flag
- Respawn at the last activated checkpoint when you die
- Visual and audio feedback when checkpoint is activated
- Multiple checkpoints throughout the level

### Health System
- Player starts with 100 health
- Contact with traps triggers respawn
- Respawn at last checkpoint or default starting position


## 🛠️ Development

### Key Classes

- **Player**: Main character with movement, jumping, and animation
- **Object**: Base class for all game objects
- **Block**: Platform and ground blocks
- **Fire**: Animated fire trap
- **Saw**: Rotating saw blade trap
- **Spike**: Static spike trap
- **Blk/Blk2**: Block-based obstacles
- **Trampoline**: Bouncing platform
- **Checkpoint**: Save point system

### Technical Details

- **Resolution**: 1000x800 pixels
- **Frame Rate**: 60 FPS
- **Physics**: Custom gravity and collision detection
- **Animation System**: Sprite sheet-based with configurable delays
- **Camera**: Horizontal scrolling with configurable scroll zones

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

### Ideas for Contributions
- Add more levels
- Implement a level editor
- Add power-ups
- Create a scoring system
- Add more trap types
- Improve UI/UX
- Add multiplayer support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Nishchay Bhudia**

- Course Work Project - Computer Science
- Development Period: October 2024 - January 2025

## 🙏 Acknowledgments

- Pygame community for excellent documentation
- Asset creators (ensure you credit your asset sources here)
- Computer Science course instructors
- **Itch.io** for Sprite Assets
- **freeCodeCamp.org** for Sprite Assets

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the developer.

---

**Note**: This is a coursework project developed as part of a Computer Science program. The game demonstrates concepts including object-oriented programming, game physics, collision detection, and user authentication.

⭐ Star this repository if you found it helpful!
