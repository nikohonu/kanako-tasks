from pathlib import Path

import click

from kanako_tasks import actions, dmenu, settings


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--random", "-r", help="start random task", default=False, is_flag=True
)
def start(random):
    actions.start(random)


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
@click.option(
    "-p",
    "--period",
    type=click.Choice(["day", "week", "month", "year", "all"]),
    default="all",
)
def stats(period):
    actions.stats(period)


@click.command()
def run():
    options = ["start", "random", "stop", "continue"]
    option = dmenu.run(options, "What you want?")
    match option:
        case "start":
            actions.start()
        case "random":
            actions.start(True)
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
