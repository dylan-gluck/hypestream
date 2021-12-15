import os
import urllib.request
import ffmpeg
from TikTokApi import TikTokApi

# Banner
print("""
######################################################
######  HypeStream v0.0.1                       ######
######                       Top Trending Comp  ######
######################################################

""")

# Create API Instance
print("Fetching Top 10 TikTok Videos")
api = TikTokApi.get_instance()

# Get Videos from API
trending = api.by_trending(count=10)

# Loop Over Results, Save in Memory video_ids[]
video_ids = []
for tiktok in trending:
    # Create Path
    video_ids.append(tiktok['id'])
    # Download Video
    print("Downloading Video:" + tiktok['id'])
    file_name = "./tmp/" + tiktok['id'] + ".mp4"
    urllib.request.urlretrieve(tiktok['video']['downloadAddr'], file_name)

# Split Video & Audio
# Add Padding to Video 16:9
# Store in Memory _v[]
print("Processing Videos to 16:9")
_v = []
tmp = []
for _id in video_ids:
    # Format Video to 16:9
    path = "./tmp/" + _id + ".mp4"
    options = {
        'width':'1820',
        'height':'1024',
        'x':'662',
        'y':'0',
        'color': 'Black'
    }
    video = ffmpeg.input(path)
    processed = {
        "v": ffmpeg.filter(video,"pad",**options),
        "a": video.audio
    }
    _v.append(processed)
    tmp.append(path)
    
# Create Concat Video
# No other way to do this and get the audio working
print("Processing Concat Video")
joined = ffmpeg.concat(
    _v[0]['v'], _v[0]['a'], 
    _v[1]['v'], _v[1]['a'], 
    _v[2]['v'], _v[2]['a'], 
    _v[3]['v'], _v[3]['a'],
    _v[4]['v'], _v[4]['a'], 
    _v[5]['v'], _v[5]['a'], 
    _v[6]['v'], _v[6]['a'], 
    _v[7]['v'], _v[7]['a'],
    _v[8]['v'], _v[8]['a'], 
    _v[9]['v'], _v[9]['a'], 
    v=1, a=1
)
out_video = ffmpeg.filter(joined.node[0],'fps', fps=24, round='up')
out_audio = joined.node[1]
out = ffmpeg.output(out_video, out_audio, "./out/tiktok-top-10.mp4")
out.run(quiet=True, overwrite_output=True)

# Remove Temp Files
for path in tmp:
    os.remove(path)

# Done
print("Done. Exiting")
