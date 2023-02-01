import os
from PIL import ImageGrab
from typing import Tuple, Union
from io import BytesIO
from src.constant import platform
from src.utils.id_utils import gen_short_id
from src.utils.notice_utils import show_notification


def get_paste_img_content() -> Tuple[bool, Union[Tuple[str, bytes], bool]]:
    if platform == "darwin":
        import pasteboard
        pb = pasteboard.Pasteboard()
        file_paths = pb.get_file_urls()
    elif platform in ("win32", "cygwin"):
        from src.utils.win_clipboard_utils import WinClipboard
        file_paths = WinClipboard.get_file_path_list()
    else:
        msg = f"not supported platform {platform}"
        show_notification(msg, "不支持的系统")
        raise Exception(msg)

    if file_paths:
        file_path = file_paths[0]
        return True, (os.path.basename(file_path), open(file_path, "rb").read())

    if not file_paths:
        img = ImageGrab.grabclipboard()
        if img:
            file_name = os.path.basename(img.filename or gen_short_id())
            content = BytesIO()
            img.save(content, format=img.format or file_name.split(".")[-1])
            content.seek(0)
            return True, (file_name, content.read())
    return False, False


if __name__ == '__main__':
    print(get_paste_img_content())
