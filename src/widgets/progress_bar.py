import time
from src.common_imports import ttk
from src.utils.task_utils import thread_pool


class ProgressBar(ttk.Progressbar):
    Init = 0
    Start = 1
    Stop = 2
    Done = 3
    Cancel = 4

    def __init__(self, master=None, interval=0.01, maximum=200, **kw):
        self.value = ttk.IntVar(master, value=0)  # 进度条的进度
        super(ProgressBar, self).__init__(master, maximum=maximum, variable=self.value, **kw)
        self.status = ttk.IntVar(master, value=self.Init)  # 0-初始状态 1-进行中 2-停止 3-完成 4-取消？
        self.interval = interval
        self.maximum = maximum

    def _real_run(self):

        while True:
            flag = self.status.get()
            if flag == self.Start:
                upload_process_var_int = self.value.get()
                step = 0
                if upload_process_var_int < 100:
                    step = 10
                if upload_process_var_int < 150:
                    step = 5
                if upload_process_var_int < 180:
                    step = 1
                self.step(step)
                time.sleep(self.interval)
            if flag == self.Stop:
                self.stop()
                self.value.set(0)
                return
            if flag == self.Done:
                self.stop()
                self.value.set(self.maximum)
                return
            if flag == self.Cancel:
                self.stop()
                return

    def start_progress(self):
        if self.status.get() == self.Start:  # 进度条进行中
            return
        self.value.set(0)
        self.status.set(self.Start)
        thread_pool.submit(self._real_run)

    def stop_progress(self):
        self.status.set(self.Stop)

    def done_progress(self):
        self.status.set(self.Done)

    def cancel_progress(self):
        self.status.set(self.Cancel)
