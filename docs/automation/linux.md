---
title: Linux
subtitle: Automation
---

## systemd

For daily user backups using systemd timers, put the following `~/.config/systemd/user/crestic@.service`

```config
[Unit]
Description=crestic %I backup

[Service]
Nice=19
IOSchedulingClass=idle
KillSignal=SIGINT
ExecStart=/usr/bin/crestic %I backup
```

and the following in `~/.config/systemd/user/crestic@.timer`

```config
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

```shell
systemctl --user enable --now crestic@home@nas.timer
```

For system backups, put these files in `/etc/systemd/system` and the config in `/etc/crestic/config.cfg`.

Also see [the Arch Linux package](https://aur.archlinux.org/cgit/aur.git/tree/?h=crestic) for a working solution including systemd timers.
