import datetime as dt
import json
import subprocess

from click import command


def process_interval(raw_interval):
    interval = {}
    for tag in raw_interval["tags"]:
        try:
            interval["max_duration"] = int(tag)
        except ValueError:
            interval["name"] = tag
    interval["start"] = dt.datetime.strptime(raw_interval["start"], "%Y%m%dT%H%M%S%z")
    end = dt.datetime.now(dt.timezone.utc)
    if "end" in raw_interval:
        end = dt.datetime.strptime(raw_interval["end"], "%Y%m%dT%H%M%S%z")
        interval["end"] = end
    interval["duration"] = end - interval["start"]
    if "max_duration" in interval:
        interval["time_left"] = (
            60 * interval["max_duration"] - interval["duration"].seconds
        )
    return interval


def get_intervals(range=""):
    command = ["timew", "export"]
    command.extend(range.split())
    raw_data = json.loads(
        subprocess.run(command, capture_output=True, text=True).stdout
    )
    intervals = []
    for raw_interval in raw_data:
        intervals.append(process_interval(raw_interval))
    return intervals


def get_current_interval():
    intervals = get_intervals("from now")
    result = intervals[0] if intervals else None
    return result


def get_last_interval():
    intervals = get_intervals(":day")
    result = intervals[-1] if intervals else None
    return result


def delete(id):
    subprocess.run(["timew", "delete", f"@{id}"])


def start(name, duration, date=""):
    command = ["timew", "start"]
    command.extend(date.split())
    command.extend([name, str(duration)])
    print(command)
    subprocess.run(command)


def stop():
    subprocess.run(["timew", "stop"])


def untag(id, tag):
    subprocess.run(["timew", "untag", f"@{id}", tag])


def send_message():
    subprocess.run(["notify-send", "Notice me, senpai!", "-a", "Kanako"])
