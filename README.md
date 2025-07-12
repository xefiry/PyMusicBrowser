# Python Music Browser

A music browser/player

## Status

In development

- Database : working
- GUI : work in progress
- Player : working

## How to run

### With uv

- Run `uv run python -m src`

### Without uv

- Install dependencies listed in pyproject.toml
- Run `python -m src`

## ToDo

- General
  - [ ] Add logging
  - [ ] Add comments
  - [ ] Create a thread to scan music at start
- Player
  - [ ] Handle missing files
- UI
  - [x] Manage multimedia keys (Using [pynput](https://github.com/moses-palmer/pynput))
  - [ ] Add scan button + dialog to ask/confirm for directories to scan
    - [x] Store directories to scan in database
  - [ ] Button to add current song album next in queue and play it
  - [ ] Allow selection of multiple items in playlist and to reorder them
  - [ ] Add keyboard shortcuts
  - [ ] Add tray icon
  - [ ] Add mini player
  - [ ] Handle multi CD albums
  - [ ] Show notification on song change if window is not visible
- Playlist
  - [x] Save playlist on exit and restore it on start
  - [ ] Calling previous replays the same song if time position is > N seconds (to define)
- Bugs
  - [ ] Fix behaviour when there are no songs in the database
  - [x] Fix song progress bar : when pressing Stop while paused, cursor should go back to 0
