import subprocess
from pathlib import Path

from brother_ql.labels import ALL_LABELS


def get_label_by_name(label_name):
    for label in ALL_LABELS:
        if label.name == label_name:
            return label


def get_label_by_identifier(ident):
    for label in ALL_LABELS:
        if label.identifier == ident:
            return label


def run_brother_ql_command(model: str, identifier: str, label: str, file: Path):
    try:
        # Execute the command and capture the output
        command = f"brother_ql -b pyusb -m {model} -p {identifier} print -l {label} {str(file)}"
        print(command)
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError as e:
        return e.output
