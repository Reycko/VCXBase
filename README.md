# VCXBase

Simple base for VCX projects, including GitHub workflows, git support (conventional commits), and settings to quickly get started with modern C++ programming.

Made for myself.

### Stuff to note
- `master` branch has automatic 'nightly' builds created on each commit/PR
- `develop` branch has automatic 'develop' builds created on each commit/PR
- If following the [conventional commits spec](https://www.conventionalcommits.org) and [semantic versionning spec](https://semver.org/),  making a commit with `<BREAKING CHANGE:|feat:|fix:> bump version to <semantic version>`, it'll automatically publish you a release.

## Installation  

### Method 1  
You're basically gonna have to rename the folders and references inside of VCXBase.sln and VCXBase\VCXBase.vcxproj  
Rename the solution, .vcxproj, and the vcxproj files (.filters, .user) in file explorer   Optionally change the GUID  
And it should work fine.

### Method 2 (better?)  
You can also make a new solution  
Copy the .github, .gitignore & .gitattributes, and Directory.Build.props  
Grab the `GetGitInfo` Target from the .vcxproj and put it in yours.  
That should also work.

## Post-install setup

Make sure to create yourself a token (fine-grained or classic) for your repo, and give write access to Contents, then put that in your Actions secret as `TOKEN` for the workflows to work.