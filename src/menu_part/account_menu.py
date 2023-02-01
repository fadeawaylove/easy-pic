from tkinter import StringVar, messagebox

from src.app import root_app
from src.common_imports import ttk
from src.manager.config_manager import default_config_manager
from src.manager.gitlab_manager import GitLabManager
from src.root_log import root_logger
from src.utils.task_utils import thread_pool


def click_account_gitlab():
    project_id_var = StringVar(value=default_config_manager.get("gitlab_project_id"))
    access_token_var = StringVar(value=default_config_manager.get("gitlab_access_token"))

    def check_access():
        project_id = project_id_var.get()
        access_token = access_token_var.get()
        manager = GitLabManager(access_token, project_id)
        try:
            return manager.projects_access_requests()
        except Exception as e:
            root_logger.error(e)
            return False, e

    def save_gitlab_account():
        ok, msg = check_access()
        if not ok:
            messagebox.showerror("保存失败", f"gitlab账号保存失败，请检查配置！\n错误信息：{msg}", parent=gitlab_toplevel)
            return
        project_id = project_id_var.get()
        access_token = access_token_var.get()
        default_config_manager.set("gitlab_project_id", project_id)
        default_config_manager.set("gitlab_access_token", access_token)
        default_config_manager.set("gitlab_ok", True)
        messagebox.showinfo("保存成功", "gitlab账号保存成功！", parent=gitlab_toplevel)
        gitlab_toplevel.destroy()

    def check_gitlab_account():
        ok, msg = check_access()
        if ok:
            messagebox.showinfo("检查成功", "gitlab账号检查成功！", parent=gitlab_toplevel)
        else:
            messagebox.showerror("检查失败", f"gitlab账号检查失败，请检查配置！\n错误信息：{msg}", parent=gitlab_toplevel)

    gitlab_toplevel = ttk.Toplevel(title="Gitlab账号设置", resizable=[False, False], transient=root_app)
    gitlab_toplevel.grab_set()

    la1 = ttk.Label(gitlab_toplevel, bootstyle="info", text="项目ID:")
    la1.grid(row=0, column=0, padx=(10, 10), pady=10)
    en1 = ttk.Entry(gitlab_toplevel, bootstyle="info", text=project_id_var)
    en1.grid(row=0, column=1, columnspan=3, padx=(0, 10), ipadx=50)

    la2 = ttk.Label(gitlab_toplevel, bootstyle="info", text='令 牌:')
    la2.grid(row=1, column=0, padx=(10, 10), pady=10)
    en2 = ttk.Entry(gitlab_toplevel, bootstyle="info", text=access_token_var)  # 密码文本框
    en2.grid(row=1, column=1, columnspan=3, padx=(0, 10), ipadx=50)  # 1行1列，跨3列

    check_btn = ttk.Button(gitlab_toplevel, text="检查", bootstyle="info-outline",
                           command=lambda: thread_pool.submit(check_gitlab_account))
    check_btn.grid(row=2, column=1, columnspan=1, pady=10, ipadx=10)

    save_btn = ttk.Button(gitlab_toplevel, text="保存", bootstyle="info-outline",
                          command=lambda: thread_pool.submit(save_gitlab_account))
    save_btn.grid(row=2, column=2, columnspan=1, pady=10, ipadx=10)

    gitlab_toplevel.place_window_center()


account_setting_menu = ttk.Menu(root_app)
account_setting_menu.add_command(label="Gitlab", command=click_account_gitlab)
account_setting_menu.add_separator()
