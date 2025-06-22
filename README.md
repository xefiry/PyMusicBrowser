# Python Music Browser

A music browser/player.

## Status

In development

## ToDo

- Add logging to a file
  - [ ] List of directories scanned
  - [ ] Number of files scanned
  - [ ] Timeit result
- Create Models
  - [x] Song
  - [x] Album
  - [x] Genre
  - [x] Artist
  - [ ] Configuration
- Add fields
  - [x] Song -> Artist
  - [x] Album -> Artist
  - [x] Song -> duration
  - [x] Song -> filesize
  - [x] Song -> year
  - [ ] Song -> track_total
  - [ ] Song -> disk
  - [ ] Song -> disk_total
- Solve album duplicates
  - [ ] ~~album name case difference -> ignore case~~
  - [x] different years in album songs -> keep lowest one
- Improve file scanning performance.
  - [x] Get file tags only if not in database or if file modified since last scan
  - [x] Check performances of other mp3 tag libraries

## Scan performance

- Items scanned (on a HDD)
  - song : 6636
  - album : 555
  - genre : 46
- Scan time
  - initial : ~~12 min 49 sec~~ 11.5 s
  - update : ~~10 min 47 sec~~ 2 s
