---
title: Examples
subtitle: Configuration
---

## Simple Example

Simple repository on a remote SFTP server. Repository password is retrieved from keychain using [secret-tool](https://man.archlinux.org/man/secret-tool.1.en).

```conf
[global.backup]
exclude-if-present: .norestic
    CACHEDIR.TAG

[home.backup]
_arguments: ~

[home]
repo: sftp:my-server.com:home.restic
password-command: secret-tool lookup type restic repo home host my-server.com
```

## Multiple Repositories using Split Options

One origin `home` and two destinations `local` and `server`. These can be combined to backup `home@local` and `home@server`.

```conf
[global.backup]
exclude: ~/home.restic
exclude-if-present: .norestic
    CACHEDIR.TAG

[home@.backup]
_arguments: ~

[@local]
repo: ~/home.restic
password-command: secret-tool lookup type restic repo home host local

[@server]
repo: sftp:my-server.com:home.restic
password-command: secret-tool lookup type restic repo home host my-server.com
```
