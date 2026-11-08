# Python Music Browser

A music browser/player

## TODO

- FIXME program crashes on start if the library exists but has no songs
- check the source of "qt.gui.imageio: libpng warning: iCCP: profile 'icm': 1000000h: invalid rendering intent"
- add all shortcuts as a menu item
- make keyboard shortcuts customizable
- clicking on top element from navigation (Album artist, Song artist, Genre, Year) expands all items in browser. Check why.

## Status

In development

- Database : working
- GUI : work in progress
- Player : working

## How to run

This project uses [uv](https://docs.astral.sh/uv/).

Run with `uv run pymusicbrowser`

## Shortcut list

global shortcut = shortcut active even if the window is not active

| Action                        | Shortcut                         | Global shortcut  |
| ----------------------------- | -------------------------------- | ---------------- |
| Play/Pause                    | Space                            | Media play/pause |
| Previous song                 | <                                | Media previous   |
| Next song                     | >                                | Media next       |
| Stop                          | ctrl + s                         | Media stop       |
| Queue song/album and play it  | Enter or Double click in browser |                  |
| Queue selected songs/albums   | ctrl + q                         |                  |
| Focus playing song in browser | ctrl + l                         |                  |
| Focus search bar              | ctrl + f                         |                  |
| Minimize to tray              | ctrl + m                         |                  |
