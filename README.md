Crestic -- Configurable Restic
==============================

This is a slim configuration wrapper for [Restic](https://restic.readthedocs.io/), a pretty awesome backup tool.

Why? [Because restic is unfortunately still missing config files](https://github.com/restic/restic/issues/16).

Usage
-----

This tool does not try to be clever, it simply maps any parameter for restic to a key in an INI file. I.e. backing up your home directory with a password and an exclude-file

    restic backup \
        --password-file ~/.config/restic/password \
        --exclude-file ~/.config/restic/excludes \
        --repo sftp:your_server:my_computer.restic \
        ~

becomes

    crestic home backup

after creating a config file like

    [home]
    password-file: ~/.config/restic/password
    repo: sftp:your_server:my_computer.restic

    [home.backup]
    exclude-file: ~/.config/restic/excludes
    params: ~

See [examples/multiple_presets.ini](examples/multiple_presets.ini) for a more complicated example with multiple repos and directories.

Installation
------------

Just place `crestic` in your `$PATH` and set the environment variable `$CRESTIC_CONFIG_FILE`, i.e.

    curl https://raw.githubusercontent.com/nils-werner/crestic/master/crestic --output ~/.local/bin/crestic
    chmod +x ~/.local/bin/crestic
    echo "export CRESTIC_CONFIG_FILE=~/.config/restic/crestic.ini" >> .bashrc

Requirements
------------

Python 3 on a UNIX system.

Debugging
---------

If you set the environment variable `$CRESTIC_DRYRUN`, `crestic` will output the final command instead of running it.
