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

See [examples/multiple_presets.ini](examples/multiple_presets.ini) for a more complicated example with multiple repos and directories and forgetting rules.

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

Crestic optionally uses `appdirs` to automatically pick up config files from [one of these locations](https://github.com/ActiveState/appdirs):

```Shell
pip install git+https://github.com/nils-werner/crestic.git[appdirs]
```

If this library is unavailable, the following are used in descending order of importance:

 - environment variable `$CRESTIC_CONFIG_FILE`, a single filename
 - environment variable `$CRESTIC_CONFIG_PATHS`, a colon separated list of directories
 - `~/.config/crestic/crestic.ini`
 - `/etc/crestic.ini`

Requirements
------------

Plain Python 3.6+ on a UNIX system. Nothing else.

Debugging
---------

If you set the environment variable `$CRESTIC_DRYRUN`, `crestic` will output the final command instead of running it. I.e.

```Shell
env CRESTIC_DRYRUN=1 crestic home backup
```

will print

```Shell
restic backup --repo sftp:your_server:my_computer.restic --password-file ~/.config/restic/password --exclude-file ~/.config/restic/excludes ~
```
