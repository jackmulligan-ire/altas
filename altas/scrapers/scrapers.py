import requests
import re
import time
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Video_Scraper():
    def __init__(self, video_id):
        self._video_id = video_id
        self._soup = self._generate_soup()
        self._video_url = self._extract_video_url()
        self._video_title = self._extract_video_title()
        self._video_category = self._extract_video_category()
        self._video_description = self._extract_video_description()
        self._video_hashtags = self._extract_video_hashtags()
        self._video_date = self._extract_video_date()
        self._video_channel = self._extract_video_channel()

    def _generate_soup(self):
        response = requests.get(f"https://www.platform.com/{self._video_id}")
        return BeautifulSoup(response.text, "html.parser")
    
    def _extract_video_url(self):
        tag = self._soup.find("source", attrs={"type": "video/mp4"})
        return tag.attrs['src']
    
    def _extract_video_title(self):
        tag = self._soup.find("h1")
        return tag.text

    def _extract_video_category(self):
        video_detail_table_tag = self._soup.find("table", class_="video-detail-list")
        a_tag = video_detail_table_tag.find("a", class_="spa")
        return a_tag.text

    def _extract_video_description(self):
        tag = self._soup.find("div", class_="full")
        return tag.text

    def _extract_video_hashtags(self):
        hashtag_tags = self._soup.select('a[href*=hashtag]')
        hashtag_list = list(map(lambda tag: tag.text.replace("#", ""), hashtag_tags))
        return ' '.join(hashtag_list)

    def _extract_video_date(self):
        def extract_video_year(date_string):
            year_regex = '(20)(\d{2})'
            year_match = re.search(year_regex, date_string)
            return year_match[0]

        def extract_video_date(date_string):
            date_regex = '(\d{1,2})([a-z]{2})'
            date_match = re.search(date_regex, date_string)
            date_charlist = list(date_match[0])
            if len(date_charlist) == 3: date_charlist.insert(0, "0")
            return "".join(date_charlist[:-2])

        def extract_video_month(date_string):
            SRE_MATCH_TYPE = type(re.match("", ""))
            month_map = {
                "January" : "01",
                "February" : "02",
                "March" : "03",
                "April" : "04",
                "May" : "05",
                "June" : "06",
                "July" : "07",
                "August" : "08",
                "September" : "09",
                "October" : "10",
                "November" : "11",
                "December" : "12"
            }
            for month in month_map.keys():
                month_match = re.search(month, date_string)
                if type(month_match) is SRE_MATCH_TYPE:
                    return month_map[month_match[0]]

        date_tag = self._soup.find('div', class_='video-publish-date')
        date_string = date_tag.text
        video_year = extract_video_year(date_string)
        video_date = extract_video_date(date_string)
        video_month = extract_video_month(date_string)

        return f"{video_year}-{video_month}-{video_date}"

    def _extract_video_channel(self):
        name_tag = self._soup.find('p', class_='name')
        a_tag = name_tag.find('a')
        return a_tag.attrs['href'].split('/')[2]

    def get_video_page_data(self):
        return {
            "id": self._video_id,
            "video_url": self._video_url,
            "title": self._video_title,
            "date": self._video_date,
            "channel": self._video_channel,
            "description": self._video_description,
            "category": self._video_category,
            "hashtags": self._video_hashtags,
        }

