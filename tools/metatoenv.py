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
parser.add_argument('--merge-with', default='')


def _number_of_leading_spaces(string):
    """
    Count the number of leading spaces in a string.
    """
    return len(string) - len(string.lstrip(' '))


def _remove_global_indentation(sections):
    out = sections.copy()
    for name in sections:
        min_num_spaces = 1000
        for item in sections[name]:
            min_num_spaces = min(min_num_spaces, _number_of_leading_spaces(item))
        out[name] = [item[min_num_spaces:] for item in sections[name]]
    return out


def _parse_yaml(text):
    out = {}
    parent = None
    handle = out
    nspaces = 0
    for line in text:
        line = line.strip('\n')
        if ':' in line:
            parts = line.split(':')
            if len(parts) == 2 and len(parts[1]) == 0:
                handle[parts[0]] = {}
                parent = handle
                handle = handle[parts[0]]
                nspaces = _number_of_leading_spaces(line)
            else:
                handle[parts[0]] = ':'.join(parts[1:])
        if _number_of_leading_spaces(line) <= nspaces:
            handle = parent
    print(out)


def _parse_metafile(text):
    """
    Search the contents of a metafile for dependencies in a set of pre-defined sections.
    Return a list of dependencies.
    """
    # dependencies = []
    sections = {"requirements:": [], "requires:": []}
    append = False
    nspaces = 0
    key = None
    for line in text:
        stripped = line.strip()
        if (key is not None) and _number_of_leading_spaces(line) <= nspaces:
            key = None
        if stripped in sections:
            key = stripped
            nspaces = _number_of_leading_spaces(line)
            # append = True
        if (key is not None) and (stripped.startswith('-')):
            # dep = stripped.strip(' -')
            if line not in sections[key]:
                sections[key].append(line.strip('\n'))

    # for name in sections:
    #     min_num_spaces = 1000
    #     for item in sections[name]:
    #         min_num_spaces = min(min_num_spaces, _number_of_leading_spaces(item))
    #     sections[name] = [item[min_num_spaces:] for item in sections[name]]
    # # print(sections)
    unindented = _remove_global_indentation(sections)
    out = []
    for deps in unindented.values():
        out += deps
    return out


def _parse_envfile(text):
    """
    Search the contents of a regular conda environment file for dependencies.
    Return a list of channels and a list of dependencies.
    """
    # dependencies = []
    sections = {"name": "", "channels": [], "dependencies": []}
    append = False
    nspaces = 0
    key = ""
    for line in text:
        parts = line.split(":")
        if parts[0] in sections:
            key = parts[0]
        elif line.strip().startswith('-'):
            sections[key].append(line.strip('\n'))

        # stripped = line.strip()
        # if append and _number_of_leading_spaces(line) <= nspaces:
        #     append = False
        # if stripped in sections:
        #     nspaces = _number_of_leading_spaces(line)
        #     append = True
        # if append and stripped.startswith('-'):
        #     # dep = stripped.strip(' -')
        #     if line not in dependencies:
        #         dependencies.append(line.strip('\n'))
    # print(sections)
    return _remove_global_indentation(sections)


def _jinja_filter(all_dependencies, platform):
    """
    Filter out deps for requested platform via jinja syntax.
    """
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
                dep = dep.replace(selector, '').strip('\n')
        if ok and (dep not in dependencies):
            dependencies.append(dep)
    return dependencies


def main(metafile, envfile, envname, channels, platform, extra, mergewith):

    # Read and parse metafile
    with open(metafile, "r") as f:
        metacontent = f.readlines()
    meta_dependencies = _parse_metafile(metacontent)
    # print(meta_dependencies)
    meta_dependencies = _jinja_filter(meta_dependencies, platform)

    _ = _parse_yaml(metacontent)

    with open(mergewith, "r") as f:
        mergecontent = f.readlines()
    additional = _parse_envfile(mergecontent)
    additional["dependencies"] = _jinja_filter(additional["dependencies"], platform)

    # dependencies = _jinja_filter(all_dependencies, platform)

    # Generate envname from output file name if name is not defined
    if len(envname) == 0:
        envname = os.path.splitext(envfile)[0]

    for e in extra:
        if len(e) > 0:
            dependencies.append(e)

    # Write to output env file
    with open(envfile, "w") as out:
        out.write("name: {}\n".format(envname))
        out.write("channels:\n")
        for channel in set([c.strip(' -') for c in channels + additional["channels"]]):
            out.write("  - {}\n".format(channel))
        out.write("dependencies:\n")
        for dep in set(meta_dependencies + additional["dependencies"]):
            out.write("{}\n".format(dep))


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
         extra=extra,
         mergewith=args.merge_with)
