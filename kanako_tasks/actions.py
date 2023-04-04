import time
from random import shuffle

from kanako_tasks import (
    actions,
    dmenu,
    formatting,
    notification,
    parcing,
    settings,
    timew,
)
from kanako_tasks.formatting import Tree, print


def start(random=False):
    tasks_with_path = parcing.get_tasks_with_path()
    if not random:
        full_path_task = dmenu.run(tasks_with_path, "Tasks")
    else:
        shuffle(tasks_with_path)
        full_path_task = tasks_with_path[0]
    if full_path_task:
        index = full_path_task.rfind(".")
        task = full_path_task[index + 1 :]
        path = full_path_task[:index]
        timew.start([task, full_path_task])
    else:
        raise "You don't chose task to start"


def stop():
    timew.stop()


def continue_task():
    timew.continue_task()


def get_counter():
    intervals = timew.get_intervals(":day")
    result = {"duration": 0, "count": 0}
    for interval in intervals:
        if interval["name"] != "Resting":
            result["duration"] += interval["duration"].seconds
            result["count"] += 1
    return result


def show():
    interval = timew.get_current_interval()
    label = ""
    if interval:
        label = f'{interval["name"]}'
    else:
        label = "Kanako is sleeping"
    data = get_counter()
    print(
        f"{label} (TT: {formatting.duration_to_str(data['duration'])}) (C: {data['count']})"
    )


def add_interval(root, path, duration):
    index = path.find(".")
    if index != -1:
        parent = path[:index]
        if parent not in root["children"]:
            root["children"][parent] = {"duration": duration, "children": {}}
            add_interval(root["children"][parent], path[index + 1 :], duration),
        else:
            root["children"][parent]["duration"] += duration
            add_interval(root["children"][parent], path[index + 1 :], duration),
    else:
        parent = path
        if parent not in root["children"]:
            root["children"][parent] = {"duration": duration, "children": {}}
        else:
            root["children"][parent]["duration"] += duration


def task_status_tree():
    intervals = timew.get_intervals()
    task_tree = {"children": {}, "duration": 0}
    for interval in intervals:
        if "path" in interval:
            add_interval(task_tree, interval["path"], interval["duration"])
            task_tree["duration"] += interval["duration"].seconds
    return task_tree


def add_brach(task_root, task_name=None, tree_root=None):
    if tree_root == None:
        tree = Tree(
            f"Stats - {formatting.duration_to_str(task_root['duration'])}"
        )
    else:
        tree = tree_root.add(
            f'{task_name} - {formatting.duration_to_str(task_root["duration"].seconds)}'
        )
    if task_root["children"]:
        for key, value in sorted(
            task_root["children"].items(),
            key=lambda x: x[1]["duration"],
            reverse=True,
        ):
            add_brach(value, key, tree)
    return tree


def stats():
    task_tree = task_status_tree()
    tree = add_brach(task_tree)
    print(tree)
