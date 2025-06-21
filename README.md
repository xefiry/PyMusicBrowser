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
  - [ ] Artist
- Add fields
  - [ ] Song -> Artist
  - [ ] Album -> Artist
  - [ ] Song -> duration
  - [ ] Song -> filesize
- Solve album duplicates
  - [ ] album name case difference -> ignore case
  - [ ] different years in album songs -> keep lowest one

## Scan performance

- Items scanned (on a HDD)
  - song : 6636
  - album : 555
  - genre : 46
- Scan time
  - initial : 12 min 49 sec
  - update : 10 min 47 sec
- Database file size : 1.36MB
