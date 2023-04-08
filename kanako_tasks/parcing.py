import datetime as dt
from pathlib import Path

from kanako_tasks import settings, timew


def get_tasks():
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
            tasks.append(
                {
                    "name": line[1],
                    "context": f"@{line[2]}",
                    "project": f"+{current_project}",
                }
            )
    return tasks


def get_modifier(tasks, intervals, key):
    names = [task[key] for task in tasks]
    data_with_timedelta = {name: dt.timedelta(seconds=0) for name in names}
    for interval in intervals:
        if key in interval:
            if interval[key] in data_with_timedelta:
                data_with_timedelta[interval[key]] += interval["duration"]
            else:
                data_with_timedelta[interval[key]] = interval["duration"]
        else:
            continue
    table = {}
    data = {}
    values = sorted(set(data_with_timedelta.values()), reverse=True)
    step = 1 / (len(values) - 1)
    modifier = 0
    for value in values:
        table[value] = modifier
        modifier += step
    for key in data_with_timedelta:
        data[key] = table[data_with_timedelta[key]]
    return data


def get_tasks_with_coefficient():
    tasks = get_tasks()
    intervals = timew.get_intervals()
    name_modifiers = get_modifier(tasks, intervals, "name")
    context_modifiers = get_modifier(tasks, intervals, "context")
    project_modifiers = get_modifier(tasks, intervals, "project")
    data = {task["name"]: None for task in tasks}
    for task in tasks:
        if data[task["name"]] == None:
            data[task["name"]] = (
                round(
                    (
                        name_modifiers[task["name"]]
                        + context_modifiers[task["context"]]
                        + project_modifiers[task["project"]]
                    )
                    * 100
                )
                / 100
            )
    for task in tasks:
        task["coefficient"] = data[task["name"]]
    return sorted(tasks, key=lambda task: task["coefficient"], reverse=True)
