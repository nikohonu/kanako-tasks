from pathlib import Path

from kanako_tasks import settings


def get_tasks_with_path():
    task_file_path = settings.get("task_file_path")
    if not task_file_path:
        raise "First set the path to the task file!"
    task_file_path = Path(task_file_path)
    tasks = []

    def get_children(lines, parent=""):
        children = {}
        while lines:
            line = lines.pop(0)
            index = line[1].find("[")
            if index != -1:
                line[1] = line[1][: index - 1]
            sub_lines = []
            while lines:
                sub_line = lines.pop(0)
                if sub_line[0] > 0:
                    sub_line[0] -= 1
                    sub_lines.append(sub_line)
                else:
                    children[line[1]] = get_children(
                        sub_lines, parent + "." + line[1]
                    )
                    lines.insert(0, sub_line)
                    break
            if not lines:
                children[line[1]] = get_children(
                    sub_lines, parent + "." + line[1]
                )
        index = parent.rfind(".")
        task_full_path = parent[1:]
        parent = parent[1:index]
        if not children:
            tasks.append(task_full_path)
            return parent
        return [children, parent]

    lines = []

    with task_file_path.open() as file:
        for line in file.readlines():
            start = line.find("-")
            if start != -1:
                lines.append([int(start), line[start + 2 : -1]])

    get_children(lines)
    return tasks
