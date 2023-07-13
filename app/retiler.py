import math
import mercantile
from PIL import Image
from .tile_provider import TileProvider


class InvalidInputParamException(Exception):
    """Raised when the input value is invalid"""
    pass


class Retiler:
    def __init__(self, config):
        self.providers = { pr_name: TileProvider(**pr_config) for pr_name, pr_config in config['providers'].items()}

    def __get_provider(self, provider_name):
        if provider_name in self.providers:
            return self.providers[provider_name]
        raise InvalidInputParamException("Error! Invalid provider.")

    def __validate_params(self, provider, resolution, z, x, y):
        if not resolution > 0:
            raise InvalidInputParamException("Error! The resolution parameter must be positive.")
        if not (0 <= z <= provider.max_zoom):
            raise InvalidInputParamException(
                "Error! The z parameter must not be negative and greater than {max_zoom}.".format(
                    max_zoom=provider.max_zoom))
        if not x >= 0:
            raise InvalidInputParamException("Error! The x parameter must not be negative.")
        if not y >= 0:
            raise InvalidInputParamException("Error! The y parameter must not be negative.")
        return

    def retile(self, provider_name, level, resolution, z, x, y):
        result_image = None
        provider = self.__get_provider(provider_name)
        self.__validate_params(provider, resolution, z, x, y)
        if level > 0:
            result_image = self.__zoom_in(provider, level, z, x, y)
        elif level == 0:
            result_image = self.__zoom_not_change(provider, z, x, y)
        else:
            result_image = self.__zoom_out(provider, level, z, x, y)
        result_image = result_image.resize((resolution, resolution))
        return result_image

    def __zoom_in(self, provider, level, z, x, y):
        if z+level > provider.max_zoom:
            raise Exception("Unable to generate tile.")
        tile = mercantile.Tile(x=x, y=y, z=z)
        tile_children = list(mercantile.children(tile, zoom=z + level))
        size = provider.tile_size
        min_x = min([t.x for t in tile_children])
        min_y = min([t.y for t in tile_children])
        max_x = max([t.x for t in tile_children])
        max_y = max([t.y for t in tile_children])
        map_image = Image.new('RGB', (size * (max_x - min_x + 1), size * (max_y - min_y + 1)))
        for t in tile_children:
            img = provider.download_tile(x=t.x, y=t.y, z=t.z)
            map_image.paste(img, box=((t.x - min_x) * size, (t.y - min_y) * size))
        return map_image

    def __zoom_out(self, provider, level, z, x, y):
        if abs(level) > math.log2(provider.tile_size):
            raise Exception("Unable to generate tile.")
        size = provider.tile_size // (2 ** abs(level))
        tile = mercantile.Tile(x=x, y=y, z=z)
        tile_parent = mercantile.parent(tile, zoom=z + level)
        tile_children = list(mercantile.children(tile_parent, zoom=z))
        min_x = min([t.x for t in tile_children])
        min_y = min([t.y for t in tile_children])
        map_image = provider.download_tile(x=tile_parent.x, y=tile_parent.y, z=tile_parent.z)
        map_image = map_image.crop(((tile.x - min_x) * size, (tile.y - min_y) * size,
                                    (tile.x - min_x + 1) * size, (tile.y - min_y + 1) * size))
        return map_image

    def __zoom_not_change(self, provider, z, x, y):
        map_image = provider.download_tile(x=x, y=y, z=z)
        return map_image
