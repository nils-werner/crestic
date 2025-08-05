1. Merge pending `for-*` branches into `master`
1. Update `CHANGELOG.md`
1. Bump version number in `pyproject.toml`
1. Commit version change
1. Run pipeline

    ```
    just pre-publish
    ```

1. Push `master`
1. Check CI tests
1. Merge `master` into `release`
1. Run pipeline

    ```
    just pre-publish
    ```

1. Push `release`
1. Check CI tests
1. Check online docs
1. Tag version number
1. Push tag
1. Release on pypi

   ```
   just publish
   ```

1. Release on AUR

   ```
   makepkg
   sha256sum *.tar.gz
   makepkg --printsrcinfo > .SRCINFO
   ```
