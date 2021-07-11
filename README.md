# MOPbx

[![CircleCI](https://circleci.com/gh/niehusst/MOPbx.svg?style=svg)](https://app.circleci.com/pipelines/github/niehusst/MOPbx)

Mop up garbage translation files and clean junk from your .pbxproj file!

If you hate manually cleaning the .pbxproj file in your iOS projects of
empty translation (.strings) files, translation files for .xibs that no
longer exist, or slowly removing pbx references to files that no longer 
exist one by one, then this is the repo/script for you! (Ryan Higa's 
voice echos in your mind; you hear him selling you a DVD about mops.)

## Usage

To use the `mopbx.py` script, you need to provide the paths to your Xcode
project root and to your `project.pbxproj` file. (Paths can be relative
or absolute.)

For example, if your project structure looks something like this:
```
.
├── mopbx.py
├── ExampleProj
│   ├── AppDelegate.swift
│   ├── Assets.xcassets
│   │   ├── AppIcon.appiconset
│   │   │   └── Contents.json
│   │   └── Contents.json
│   ├── Base.lproj
│   │   ├── LaunchScreen.storyboard
│   │   └── Main.storyboard
│   ├── Info.plist
│   ├── SceneDelegate.swift
│   └── ViewController.swift
├── ExampleProj.xcodeproj
│   ├── project.pbxproj
│   ├── project.xcworkspace
│   │   ├── contents.xcworkspacedata
│   │   ├── xcshareddata
│   │   │   └── IDEWorkspaceChecks.plist
│   │   └── xcuserdata
│   │       └── user.xcuserdatad
│   │           └── UserInterfaceState.xcuserstate
│   └── xcuserdata
│       └── user.xcuserdatad
│           └── xcschemes
│               └── xcschememanagement.plist
├── ExampleProjTests
│   ├── ExampleProjTests.swift
│   └── Info.plist
└── ExampleProjUITests
    ├── ExampleProjUITests.swift
    └── Info.plist
```
Then executing your script will be as follows:
```
python mopbx.py -p ExampleProj/ -x ExampleProj.xcodeproj/project.pbxproj
```
And if you decide you want to execute the changes that script wants to make,
you'll need to add the flag `--not-dry` when you run the script. 

## Setup

If you only want to use this script in your own projects, just copy and paste
the script (`MOPbx/src/mopbx.py`); no need to install anything. I purposely 
developed this script to be as dependency-light as possible.

If you want to contribute, install the requirements using
```
pip install -r requirements.txt
```
These dependencies are to assist with testing.

## Testing

This repo uses `pytest`, so to run all tests, you can simply run in you
terminal the following command (after doing the setup process) FROM WITHIN
THE `MOPbx/tests/` DIRECTORY:
```
pytest
```
Running tests from the `MOBPbx/tests/` directory is important because the
relative paths to the test data won't match up otherwise.

## Authors

* [Liam Niehus-Staab](https://github.com/niehusst)

