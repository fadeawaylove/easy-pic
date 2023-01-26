import os

from src.constant import resource_path, platform


def show_notification(message, title, subtitle=None, sound_name=None):
    if platform == "darwin":
        show_notification_mac(message, title, subtitle, sound_name)
    elif platform in ("win32", "cygwin"):
        show_notification_win(message, title)


def show_notification_mac(message, title, subtitle=None, sound_name=None):
    """
        Display an OSX notification with message title an subtitle
        sounds are located in /System/Library/Sounds or ~/Library/Sounds
    """
    title_part = ''
    if title:
        title_part = 'with title "{0}"'.format(title)
    subtitle_part = ''
    if subtitle:
        subtitle_part = 'subtitle "{0}"'.format(subtitle)
    soundname_part = ''
    if sound_name:
        soundname_part = 'sound name "{0}"'.format(sound_name)

    apple_script_notification = 'display notification "{0}" {1} {2} {3}'.format(message, title_part, subtitle_part,
                                                                                soundname_part)
    os.system("osascript -e '{0}'".format(apple_script_notification))


def show_notification_win(message, title):
    from win10toast import ToastNotifier

    toaster = ToastNotifier()

    toaster.show_toast(title,
                       message,
                       icon_path=os.path.join(resource_path, "icon.png"),
                       duration=10)


if __name__ == '__main__':
    show_notification("message", "title", "123")
