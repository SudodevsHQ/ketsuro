from models.video_model import Video


def upload_summary(yt_url, summary):
    try: 
        video = Video()
        video.yt_url= yt_url
        video.summary = summary
        video.save()
        
    except Exception:
        print('Failed to upload summary')
        
        
    
# def update_summarized_video(yt_url, uploaded_url):
#     try:
#         video = Video()
        