from gtts import gTTS
import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, vfx

# Get text input from the user
text = input("Enter the text you want to voice: ")

# Set the folder for temporary files created by libraries
output_folder = r"C:\output"  # You can specify the video output folder here
os.makedirs(output_folder, exist_ok=True)

# Text-to-speech conversion
audio_file = os.path.join(output_folder, "audio.mp3")
tts = gTTS(text, lang="en")  # Perform English text-to-speech
tts.save(audio_file)

# Select a random video
video_folder = r"C:\videos"
video_list = os.listdir(video_folder)
selected_video = random.choice(video_list)

# Video editing
video = VideoFileClip(os.path.join(video_folder, selected_video))

# If the video is not vertical and not in 16:9 aspect ratio, crop it to 9:16 while keeping the center part
if video.aspect_ratio != (9, 16) and video.size[0] > video.size[1]:
    new_width = video.size[1] * 9 // 16
    video = video.crop(x_center=(video.size[0] - new_width) * 7 / 10, width=new_width)

frame_rate = video.fps
frame_width, frame_height = video.size
video_duration = min(59, video.duration)

# Audio processing
audio_clip = AudioFileClip(audio_file)
if audio_clip.duration > 59:
    audio_speedup_factor = audio_clip.duration / 59
    audio_clip_speedup = audio_clip.fx(vfx.speedx, audio_speedup_factor)
    audio_clip_speedup = audio_clip_speedup.set_duration(59)  # Set audio duration to 60 seconds
else:
    audio_clip_speedup = audio_clip

# Trim and synchronize the audio file
if audio_clip.duration < video_duration:
    video_duration = audio_clip.duration
    video = video.subclip(0, video_duration)

# Formatting the text
txt_clip = TextClip(
    text,
    color="white",
    fontsize=20,
    size=(frame_width - 175, None),
    method="caption",
    align="center",
    kerning=0,
    interline=-5,
    bg_color="rgba(0, 0, 0, 0.5)"
)
txt_clip = txt_clip.set_duration(video_duration)

# Position the text in the middle of the screen
txt_clip = txt_clip.set_position(("center", "center"))

# Combine video and text
video_with_text = CompositeVideoClip([video, txt_clip.set_duration(video_duration)])
video_with_audio = video_with_text.set_audio(audio_clip_speedup)

# Trim the final video to 59 seconds if necessary
if audio_clip.duration > 59:
    video_with_audio = video_with_audio.subclip(0, 59)
else:
    video_with_audio = video_with_audio.subclip(0, audio_clip.duration)

# Save the result
now = datetime.now()
output_file_name = now.strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
output_file = os.path.join(output_folder, output_file_name)
video_with_audio.write_videofile(output_file, codec="libx265", audio_codec="aac")

# Delete the audio file
os.remove(audio_file)

print(f"Video successfully created: {output_file}")
print("Output File Path:", output_file)
