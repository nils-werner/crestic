---
title: Config Files
subtitle: Configuration
---

## Config File Locations

The following locations are used in ascending order of importance. All files are read, and values in later files override values in earlier ones:

 1. `/usr/share/crestic/config.cfg`
 1. `/usr/share/crestic/conf.d/*.cfg`
 1. `/etc/crestic/config.cfg`
 1. `/etc/crestic/conf.d/*.cfg`
 1. `~/.config/crestic/config.cfg`
 1. `~/.config/crestic/conf.d/*.cfg`
 1. environment variable `$CRESTIC_CONFIG_PATHS`, a colon separated list of files

The environment variable `$CRESTIC_CONFIG_FILE` can be used to override the joint loading behaviour. After setting this variable, no other files will be read.
