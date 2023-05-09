import streamlit as st
import requests
from moviepy.editor import *
from pytube import YouTube
import tempfile
import os
from moviepy.editor import AudioFileClip
import shutil
import yt_dlp as youtube_dl

def download_video(video_url):
    temp_path = tempfile.mktemp()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_path,
        'noplaylist': True,
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        extension = info['ext']

    temp_file_with_ext = f"{temp_path}.{extension}"
    shutil.copy(temp_path, temp_file_with_ext)
    os.remove(temp_path)

    return temp_file_with_ext

def convert_video_to_audio(video_path, audio_format="mp3"):
    audio = AudioFileClip(video_path)
    audio_path = video_path.rsplit(".", 1)[0] + f".{audio_format}"
    codec = "libmp3lame" if audio_format == "mp3" else "pcm_s16le"
    audio.write_audiofile(audio_path, codec=codec)
    return audio_path


st.title('Video-to-Audio Converter')

video_source = st.radio('Select source', ['URL', 'Upload'])

st.write(video_source)

video_url = None
video_upload = None

if video_source == "URL":
    video_url = st.text_input("Enter video URL")
else:
    video_upload = st.file_uploader("Choose a file to upload")

if video_url or video_upload:
    audio_format = st.radio("Choose audio format", ["mp3", "wav"])

    if video_url:
        video_path = download_video(video_url)
    else:
        video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        with open(video_path, "wb") as video_file:
            video_file.write(video_upload.read())

    audio_path = convert_video_to_audio(video_path, audio_format)

    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format=f'audio/{audio_format}')
    
    st.download_button(
     label="Download Audio",
     data=audio_bytes,
     file_name=f"converted_audio.{audio_format}",
    )   

    os.remove(video_path)
    os.remove(audio_path)
