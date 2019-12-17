Crestic -- Configurable Restic
==============================

This is a slim configuration wrapper for [Restic](https://restic.readthedocs.io/), a pretty awesome backup tool.

Why? [Because restic is unfortunately still missing config files](https://github.com/restic/restic/issues/16).

Usage
-----

This tool does not try to be clever, it simply maps any parameter for restic to a key in an INI file. I.e. backing up your home directory with a password and an exclude-file

    restic backup --password-file /home/me/.config/restic/password --exclude-file /home/me/.config/restic/excludes --repo sftp:your_server:my_computer.restic /home/me

becomes

    [home]          # <- this is a preset `home`
    password-file: /home/me/.config/restic/password
    repo: sftp:your_server:my_computer.restic

    [home.backup]   # <- this is for the command `backup` in the preset `home`
    exclude-file: /home/me/.config/restic/excludes
    params: /home/me

and then a simple call to

    crestic home backup

See [examples/multiple_presets.ini](examples/multiple_presets.ini) for a more complicated example with multiple repos and directories.

Installation
------------

Just place `crestic` in your `$PATH` and set the environment variable `$CRESTIC_CONFIG_FILE`, i.e.

    curl https://raw.githubusercontent.com/nils-werner/crestic/master/crestic --output ~/.local/bin/crestic
    echo "export CRESTIC_CONFIG_FILE=~/.config/restic/crestic.ini" >> .bashrc

Requirements
------------

Python 3 on a UNIX system.

Debugging
---------

If you set the environment variable `$CRESTIC_DRYRUN`, `crestic` will output the final command instead of running it.
