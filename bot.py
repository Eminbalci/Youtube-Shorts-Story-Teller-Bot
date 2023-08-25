from gtts import gTTS
import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, vfx, concatenate_videoclips

# Get text input from the user
text = input("Enter the text to narrate: ")
sentences = text.split(". ")  # Split the text into sentences

# Define the output folder for temporary files created by libraries
output_folder = r"C:\output"  # You can specify the video output folder here
os.makedirs(output_folder, exist_ok=True)

# Select a random video
video_folder = r"C:\videos"
video_list = os.listdir(video_folder)
selected_video = random.choice(video_list)
background_video = VideoFileClip(os.path.join(video_folder, selected_video))

# Code used to edit the background video
def edit_background(video):
    if video.aspect_ratio != (9, 16) and video.size[0] > video.size[1]:
        new_width = video.size[1] * 9 // 16
        video = video.crop(x_center=(video.size[0] - new_width) * 7 / 10, width=new_width)
    frame_rate = video.fps
    frame_width, frame_height = video.size
    video_duration = min(59, video.duration)
    return video, frame_rate, frame_width, frame_height, video_duration

background_video, frame_rate, frame_width, frame_height, background_duration = edit_background(background_video)

# Processing for each sentence
video_clips = []
background_offset = 0

for idx, sentence in enumerate(sentences):
    # Generate speech for the sentence
    audio_file = os.path.join(output_folder, f"audio_{idx}.mp3")
    tts = gTTS(sentence, lang="en")  # English text-to-speech
    tts.save(audio_file)

    # Calculate sentence duration
    audio_clip = AudioFileClip(audio_file)
    sentence_duration = audio_clip.duration

    # Edit the video
    background_clip = background_video.subclip(background_offset, background_offset + sentence_duration)
    background_clip, _, _, _, _ = edit_background(background_clip)

    video_duration = sentence_duration

    # Trim and adjust the audio file
    sped_up_audio_clip = audio_clip.fx(vfx.speedx, video_duration / sentence_duration)
    sped_up_audio_clip = sped_up_audio_clip.set_duration(video_duration)

    # Format the sentence as text overlay
    text_clip = TextClip(
        sentence,
        color="white",
        fontsize=20,
        size=(frame_width - 175, None),
        method="caption",
        align="center",
        kerning=0,
        interline=-5,
        bg_color="rgba(0, 0, 0, 0.5)"
    )
    text_clip = text_clip.set_duration(video_duration)

    # Position the text in the center of the screen
    text_clip = text_clip.set_position(("center", "center"))

    # Combine video and text
    video_with_text = CompositeVideoClip([background_clip.set_duration(video_duration), text_clip])
    video_with_audio = video_with_text.set_audio(sped_up_audio_clip)

    video_clips.append(video_with_audio)
    background_offset += sentence_duration  # Update the starting point of the background

# Concatenate all video clips
final_video = concatenate_videoclips(video_clips)

# Save the result
now = datetime.now()
output_file_name = now.strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
output_file = os.path.join(output_folder, output_file_name)
final_video.write_videofile(output_file, codec="libx265", audio_codec="aac")

# Delete unused audio files
for idx in range(len(sentences)):
    os.remove(os.path.join(output_folder, f"audio_{idx}.mp3"))

print(f"Video successfully created: {output_file}")
print("Output File Path:", output_file)
