---
title: Options Syntax
subtitle: Configuration
---

Crestic uses a distinct INI file syntax to that maps to special command line arguments:

## Positional Arguments

{% include notification.html message="This syntax was changed in version 0.8.0. Previously, the key was called `arguments:`" status="is-warning" %}

Positional arguments are given using the `_arguments:` key:

```conf
[home.backup]
_arguments: ~
```

## Repeating Options

To give a commandline option more than once, use a multi line config value:

```conf
[home.backup]
exclude: *.secret
   *.bin
```

is mapped to

```shell
restic backup --exclude *.secret --exclude *.bin
```

## Option Switches

{% include notification.html message="This syntax was changed in version 0.7.0. Previously, a following colon was required." status="is-warning" %}

To give an empty commandline option (a switch option), just provide the word without a following colon (`:`) or equal sign (`=`)

```conf
[home.backup]
verbose
```

is mapped to

```shell
restic backup --verbose
```

## Environment Variables

Environment variables can be set using the `[preset.environ]` section.

```conf
[home.environ]
B2_ACCOUNT_ID: <MY_APPLICATION_KEY_ID>
B2_ACCOUNT_KEY: <MY_APPLICATION_KEY>
```

## Command Aliases

{% include notification.html message="The `_command:` key was introduced in version 0.8.0." status="is-warning" %}

You can define command aliases by using the `_command:` key, e.g.

```conf
[home.my_alias]
_command: backup
```

will allow you to run `crestic home my_alias`, which is then mapped to `restic backup`.

## Working Directory

{% include notification.html message="The `_workdir:` key was introduced in version 0.8.0." status="is-warning" %}

You can set a working directory using the `_workdir:` key, e.g.

```conf
[home.backup]
_workdir: ~
```

which will cause `restic` to be run in that directory. All other paths will be relative to this directory.

However, it is recommended to use absolute paths wherever possible because the backup path will be saved in the backup while the working directory does not. Using relative paths may then cause ambiguity and confusion.
