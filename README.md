# VCXBase

A simple base for VCX projects, including GitHub workflows, and settings for modern C++ programming.

Made for myself.

### Stuff to note
> [!NOTE]  
> If your commit ends with `[skip ci]`, none of these will run.
- `master` branch has automatic 'nightly' builds created on each commit/PR
- `develop` branch has automatic 'develop' builds created on each commit/PR
- If following the [conventional commits spec](https://www.conventionalcommits.org) and [semantic versionning spec](https://semver.org/), making a commit with `<BREAKING CHANGE|feat|fix>: bump version to <semantic version>`, it'll automatically publish you a release.

## Installation  

Run the setup.py file.  
`-h` or `--help` will show you the available command line inputs. Providing no arguments will prompt you everything in your terminal window.
