# MOPbx

[![CircleCI](https://circleci.com/gh/niehusst/MOPbx.svg?style=svg)](https://app.circleci.com/pipelines/github/niehusst/MOPbx)

Mop up garbage translation files and clean junk from your .pbxproj file!

If you hate manually cleaning the .pbxproj file in your iOS projects of
empty translation (.strings) files, translation files for .xibs that no
longer exist, or slowly removing pbx references to files that no longer 
exist one by one, then this is the repo/script for you! (Ryan Higa's 
voice echos in your mind; you hear him selling you a DVD about mops.)

## Setup

If you want to use this script in your own projects, just copy and paste
the script (`src/mopbx.py`); no need to install anything. I purposely 
developed this script to be as dependency-light as possible.

If you want to contribute, install the requirements using
```
pip install -r requirements.txt
```
These dependencies are to assist with testing.

## Testing

This repo uses `pytest`, so to run all tests, you can simply run in you
terminal the following command (after doing the setup process):
```
pytest --rootdir=tests
```

## Authors

* [Liam Niehus-Staab](https://github.com/niehusst)

