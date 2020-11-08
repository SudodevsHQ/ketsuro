from models.video_model import Video


async def upload_summary(video_id, summary, punctuatedCaptions, request_id):
    try: 
        video = Video()
        video.video_id= video_id
        video.summary = summary
        video.request_id = request_id
        video.punctuatedCaptions = punctuatedCaptions
        video.save()
        
    except Exception as e:
        print('Failed to upload summary', e)
        
        
    
async def update_summarized_video(video_id, uploaded_url):
    try:
        video = Video.collection.filter('video_id', '==', video_id).get()
        video.summary_video = uploaded_url;
        video.update()
    except Exception:
        print('Failed to upload summarized video url')
        