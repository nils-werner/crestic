---
title: Options Syntax
subtitle: Configuration
---

Crestic uses a distinct INI file syntax to that maps to special command line arguments:

## Positional Arguments

{% include notification.html message="This syntax was changed in version 0.8.0. Previously, the key was called `arguments:`" status="is-warning" %}

Positional arguments are given using the `_args:` key:

```conf
[home.backup]
_args: ~
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
