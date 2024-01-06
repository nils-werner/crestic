#!/usr/bin/env python3

# mypy: disallow-untyped-defs

import os
import re
import sys
import glob
import argparse
import warnings
import subprocess
import configparser

from typing import Optional, Dict, List


def config_files(environ: Optional[Dict[str, str]] = None) -> List[str]:
    if environ is None:
        environ = {}

    # Lowest priority: hardcoded values
    paths = [
        "/usr/share/crestic/config.cfg",
        *sorted(glob.glob("/usr/share/crestic/conf.d/*.cfg")),
        "/etc/crestic/config.cfg",
        *sorted(glob.glob("/etc/crestic/conf.d/*.cfg")),
        pathexpand("~/.config/crestic/config.cfg"),
        *sorted(glob.glob(pathexpand("~/.config/crestic/conf.d/*.cfg"))),
    ]

    # Medium priority: CRESTIC_CONFIG_PATHS
    try:
        paths = paths + [
            f
            for d in environ["CRESTIC_CONFIG_PATHS"].split(os.pathsep)
            for f in sorted(glob.glob(pathexpand(d)))
        ]
    except KeyError:
        pass

    # High priority: CRESTIC_CONFIG_FILE, dropping the rest
    try:
        paths = [environ["CRESTIC_CONFIG_FILE"]]
    except KeyError:
        pass

    return paths


def split(string: str, delimiter: str = "@", maxsplit: int = 1) -> List[str]:
    """
    Split a string using a delimiter string. But keep the delimiter in all returned segments

    """
    splits = string.split(delimiter, maxsplit=maxsplit)
    splits[1:] = [delimiter + s for s in splits[1:]]
    splits[:-1] = [s + delimiter for s in splits[:-1]]
    return splits


def valid_preset(value: str) -> str:
    if not re.match(r"^[^@]+(@[^@]+)?$", value):
        raise argparse.ArgumentTypeError(
            "%s is an invalid preset name, only preset names in the format of name[@suffix] are allowed."
            % value
        )
    return value


def pathexpand(val: str) -> str:
    return os.path.expanduser(os.path.expandvars(val))


def splitlines(val: str) -> List[str]:
    """
    str.splitlines() that is tolerant to empty strings and None values

    """
    if val == "":
        return [""]
    if val is None:
        return [None]
    else:
        return val.splitlines()


def main(
    argv: List[str],
    environ: Optional[os._Environ[str]] = None,
    conffile: Optional[List[str]] = None,
    dryrun: Optional[bool] = None,
    executable: Optional[str] = None,
) -> int:
    if environ is None:
        environ = os.environ

    if conffile is None:
        conffile = config_files(dict(environ))

    if dryrun is None:
        dryrun = bool(environ.get("CRESTIC_DRYRUN", False))

    if executable is None:
        executable = environ.get("CRESTIC_EXECUTABLE", "restic")

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("preset", nargs="?", type=valid_preset)
    parser.add_argument("command", help="the restic command")

    # CLI options that override values given in config file
    for arg in argv:
        if arg.startswith(("-", "--")) and arg != "--":
            try:
                parser.add_argument(
                    arg, nargs="?", action="append", dest=arg.lstrip("-")
                )
            except argparse.ArgumentError:
                pass

    parser.add_argument(
        "arguments", nargs="*", help="positional arguments for the restic command"
    )
    try:
        python_args = parser.parse_intermixed_args(argv)
    except AttributeError:
        python_args = parser.parse_args(argv)

    config = configparser.ConfigParser(
        allow_no_value=True,
        interpolation=configparser.ExtendedInterpolation(),
    )
    # dont map config keys to lower case
    config.optionxform = str  # type: ignore
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
            restic_options.update(dict(config[section]))
            sections_read.append(section)
        except KeyError:
            pass

    # Load restic environment variables from config, in ascending precedence
    restic_environ = dict(environ)
    envsections_read = []
    for envsection in envsections:
        try:
            restic_environ.update(
                {k: pathexpand(v) for k, v in dict(config[envsection]).items()}
            )
            envsections_read.append(envsection)
        except KeyError:
            pass

    restic_options_split = {
        k: splitlines(v) for k, v in restic_options.items()
    }

    command = python_args.command

    # Override config arguments with arguments from CLI
    if python_args.arguments:
        restic_options_split["_arguments"] = python_args.arguments

    # Extract positional arguments from options dict
    try:
        restic_arguments = restic_options_split["_arguments"]
        del restic_options_split["_arguments"]
    except KeyError:
        restic_arguments = []

    # Extract workdir from options dict
    try:
        workdir = restic_options_split["_workdir"][0]
        del restic_options_split["_workdir"]
    except KeyError:
        workdir = os.getcwd()
    workdir = pathexpand(workdir)

    # Extract command overload
    try:
        command = restic_options_split["_command"][0]
        del restic_options_split["_command"]
    except KeyError:
        pass

    # Override config options with options from CLI
    python_args_dict = dict(vars(python_args))
    del python_args_dict["preset"]
    del python_args_dict["command"]
    del python_args_dict["arguments"]
    restic_options_split.update(python_args_dict)

    # Construct command
    argstring = [executable]
    argstring.append(f"{command}")
    for key, lines in restic_options_split.items():
        for value in lines:
            if len(key) == 1:
                argstring.append(f"-{key}")
            else:
                argstring.append(f"--{key}")
            if value is not None:
                argstring.append(f"{value}")
    argstring += restic_arguments

    argstring = [pathexpand(val) for val in argstring]

    if dryrun:
        print(
            "             Warning:",
            "Executing in debug mode. restic will not run, backups are not touched!",
        )
        print("        Config files:", ", ".join(conffile))
        print("   Config files used:", ", ".join(conffile_read))
        print("     Config sections:", ", ".join(sections))
        print("Config sections used:", ", ".join(sections_read))
        print("        Env sections:", ", ".join(envsections))
        print("   Env sections used:", ", ".join(envsections_read))
        print("   Working directory:", workdir)
        print("    Expanded command:", '"' + ('" "'.join(argstring)) + '"')
        return 1
    else:
        os.chdir(workdir)
        return os.execvpe(argstring[0], argstring, env=restic_environ)


def cli() -> int:
    return main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
