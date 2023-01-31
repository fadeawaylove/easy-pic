import time
import os
from io import BytesIO
from typing import Tuple, Union

import win32con
from PIL import ImageGrab
from win32clipboard import GetClipboardData, OpenClipboard, CloseClipboard, EmptyClipboard, SetClipboardData, \
    EnumClipboardFormats


def clipboard_context(f):
    def wrapped(*args, **kwargs):
        try:
            OpenClipboard()
            r = f(*args, **kwargs)
        except Exception as e:
            CloseClipboard()
            raise Exception(e)
        finally:
            CloseClipboard()
        return r

    return wrapped


class WinClipboard:

    @classmethod
    @clipboard_context
    def get_clipboard(cls):
        """
            完整 : win32con.CF_TEXT
            CF_TEXT(1):文本格式。 每行以回车/换行符结尾 (CR-LF) 组合。 空字符指示数据的末尾。 将此格式用于 ANSI 文本。
            CF_UNICODETEXT(13):Unicode 文本格式。 每行以回车/换行符结尾 (CR-LF) 组合。 空字符指示数据的末尾。
            CF_BITMAP(2):位图 (HBITMAP) 的句柄。
            CF_HDROP(15):文件地址元组
        """
        formats = []
        last_format = 0
        while True:
            next_format = EnumClipboardFormats(last_format)
            if 0 == next_format:
                break
            else:
                formats.append(next_format)
                last_format = next_format
        if not formats:
            return None
        elif 13 in formats:
            return {'format': "Unicode", 'data': GetClipboardData(13)}
        elif 1 in formats:
            return {'format': "ANSI", 'data': GetClipboardData(1)}
        elif win32con.CF_BITMAP in formats:
            return {'format': "BITMAP", 'data': GetClipboardData(2)}
        elif 15 in formats:
            return {'format': "HDROP", 'data': GetClipboardData(15)}

    @classmethod
    def get_file_path_list(cls):
        result = cls.get_clipboard()
        if result['format'] != 'HDROP':
            return []
        return result['data']

    @classmethod
    @clipboard_context
    def set_clipboard(cls, data: str):
        EmptyClipboard()
        time.sleep(0.1)
        SetClipboardData(win32con.CF_UNICODETEXT, data)


if __name__ == '__main__':
    print(WinClipboard.get_file_path_list())
