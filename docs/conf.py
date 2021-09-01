# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
import os
import sys
from pathlib import Path
docs_dir = str(Path(__file__).parent.absolute())
sys.path.append(os.path.join(docs_dir, '..', 'src'))
try:
    from scippbuildtools.sphinxconf import *  # noqa: E402, F401, F403
except ImportError:
    pass

project = u'pipelines-test'

extensions = ['sphinx.ext.doctest']

# Output file base name for HTML help builder.
htmlhelp_basename = 'pipelines-test-doc'
