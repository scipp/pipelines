# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)

import os
import sys
from pathlib import Path
docs_dir = str(Path(__file__).parent.absolute())
sys.path.append(os.path.join(docs_dir, '..', 'src'))
import scippbuildtools as sbt  # noqa: E402

if __name__ == '__main__':
    args, _ = sbt.docs_argument_parser().parse_known_args()
    builder = sbt.DocsBuilder(docs_dir=docs_dir, **vars(args))
    builder.run_sphinx(builder=args.builder, docs_dir=docs_dir)
