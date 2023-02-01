import cgi
import ntpath
from tkinter import filedialog, messagebox

import filetype
import pyperclip
import requests

from src.app import root_app
from src.common_imports import ttk, ToolTip
from src.component.picture_gallery import PictureGallery
from src.constant import image_file_types
from src.manager.config_manager import default_config_manager, PicRecordManager
from src.manager.gitlab_manager import GitLabManager
from src.root_log import logger
from src.utils.id_utils import get_uuid
from src.utils.paste_utils import get_paste_img_content
from src.utils.task_utils import thread_pool
from src.utils.ttk_image_utils import TTkImageContext, get_image_size, TTkImageCache
from src.widgets.progress_bar import ProgressBar

upload_frame = ttk.Frame(root_app, bootstyle="flatly")

COMMON_PAD_X = 60


def get_select_upload_manager():
    repo_name = repo_opt.get() or ""
    if repo_name.lower() == "gitlab":
        return GitLabManager(default_config_manager.get("gitlab_access_token"),
                             default_config_manager.get("gitlab_project_id"))
    return False


class FileUploadHandler:
    progress_bar = ProgressBar(
        master=upload_frame,
        name="上传进度",
        maximum=200,
        orient=ttk.HORIZONTAL,
        bootstyle="success",
        value=0)
    progress_bar.pack(fill=ttk.X, side=ttk.BOTTOM, pady=(0, 20))
    ToolTip(progress_bar, text="上传进度条", bootstyle=ttk.INFO)

    @classmethod
    def _upload(cls, file_name, file_content):
        manager = get_select_upload_manager()
        if not manager:
            messagebox.showerror("上传错误", "请选择上传账号")
            return
        cls.progress_bar.start_progress()
        try:
            ok, msg = manager.create_file(file_name, file_content)
        except Exception as e:
            logger.error(e)
            return
        logger.info("upload file %s %s, msg %s" % (file_name, ok, msg))
        if ok:
            # 记录文件信息
            TTkImageCache.save_image(msg, file_content)
            file_info = {"name": file_name, "link": msg, "size": get_image_size(file_content)}
            PicRecordManager.add_record(file_info)
            cls.progress_bar.done_progress()
            pyperclip.copy(msg)
            PictureGallery.refresh_images()
            messagebox.showinfo("上传成功", "上传成功，文件地址已复制到剪切板！", parent=upload_frame)
        else:
            cls.progress_bar.stop_progress()
            messagebox.showerror("上传失败", f"上传失败：{msg}", parent=upload_frame)

    @classmethod
    def upload_from_select_file(cls, *_, **__):
        """选择文件上传"""

        def _run():
            file_path = filedialog.askopenfilename(
                filetypes=(('Image files', ["*." + it for it in image_file_types]), ("All Files", "*.*")),
                title="Select")
            cls._upload(ntpath.basename(file_path), open(file_path, "rb").read())

        thread_pool.submit(_run)

    @classmethod
    def upload_from_drag_file(cls, event):
        """文件拖拽上传"""
        file_path: str = event.data
        file_path = file_path.strip("{}")

        def _run():
            cls._upload(ntpath.basename(file_path), open(file_path, "rb").read())

        thread_pool.submit(_run)

    @classmethod
    def upload_from_url(cls):
        url = pyperclip.paste()
        url_var = ttk.StringVar(value=url or "")

        url_input_top = ttk.Toplevel(title="输入URL", resizable=[False, False], transient=root_app)
        url_input_top.grab_set()

        url_label = ttk.Label(url_input_top, bootstyle="info", text="图片URL:")
        url_label.grid(row=0, column=0, padx=(10, 10), pady=20)
        url_entry = ttk.Entry(url_input_top, bootstyle="info", text=url_var)
        url_entry.grid(row=0, column=1, columnspan=3, padx=(0, 10), ipadx=50)

        def click_confirm():
            url_input_top.destroy()
            thread_pool.submit(_run)

        def _run():
            url_str = url_var.get() or ""
            cls.progress_bar.start_progress()
            try:
                resp = requests.get(url_str)
            except Exception as e:
                cls.progress_bar.stop_progress()
                messagebox.showwarning("获取失败", f"获取文件内容失败，错误信息：\n{e}")
                return
            resp_headers = resp.headers
            content_disposition = resp_headers.get("Content-Disposition") or ""
            filename = ""
            if content_disposition:
                _, filename_map = cgi.parse_header(content_disposition)
                filename = filename_map.get("filename")
            if filename:
                cls._upload(filename, resp.content)
                return
            logger.info(f"can't parse filename from Content-Disposition: {content_disposition}")

            content_type = resp_headers.get("Content-Type") or ""
            content_type = content_type.split("/")[-1]
            if not content_type:
                guess_result = filetype.guess(resp.content)
                if guess_result:
                    content_type = guess_result.extension
            if not content_type:
                cls.progress_bar.stop_progress()
                messagebox.showwarning("未知文件类型", f"获取文件类型失败！")
                return
            filename = get_uuid() + "." + content_type
            cls._upload(filename, resp.content)
            return

        url_btn = ttk.Button(url_input_top, text="确定", command=click_confirm, bootstyle="info-outline")
        url_btn.grid(row=1, column=1, columnspan=2, ipadx=20, padx=(40, 0), pady=10)
        url_input_top.place_window_center()

    @classmethod
    def upload_from_clipboard(cls):
        """剪切板上传"""

        def _run():
            ok, data = get_paste_img_content()
            if not ok:
                messagebox.showwarning("剪切板无内容", "剪切板内容为空")
                return
            cls._upload(*data)

        thread_pool.submit(_run)


