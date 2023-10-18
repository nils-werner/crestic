## Changelog

### Next Release

### `1.0.0`

 - Changed behaviour of old `--switch` syntax (`empty:` with a following colon) to new `--empty ''` behaviour (#30)
 - Removed `arguments:` key
 - Enabled environment variable expansion in `[.environ]` sections (#36)

### `0.8.0`

 - Deprecated `arguments:` in favor of `_arguments:`
 - `_workdir:` parameter for setting a working directory
 - `_command:` parameter for creating command aliases
 - Enabled `ExtendedInterpolation`

### `0.7.0`

 - Introduce new `--switch` syntax (`switch` without a following colon) (#30)
 - Add DeprecationWarning for old `--switch` syntax (`switch:` with a following colon) (#30)
