import csv
import os.path
import pandas as pd
import datetime
from dateutil.parser import isoparse
import sys

import altas
from altas.scrapers.scrapers import Video_Scraper, Channel_Scraper
from altas.transcribers.transcribers import Transcriber

usage_error = "Error. Usage: python -m altas [scrape_video_pages|transcribe_videos|scrape_channel_pages]"

class Main:
    @classmethod
    def main(cls):
        if sys.argv[1] == "scrape_video_pages":
            cls.scrape_video_pages()
            print("Video page scraping completed.")
        elif sys.argv[1] == "transcribe_videos":
            cls.transcribe_videos()
            print("Video transcription completed.")
        elif sys.argv[1] == "scrape_channel_pages":
            cls.scrape_channel_pages()
            print("Channel page scraping completed.")
        else:
            raise SystemExit(usage_error)

    @classmethod
    def scrape_video_pages(cls):        
        def get_video_ids():
            def is_valid_date(date):
                '''
                Checks whether video was published after target date.
                '''
                if isoparse(date) >= isoparse('2010-12-25'): return True
                else: return False

            with open(altas.CHANNEL_DATA_FP, 'r') as channel_data_csv:
                channel_data_reader = csv.reader(channel_data_csv)
                next(channel_data_reader, None) # Header of csv file skipped
                if os.path.exists(altas.VIDEO_PAGE_DATA_FP):
                    with open(altas.VIDEO_PAGE_DATA_FP, 'r') as video_data_csv:
                        video_data_reader = csv.reader(video_data_csv)
                        next(video_data_reader, None)
                        scraped_video_ids = [row[0] for row in video_data_reader if 'http' in row[1]]
                    return [row[0] for row in channel_data_reader if is_valid_date(row[2]) and row[0] not in scraped_video_ids]
                else:
                    return [row[0] for row in channel_data_reader if is_valid_date(row[2])]          

        for video_id in get_video_ids():
            try:    
                scraper = Video_Scraper(video_id)
                video_page_data = scraper.get_video_page_data()
                with open( altas.VIDEO_PAGE_DATA_FP, 'a') as file:
                    fieldnames = video_page_data.keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)

                    if os.path.getsize( altas.VIDEO_PAGE_DATA_FP) == 0:
                        writer.writeheader()

                    writer.writerow(video_page_data)      
            except Exception as e:
                with open('data/logs/scrape-errors.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    if os.path.getsize('data/logs/scrape-videos-errors.csv') == 0:
                        writer.writerow([
                            'timestamp',
                            'error',
                            'video_id',
                        ])
                    writer.writerow([
                        datetime.datetime.now().strftime("%d/%m/20%y %H:%M"),
                        e,
                        video_id
                    ])
            
    @classmethod
    def transcribe_videos(cls):
        def get_video_ids():
            with open(altas.VIDEO_PAGE_DATA_FP, 'r') as page_data_file:
                page_data_reader = csv.reader(page_data_file)
                next(page_data_reader, None)
                page_data_ids = [row[0] for row in page_data_reader]
                if os.path.exists(altas.VIDEO_TRANSCRIPTION_DATA_FP):
                    with open(altas.VIDEO_TRANSCRIPTION_DATA_FP, 'r') as transcription_data_file:
                        transcription_data_reader = csv.reader(transcription_data_file)
                        next(transcription_data_reader, None)
                        transcribed_ids = [row[0] for row in transcription_data_reader]
                        return [video_id for video_id in page_data_ids if video_id not in transcribed_ids]
                else:
                    return page_data_ids

        for video_id in get_video_ids():
            try:
                transcriber = Transcriber(video_id)
                transcript = transcriber.get_transcript()
            except Exception as e:
                transcript = f"Error"
                with open('data/logs/transcribe-errors.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    if os.path.getsize('data/logs/transcribe-errors.csv') == 0:
                        writer.writerow([
                            'timestamp',
                            'error',
                            'video_id',
                        ])
                    writer.writerow([
                        datetime.datetime.now().strftime("%d/%m/20%y %H:%M"),
                        e,
                        video_id
                    ])
            finally:
                with open(altas.VIDEO_TRANSCRIPTION_DATA_FP, 'a') as transcription_data_file:
                    writer = csv.writer(transcription_data_file)
                    if os.path.getsize(altas.VIDEO_TRANSCRIPTION_DATA_FP) == 0:
                        writer.writerow(['id','transcript'])
                    writer.writerow([video_id, transcript])
                
    @classmethod
    def scrape_channel_pages(cls):
        CHANNEL_SAMPLE_FP = 'data/channel-sample.csv'

        def timestamp_channel_sample(channel_id):
            timestamp = datetime.datetime.now().strftime("%d/%m/20%y")
            df = pd.read_csv(CHANNEL_SAMPLE_FP)
            df.loc[df.id == channel_id, "date_scraped"] = timestamp
            df.to_csv(CHANNEL_SAMPLE_FP, index=False)

        def get_channel_ids():
            with open(CHANNEL_SAMPLE_FP, 'r') as channel_sample_file:
                channel_sample_reader = csv.reader(channel_sample_file)
                next(channel_sample_reader, None)
                return [row[0] for row in channel_sample_reader if row[2] == '']
        
        try:
            for channel_id in get_channel_ids():
                channel_scraper = Channel_Scraper(channel_id, days=500)
                channel_data = channel_scraper.get_channel_data()
                with open(altas.CHANNEL_DATA_FP, 'a') as channel_data_file:
                    if os.path.getsize(altas.CHANNEL_DATA_FP) == 0:
                        dict_writer = csv.DictWriter(channel_data_file, fieldnames=channel_data.keys()) 
                        dict_writer.writeheader()
                    channel_videos_list = list(zip(*channel_data.values()))
                    channel_data_writer = csv.writer(channel_data_file)
                    channel_data_writer.writerows(channel_videos_list)
                    timestamp_channel_sample(channel_id)
        except Exception as e:
            with open('data/logs/scrape-channel-errors.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                if os.path.getsize('data/logs/scrape-channel-errors.csv') == 0:
                    writer.writerow([
                        'timestamp',
                        'error',
                        'channel_id',
                    ])
                writer.writerow([
                    datetime.datetime.now().strftime("%d/%m/20%y %H:%M"),
                    e,
                    channel_id 
                ])
    
if __name__ == "__main__":
    try:
        cmd_line_arg = sys.argv[1]
        Main.main()
    except:
        raise SystemExit(usage_error)
    