import os
import tkinter

import tkinterDnD
from ttkbootstrap import utility
from ttkbootstrap.icons import Icon
from ttkbootstrap.style import Style
from ttkbootstrap.window import apply_class_bindings, apply_all_bindings
from src.constant import resource_path


class TTkWindow(tkinter.Tk):

    def __init__(
            self,
            title="ttkbootstrap",
            themename="litera",
            iconphoto='',
            size=None,
            position=None,
            minsize=None,
            maxsize=None,
            resizable=None,
            hdpi=True,
            scaling=None,
            transient=None,
            overrideredirect=False,
            alpha=1.0,
            *args,
            **kwargs
    ):
        if hdpi:
            utility.enable_high_dpi_awareness()

        self.winsys = self.tk.call('tk', 'windowingsystem')

        if scaling is not None:
            utility.enable_high_dpi_awareness(self, scaling)

        if iconphoto is not None:
            if iconphoto == '':
                # the default ttkbootstrap icon
                self._icon = tkinter.PhotoImage(master=self, data=Icon.icon)
                self.iconphoto(True, self._icon)
            else:
                try:
                    # the user provided an image path
                    self._icon = tkinter.PhotoImage(file=iconphoto, master=self)
                    self.iconphoto(True, self._icon)
                except tkinter.TclError:
                    # The fallback icon if the user icon fails.
                    print('iconphoto path is bad; using default image.')
                    self._icon = tkinter.PhotoImage(data=Icon.icon, master=self)
                    self.iconphoto(True, self._icon)

        self.title(title)

        if size is not None:
            width, height = size
            self.geometry(f"{width}x{height}")

        if position is not None:
            xpos, ypos = position
            self.geometry(f"+{xpos}+{ypos}")

        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)

        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)

        if resizable is not None:
            width, height = resizable
            self.resizable(width, height)

        if transient is not None:
            self.transient(transient)

        if overrideredirect:
            self.overrideredirect(1)

        if alpha is not None:
            if self.winsys == 'x11':
                self.wait_visibility(self)
            self.attributes("-alpha", alpha)

        apply_class_bindings(self)
        apply_all_bindings(self)
        self._style = Style(themename)

    @property
    def style(self):
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return self._style

    def place_window_center(self):
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

    position_center = place_window_center  # alias


class TkApp(tkinterDnD.Tk, TTkWindow):

    def __init__(self, title="ttkbootstrap",
                 themename="litera",
                 iconphoto='',
                 size=None,
                 position=None,
                 minsize=None,
                 maxsize=None,
                 resizable=None,
                 hdpi=True,
                 scaling=None,
                 transient=None,
                 overrideredirect=False,
                 alpha=1.0, *args, **kwargs):
        tkinterDnD.Tk.__init__(self, *args, **kwargs)
        TTkWindow.__init__(self, title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi,
                           scaling, transient, overrideredirect, alpha, *args, **kwargs)


root_app = TkApp(title="EasyPic",
                 themename="solar",
                 size=(400, 600),
                 # minsize=(400, 600),
                 # maxsize=(600, 800),
                 resizable=(False, False),
                 iconphoto=os.path.join(resource_path, "icon.png")
                 )
