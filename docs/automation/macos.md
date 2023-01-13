---
title: MacOS
subtitle: Automation
---

## launchctl

For daily user backups using launchctl timers, i.e. for the `home@nas` preset, put the following in `~/Library/LaunchAgents/local.crestic.home@nas.plist`

```xml
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

then activate the timer using

```shell
launchctl load ~/Library/LaunchAgents/local.crestic.home@nas.plist
```

For system backups, put this file in `/Library/LaunchAgents` and the config in `/etc/crestic/crestic.cfg`