def get_account_list():
    res = []
    if default_config_manager.get("gitlab_ok"):
        res.append("Gitlab")
    return res


def get_default_account():
    return default_config_manager.get("default_account")


# 选择账号
repo_opt = ttk.Combobox(upload_frame, bootstyle="morph", state="readonly", value=get_account_list(), width=10)
if get_default_account():
    repo_opt.set(get_default_account())
repo_opt.pack(pady=(10, 0))
repo_opt.bind("<<ComboboxSelected>>", lambda _: default_config_manager.set("default_account", repo_opt.get()))

# 点击上传
select_frame = ttk.Frame(upload_frame, ondrop=FileUploadHandler.upload_from_drag_file)
select_frame.bind("<Button-1>", FileUploadHandler.upload_from_select_file)
select_frame.pack(pady=(10, 0), fill=ttk.X, padx=COMMON_PAD_X)

# 上传区域背景图片
bg_label = ttk.Label(select_frame, image=TTkImageContext.get_upload_bg(size=(160, 100)))
bg_label.bind("<Button-1>", FileUploadHandler.upload_from_select_file)
bg_label.pack(pady=(4, 20))
ToolTip(select_frame, text="将图片拖到此处或点击上传", bootstyle=ttk.INFO)

# 剪切板、url上传
btn_frame = ttk.Frame(upload_frame)
btn_frame.pack(pady=(0, 0), padx=100)

clip_btn = ttk.Button(btn_frame, bootstyle="info-outline", text="剪切板",
                      command=FileUploadHandler.upload_from_clipboard)
clip_btn.pack(anchor=ttk.CENTER, side=ttk.LEFT, padx=10, pady=10)
ToolTip(clip_btn, text="上传剪切板复制的图片", bootstyle=ttk.INFO)

url_btn = ttk.Button(btn_frame, bootstyle="info-outline", text="图片URL", command=FileUploadHandler.upload_from_url)
url_btn.pack(anchor=ttk.CENTER, side=ttk.LEFT, padx=10, pady=10)
ToolTip(url_btn, text="上传url地址的图片", bootstyle=ttk.INFO)
