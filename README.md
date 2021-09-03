# Pipelines

Azure Pipelines templates and tools for CI builds.

## Azure Pipelines templates

This repository contains templates for CI on Azure pipelines, which are located in the
[pipelines](https://github.com/scipp/pipelines/tree/main/pipelines) folder.

These are used by the repositories in the [Scipp](https://github.com/scipp) organisation.
They make heavy use of parameters,
which makes it possible to avoid much duplication between the repositories.

## Scippbuildtools

This repository also contains a small python library of helper functions,
called `scippbuildtools`,
for building C++ libraries, python packages and documentation.

The goal of `scippbuildtools` is to reduce duplication in the CI setup between all the repositories of the [Scipp](https://github.com/scipp) organisation.

- `cpp.py` defines a `CppBuilder` used by `scipp/<repo>/tools/build_cpp.py`
- `filemover.py` is used by `scipp/<repo>/tools/build_conda.py`
- `docs.py` defines a `DocsBuilder` used by `scipp/<repo>/docs/build_docs.py`
- `sphinxconf.py` defines common variables for sphinx, which can be overridden in `scipp/<repo>/docs/conf.py`. It also writes a `_static/theme_overrides.css` file when imported.

`scippbuildtools` is made available to the other repositories via a `conda` package,
which is built and uploaded to [Anaconda](https://anaconda.org/scipp/scippbuildtools)
as part of the CI of this repository.
