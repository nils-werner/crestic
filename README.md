Crestic - configurable Restic
=============================

This is a slim configuration wrapper for [Restic](https://restic.readthedocs.io/), a pretty awesome backup tool.

Why? [Because restic is unfortunately still missing config files](https://github.com/restic/restic/issues/16).

Usage
-----

This tool does not try to be clever, it simply maps any *commandline options* for `restic` to a *key in an config file*.

For example, to use `restic` to back up your home directory with a password and an exclude-file, you would use

```Shell
restic backup \
    --repo sftp:your_server:my_computer.restic \
    --password-file ~/.config/restic/password \
    --exclude-file ~/.config/restic/excludes \
    ~
```

With `crestic`, you can set all these values in a config file

```INI
[home]
repo: sftp:your_server:my_computer.restic
password-file: ~/.config/restic/password

[home.backup]
exclude-file: ~/.config/restic/excludes
arguments: ~
```

and then call one simple command

```Shell
crestic home backup
```

More advanced usage examples can be found further down this file.

Installation
------------

Just install it using `pip`

```Shell
pip install crestic
```

or download `crestic` into your `$PATH`

```Shell
curl https://raw.githubusercontent.com/nils-werner/crestic/master/crestic.py --output ~/.local/bin/crestic
chmod +x ~/.local/bin/crestic
```

### Config File Detection

The following locations are used in descending order of importance:

 - environment variable `$CRESTIC_CONFIG_FILE`, a single filename
 - environment variable `$CRESTIC_CONFIG_PATHS`, a colon separated list of directories containing a file `crestic.cfg`
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
env CRESTIC_DRYRUN=1 crestic home backup
```

will print

```
             Warning: Executing in debug mode. restic will not run, backups are not touched!
        Config files: examples/multiple_presets.cfg
   Config files used: examples/multiple_presets.cfg
     Config sections: global, global.backup, home, home.backup
Config sections used: global, global.backup
        Env sections: global.environ, global.backup.environ, home.environ, home.backup.environ
   Env sections used:
    Expanded command: restic backup --password-file ~/.config/restic/password --exclude-file ~/.config/restic/excludes --exclude config.py --exclude passwords.txt
```

Config File Parsing
-------------------

On the commandline, `crestic` commands follow the syntax

```Shell
crestic preset command [--options, ...]
```

Where `preset` is a preset key in the config file, and `command` is the `restic` command.

Crestic config keys follow the convention

```INI
[preset]
[preset.command]
```

where `preset` and `command` are the preset and command names from above. For example

```INI
[home]
...
[home.backup]
...
```

are read for `crestic home backup` calls.

There exist a few special config keys:

 - `[global]` is a special pseudo preset which is always read *before* any actual preset value.
 - `[global.command]` is a special pseudo command which is always read *before* any actual preset command. These two keys can be used to set global values, valid for any preset, i.e. a password-file
 - `[global.environ]`, `[preset.environ]`, `[global.command.environ]` and `[preset.command.environ]` are special pseudo commands which are used to set environment variables for the `restic` command. They are usually used to set [cloud provider credentials](https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#amazon-s3).

Config keys are always read in the following order, of ascending importance. Later values override earlier ones:

 1. `[global]`
 1. `[global.command]`
 1. `[preset]`
 1. `[preset.command]`
 1. options from the commandline

Advanced Usage
--------------

### Multiple preset

`crestic` allows multiple presets per config file, so you can define config files

```INI
[global]
password-file: ~/.config/restic/password

[global]
repo: sftp:your_server:my_computer.restic

[global.backup]
exclude-file: ~/.config/restic/excludes

[home.backup]
arguments: ~

[work.backup]
arguments: ~/work
```

Which can be used as `crestic home backup` and `crestic work backup`

See [examples/multiple_presets.cfg](examples/multiple_presets.cfg) for a more complicated example with multiple repos and directories and forgetting rules.

### Split preset

`crestic` allows for so-called *split presets*. These split presets are in the format of `prefix@suffix` and are usually used to separate local location values from remote repo locations, i.e. `location@repo`.

Using this techique you can back up several locations on your machine to several remote repositories, i.e. a `home` and a `work` location to a `disk` and a `cloud` repo

```Shell
crestic home@disk backup
crestic home@cloud backup
crestic work@disk backup
crestic work@cloud backup
```

To use these split presets, simply define location keys with an `@` suffix

```INI
[home@.backup]
arguments: ~

[work@.backup]
arguments: ~/work
```

and repo keys with an `@` prefix

```INI
[@disk]
repo: /Volumes/Backup

[@cloud]
repo: b2:bucketname:my_computer.restic

[@cloud.environ]
B2_ACCOUNT_ID: <MY_APPLICATION_KEY_ID>
B2_ACCOUNT_KEY: <MY_APPLICATION_KEY>
```

Split config keys are always read in the following order, of ascending importance. Later values override earlier ones:

 1. `[global]`
 1. `[global.command]`
 1. `[@repo]`
 1. `[@repo.command]`
 1. `[location@]`
 1. `[location@.command]`
 1. `[location@repo]`
 1. `[location@repo.command]`
 1. options from the commandline

See [examples/split_presets.cfg](examples/split_presets.cfg) for a complete example of `location@repo` *split presets*.

### Automated Backups

Make sure to adjust the path to the `crestic` executable in the following sections.

#### Linux/systemd

For daily user backups using systemd timers, create a file `~/.config/systemd/user/crestic@.service`

```INI
[Unit]
Description=crestic %I backup

[Service]
Nice=19
IOSchedulingClass=idle
KillSignal=SIGINT
ExecStart=/usr/bin/crestic %I backup
```

and a file `~/.config/systemd/user/crestic@.timer`

```INI
[Unit]
Description=Daily crestic %I backup

[Timer]
OnCalendar=daily
AccuracySec=1m
RandomizedDelaySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```

then activate the timer for your crestic preset, i.e. for `home@nas`


```Shell
systemctl --user enable --now crestic@home@nas.timer
```

For system backups, put these files in `/etc/systemd/system` and the config in `/etc/crestic.cfg`

Also see [the Arch Linux package](https://aur.archlinux.org/cgit/aur.git/tree/?h=crestic) for a working solution including systemd timers.

#### macOS/launchctl

For daily user backups using launchctl timers, i.e. for the `home@nas` preset, create a file `~/Library/LaunchAgents/local.crestic.home@nas.plist`

```XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Daily crestic home@nas backup</key>
    <string>local.crestic.home@nas</string>
    <key>ProgramArguments</key>
    <array>
        <string>crestic</string>
        <string>home@nas</string>
        <string>backup</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
</dict>
</plist>
```

then activate the timer


```Shell
launchctl load ~/Library/LaunchAgents/local.crestic.home@nas.plist
```

For system backups, put this file in `/Library/LaunchAgents` and the config in `/etc/crestic.cfg`
