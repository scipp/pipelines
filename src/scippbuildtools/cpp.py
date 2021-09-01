# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
import os
import shutil
import multiprocessing
import sys
from . import tools


class CppBuilder:
    """
    Platform-independent builder to run cmake, build, install and C++ tests.
    """
    def __init__(self, prefix, source_dir, build_dir, caching, **ignored):
        self._prefix, self._build_dir, self._source_dir = tools.get_absolute_paths(
            prefix, build_dir, source_dir)
        self._caching = caching
        self._config = {}

    def enter_build_dir(self):
        tools.make_dir(self._build_dir)
        os.chdir(self._build_dir)

    def cmake_configure(self):

        # Get the platform name: 'linux', 'darwin' (osx), or 'win32'.
        self._config["platform"] = sys.platform

        # Default options
        self._config["shell"] = False
        parallel_flag = '-j{}'.format(multiprocessing.cpu_count())
        self._config["build_config"] = ''

        # Some flags use a syntax with a space separator instead of '='
        use_space = ['-G', '-A']

        # Default cmake flags
        cmake_flags = {
            '-G': 'Ninja',
            '-DPython_EXECUTABLE': shutil.which("python"),
            '-DCMAKE_INSTALL_PREFIX': self._prefix,
            '-DWITH_CTEST': 'OFF',
            '-DCMAKE_INTERPROCEDURAL_OPTIMIZATION': 'ON'
        }

        if self._config["platform"] == 'darwin':
            cmake_flags.update({'-DCMAKE_INTERPROCEDURAL_OPTIMIZATION': 'OFF'})
            osxversion = os.environ.get('OSX_VERSION')
            if osxversion is not None:
                cmake_flags.update({
                    '-DCMAKE_OSX_DEPLOYMENT_TARGET':
                    osxversion,
                    '-DCMAKE_OSX_SYSROOT':
                    os.path.join('/Applications', 'Xcode.app', 'Contents', 'Developer',
                                 'Platforms', 'MacOSX.platform', 'Developer', 'SDKs',
                                 'MacOSX{}.sdk'.format(osxversion))
                })

        if self._config["platform"] == 'win32':
            cmake_flags.update({'-G': 'Visual Studio 16 2019', '-A': 'x64'})
            # clcache conda installed to env Scripts dir in env if present
            scripts = os.path.join(os.environ.get('CONDA_PREFIX'), 'Scripts')
            if self._caching and os.path.exists(os.path.join(scripts, 'clcache.exe')):
                cmake_flags.update({'-DCLCACHE_PATH': scripts})
            self._config["shell"] = True
            self._config["build_config"] = 'Release'
            # cmake --build --parallel is detrimental to build performance on
            # windows, see https://github.com/scipp/scipp/issues/2078 for
            # details
            self._config["build_flags"] = []
        else:
            # For other platforms we do want to add the parallel build flag.
            self._config["build_flags"] = [parallel_flag]

        if len(self._config["build_config"]) > 0:
            self._config["build_flags"] += ['--config', self._config["build_config"]]

        # Parse cmake flags
        self._config["flags_list"] = []
        for key, value in cmake_flags.items():
            if key in use_space:
                self._config["flags_list"] += [key, value]
            else:
                self._config["flags_list"].append('{}={}'.format(key, value))

    def cmake_run(self):
        # Run cmake
        tools.run_command(['cmake'] + self._config["flags_list"] + [self._source_dir],
                          shell=self._config["shell"])
        # Show cmake settings
        tools.run_command(['cmake', '-B', '.', '-S', self._source_dir, '-LA'],
                          shell=self._config["shell"])

    def cmake_build(self, target_list):
        # Compile benchmarks, C++ tests, and python library
        for target in target_list:
            tools.run_command(['cmake', '--build', '.', '--target', target] +
                              self._config["build_flags"],
                              shell=self._config["shell"])

    def run_cpp_tests(self, test_list, test_dir='bin'):
        for test in test_list:
            tools.run_command(
                [os.path.join(test_dir, self._config["build_config"], test)],
                shell=self._config["shell"])
