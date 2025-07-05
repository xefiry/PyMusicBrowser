# Python Music Browser

A music browser/player

## Status

In development

- Database : working
- GUI : work in progress
- Player : working

## ToDo

- General
  - [ ] Add logging
  - [ ] Add comments
  - [ ] Create a thread to scan music at start
- Database
  - [x] Create Configuration model to store settings
- Player
  - [x] Add playlist for songs to play
  - [x] Improve next() method
  - [x] Create previous() method
  - [ ] Handle missing files
- UI
  - [x] Show song playing curently : album art, song/album/artist name, curent/total time
  - [x] Show playlist
  - [x] Add song progress bar
    - [x] Make it navigable to seek in the song
  - [x] Add volume slider
    - [x] Display volume %
    - [x] Increase/Decrease volume with mouse wheel
    - [x] Save volume on exit and restore it on start
  - [x] Add Previous/Next buttons
  - [ ] Add scan button + dialog to ask/confirm for directories to scan
    - [x] Store directories to scan in database
  - [ ] Button to add current song album next in queue and play it
  - [ ] Manage multimedia keys (Using [keyboard](https://pypi.org/project/keyboard/) ?)
- Playlist
  - [x] Save playlist on exit and restore it on start
  - [ ] Calling previous replays the same song if time position is > N seconds (to define)
- Bugs
  - [ ] Fix behaviour when there are no songs in the database
  - [x] Fix song progress bar : when pressing Stop while paused, cursor should go back to 0
