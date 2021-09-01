# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
import os
import requests
import subprocess


def run_command(cmd, shell):
    """
    Run a command (supplied as a list) using subprocess.check_call
    """
    os.write(1, "{}\n".format(' '.join(cmd)).encode())
    return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=shell)


def get_absolute_paths(*paths, root=None):
    abs_paths = []
    if root is not None:
        abs_root = os.path.abspath(root)
    for path in paths:
        if os.path.isabs(path):
            abs_paths.append(path)
        else:
            if root is not None:
                abs_paths.append(os.path.join(abs_root, path))
            else:
                abs_paths.append(os.path.abspath(path))
    return abs_paths


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_file(source, target):
    os.write(1, "Downloading: {}\n".format(source).encode())
    r = requests.get(source, stream=True)
    with open(target, "wb") as f:
        for chunk in r.iter_content(chunk_size=1_048_576):
            if chunk:
                f.write(chunk)
