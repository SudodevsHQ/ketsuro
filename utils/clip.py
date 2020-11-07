from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def clip_video(video_id: str, regions):
    subclips = []
    orignal = VideoFileClip(os.path.join('videos', f"{video_id}.mkv"))
    prev_end = 0
    for region in regions:
        subclip = orignal.subclip(region['start'], region['end'])
        subclips.append(subclip)
        prev_end = region['end']
    concatenate_videoclips(subclips).to_videofile(
                f'clipped/{video_id}.mp4',
                codec="h264",
                temp_audiofile="clipped/temp.m4a", remove_temp=True, audio_codec="aac")

    return True