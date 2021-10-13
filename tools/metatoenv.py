# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
import os
import argparse

parser = argparse.ArgumentParser(
    description='Generate a conda environment file from a conda recipe meta.yaml file')
parser.add_argument('--dir', default='.')
parser.add_argument('--meta-file', default='meta.yaml')
parser.add_argument('--env-file', default='environment.yml')
parser.add_argument('--env-name', '--name', default='')
parser.add_argument('--channels', default='conda-forge')
parser.add_argument('--platform', '--os', default='linux64')
parser.add_argument('--extra', default='')


def _number_of_leading_spaces(string):
    """
    Count the number of leading spaces in a string.
    """
    return len(string) - len(string.lstrip(' '))


def _find_dependencies(text):
    """
    Search the contents of a metafile for dependencies in a set of pre-defined sections.
    Return a list of dependencies.
    """
    dependencies = []
    sections = ["requirements:", "requires:", "developer_dependencies:"]
    append = False
    nspaces = 0
    for line in text:
        stripped = line.strip()
        if append and _number_of_leading_spaces(line) <= nspaces:
            append = False
        if stripped in sections:
            nspaces = _number_of_leading_spaces(line)
            append = True
        if append and stripped.startswith('-'):
            dep = stripped.strip(' -')
            if dep not in dependencies:
                dependencies.append(dep)
    return dependencies


def main(metafile, envfile, envname, channels, platform, extra):

    # Read and parse metafile
    with open(metafile, "r") as f:
        content = f.readlines()
    all_dependencies = _find_dependencies(content)

    # Filter out deps for selected OS
    dependencies = []
    for dep in all_dependencies:
        ok = True
        if dep.endswith(']'):
            left = dep.rfind('[')
            if left == -1:
                raise RuntimeError("Unmatched square bracket in preprocessing selector")
            selector = dep[left:]
            if selector.startswith('[not'):
                if (platform in selector) or (selector.replace('[not', '')[:-1].strip()
                                              in platform):
                    ok = False
            else:
                if (platform not in selector) and (selector[1:-1] not in platform):
                    ok = False
            if ok:
                dep = dep.replace(selector, '').strip()
        if ok and (dep not in dependencies):
            dependencies.append(dep)

    # Generate envname from output file name if name is not defined
    if len(envname) == 0:
        envname = os.path.splitext(envfile)[0]

    # Write to output env file
    with open(envfile, "w") as out:
        out.write("name: {}\n".format(envname))
        out.write("channels:\n")
        for channel in channels:
            out.write("  - {}\n".format(channel))
        out.write("dependencies:\n")
        for dep in dependencies + extra:
            out.write("  - {}\n".format(dep))


if __name__ == '__main__':
    args = parser.parse_args()

    channels = [args.channels]
    if "," in args.channels:
        channels = args.channels.split(",")
    extra = [args.extra]
    if "," in args.extra:
        extra = args.extra.split(",")

    main(metafile=os.path.join(args.dir, args.meta_file),
         envfile=args.env_file,
         envname=args.env_name,
         channels=channels,
         platform=args.platform.replace('-', ''),
         extra=extra)