class Channel_Scraper():
    def __init__(self, channel_id, days=4500):
        '''
        Days: assumes max possible scrolls of 2 videos posted per day since platform created.

        Each channel takes approx. 10 mins to reach max scroll depth and scrape.
        '''
        self._days = days
        self._soup = self._get_channel_soup(channel_id)
        self._datadict = {}
        self._datadict['video_id'] = self._extract_video_id()
        self._datadict['title'] = self._extract_video_titles()
        self._datadict['date(YYYY-MM-DD)'] = self._extract_video_dates()
        self._datadict['length(H:MM:SS)'] = self._extract_video_lengths()
        self._datadict['views'] = self._extract_video_views()
        self._datadict['channel_name'] = self._extract_channel_name()

    def _get_channel_soup(self, channel_id):
        def create_chrome_options():
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            return chrome_options

        VIDEOS_PER_SCROLL = 25
        num_of_scrolls = math.ceil((self._days/VIDEOS_PER_SCROLL)) - 1
        with(webdriver.Chrome(options=create_chrome_options())) as driver:
            driver.get(f"https://www.platform.com/{channel_id}/")
            for i in range(num_of_scrolls):
                scroll_height = driver.execute_script('return document.body.scrollHeight')
                driver.execute_script(f"window.scrollTo(0, {scroll_height})")
                time.sleep(3)
            
            return BeautifulSoup(driver.page_source, 'html.parser')

    def _extract_video_titles(self):
        video_titles_tags = self._soup.find_all('div', class_='channel-videos-title')
        video_titles_map = map(lambda tag: tag.text.strip(), video_titles_tags)
        return list(video_titles_map)

    def _extract_video_lengths(self):
        video_duration_tags = self._soup.find_all('span', class_='video-duration')
        video_duration_map = map(lambda tag: tag.text, video_duration_tags)
        return list(video_duration_map)

    def _extract_video_dates(self):
        def extract_date_strings(soup):
            container_div = soup.find('div', 'container')
            date_tags = container_div .find_all('div', class_='text-right')
            date_string_map = map(lambda tag: tag.text.strip(), date_tags)
            return list(date_string_map)

        def extract_year_from_strings(string_list):
            year_regex = '(20)(\d{2})'
            year_strings_map = map(lambda string: re.search(year_regex, string)[0], string_list)
            return list(year_strings_map)

        def extract_day_from_strings(string_list):
            day_regex = '(\d{2}),'
            day_strings_map = map(lambda string: re.search(day_regex, string)[0].replace(',',''), string_list)
            return list(day_strings_map)

        def extract_month_from_string(string_list):
            def find_month_match(string):
                SRE_MATCH_TYPE = type(re.match("", ""))
                month_map = {
                    "Jan" : "01",
                    "Feb" : "02",
                    "Mar" : "03",
                    "Apr" : "04",
                    "May" : "05",
                    "Jun" : "06",
                    "Jul" : "07",
                    "Aug" : "08",
                    "Sep" : "09",
                    "Oct" : "10",
                    "Nov" : "11",
                    "Dec" : "12"
                }
                for month in month_map.keys():
                    month_match = re.search(month, string)
                    if type(month_match) is SRE_MATCH_TYPE:
                        return month_map[month_match[0]]

            month_strings_map = map(find_month_match, string_list)
            return list(month_strings_map)

        date_strings = extract_date_strings(self._soup)
        year_strings = extract_year_from_strings(date_strings)
        day_strings = extract_day_from_strings(date_strings)
        month_strings = extract_month_from_string(date_strings)
        date_list = list(zip(year_strings, month_strings, day_strings))
        ISO_string_map = map(lambda date: f"{date[0]}-{date[1]}-{date[2]}", date_list)
        return list(ISO_string_map)

    def _extract_video_id(self):
        def extract_id_from_tag(tag):
            video_href = tag.find('a').attrs['href']
            video_id = video_href.split('/')[2]
            return video_id
    
        image_container_tags = self._soup.find_all('div', 'channel-videos-image-container')
        video_id_map = map(extract_id_from_tag, image_container_tags)
        return list(video_id_map)

    def _extract_video_views(self):
        def eval_string_to_int(views_string):
            if 'K' in views_string:
                if '.' in views_string:
                    views_string = views_string.replace('.', '').replace('K', '00')
                else:
                    views_string = views_string.replace('K', '000')
            elif 'M' in views_string:
                views_string = views_string.replace('.', '').replace('M', '00000')

            return int(views_string)
        
        channel_video_list_tag = self._soup.find('div', class_='channel-videos-list')
        video_views_tags = channel_video_list_tag.find_all('span', class_='video-views')
        video_views_string_map = map(lambda tag: tag.text.strip(), video_views_tags)
        video_views_ints_map = map(eval_string_to_int, video_views_string_map)
        return list(video_views_ints_map)
    
    def _extract_channel_name(self):
        name_tag = self._soup.find('p', class_='name')
        a_tag = name_tag.find('a')
        channel_href = a_tag.attrs['href']
        channel_name = channel_href.split('/')[2]
        channel_name_list = [channel_name for i in range(len(self._datadict['video_id']))]
        return channel_name_list
    
    def get_channel_data(self):
        return self._datadict
            
