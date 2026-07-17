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
