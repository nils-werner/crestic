# Automated Backups using systemd

For daily user backups using systemd timers, put these files in `~/.config/systemd/user/` then activate the timer for your crestic preset, i.e. for `home@nas`

```Shell
systemctl --user enable --now crestic@home@nas.timer
```

For system backups, put these files in `/etc/systemd/system` and the config in `/etc/crestic/config.cfg`

Also see [the Arch Linux package](https://aur.archlinux.org/cgit/aur.git/tree/?h=crestic) for a working solution including systemd timers.
