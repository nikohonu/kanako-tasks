import rich.console
from rich.table import Table

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
    result += f"{minutes}m " if minutes else ""
    result += f"{seconds}s" if seconds else ""
    return result.strip()
