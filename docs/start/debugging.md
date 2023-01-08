---
title: Debugging
subtitle: Getting Started
---

## Debugging

If you set the environment variable `$CRESTIC_DRYRUN`, crestic will not run restic but instead output

 - the config files in use
 - the config sections in use
 - the final command

```shell
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
