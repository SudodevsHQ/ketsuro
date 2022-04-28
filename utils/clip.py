from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

async def clip_video(video_id: str, regions):
    subclips = []
    orignal = VideoFileClip(os.path.join('videos', f"{video_id}"))
    for region in regions:
        subclip = orignal.subclip(region['start'], region['end']+1)
        subclips.append(subclip)
    concatenate_videoclips(subclips).to_videofile(
                f'clipped/{video_id}.mkv',
                codec="libx264",
                temp_audiofile="clipped/temp.m4a", remove_temp=True, audio_codec="aac")
    orignal.close()
    return True