import datetime as dt
import time

import click
import rich.console
from rich.table import Table

import kanako_tasks.timew as timew

console = rich.console.Console()


def duration_to_str(duration):
    if duration <= 0:
        result = "-"
        duration = -duration
    else:
        result = ""
    seconds = duration
    minutes = int(duration / 60)
    hours = int(minutes / 60)
    seconds = seconds % 60
    minutes = minutes % 60
    result += f"{hours}h " if hours else ""
    result += f"{minutes}m " if minutes else ""
    result += f"{seconds}s" if seconds else ""
    return result.strip()


@click.group()
def cli():
    pass


def start_task(name, max_time=25):
    timew.start(name)
    time.sleep(1)
    while True:
        data = timew.get_current_interval()
        if data:
            start = data["start"]
            now = dt.datetime.now(dt.timezone.utc)
            duration = now - start
            if duration.seconds >= max_time * 60:
                timew.stop()
                timew.send_message()
                return
            else:
                time.sleep(0.5)
                continue
        return


@click.command()
@click.argument("name", type=str)
def start(name):
    if name == "Resting":
        start_task(name, 5)
    else:
        start_task(name, 25)


@click.command()
def show():
    max_time = 25
    data = timew.get_current_interval()
    if data:
        name = data["name"]
        if name == "Resting":
            max_time = 5
            name = f"Kanako asks to rest for"
        else:
            name = f'Kanako asks to work on "{name}" for'
        start = data["start"]
        now = dt.datetime.now(dt.timezone.utc)
        duration = now - start
        last = 60 * max_time - duration.seconds
        minutes = int(last / 60)
        seconds = last - minutes * 60
        result = f"{name}"
        if minutes:
            result += f" {minutes}m"
        result += f" {seconds}s"
        print(result)
    else:
        print("Kanako is sleeping")


@click.command()
def stop():
    timew.stop()


@click.command()
def stats():
    intervals = timew.get_intervals()
    tasks = {}
    for interval in intervals:
        if interval["name"] in tasks:
            tasks[interval["name"]] += interval["duration"]
        else:
            tasks[interval["name"]] = interval["duration"]
    console.print(tasks)
    table = Table(title="Tasks")
    table.add_column(
        "Task name",
    )
    table.add_column("Total duration", justify="right", style="red")
    for task in tasks:
        table.add_row(task, duration_to_str(tasks[task].seconds))
    console.print(table)


cli.add_command(start)
cli.add_command(stop)
cli.add_command(show)
cli.add_command(stats)


def main():
    cli()


if __name__ == "__main__":
    main()
