import copy
import io
import urllib.request
import time
from PIL import Image


class TileProvider:
    def __init__(self, url_template, max_zoom, tile_size=256, token=None):
        self.url_template = url_template
        self.max_zoom = max_zoom
        self.tile_size = tile_size
        self.token = token

    def __create_url(self, **kwargs):
        args = copy.deepcopy(kwargs)
        args.update({"token": self.token})
        return self.url_template.format(**args)

    def download_tile(self, **kwargs):
        url = self.__create_url(**kwargs)
        response = urllib.request.urlopen(url)
        img = Image.open(io.BytesIO(response.read()))
        time.sleep(1)
        return img
