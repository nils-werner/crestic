Crestic - configurable Restic
=============================

This is a slim configuration wrapper for [Restic](https://restic.readthedocs.io/), a pretty awesome backup tool.

Why? [Because restic is unfortunately still missing config files](https://github.com/restic/restic/issues/16).

Usage
-----

The goal of `crestic` is to make running `restic` easy, e.g. creating backups using

```Shell
crestic home backup
```

instead of running complex `restic` commands

```Shell
restic backup \
    --repo sftp:your_server:my_computer.restic \
    --password-file ~/.config/restic/password \
    --exclude-file ~/.config/restic/excludes \
    ~
```

To achieve this, this tool does not try to be clever, it simply maps any *commandline options* for `restic` to a *key in an config file*:

```INI
[home]
repo: sftp:your_server:my_computer.restic
password-file: ~/.config/restic/password

[home.backup]
exclude-file: ~/.config/restic/excludes
_arguments: ~
```

More advanced usage examples can be found [in the docs](https://nils-werner.github.io/crestic/)
