import webbrowser

import pyperclip
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip

from src.app import root_app
from src.common_imports import ttk
from src.manager.config_manager import PicRecordManager
from src.utils.notice_utils import show_notification
from src.utils.ttk_image_utils import TTkImageContext, TTkImageCache

copy_icon = TTkImageContext.get_copy_icon()
open_net_icon = TTkImageContext.get_open_net()

album_frame = ScrolledFrame(root_app, autohide=True, bootstyle=ttk.SECONDARY, padding=0)


class ImageItem(ttk.Frame):

    def __init__(self, master, pic_info: dict, **kw):
        """
        {"name": file_name, "link": link}
        :param master:
        :param pic_info:
        :param kw:
        """
        super(ImageItem, self).__init__(master, **kw)
        width = kw.get("width", 80)
        height = kw.get("height", 80)
        self.pic_info = pic_info
        pic_link = pic_info["link"]
        pic_name = pic_info["name"]
        pic_width, pic_height = pic_info.get("size", [1920, 1080])

        img = TTkImageCache.get_image_obj(pic_link, size=(width, height))

        def show_big_image():
            show_width = 600
            show_height = 400
            show_top = ttk.Toplevel(title=pic_name, resizable=(False, False), transient=root_app, width=600,
                                    height=400, topmost=True)
            show_top.grab_set()
            show_top.propagate(0)
            show_top.place_window_center()

            w_f = pic_width / show_width
            h_f = pic_height / show_height
            factory = max(w_f, h_f)
            size = (int(pic_width // factory), int(pic_height // factory))
            big_img_lb = ttk.Label(show_top, image=TTkImageCache.get_image_obj(pic_link, size=size))

            if w_f > h_f:
                big_img_lb.pack(anchor=ttk.CENTER, side=ttk.LEFT)
            else:
                big_img_lb.pack(anchor=ttk.CENTER)

        show_btn = ttk.Button(self, image=img, bootstyle="info-link", command=show_big_image)
        ToolTip(show_btn, text="点击查看大图", bootstyle=ttk.LIGHT)
        show_btn.pack()

        action_frame = ttk.Frame(self)
        action_frame.pack(fill=ttk.X)

        def do_copy():
            pyperclip.copy(pic_link)
            show_notification(pic_link, "复制成功", pic_name)

        def do_open_net():
            webbrowser.open(pic_link)

        copy_btn = ttk.Button(action_frame, image=copy_icon, bootstyle="success-link", command=do_copy)
        copy_btn.pack(anchor=ttk.W, side=ttk.LEFT)
        ToolTip(copy_btn, text="点击复制地址", bootstyle=ttk.LIGHT)

        open_net_btn = ttk.Button(action_frame, image=open_net_icon, bootstyle="success-link", command=do_open_net)
        open_net_btn.pack(anchor=ttk.W, side=ttk.LEFT)
        ToolTip(open_net_btn, text="点击浏览器打开图片", bootstyle=ttk.LIGHT)


class PictureGallery:

    @classmethod
    def show_images(cls):
        for one_row in list(zip(*[iter(PicRecordManager.read_records())] * 3)):
            row_frame = ttk.Frame(album_frame)
            row_frame.pack()
            for info in one_row:
                img_item = ImageItem(row_frame, info, width=110, height=110)
                img_item.pack(side=ttk.LEFT)

    @classmethod
    def refresh_images(cls):
        for child in album_frame.winfo_children():
            child.destroy()
        cls.show_images()
