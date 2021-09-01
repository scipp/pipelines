# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)

import setuptools

setuptools.setup(name='scippbuildtools',
                 packages=setuptools.find_packages('src'),
                 package_dir={"": "src"})
