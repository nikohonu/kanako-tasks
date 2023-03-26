import datetime as dt
import json
import subprocess


def get_intervals():
    data = json.loads(
        subprocess.run("timew export".split(), capture_output=True, text=True).stdout
    )
    intervals = []
    for interval in data:
        result = {}
        result["name"] = interval["tags"][0]
        result["start"] = dt.datetime.strptime(interval["start"], "%Y%m%dT%H%M%S%z")
        if "end" in interval:
            result["end"] = dt.datetime.strptime(interval["end"], "%Y%m%dT%H%M%S%z")
        else:
            result["end"] = dt.datetime.now(dt.timezone.utc)
        result["duration"] = result["end"] - result["start"]
        intervals.append(result)
    return intervals


def get_current_interval():
    data = json.loads(
        subprocess.run(
            "timew export for 1s".split(), capture_output=True, text=True
        ).stdout
    )
    if data:
        result = {}
        result["name"] = data[0]["tags"][0]
        result["start"] = dt.datetime.strptime(data[0]["start"], "%Y%m%dT%H%M%S%z")
        return result
    return None


def start(name):
    subprocess.run(["timew", "start", name])


def stop():
    subprocess.run(["timew", "stop"])


def send_message():
    subprocess.run(["notify-send", "Notice me, senpai!", "-a", "Kanako"])
