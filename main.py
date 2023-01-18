from tkinter import *
from tkinter import messagebox, filedialog

import pyperclip
from PIL import ImageTk, Image
from log import logger
from manager.config_manager import default_config_manager
from manager.gitlab_manager import GitLabManager

root = Tk()

win_width = 800
winHeight = 600
screen_width = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = int((screen_width - win_width) / 2)
y = int((screenHeight - winHeight) / 2)

# 设置主窗口标题
root.title("easy-pic")

# 设置窗口初始位置在屏幕居中
root.geometry("%sx%s+%s+%s" % (win_width, winHeight, x, y))
# 设置窗口图标
# root.iconbitmap("./image/icon.ico")
# 设置窗口宽高固定
root.resizable(0, 0)

root_menu = Menu(root)
root.config(menu=root_menu)


def click_account_gitlab():
    project_id_var = StringVar(value=default_config_manager.get("gitlab_project_id"))
    access_token_var = StringVar(value=default_config_manager.get("gitlab_access_token"))

    def save_gitlab_account():
        project_id = project_id_var.get()
        access_token = access_token_var.get()
        manager = GitLabManager(access_token, project_id)
        ok, msg = manager.projects_access_requests()
        if not ok:
            messagebox.showwarning("Account Error!", f"error msg: {msg}")
            return
        default_config_manager.set("gitlab_project_id", project_id)
        default_config_manager.set("gitlab_access_token", access_token)
        default_config_manager.set("gitlab_ok", True)
        messagebox.showinfo("Account Successful!", f"Set Gitlab Account Success!")
        gitlab_toplevel.destroy()

    gitlab_toplevel = Toplevel(root)
    gitlab_toplevel.title = "gitlab账号设置"
    gitlab_toplevel.geometry("+%d+%d" % (root.winfo_x() + 200, root.winfo_y() + 200))
    gitlab_toplevel.transient(root)

    la1 = Label(gitlab_toplevel, text="Project ID:")
    la1.grid(row=0, column=0, padx=(10, 0), pady=10)
    en1 = Entry(gitlab_toplevel, text=project_id_var)
    en1.grid(row=0, column=1, columnspan=2, padx=(0, 10), ipadx=60)

    la2 = Label(gitlab_toplevel, text='Access Token:')
    la2.grid(row=1, column=0, padx=(10, 0), pady=10)
    en2 = Entry(gitlab_toplevel, text=access_token_var)  # 密码文本框
    en2.grid(row=1, column=1, columnspan=2, padx=(0, 10), ipadx=60)  # 1行1列，跨2列

    but1 = Button(gitlab_toplevel, text="Save", command=save_gitlab_account)
    but1.grid(row=2, column=1, columnspan=1, pady=10, ipadx=30)


setting_menu = Menu(root_menu)
root_menu.add_cascade(label="Account", menu=setting_menu)
setting_menu.add_command(label="Gitlab", command=click_account_gitlab)
setting_menu.add_separator()

# 功能主页
# 图片上传区
upload_frame = LabelFrame(root, borderwidth=1, relief=GROOVE)
upload_frame.pack(fill=X)


def get_account_list():
    res = []
    if default_config_manager.get("gitlab_ok"):
        res.append("Gitlab")
    return res


repo_variable = StringVar(upload_frame)
repo_variable.set(get_account_list()[0])
repo_opt = OptionMenu(upload_frame, repo_variable, *get_account_list())
repo_opt.pack()


def resize_image(w_box, h_box, pil_image):
    s = pil_image.size
    f1 = 1.0 * w_box / s[0]  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / s[1]
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height))


def get_select_upload_manager():
    repo_name = repo_variable.get() or ""
    repo_name = repo_name.lower()
    if repo_name == "gitlab":
        return GitLabManager(default_config_manager.get("gitlab_access_token"),
                             default_config_manager.get("gitlab_project_id"))

    return False, "不存在此上传器"


select_height = 200
select_width = 400


def select_file_upload(*_):
    file_path = filedialog.askopenfilename()
    logger.info(file_path)
    manager = get_select_upload_manager()
    ok, msg = manager.create_file_from_path(file_path)
    if ok:
        pyperclip.copy(msg)
        messagebox.showinfo("上传成功", "上传成功，文件地址已复制到剪切板！")
    else:
        messagebox.showerror("上传失败", f"上传失败：{msg}")


select_frame = Frame(upload_frame,
                     height=select_height,
                     width=select_width,
                     highlightbackground="grey",
                     highlightthickness=1,
                     bd=0)
select_frame.bind("<Button-1>", select_file_upload)
select_frame.pack(pady=10)

upload_image = Image.open("resource/upload_background.png")

w, h = upload_image.size
upload_image = resize_image(70, 70, upload_image)
upload_image = ImageTk.PhotoImage(upload_image)

upload_image_label = Label(select_frame, image=upload_image)
upload_image_label.bind("<Button-1>", select_file_upload)
upload_image_label.pack(pady=(50, 0), padx=80)

upload_text_label = Label(select_frame, text="将文件拖到此处或点击上传")
upload_text_label.bind("<Button-1>", select_file_upload)
upload_text_label.pack(pady=(20, 50), padx=80)

select_path_var = StringVar(upload_frame)

# file_path_entry = Entry(upload_frame, text=select_path_var)
# file_path_entry.grid(row=1, column=2, padx=10, pady=10, ipadx=100)
#
# up_btn1 = Button(upload_frame, text="选择文件上传", command=select_file_upload)
# up_btn1.grid(row=2, column=2, padx=10)

root.mainloop()
