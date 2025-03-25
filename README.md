# Lunar Lander Game

This repository contains a simple Lunar Lander game I built with Python, PyGame for rendering, and pybox2d (Box2D) for physics simulation.

The Lunar Lander game simulates a spaceship attempting to land safely on a flat surface. You can control the lander’s thrusters to navigate and gently touch down without crashing

## Features
- Realistic physics simulation using Box2D.
- Minimal but functional PyGame rendering.
- Keyboard controls for thrust and rotation.
- Simple collision detection with a static ground.

#### Here is a video of me playing it
![Image](https://github.com/user-attachments/assets/6c84c884-180f-4bf4-b7a0-0152be598f19)

## Requirements:
(Use these versions specfically for the best functionality)
  - Python 3.11
  - Pygame 2.5.2
  - Box2D 2.3.10

## File structure
dt-g7/

├── .idea/               # IDE settings (optional)

├── __pycache__/         # Python cache files (auto-generated)

├── %USERPROFILE%/.pyenv # Local pyenv-win installation directory (ignored in Git)

├── input_handler.py     # Handles keyboard input and applies forces

├── main.py              # Main entry point with game loop

├── physics.py           # Sets up and updates the Box2D world

├── rendering.py         #  PyGame rendering (converting Box2D coords to screen coords)

├── requirements.txt     #  dependencies

└── README.md            


## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Controls

- W: Apply thrust
- A: Rotate counterclockwise
- D: Rotate clockwise

## Objective

Land the spacecraft safely on the ground by controlling its thrust and rotation. Use the thrusters carefully to manage your descent speed and angle. 

## License
This project does not have a license, but message me if you have any questions or intend to use it.
