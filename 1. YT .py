import os
import csv
import whisper
import yt_dlp
import multiprocessing
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import torch.multiprocessing as mp
from youtubesearchpython import VideosSearch
import time
import pandas as pd

df = pd.read_csv("u_item.csv", encoding="ISO-8859-1")
movie_titles = df["movie title"].tolist()

CSV_FILE = "movies_sub.csv"


def search_trailer(movie):
    """Searches for the official trailer on YouTube and returns the video ID."""
    try:
        search = VideosSearch(f"{movie} official trailer", limit=1)
        result = search.result()
        if result["result"]:
            return result["result"][0]["id"]
    except Exception as e:
        print(f"Error searching trailer for {movie}: {e}")
    return None


def get_transcript_youtube(video_id):
    """Fetches subtitles from YouTube API."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"Error fetching subtitles for {video_id}: {e}")
        return None


def download_audio(video_id, output_file):
    """Downloads audio from YouTube for Whisper transcription."""
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_file,
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "quiet": True,
            "ffmpeg_location": r"C:\Program Files\ffmpeg\bin",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Audio downloaded for {video_id}")
    except Exception as e:
        print(f"Error downloading audio for {video_id}: {e}")


def read_existing_movies():
    """Reads the existing CSV file and returns a set of completed movies."""
    if not os.path.exists(CSV_FILE):
        return set()
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            return {row[1] for row in csv.reader(f) if row}
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return set()


def write_to_csv(index, movie, transcript):
    """Writes transcript to CSV."""
    try:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([index, movie, transcript])
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def process_movie(index, movie):
    """Processes a movie to extract its transcript."""
    print(f"Processing: {movie}")
    video_id = search_trailer(movie)
    if not video_id:
        write_to_csv(index, movie, "Trailer not found")
        return

    transcript = get_transcript_youtube(video_id)
    if transcript:
        write_to_csv(index, movie, transcript)
        return

    print(f"No subtitles found using YouTube API. Downloading audio for : {movie}")
    if not os.path.exists(f"{index}.mp3.mp3"):
        audio_file = f"{index}.mp3"
        download_audio(video_id, audio_file)
        write_to_csv(index, movie, f"Audio downloaded: {audio_file}")  # Whisper handled separately


def get_trailer_transcripts_parallel(movies, num_workers=4):
    """Parallelized processing of YouTube subtitle extraction and audio downloads."""
    completed_movies = read_existing_movies()
    movies_to_process = [(i, movie) for i, movie in enumerate(movies, start=1) if movie not in completed_movies]

    with multiprocessing.Pool(num_workers) as pool:
        pool.starmap(process_movie, movies_to_process)


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    movies = movie_titles
    get_trailer_transcripts_parallel(movies, num_workers=4)
    print(f"Transcripts saved to {CSV_FILE}")
