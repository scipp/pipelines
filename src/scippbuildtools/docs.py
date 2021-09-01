# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)

import os
from pathlib import Path
import sys
import tarfile
from . import tools


class DocsBuilder:
    """
    Platform-independent builder to build the docs with sphinx.
    """
    def __init__(self, docs_dir, prefix, work_dir, data_dir, **ignored):
        self._work_dir, self._prefix, self._data_dir = tools.get_absolute_paths(
            work_dir, prefix, data_dir, root=docs_dir)
        self._shell = sys.platform == "win32"

    def download_test_data(self,
                           tar_name,
                           remote_url="https://public.esss.dk/groups/scipp"):
        # Download and extract tarball containing data files
        target = os.path.join(self._data_dir, tar_name)
        tools.make_dir(self._data_dir)
        tools.download_file(os.path.join(remote_url, tar_name), target)
        os.write(1, "Unpacking {} to {}\n".format(target, self._data_dir).encode())
        tar = tarfile.open(target, "r:gz")
        tar.extractall(path=self._data_dir)
        tar.close()

    def make_mantid_config(self, content):
        # Create Mantid properties file so that it can find the data files.
        # Also turn off the logging so that it doesn't appear in the docs.
        home = str(Path.home())
        config_dir = os.path.join(home, ".mantid")
        tools.make_dir(config_dir)
        properties_file = os.path.join(config_dir, "Mantid.user.properties")
        os.write(1, "Mantid Config: {}\n".format(content).encode())
        with open(properties_file, "a") as f:
            f.write(content)

    def run_sphinx(self, docs_dir, builder='html'):
        tools.run_command([
            'sphinx-build', '-b', builder, '-d', self._work_dir, docs_dir, self._prefix
        ],
                          shell=self._shell)
