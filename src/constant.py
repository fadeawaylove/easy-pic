import sys
import os
from pathlib import Path

image_file_types = ("bmp", "jpg", "png", "tif", "gif", "pcx", "tga", "exif", "fpx", "svg", "psd", "cdr", "pcd", "dxf",
                    "ufo", "eps", "ai", "raw", "WMF", "webp", "avif", "apng")

# 系统上的用户目录
home_path = Path.home()
# 程序存放文件的目录
documents_path = os.path.join(home_path, ".easy_pic")
os.makedirs(documents_path, exist_ok=True)

# 日志目录
log_path = os.path.join(documents_path, "root.log")

# 程序资源文件目录
resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource")

platform = sys.platform  # win32, linux, cygwin, darwin
