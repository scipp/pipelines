# Pipelines

Azure Pipelines templates shared by various subprojects such as `scipp` and `scippneutron`.

## Caveats

The pipelines uses a common conda environment file for its various stages passes as `conda_env`.
For c++ projects where you will have build dependencies as well as run dependencies, this will mean that all stages, not just those conducting the build, will bring in build dependencies as well as run dependencies
There is special mitigation for this in the documentation stages, where the input environment file is stripped of blocks identified as build dependencies, i.e those between lines `# Build` and the next empty line.

