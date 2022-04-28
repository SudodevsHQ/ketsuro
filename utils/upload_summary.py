from models.video_model import Video


async def upload_summary(video_id, summary, request_id):
    try: 
        video = Video()
        video.video_id= video_id
        video.summary = summary
        video.request_id = request_id
        video.save()
        
    except Exception:
        print('Failed to upload summary')
        
        
    
async def update_summarized_video(video_id, uploaded_url):
    try:
        video = Video.collection.filter('video_id', '==', video_id).get()
        video.summary_video = uploaded_url;
        video.update()
    except Exception:
        print('Failed to upload summarized video url')
        