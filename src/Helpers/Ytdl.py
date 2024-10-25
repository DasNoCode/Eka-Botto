import os
import re

from pytube import YouTube, cipher
from pytube.innertube import _default_clients

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


class YouTubeDownloader:
    def __init__(self):
        cipher.get_throttling_function_name = self.get_throttling_function_name

    @staticmethod
    def get_throttling_function_name(js: str) -> str:
        """Extract the name of the function that computes the throttling parameter.

        :param str js: The contents of the base.js asset file.
        :rtype: str
        :returns: The name of the function used to compute the throttling parameter.
        """
        function_patterns = [
            r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
            r"\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)",
            r"\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)",
        ]

        for pattern in function_patterns:
            regex = re.compile(pattern)
            match = regex.search(js)
            if match:
                func_name = match.group(1)
                idx = match.group(2)
                if idx:
                    idx = int(idx.strip("[]"))
                    array_match = re.search(
                        rf"var {re.escape(func_name)}\s*=\s*(\[.*?\]);", js
                    )
                    if array_match:
                        array = array_match.group(1).strip("[]").split(",")
                        return array[idx].strip()
                else:
                    return func_name

        raise RegexMatchError(  # type: ignore
            "get_throttling_function_name", "multiple patterns"
        )

    def audio_dl(url: str):
        try:
            url = f"https://youtu.be/{url}"
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream is None:
                raise ValueError("No audio stream found.")
            download_path = audio_stream.download(output_path="downloads")
            return audio_stream.title, download_path, yt.length
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None, None, None

    def video_dl(url: str):
        try:
            url = f"https://youtu.be/{url}"
            yt = YouTube(url)
            video_stream = yt.streams.get_highest_resolution()
            if video_stream is None:
                raise ValueError("No video stream found.")
            download_path = video_stream.download(output_path="downloads")
            return video_stream.title, download_path, yt.length
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None, None, None

    def delete():
        [
            os.remove(os.path.join("downloads", f))
            for f in os.listdir("downloads")
            if os.path.isfile(os.path.join("downloads", f))
        ]
