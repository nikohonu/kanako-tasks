import rich.console
from rich.tree import Tree

console = rich.console.Console()

print = console.print


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
    result += f"{minutes}m " if minutes or hours else ""
    result += f"{seconds}s" if seconds or minutes else ""
    return f"[red]{result.strip()}[/red]"
