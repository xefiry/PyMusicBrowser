# Python Music Browser

A music browser/player

## Status

In development

- Database : working
- GUI : draft
- Player : work in progress

## ToDo

- General
  - [ ] Add logging
  - [ ] Add comments
- Database
  - [ ] Create Configuration model to store settings
  - [ ] Create a separate thread for scanning
- Player
  - [x] Add playlist for songs to play
  - [x] Improve next() method
  - [x] Create previous() method
- UI
  - [ ] Show song playing curently : album art, song/album/artist name,  curent/total time
  - [ ] Show playlist
  - [x] Add song progress bar
    - [ ] Make it navigable to seek in the song
  - [ ] Add volume selector
    - [ ] Save volume on exit and restore it on start
  - [x] Add Previous/Next buttons
  - [ ] Add scan button + dialog to ask for directory to scan
  - [ ] Add multimedia key management
  - [ ] Add volume control
- Playlist
  - [ ] Save playlist on exit and restore it on start
  - [ ] Calling previous replays the same song if time position is > N seconds (to define)
