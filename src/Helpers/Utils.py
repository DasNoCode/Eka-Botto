import os
import random
import base64
import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip
import tempfile
import shutil
import re
import asyncio


class Utils:

    @staticmethod
    def sleep(ms):
        asyncio.sleep(ms / 1000.0)

    @staticmethod
    def fetch(url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def fetch_buffer(url):
        response = requests.get(url, stream=True)
        return response.content

    @staticmethod
    def is_truthy(value):
        return value is not None and value is not False

    @staticmethod
    def readdir_recursive(directory):
        results = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                results.append(os.path.join(root, file))

        return results

    @staticmethod
    def buffer_to_base64(buffer):
        return base64.b64encode(buffer).decode('utf-8')

    @staticmethod
    def webp_to_mp4(webp):
        def request(form, file=None):
            url = f'https://ezgif.com/webp-to-mp4/{file}' if file else 'https://ezgif.com/webp-to-mp4'
            response = requests.post(url, files=form)
            return BeautifulSoup(response.text, 'html.parser')

        files = {'new-image': ('bold.webp', webp, 'image/webp')}
        soup1 = request(files)
        file = soup1.find('input', {'name': 'file'})['value']
        files = {'file': (file, 'image/webp'),
                 'convert': 'Convert WebP to MP4!'}
        soup2 = request(files, file)
        video_url = 'https:' + \
            soup2.find('div', {'id': 'output'}).find(
                'video').find('source')['src']
        return requests.get(video_url).content

    @staticmethod
    def extract_numbers(content):
        numbers = re.findall(r'-?\d+', content)
        return [max(int(n), 0) for n in numbers]

    @staticmethod
    def get_random_int(min, max):
        return random.randint(min, max)

    @staticmethod
    def get_random_float(min, max):
        return random.uniform(min, max)

    @staticmethod
    def get_random_item(array):
        return random.choice(array)

    @staticmethod
    def get_random_items(array, count):
        return [Utils.get_random_item(array) for _ in range(count)]

    @staticmethod
    def get_urls(text):
        return set(re.findall(r'https?://[^\s]+', text))

    @staticmethod
    def gif_to_mp4(gif):
        temp_dir = tempfile.mkdtemp()
        gif_path = os.path.join(temp_dir, 'temp.gif')
        mp4_path = os.path.join(temp_dir, 'temp.mp4')

        with open(gif_path, 'wb') as f:
            f.write(gif)

        clip = VideoFileClip(gif_path)
        clip.write_videofile(mp4_path, codec='libx264')

        with open(mp4_path, 'rb') as f:
            buffer = f.read()

        shutil.rmtree(temp_dir)
        return buffer

    @staticmethod
    def capitalize(s):
        return s[0].upper() + s[1:]
