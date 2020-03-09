Crestic - configurable Restic
=============================

This is a slim configuration wrapper for [Restic](https://restic.readthedocs.io/), a pretty awesome backup tool.

Why? [Because restic is unfortunately still missing config files](https://github.com/restic/restic/issues/16).

Usage
-----

This tool does not try to be clever, it simply maps any commandline options for restic to a key in an INI file. I.e. backing up your home directory with a password and an exclude-file

```Shell
restic backup \
    --repo sftp:your_server:my_computer.restic \
    --password-file ~/.config/restic/password \
    --exclude-file ~/.config/restic/excludes \
    ~
```

can be set in a config file

```INI
# these are the options for any `crestic home` command
[home]
repo: sftp:your_server:my_computer.restic
password-file: ~/.config/restic/password

# these are the options for the `crestic home backup` command
# `arguments` are positional arguments that are appended at the end of the
# commandline. Restic expects the list of directories here.
[home.backup]
exclude-file: ~/.config/restic/excludes
arguments: ~
```

and then called

```Shell
crestic home backup
```

See [examples/multiple_presets.cfg](examples/multiple_presets.cfg) for a more complicated example with multiple repos and directories and forgetting rules.

Installation
------------

Just install it using `pip`

```Shell
pip install git+https://github.com/nils-werner/crestic.git
```

or download `crestic` into your `$PATH`

```Shell
curl https://raw.githubusercontent.com/nils-werner/crestic/master/crestic.py --output ~/.local/bin/crestic
chmod +x ~/.local/bin/crestic
```

### Config File Detection

The following locations are used in descending order of importance:

 - environment variable `$CRESTIC_CONFIG_FILE`, a single filename
 - environment variable `$CRESTIC_CONFIG_PATHS`, a colon separated list of directories
 - `~/.config/crestic/crestic.cfg`
 - `/etc/crestic.cfg`

`crestic` may also optionally use `appdirs` to automatically pick up config files from platform-dependent locations. This is especially useful on macOS or Windows. Just install `appdirs`

```Shell
pip install appdirs
```

Requirements
------------

Plain Python 3.6+ on a UNIX system. Nothing else.

Debugging
---------

If you set the environment variable `$CRESTIC_DRYRUN`, `crestic` will not run `restic` but instead output

 - the config files in use
 - the config sections in use
 - the final command

```Shell
env CRESTIC_CONFIG_FILE=examples/multiple_presets.cfg CRESTIC_DRYRUN=1 crestic home backup
```

will print

```
         Warning: Executing in debug mode. restic will not run, backups are not touched!
    Config files: examples/multiple_presets.cfg
 Config sections: global, global.backup, home, home.backup
Expanded command: restic backup --password-file ~/.config/restic/password --exclude-file ~/.config/restic/excludes --exclude config.py --exclude passwords.txt

```
