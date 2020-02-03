#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import configparser


def main(argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("preset", nargs="?")
    parser.add_argument("command", help="the restic command")

    # CLI options that override values given in config file
    for arg in argv:
        if arg.startswith(("-", "--")) and arg != "--":
            parser.add_argument(arg, nargs='?', dest=arg.lstrip("-"))

    parser.add_argument(
        "arguments", nargs="*", help="positional arguments for the restic command"
    )
    python_args = parser.parse_args(argv)

    config = configparser.ConfigParser()
    config.optionxform = str  # dont map config keys to lower case
    config.read(os.environ['CRESTIC_CONFIG_FILE'])

    sections = [
        "global",
        f"global.{python_args.command}",
    ]
    if python_args.preset is not None:
        sections += [
            f"{python_args.preset}",
            f"{python_args.preset}.{python_args.command}",
        ]

    # Load restic options from config, in ascending precedence
    restic_options = {}
    for section in sections:
        try:
            restic_options.update(**dict(config[section]))
        except KeyError:
            pass

    # Load restic environment variables from config, in ascending precedence
    restic_environ = dict(os.environ)
    for section in sections:
        try:
            restic_environ.update(**dict(config[f"{section}.environ"]))
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
    python_args_dict = {
        k: v.splitlines() if v is not None else [""]
        for k, v in python_args_dict.items()
    }
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

    if os.environ.get("CRESTIC_DRYRUN", False):
        print(" ".join(argstring))
    else:
        try:
            sys.exit(
                subprocess.call(" ".join(argstring), env=restic_environ, shell=True)
            )
        except KeyboardInterrupt:
            sys.exit(130)


def cli():
    return main(sys.argv[1:])


if __name__ == "__main__":
    main(sys.argv[1:])
