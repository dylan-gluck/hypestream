import os
import urllib.request
import ffmpeg
from TikTokApi import TikTokApi

# Banner
print("""
######################################################
######  HypeStream v0.0.1                       ######
######                            Hashtag Comp  ######
######################################################

""")
hashtag = input("Enter Hashtag: ")

# Create API Instance
print("Fetching Top 10 TikTok Videos with Hashtag: " + hashtag)
api = TikTokApi.get_instance()

# Get Videos from API
trending = api.by_hashtag(hashtag, count=10)

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
print("Processing Videos to 16:9")
videos = []
tmp_files = []
for _id in video_ids:
    # Format Video to 16:9
    path = "./tmp/" + _id + ".mp4"
    PAD_OPTIONS = {
        'width':'1820',
        'height':'1024',
        'x':'662',
        'y':'0',
        'color': 'Black'
    }
    video = ffmpeg.input(path)
    processed = {
        "video": ffmpeg.filter(video,"pad",**PAD_OPTIONS),
        "audio": video.audio
    }
    videos.append(processed)
    tmp_files.append(path)
    
# Create Concat Video
print("Processing Concat Video")
joined = ffmpeg.concat(
    videos[0]['video'], videos[0]['audio'], 
    videos[1]['video'], videos[1]['audio'], 
    videos[2]['video'], videos[2]['audio'], 
    videos[3]['video'], videos[3]['audio'],
    videos[4]['video'], videos[4]['audio'], 
    videos[5]['video'], videos[5]['audio'], 
    videos[6]['video'], videos[6]['audio'], 
    videos[7]['video'], videos[7]['audio'],
    videos[8]['video'], videos[8]['audio'], 
    videos[9]['video'], videos[9]['audio'], 
    v=1, a=1
)
out_video = ffmpeg.filter(joined.node[0],'fps', fps=24, round='up')
out_audio = joined.node[1]
out = ffmpeg.output(out_video, out_audio, "./out/tiktok-top-10-" + hashtag + ".mp4")
out.run()

# Remove Temp Files
for path in tmp_files:
    os.remove(path)


