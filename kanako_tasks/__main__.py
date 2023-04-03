import datetime as dt
from pathlib import Path

import click

from kanako_tasks import (
    actions,
    dmenu,
    formatting,
    notification,
    settings,
    timew,
)


@click.group()
def cli():
    pass


@click.command()
def start():
    actions.start()


@click.command()
def stop():
    actions.stop()


@click.command(name="continue")
def continue_task():
    actions.continue_task()


@click.command()
def show():
    actions.show()


@click.command()
def stats():
    actions.stats()


@click.command()
def run():
    options = ["start", "stop", "continue"]
    option = dmenu.run(options, "What you want?")
    match option:
        case "start":
            actions.start()
        case "stop":
            actions.stop()
        case "continue":
            actions.continue_task()


@click.command()
@click.argument(
    "task_file_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def set_task_file(task_file_path):
    settings.set("task_file_path", task_file_path)


cli.add_command(start)
cli.add_command(stop)
cli.add_command(continue_task)
cli.add_command(show)
cli.add_command(stats)
cli.add_command(run)
cli.add_command(set_task_file)


def main():
    cli()


if __name__ == "__main__":
    main()
