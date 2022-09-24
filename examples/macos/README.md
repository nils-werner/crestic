# Automated Backups using launchctl

For daily user backups using launchctl timers, i.e. for the `home@nas` preset, put this file in `~/Library/LaunchAgents/`, then activate the timer

```Shell
launchctl load ~/Library/LaunchAgents/local.crestic.home@nas.plist
```

For system backups, put this file in `/Library/LaunchAgents` and the config in `/etc/crestic.cfg`
