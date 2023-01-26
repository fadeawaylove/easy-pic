import hashlib
import os
import requests
from io import BytesIO
from PIL import ImageTk, Image

from src.constant import home_path, resource_path
from src.root_log import root_logger


def get_image_size(content: bytes) -> tuple:
    return Image.open(BytesIO(content)).size


class TTkImageContext:
    image_map = set()

    path_upload_bg = os.path.join(resource_path, "upload_background.png")
    image_damage = os.path.join(resource_path, "image_damage.jpeg")
    copy_icon = os.path.join(resource_path, "copy_icon.png")
    open_net = os.path.join(resource_path, "open_net.png")

    @classmethod
    def get_image(cls, path: str, size=(100, 100)):
        if size:
            img = ImageTk.PhotoImage(Image.open(path).resize(size))
        else:
            img = ImageTk.PhotoImage(Image.open(path))
        cls.image_map.add(img)
        return img

    @classmethod
    def get_upload_bg(cls, size=(100, 100)):
        return cls.get_image(cls.path_upload_bg, size)

    @classmethod
    def get_damage_image(cls, size=(100, 100)):
        return cls.get_image(cls.image_damage, size)

    @classmethod
    def get_copy_icon(cls, size=(18, 20)):
        return cls.get_image(cls.copy_icon, size)

    @classmethod
    def get_open_net(cls, size=(18, 18)):
        return cls.get_image(cls.open_net, size)


class TTkImageCache:
    image_map = set()

    cache_path = os.path.join(home_path, ".easy_pic/cache/")
    os.makedirs(cache_path, exist_ok=True)

    @classmethod
    def _get_cache_path(cls, url: str):
        md = hashlib.md5(url.encode())
        md5_val = md.hexdigest()
        return os.path.join(cls.cache_path, md5_val)

    @classmethod
    def save_image(cls, url: str, content: bytes = None) -> str:
        cache_path = cls._get_cache_path(url)
        if not content:
            content = requests.get(url).content
        open(cache_path, "wb").write(content)
        return cache_path

    @classmethod
    def get_image(cls, url: str) -> bytes:
        try:
            cache_path = cls._get_cache_path(url)
            if os.path.exists(cache_path):
                return open(cache_path, "rb").read()
            else:
                res = requests.get(url).content
                open(cache_path, "wb").write(res)
                return res

        except Exception as e:
            root_logger.warning(e)
        return b""

    @classmethod
    def get_image_obj(cls, url: str, size=(100, 100)) -> Image:
        res = cls.get_image(url)
        if res:
            img = TTkImageContext.get_image(cls._get_cache_path(url), size=size)
            # img = ImageTk.PhotoImage(Image.open(cls._get_cache_path(url)).resize(size))
            cls.image_map.add(img)
            return img
        root_logger.warning(f"pic url {url}")
        return TTkImageContext.get_damage_image(size=size)


if __name__ == '__main__':
    # print(TTkImageCache.get_image_obj("https://gitlab.com/api/v4/projects/42641795/repository/files/tmpbiinyzh6.jpg/raw"))
    TTkImageContext.get_upload_bg()
    pass
