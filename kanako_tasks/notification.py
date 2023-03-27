import subprocess


def send():
    subprocess.run(["notify-send", "Notice me, senpai!", "-a", "Kanako"])
