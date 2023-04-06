from random import shuffle

from kanako_tasks import dmenu, formatting, parcing, timew
from kanako_tasks.formatting import Tree, duration_to_str, print


def start(random=False):
    tasks = parcing.get_tasks_with_path()
    context = dmenu.run(
        ["any", "@fun", "@work", "@study"],
        "What is the context of a random task?",
    )
    if context != "any":
        tasks = [task for task in tasks if task[2] == context]
    tasks_dict = {" ".join(task).lower(): task for task in tasks}
    if not random:
        task = tasks_dict[dmenu.run(list(tasks_dict.keys()), "Tasks")]
    else:
        shuffle(tasks)
        task = tasks[0]
    if task:
        timew.start(task)
    else:
        raise Exception("You don't chose task to start")


def stop():
    timew.stop()


def continue_task():
    timew.continue_task()


def get_counter():
    intervals = timew.get_intervals(":day")
    result = {"duration": 0, "count": 0}
    for interval in intervals:
        result["duration"] += interval["duration"].seconds
        result["count"] += 1
    return result


def show():
    interval = timew.get_current_interval()
    label = ""
    if interval:
        label = f'{interval["name"]} {interval["project"]} {interval["context"]} for {duration_to_str(interval["duration"].seconds)}'
    else:
        label = "Kanako is sleeping"
    data = get_counter()
    print(
        f"{label} (TT: {formatting.duration_to_str(data['duration'])}) (C: {data['count']})"
    )


def add_branch(key, intervals, root):
    data = {}
    for interval in intervals:
        if key in interval:
            if interval[key] in data:
                data[interval[key]] += interval["duration"]
            else:
                data[interval[key]] = interval["duration"]
        else:
            continue
    for key, value in sorted(
        data.items(), key=lambda item: item[1], reverse=True
    ):
        root.add(f"{key} {duration_to_str(value.seconds)}")


def stats(period):
    intervals = timew.get_intervals(f":{period}")
    total_time = sum([interval["duration"].seconds for interval in intervals])
    tree = Tree(f"Total duration {duration_to_str(total_time)}")
    branch = tree.add("By name")
    add_branch("name", intervals, branch)
    branch = tree.add("By project")
    add_branch("project", intervals, branch)
    branch = tree.add("By context")
    add_branch("context", intervals, branch)
    print(tree)
