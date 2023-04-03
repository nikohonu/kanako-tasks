import subprocess


def run(data: list, message):
    ps = subprocess.run(
        ["echo", "\n".join(data)], check=True, capture_output=True, text=True
    )
    return subprocess.run(
        ["dmenu", "-p", message], input=ps.stdout, capture_output=True, text=True
    ).stdout[:-1]
