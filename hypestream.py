import os
import glob
import random
import urllib.request
import ffmpeg
from TikTokApi import TikTokApi as tt

# Banner
print("""
88888888888888888888888888888888888888888888888888888888888888888888888
88.._|      | `-.  | `.  -_-_ _-_  _-  _- -_ -  .'|   |.'|     |  _..88
88   `-.._  |    |`!  |`.  -_ -__ -_ _- _-_-  .'  |.;'   |   _.!-'|  88
88      | `-!._  |  `;!  ;. _______________ ,'| .-' |   _!.i'     |  88
88..__  |     |`-!._ | `.| |_______________||."'|  _!.;'   |     _|..88
88   |``"..__ |    |`";.| i|_|MMMMMMMMMMM|_|'| _!-|   |   _|..-|'    88
88   |      |``--..|_ | `;!|l|MMoMMMMoMMM|1|.'j   |_..!-'|     |     88
88   |      |    |   |`-,!_|_|MMMMP'YMMMM|_||.!-;'  |    |     |     88
88___|______|____!.,.!,.!,!|d|MMMo * loMM|p|,!,.!.,.!..__|_____|_____88
88      |     |    |  |  | |_|MMMMb,dMMMM|_|| |   |   |    |      |  88
88      |     |    |..!-;'i|r|MPYMoMMMMoM|r| |`-..|   |    |      |  88
88      |    _!.-j'  | _!,"|_|M<>MMMMoMMM|_||!._|  `i-!.._ |      |  88
88     _!.-'|    | _."|  !;|1|MbdMMoMMMMM|l|`.| `-._|    |``-.._  |  88
88..-i'     |  _.''|  !-| !|_|MMMoMMMMoMM|_|.|`-. | ``._ |     |``"..88
88   |      |.|    |.|  !| |u|MoMMMMoMMMM|n||`. |`!   | `".    |     88
88   |  _.-'  |  .'  |.' |/|_|MMMMoMMMMoM|_|! |`!  `,.|    |-._|     88
88  _!"'|     !.'|  .'| .'|[@]MMMMMMMMMMM[@] \|  `. | `._  |   `-._  88
88-'    |   .'   |.|  |/| /                 \|`.  |`!    |.|      |`-88
88      |_.'|   .' | .' |/                   \  \ |  `.  | `._-Lee|  88
88     .'   | .'   |/|  /                     \ |`!   |`.|    `.  |  88
88  _.'     !'|   .' | /                       \|  `  |  `.    |`.|  88
88 HypeStream v0.0.2 88888888888888888888888888888888888888888888888888

HypeStream TikTok Trending Video Bot
by: Dylan Navajas Gluck
-----------------------------------------------------------------------

""")

# Get Series Index
def series_index(filename="index.dat"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 1) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

# Get Values from User
INDEX = str(series_index())
TITLE = "Top Trending TikTok Compilation " + INDEX
FETCH_SIZE = int(input("[!] Number of videos to fetch (1000): ") or "1000")
SELECT_SIZE = int(input("[!] Number of videos to select (50): ") or "50")
VIDEO_TITLE = TITLE + " | HypeStream Comp"
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
out_video = joined.node[0].filter('fps', fps=24, round='up').filter("setsar", sar="1/1")
out_audio = joined.node[1]
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
