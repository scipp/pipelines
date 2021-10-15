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


def _indentation_level(string):
    """
    Count the number of leading spaces in a string.
    """
    return len(string) - len(string.lstrip(' '))


def _parse_yaml(text):
    out = {}
    contents = {}
    parent = out
    nspaces = 0
    indents = {}
    handle = out

    path = []

    # Remove all empty lines in text
    clean_text = []
    for line in text:
        line = line.rstrip(' \n')
        if len(line) > 0:
            clean_text.append(line)

    for i, line in enumerate(clean_text):
        line = line.rstrip(' \n')
        # if len(line) == 0:
        #     continue

        print(line)
        if i > 0:
            line_indent = _indentation_level(line)
            if line_indent < _indentation_level(clean_text[i - 1]):
                # Find handle
                # handles = []
                current_indent = line_indent
                for p in path[::-1]:
                    if current_indent == p[1]:
                        print("found path:", p[0])
                        ind = path.index(p)
                        handle = out
                        for j in range(ind):
                            handle = handle[path[j][0]]
                        path = path[:ind]
                        print("Path is now:", path)
                        break

        if line.endswith(':'):
            key = line.strip(' -\n')
            handle[key] = {}
            handle = handle[key]
            nspaces = _indentation_level(line)
            path.append((key, nspaces))
            print(path)

        else:
            # if len(line) > 0:
            # handle.append(line)
            #     # print("handle is:", handle)
            stripped = line.lstrip(' ')
            if stripped.startswith('-'):
                handle[stripped.strip(' -')] = None
            elif ':' in stripped:
                ind = stripped.find(':')
                handle[stripped[:ind]] = stripped[ind + 1:]

    return out


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
    # meta_dependencies = _parse_metafile(metacontent)
    # print(meta_dependencies)
    meta = _parse_yaml(metacontent)
    print(meta)

    # meta_dependencies = _jinja_filter(meta_dependencies, platform)
    meta_dependencies = {**meta["requirements:"], **meta["test:"]["requires:"]}
    print("==========================")
    print(meta_dependencies)
    print("==========================")

    with open(mergewith, "r") as f:
        mergecontent = f.readlines()
    additional = _parse_yaml(mergecontent)
    # additional["dependencies"] = _jinja_filter(additional["dependencies"], platform)
    additional_dependencies = additional["dependencies:"]
    print(additional_dependencies)
    return

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
