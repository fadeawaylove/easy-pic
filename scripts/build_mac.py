import os
import pyinstaller_versionfile

VERSION = '0.0.0.2'
VERSION_FILE = "versionfile.txt"

pyinstaller_versionfile.create_versionfile(
    output_file=VERSION_FILE,
    version=VERSION,
    company_name="呆瓜顶呱呱",
    file_description="easy upload images to public network repository.",
    internal_name="EasyPic",
    legal_copyright="© 呆瓜顶呱呱. All rights reserved.",
    original_filename="main.py",
    product_name="EasyPic"
)

install_command = "pip install -r requirements_mac.txt"
pack_command = f"pyinstaller -w -i appico.icns -n EasyPic --version-file=scripts/{VERSION_FILE} main.py --collect-all tkinterDnD --add-data src:src -y"
exec_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.system(f"cd {exec_path} && {install_command} && {pack_command}")

#  pyinstaller -w main.py --additional-hooks-dir ext_hooks --collect-all tkinterDnD --add-data src:src
#  pyinstaller -w main.py --collect-all tkinterDnD --add-data src:src
# os.system("cd ../ && python setup.py py2app ")
