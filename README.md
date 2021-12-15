![HypeStream Screenshot](screen.jpg)

# HypeStream

Bot that pulls the latest trending videos from TikTok, concatonates into single video & uploads to youtube.

## Usage

Install Dependencies:

```
pip install ffmpeg-python TikTokApi
```

Run Script:

```
python ./hypestream.py
```

## Upcoming Features

- Add youtube API support
  - Create metadata template
- Create multiple videos from sample in batch
  - If user selects 300 top videos and selects 30 per video, create multiple videos in batch.

## Changelog

v0.0.2

- Removed hashtag script, will not work due to TikTok restrictions
- Added interactive prompt
- Can now get dynamic number of videos
- Added dynamic series index

v0.0.1

- Trending script working, able to create single concat video
- Hashtag not working, video url from API is 403 when trying to download
- Youtube API not added yet
