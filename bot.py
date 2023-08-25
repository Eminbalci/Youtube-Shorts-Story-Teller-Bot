from gtts import gTTS
import os
import random
from datetime import datetime
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, vfx, concatenate_videoclips

def duzenle_arkaplan(video):
    if video.aspect_ratio != (9, 16) and video.size[0] > video.size[1]:
        new_width = video.size[1] * 9 // 16
        video = video.crop(x_center=(video.size[0] - new_width) * 7 / 10, width=new_width)
    frame_rate = video.fps
    frame_width, frame_height = video.size
    video_duration = min(59, video.duration)
    return video, frame_rate, frame_width, frame_height, video_duration

def create_video(video_clips, output_folder):
    if not video_clips:
        return

    final_video = concatenate_videoclips(video_clips)

    now = datetime.now()
    output_file_name = now.strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
    output_file = os.path.join(output_folder, output_file_name)
    final_video.write_videofile(output_file, codec="libx265", audio_codec="aac")

    print(f"Video başarıyla oluşturuldu: {output_file}")
    print("Çıktı Dosyasının Yolu:", output_file)

def generate_audio_files(cumleler, output_folder):
    for idx, cumle in enumerate(cumleler):
        ses_file = os.path.join(output_folder, f"ses_{idx + 1}.mp3")  # Sıfırdan başlamıyor
        tts = gTTS(cumle, lang="en")
        tts.save(ses_file)

def delete_audio_files(output_folder, num_files):
    for idx in range(1, num_files + 1):
        ses_file_path = os.path.join(output_folder, f"ses_{idx}.mp3")
        if os.path.exists(ses_file_path):
            os.remove(ses_file_path)

metin = input("Seslendirmek istediğiniz metni girin: ")
cumleler = metin.split(". ")  # Metni cümlelere bölelim

output_folder = r"C:\cikti"
os.makedirs(output_folder, exist_ok=True)

# Ses dosyalarını oluştur
generate_audio_files(cumleler, output_folder)

video_klasoru = r"C:\video"
video_listesi = os.listdir(video_klasoru)

video_clips = []
arkaplan_offset = 0

# Rastgele arkaplan video seçimi
arkaplan_video = VideoFileClip(os.path.join(video_klasoru, random.choice(video_listesi)))
arkaplan_video, frame_rate, frame_width, frame_height, _ = duzenle_arkaplan(arkaplan_video)

for idx, cumle in enumerate(cumleler):
    # Cümlenin süresini hesaplama
    ses_clip = AudioFileClip(os.path.join(output_folder, f"ses_{idx + 1}.mp3"))
    cumle_suresi = ses_clip.duration

    # Videonun süresi 59 saniyeyi geçerse mevcut videoyu tamamlayıp yeni bir video oluştur
    if arkaplan_offset + cumle_suresi > 59:
        create_video(video_clips, output_folder)
        video_clips = []
        arkaplan_offset = 0

        # Rastgele arkaplan video seçimi (yeni bir video başladığında)
        arkaplan_video = VideoFileClip(os.path.join(video_klasoru, random.choice(video_listesi)))
        arkaplan_video, _, _, _, _ = duzenle_arkaplan(arkaplan_video)

    arkaplan_clip = arkaplan_video.subclip(arkaplan_offset, arkaplan_offset + cumle_suresi)
    arkaplan_clip, _, _, _, _ = duzenle_arkaplan(arkaplan_clip)

    video_duration = cumle_suresi

    ses_clip_speedup = ses_clip.set_duration(video_duration)

    txt_clip = TextClip(
        cumle,
        color="white",
        fontsize=30,
        size=(frame_width - 175, None),
        method="caption",
        align="center",
        kerning=0,
        interline=-5,
        bg_color="rgba(0, 0, 0, 0.5)",
    )
    txt_clip = txt_clip.set_duration(video_duration)

    y_position = frame_height // 2 + 100
    txt_clip = txt_clip.set_position(("center", y_position))

    video_with_text = CompositeVideoClip([arkaplan_clip.set_duration(video_duration), txt_clip])
    video_with_audio = video_with_text.set_audio(ses_clip_speedup)

    video_clips.append(video_with_audio)
    arkaplan_offset += cumle_suresi

# Kapatmadan önce son videoyu tamamlayalım
create_video(video_clips, output_folder)

# Tüm videolar oluşturulduktan sonra ses dosyalarını silme
delete_audio_files(output_folder, len(cumleler))
