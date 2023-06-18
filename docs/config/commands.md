---
title: Command Names
subtitle: Configuration
---

## Key Syntax

On the commandline, `crestic` commands follow the syntax

```shell
crestic preset command [--options, ...]
```

Where `preset` is a preset key in the config file, and `command` is the [`restic` command](https://restic.readthedocs.io/en/latest/manual_rest.html).

Crestic config keys follow the convention

```conf
[preset]
[preset.command]
```

where `preset` and `command` are the preset and command names from above. For example

```conf
[home]
...

[home.backup]
...
```

are read for `crestic home backup` calls.

## Special Keys

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


## Mixing Keys

`crestic` allows multiple presets per config file. For example you can define a config file

```conf
[global]
password-file: ~/.config/restic/password
repo: sftp:your_server:my_computer.restic

[global.backup]
exclude-file: ~/.config/restic/excludes

[home.backup]
_args: ~

[work.backup]
_args: ~/work
```

which can be used as `crestic home backup` and `crestic work backup`. Both commands back up using the same `password-file`, `repo`, and `exclude-file`, but different `argument`s (directories that are being backed up.)

## Split Keys

`crestic` allows for so-called *split presets*. These split presets are in the format of `prefix@suffix` and are usually used to separate local location values from remote repo locations, i.e. `location@repo`.

Using this techique you can back up several locations on your machine to several remote repositories, i.e. the locations `home` and `work` to the repos `disk` and `cloud`

```shell
crestic home@disk backup
crestic home@cloud backup
crestic work@disk backup
crestic work@cloud backup
```

To use these split presets, simply define location keys with an `@` suffix

```conf
[home@.backup]
_args: ~

[work@.backup]
_args: ~/work
```

and repo keys with an `@` prefix

```conf
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
