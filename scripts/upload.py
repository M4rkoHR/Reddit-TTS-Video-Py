from .createVideo import createVideo
from .createThumbnail import createThumbnail
from youtube_uploader_selenium import YouTubeUploader
import json
from .Google import Create_Service
from googleapiclient.http import MediaFileUpload

def upload_video(videoLengthSecs=603, subreddit="askreddit", submissionSort="month"):
  CLIENT_SECRET_FILE = 'client_secret.json'
  API_NAME = 'youtube'
  API_VERSION = 'v3'
  SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
  error=True
  while error==True:
    try:
      error=False
      ogtitle, author = createVideo(v_length=videoLengthSecs, sub=subreddit, top=submissionSort)
    except:
      error=True
  createThumbnail(ogtitle, author)

  title=f"AskReddit: {ogtitle[:51]}..."
  description=f"""AskReddit {ogtitle}
  Like and Subscribe for more Daily content
  Thanks for watching!
  """
  data={
    "title": title,
    "description": description
  }
  with open('export/video.json', 'w') as outfile:
      json.dump(data, outfile)
  video_path = 'export/video.mp4'
  metadata_path = 'export/video.json'
  uploader = YouTubeUploader(video_path, metadata_path)
  was_video_uploaded, video_id = uploader.upload()
  print(was_video_uploaded)
  print(video_id)

  service.thumbnails().set(
      videoId=video_id,
      media_body=MediaFileUpload('thumbnail.png')
  ).execute()