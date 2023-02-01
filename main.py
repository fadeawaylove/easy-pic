from src.app import root_app
from src.common_imports import ttk
from src.component.picture_gallery import album_frame, PictureGallery
from src.component.upload_component import upload_frame
from src.menu_part.account_menu import account_setting_menu

# 功能菜单
root_menu = ttk.Menu(root_app)
root_app.config(menu=root_menu)
root_menu.add_cascade(label="账号", menu=account_setting_menu)  # 账号设置

# 上传区
upload_frame.pack(fill=ttk.X)

# 展示区
album_frame.pack(fill=ttk.BOTH, expand=ttk.YES)
PictureGallery.show_images()

if __name__ == '__main__':
    root_app.place_window_center()
    root_app.grab_set()
    root_app.mainloop()
