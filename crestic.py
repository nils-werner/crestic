#!/usr/bin/env python3

import os
import re
import sys
import argparse
import subprocess
import configparser


def config_files(environ=None):
    if environ is None:
        environ = {}

    # Lowest priority: hardcoded values
    paths = os.pathsep.join([
        os.path.expanduser('~/.config/crestic'),
        '/etc/crestic'
    ])

    # Low priority: optional appdirs import
    try:
        import appdirs
        paths = os.pathsep.join([
            appdirs.user_config_dir('crestic'),
            appdirs.site_config_dir('crestic', multipath=True)
        ])
    except ImportError as e:
        pass

    # Medium priority: CRESTIC_CONFIG_PATHS
    try:
        paths = environ['CRESTIC_CONFIG_PATHS']
    except KeyError:
        pass

    # High priority: CRESTIC_CONFIG_FILE
    try:
        return [environ['CRESTIC_CONFIG_FILE']]
    except KeyError:
        pass

    return [os.path.join(x, 'crestic.cfg') for x in paths.split(os.pathsep)]


def split(string, delimiter="@", maxsplit=1):
    """
    Split a string using a delimiter string. But keep the delimiter in all returned segments

    """
    splits = string.split(delimiter, maxsplit=maxsplit)
    splits[1:] = [delimiter + s for s in splits[1:]]
    splits[:-1] = [s + delimiter for s in splits[:-1]]
    return splits


def valid_preset(value):
    if not re.match(r"^[^@]+(@[^@]+)*$", value):
        raise argparse.ArgumentTypeError(
            "%s is an invalid preset name, only preset names in the format of name[@suffix] are allowed." % value
        )
    return value


def main(argv, environ=None, conffile=None, dryrun=None):
    if environ is None:
        environ = os.environ

    if conffile is None:
        conffile = config_files(environ)

    if dryrun is None:
        dryrun = environ.get("CRESTIC_DRYRUN", False)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("preset", nargs="?", type=valid_preset)
    parser.add_argument("command", help="the restic command")

    # CLI options that override values given in config file
    for arg in argv:
        if arg.startswith(("-", "--")) and arg != "--":
            try:
                parser.add_argument(arg, nargs='?', action='append', dest=arg.lstrip("-"))
            except argparse.ArgumentError:
                pass

    parser.add_argument(
        "arguments", nargs="*", help="positional arguments for the restic command"
    )
    python_args = parser.parse_args(argv)

    config = configparser.ConfigParser()
    config.optionxform = str  # dont map config keys to lower case
    conffile_read = config.read(conffile)

    sections = [
        "global",
        f"global.{python_args.command}",
    ]
    if python_args.preset is not None:
        for preset in split(python_args.preset)[::-1]:
            sections += [
                f"{preset}",
                f"{preset}.{python_args.command}",
            ]

        sections += [
            f"{python_args.preset}",
            f"{python_args.preset}.{python_args.command}",
        ]

    envsections = [f"{section}.environ" for section in sections]

    # Load restic options from config, in ascending precedence
    restic_options = {}
    sections_read = []
    for section in sections:
        try:
            restic_options.update(**dict(config[section]))
            sections_read.append(section)
        except KeyError:
            pass

    # Load restic environment variables from config, in ascending precedence
    restic_environ = dict(environ)
    envsections_read = []
    for envsection in envsections:
        try:
            restic_environ.update(**dict(config[envsection]))
            envsections_read.append(envsection)
        except KeyError:
            pass

    restic_options = {
        k: v.splitlines() if v != "" else [""]
        for k, v in restic_options.items()
    }

    # Override config arguments with arguments from CLI
    if python_args.arguments:
        restic_options['arguments'] = python_args.arguments

    # Extract positional arguments from options dict
    try:
        restic_arguments = restic_options['arguments']
        del restic_options['arguments']
    except KeyError:
        restic_arguments = []

    # Override config options with options from CLI
    python_args_dict = dict(vars(python_args))
    del python_args_dict['preset']
    del python_args_dict['command']
    del python_args_dict['arguments']
    restic_options.update(python_args_dict)

    # Construct command
    argstring = ["restic", f"{python_args.command}"]
    for key, lines in restic_options.items():
        if lines is not None:
            for value in lines:
                if len(key) == 1:
                    argstring.append(f"-{key}")
                else:
                    argstring.append(f"--{key}")
                if value is not None:
                    argstring.append(f"{value}")
    argstring += restic_arguments

    argstring = [val for val in argstring if val != ""]

    if dryrun:
        print("             Warning:", "Executing in debug mode. restic will not run, backups are not touched!")
        print("        Config files:", ", ".join(conffile))
        print("   Config files used:", ", ".join(conffile_read))
        print("     Config sections:", ", ".join(sections))
        print("Config sections used:", ", ".join(sections_read))
        print("        Env sections:", ", ".join(envsections))
        print("   Env sections used:", ", ".join(envsections_read))
        print("    Expanded command:", " ".join(argstring))
        return 0
    else:
        try:
            return subprocess.call(" ".join(argstring), env=restic_environ, shell=True)
        except KeyboardInterrupt:
            return 130


def cli():
    return main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
