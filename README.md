# VCXBase

A simple base for VCX projects, including GitHub workflows, and settings for modern C++ programming.

Made for myself.

### Stuff to note
- `master` branch has automatic 'nightly' builds created on each commit/PR
- `develop` branch has automatic 'develop' builds created on each commit/PR
- If following the [conventional commits spec](https://www.conventionalcommits.org) and [semantic versionning spec](https://semver.org/), making a commit with `<BREAKING CHANGE:|feat:|fix:> bump version to <semantic version>`, it'll automatically publish you a release.

## Installation  

### Method 1  
Rename the folders and references of `VCXBase` inside of VCXBase.sln and VCXBase\VCXBase.vcxproj.
Optionally change the GUID.
It should work fine.

### Method 2 (better?)  
You can also create a new solution.  
Copy .github, .gitignore, .gitattributes and Directory.Build.props.  
Get the `GetGitInfo` target from the .vcxproj and put it on your project.  
That should work.

## Post-install setup

Create a token for your repo and give write access to Contents. Put that in your Actions secret as `TOKEN` for the workflows to work.