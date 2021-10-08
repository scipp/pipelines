# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
import os
import yaml
import argparse

parser = argparse.ArgumentParser(
    description='Generate a conda environment file from a conda recipe meta.yaml file')
parser.add_argument('--dir', default='.')
parser.add_argument('--meta-file', default='meta.yaml')
parser.add_argument('--config-file', default='conda_build_config.yaml')
parser.add_argument('--env-file', default='environment.yml')
parser.add_argument('--env-name', '--name', default='')
parser.add_argument('--channels', default='conda-forge')
parser.add_argument('--platform', '--os', default='linux64')


def main(metafile, configfile, envfile, envname, channels, platform):

    if os.path.exists(configfile):
        with open(configfile, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    with open(metafile, "r") as f:
        asstring = f.read()

    for key, value in config.items():
        asstring = asstring.replace("{{{{ {} }}}}".format(key), "= {}".format(value[0]))
    asstring = asstring.replace("{{", "")
    asstring = asstring.replace("}}", "")
    content = yaml.safe_load(asstring)

    # Create dependencies
    all_dependencies = []
    for r in content["requirements"].values():
        all_dependencies += r
    all_dependencies += content["test"]["requires"]

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

    if len(envname) == 0:
        envname = os.path.splitext(envfile)[0]
    output = {"name": envname, "channels": channels, "dependencies": dependencies}

    with open(envfile, "w") as out:
        yaml.dump(output, out, default_flow_style=False)


if __name__ == '__main__':
    args = parser.parse_args()

    channels = [args.channels]
    for delimiter in ":,":
        if delimiter in args.channels:
            channels = args.channels.split(delimiter)

    main(metafile=os.path.join(args.dir, args.meta_file),
         configfile=os.path.join(args.dir, args.config_file),
         envfile=args.env_file,
         envname=args.env_name,
         channels=channels,
         platform=args.platform)
