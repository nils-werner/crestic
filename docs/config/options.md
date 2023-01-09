---
title: Options Syntax
subtitle: Configuration
---

Crestic uses a distinct INI file syntax to that maps to special command line arguments:

## Positional Arguments

Positional arguments are given using the `arguments:` key:

```conf
[home.backup]
arguments: ~
```

## Repeating Options

To give a commandline option more than once, use a multi line config value:

```conf
[home.backup]
exclude:
   *.secret
   *.bin
```

is mapped to

```shell
restic backup --exclude *.secret --exclude *.bin
```

## Option Switches

To give an empty commandline option (a switch option), provide the word with an empty value:

```conf
[home.backup]
verbose:
```

is mapped to

```shell
restic backup --verbose
```
