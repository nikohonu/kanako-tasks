import datetime as dt
import time
from pathlib import Path

import click

from kanako_tasks import dmenu, formatting, notification, settings, timew
from kanako_tasks.formatting import Table, print

work_durations = ["25", "45"]
break_durations = ["5", "15"]


@click.group()
def cli():
    pass


def stop():
    timew.stop()
    for duration in work_durations:
        timew.untag(1, duration)


def pause():
    timew.stop()


@click.command()
def stop_command():
    stop()


@click.command()
def pause_command():
    pause()


def start(name, duration):
    pause()
    time.sleep(1)
    last_interval = timew.get_last_interval()
    if (
        last_interval
        and last_interval["name"] == name
        and "max_duration" in last_interval
    ):
        seconds = last_interval["duration"].seconds
        timew.delete(1)
        timew.start(name, duration, f"{seconds}s ago")
    else:
        timew.start(name, duration)
    time.sleep(1)
    try:
        while True:
            interval = timew.get_current_interval()
            if interval:
                time_left = interval["max_duration"] * 60 - interval["duration"].seconds
                if time_left <= 0:
                    stop()
                    notification.send()
                    return
                else:
                    time.sleep(0.5)
                    continue
            else:
                return
    except KeyboardInterrupt:
        pause()


@click.command(name="start")
@click.argument("name", type=str)
@click.argument("duration", type=int)
def start_command(name, duration):
    start(name, duration)


def get_counter():
    intervals = timew.get_intervals(":day")
    result = {"duration": 0, "count": 0}
    for interval in intervals:
        if interval["name"] != "Resting":
            result["duration"] += interval["duration"].seconds
            result["count"] += 1
    return result


@click.command()
def show():
    interval = timew.get_current_interval()
    label = ""
    if interval:
        name = interval["name"]
        if name == "Resting":
            label = f"Kanako asks to rest for"
        else:
            label = f'"{name}" for'
        label += f' {formatting.duration_to_str(interval["time_left"])}'
    else:
        label = "Kanako is sleeping"
    data = get_counter()
    print(
        f"{label} (TT: {formatting.duration_to_str(data['duration'])}) (C: {data['count']})"
    )


def get_tasks_stats():
    intervals = timew.get_intervals()
    tasks = {}
    for interval in intervals:
        if interval["name"] in tasks:
            tasks[interval["name"]] += interval["duration"]
        else:
            tasks[interval["name"]] = interval["duration"]
    return tasks


@click.command()
def stats_command():
    tasks = get_tasks_stats()
    table = Table(title="Tasks")
    table.add_column("Name")
    table.add_column("Total duration", justify="right", style="red")
    for key, value in tasks.items():
        if key != "Resting":
            table.add_row(key, formatting.duration_to_str(value.seconds))
    print(table)


def load_task_lists(task_file_path):
    tasks = []
    with task_file_path.open() as file:
        for line in file.readlines():
            if line.startswith("-"):
                tasks.append(line[2:-1])
    return tasks


@click.command(name="dmenu")
def dmenu_command():
    task_file_path = settings.get("task_file_path")
    if not task_file_path:
        print("First set the path to the task file!")
        return
    task_file_path = Path(task_file_path)
    tasks = load_task_lists(task_file_path)
    options = ["Start", "Stop", "Pause", "Break"]
    option = dmenu.run(options, "What you want?")
    match option:
        case "Start":
            stats = get_tasks_stats()
            tasks = sorted(
                tasks, key=lambda task: stats.get(task, dt.timedelta(0)), reverse=True
            )
            last_interval = timew.get_last_interval()
            tasks = [
                [
                    task,
                    f"continue {formatting.duration_to_str(last_interval['duration'].seconds)}",
                ]
                if last_interval
                and last_interval["name"] == task
                and "max_duration" in last_interval
                else [task]
                for task in tasks
            ]
            tasks = [
                task
                + [
                    formatting.duration_to_str(
                        stats.get(task[0], dt.timedelta(0)).seconds
                    )
                ]
                for task in tasks
            ]
            tasks = [", ".join(task) for task in tasks]
            task = dmenu.run(tasks, "What task to you want to start?")
            task = task.split(", ")[0]
            if not task:
                return
            duration = dmenu.run(work_durations, "How long?")
            if not duration:
                return
            duration = int(duration)
            start(task, duration)
        case "Stop":
            stop()
        case "Pause":
            pause()
        case "Break":
            duration = dmenu.run(break_durations, "How long?")
            start("Resting", duration)


@click.command()
@click.argument(
    "task_file_path", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
def set_task_file(task_file_path):
    settings.set("task_file_path", task_file_path)


cli.add_command(start_command)
cli.add_command(stop_command)
cli.add_command(show)
cli.add_command(stats_command)
cli.add_command(dmenu_command)
cli.add_command(set_task_file)


def main():
    cli()


if __name__ == "__main__":
    main()
