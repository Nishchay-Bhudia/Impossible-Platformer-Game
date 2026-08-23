# Impossible Platformer Game

A 2D side-scrolling platformer written in Python with Pygame. I built it as my Computer
Science coursework between October 2024 and January 2025. The design goal was not to make
a fair game, it was to make one long level that is genuinely irritating to finish.

## What it does

You sign in, press a key on the title screen, then run right across a single level while
fire, spinning saws, spikes and a spike head try to kill you. Touching any trap sends you
straight back to the last checkpoint you walked past. There are three checkpoints spread
across roughly 7000 pixels of level, so the gaps between them are long enough to hurt.

- Double jump, tracked with a jump counter so you cannot chain a third one
- Trampolines that launch you higher than a normal jump reaches
- Username and password sign up or log in, stored in a `users.csv` next to the script
- Pause menu with resume, respawn at checkpoint, and restart
- Sprite animation for idle, run, jump, double jump, fall and hit states
- Background music plus sound effects for starting, dying and reaching a checkpoint

## Controls

| Key | Action |
|-----|--------|
| Left / Right arrow | Walk |
| Up arrow | Jump. Press it again in mid-air for the double jump |
| Escape | Pause menu |
| Up / Down then Enter | Move through the pause menu and pick an option |

On the first screen press `1` to sign up or `2` to log in, type a username and press Enter,
then type a password and press Enter. After that any key starts the level.

## How it works

It is one file, about 870 lines, structured around a `pygame.sprite.Sprite` subclass per
kind of object. The parts I think are worth pointing at:

Collision uses pixel masks rather than rectangles. Spikes and saws are mostly transparent
inside their bounding box, so a rectangle test would kill you for standing near a spike
instead of on one. `pygame.sprite.collide_mask` compares the actual opaque pixels.

Horizontal collision is a look-ahead. The player is moved two velocities forward, tested,
then moved back before anything is drawn, so a wall is detected before you are ever inside
it. That avoids the classic bug where you clip into a block and get stuck.

The camera never moves the world. Every object draws itself at `rect.x - offset_x`, and
`offset_x` only changes when the player crosses into a 200 pixel margin at either edge of
the window. Level layout is hand-placed coordinate lists near the top of `main()`, which is
tedious to edit but meant I did not have to write a level file format.

## Running it

You need Python 3 and Pygame.

```bash
pip install pygame
python "Impossible Platformer Game.py"
```

Note the quotes, the filename has spaces in it. An earlier version of this README said
`main.py`, which was never the name of anything here.

## Current state

The game is finished as coursework and I am not actively working on it. Things a reader
should know before cloning:

- The `assets` folder is not in this repository. The script loads sounds and sprite sheets
  from `assets/` at import time, so a fresh clone crashes on the first line that touches
  Pygame's mixer. You need the sprite and sound files in place for it to start at all.
- Passwords are written to `users.csv` in plain text. Sign up accepts anything and does not
  check for an existing username. A failed login just drops you back to the menu with no
  message. This was in scope for the coursework, it is not a security model.
- There is no win condition. Past the last checkpoint the level simply runs out of blocks.
- The player has a `health` attribute set to 100 that nothing ever decrements. Trap contact
  is instant death, so the health system is effectively dead code.
- The second block trap (`blk2`) is solid but is not in the list of names that trigger a
  hit, so it blocks you rather than killing you.
- "Reset Game" in the pause menu moves you back to the start but does not clear the
  checkpoint you already reached, so your next death still sends you forward again.

## Tech

Python 3 and Pygame, no other dependencies. Sprite and sound assets came from itch.io
asset packs and the freeCodeCamp Pygame platformer material. MIT licensed, see LICENSE.
