# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)

import argparse


def cpp_argument_parser():
    """
    Create a common argument parser for building the C++ library with cmake.
    """
    parser = argparse.ArgumentParser(description='Build C++ library and run tests')
    parser.add_argument('--prefix', default='install')
    parser.add_argument('--source_dir', default='.')
    parser.add_argument('--build_dir', default='build')
    parser.add_argument('--caching', action='store_true', default=False)
    return parser


def docs_argument_parser():
    """
    Create a common argument parser for building the docs with sphinx.
    """
    parser = argparse.ArgumentParser(description='Build doc pages with sphinx')
    parser.add_argument('--prefix', default='build')
    parser.add_argument('--work_dir', default='.doctrees')
    parser.add_argument('--data_dir', default='data')
    parser.add_argument('--builder', default='html')
    parser.add_argument('--no-setup', action='store_true', default=False)
    return parser
