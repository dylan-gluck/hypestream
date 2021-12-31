import os
import glob
import random
import urllib.request
import ffmpeg
from TikTokApi import TikTokApi as tt

# Banner
print("""
  |\/\/\/\/\/|
  |          |
  |          |
  |          |
  |    __  __|
  |   /  \/  \ 
  |  (o   )o  )
 /c   \__/ --.
 \_   ,     -'
  |  '\_______)
  |      _)
  |     |
 /`-----'\  Hypestream v0.0.3 
/         \ TikTok Top Trending Video Bot
-----------------------------------------------------------------------
""")

# Get Series Index
def series_index(filename="index.dat"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

# Get Values from User
INDEX = str(series_index())
FETCH_SIZE = int(input("[!] Number of videos to fetch (1000): ") or "1000")
SELECT_SIZE = int(input("[!] Number of videos to select (25): ") or "25")
VIDEO_TITLE = "Top Trending TikTok Mashup " + INDEX + " | HypeStream Comp"
VIDEO_FILE = "./out/tiktok-trending-videos-" + INDEX + ".mp4"

print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[+] Youtube Title: """ + VIDEO_TITLE + """
[+] Videos to Get: """ + str(FETCH_SIZE) + """
[+] Videos to Use: """ + str(SELECT_SIZE) + """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")

# Create API Instance
print("-> Fetching Videos from API ...")
api = tt.get_instance()
# Get (FETCH_SIZE) Videos from API
trending = api.by_trending(count=FETCH_SIZE)
# Select Random (SELECT_SIZE)
print("-> Downloading Random " + str(SELECT_SIZE) + " TikToks ...")
random.shuffle(trending)

# Loop Over Results, Save in Memory video_ids[]
video_ids = []
for tiktok in trending[0:SELECT_SIZE]:
    # Create Path
    video_ids.append(tiktok['id'])
    # Download Video
    # print("Downloading Video:" + tiktok['id'])
    file_name = "./tmp/" + tiktok['id'] + ".mp4"
    urllib.request.urlretrieve(tiktok['video']['downloadAddr'], file_name)

# Split Video & Audio
# Add Padding to Video 16:9
# Store in Memory _v[]
print("-> Splitting Video and Audio ...")
_v = []
for _id in video_ids:
    # Format Video to 16:9
    path = "./tmp/" + _id + ".mp4"
    options = {
        'width': '1920',
        'height': '1080',
        'x': '(ow-iw)/2',
        'y': '(oh-ih)/2',
        'color': 'Black'
    }
    video = ffmpeg.input(path)
    _v.append(
        video["v"]
        .filter("scale", w="-1", h="1080")
        .filter("pad",**options)
        .filter("setsar", sar="1/1")
    )
    _v.append(video["a"])
    
# Create Concat Video
print("-> Processing Concat Video ...")
joined = ffmpeg.concat(*_v, v=1, a=1)
# Filter video and audio separately and then combine
out_video = joined.node[0].filter('setpts', '0.5*PTS').filter('fps', fps=24, round='up').filter("setsar", sar="1/1")
out_audio = joined.node[1].filter('atempo', '2.0')
out = ffmpeg.output(out_video, out_audio, VIDEO_FILE)
out.run(quiet=True, overwrite_output=True)

# Remove Temp Files
tmp = glob.glob('./tmp/*.mp4')
for path in tmp:
    os.remove(path)

# Done
print("""
-----------------------------------------------------------------------
New Video Created at: """ + VIDEO_FILE + """

Done! Exiting...
""")
