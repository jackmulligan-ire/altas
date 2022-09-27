import requests
import time
import wave
import math
import csv
import os
from moviepy.editor import AudioFileClip
from speech_recognition import AudioFile, Recognizer

import altas

class Transcriber():
    def __init__(self, video_id):
        try:
            self._video_id = video_id
            self._file_url = self._retrieve_file_url()
            self._download_video()
            self._transcript = self._generate_transcript()
        except Exception as e:
            raise e
        finally:
            self._remove_media_files()

    def _retrieve_file_url(self):
        with open(altas.VIDEO_PAGE_DATA_FP, 'r') as video_page_data_file:
            for row in csv.reader(video_page_data_file):
                if row[0] == self._video_id: return row[1]
        
    def _download_video(self):
        video_obj = requests.get(self._file_url)
        with open(f"data/tmp/{self._video_id}.mp4", "wb") as video_file:
            video_file.write(video_obj.content)

    def _generate_transcript(self):
        def generate_audio_file():
            video_file_name = f"data/tmp/{self._video_id}.mp4"
            audioclip = AudioFileClip(video_file_name)
            audioclip.write_audiofile(audio_file_name)

        def get_num_of_queries():
            max_minutes = 10
            with wave.open(audio_file_name, 'r') as audio_file:
                frames = audio_file.getnframes()
                rate = audio_file.getframerate()
                duration = frames / float(rate)
            
            return min(max_minutes, math.ceil(duration/60))

        try:
            audio_file_name = f"data/tmp/{self._video_id}.wav"
            transcript = ""
            r = Recognizer()
            
            generate_audio_file()
            num_of_queries = get_num_of_queries()

            for i in range(num_of_queries):
                with AudioFile(audio_file_name) as source:
                    audio = r.record(source, offset=i*60, duration=60)
                    transcript_segment = r.recognize_google_cloud(audio, language="en-IE")
                    transcript += transcript_segment
                time.sleep(1)
            
            return transcript
        except Exception as e:
            raise Exception(f"{e}")
        
    def _remove_media_files(self):
        exts = ["mp4", "wav"]
        for ext in exts:
            os.remove(f"data/tmp/{self._video_id}.{ext}")

    def get_transcript(self):
        return self._transcript