1. Merge pending `for-` branches into `master`
1. Update `CHANGELOG.md`
1. Bump version number in `setup.cfg`
1. Commit version change
1. Run `pytest`
1. Push `master`
1. Check CI tests
1. Merge `master` into `release`
1. Run `pytest`
1. Push `release`
1. Check CI tests
1. Check online docs
1. Tag version number
1. Push tag
1. Release on pypi

   ```
   rm dist/*
   python -m build
   python -m twine upload --repository testpypi dist/*
   python -m twine upload dist/*
   ```

1. Release on AUR

   ```
   makepkg
   sha256sum *.tar.gz
   makepkg --printsrcinfo > .SRCINFO
   ```
