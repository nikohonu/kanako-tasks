from pathlib import Path

from kanako_tasks import settings


def get_tasks_with_path():
    task_file_path = settings.get("task_file_path")
    if not task_file_path:
        raise Exception("First set the path to the task file!")
    task_file_path = Path(task_file_path)
    lines = []
    with task_file_path.open() as file:
        for line in file.readlines():
            start = line.find("-")
            tag_start = line.find("#")
            if start != -1:
                lines.append(
                    [
                        start,
                        line[start + 2 : tag_start - 1].strip()[2:-2]
                        if start == 1
                        else line[start + 2 : tag_start].strip(),
                        line[tag_start + 1 :].strip() if start == 1 else "",
                    ]
                )
    tasks = []
    current_project = ""
    for line in lines:
        if line[0] == 0:
            current_project = line[1]
        else:
            tasks.append([line[1], f"+{current_project}", f"@{line[2]}"])
    return tasks
