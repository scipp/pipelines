# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
# @author Neil Vaytet

import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description='Build doc pages with sphinx')
parser.add_argument('--prefix', default='build')
parser.add_argument('--work_dir', default='.doctrees')
parser.add_argument('--builder', default='html')

if __name__ == '__main__':

    args = parser.parse_known_args()

    # Build the docs with sphinx-build
    status = subprocess.check_call([
        'sphinx-build', '-b', args.builder, '-d', args.work_dir, '.',
        args.prefix
    ],
                                   stderr=subprocess.STDOUT,
                                   shell=sys.platform == "win32")
