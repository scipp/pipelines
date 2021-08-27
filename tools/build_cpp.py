# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)

import scippbuildtools as sbt


def main(**kwargs):
    builder = sbt.CppBuilder(**kwargs)
    builder.cmake_configure()
    builder.enter_build_dir()
    builder.cmake_run()
    builder.cmake_build(['pipelines-test', 'install'])
    builder.run_cpp_tests(test_list=['pipelines-test'], test_dir='.')


if __name__ == '__main__':

    args, _ = sbt.cpp_argument_parser().parse_known_args()
    # Convert Namespace object `args` to a dict with `vars(args)`
    main(**vars(args))
