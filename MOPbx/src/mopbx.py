# if you make any additions that could also be useful for someone else,
# consider making a PR!  https://github.com/niehusst/MOPbx

import argparse


# hard-code the path to your pbxproj file here for easier use
pbx_path = ""

def remove_empty_translation_files():
    pass

def remove_translation_files_without_xib():
    pass

def clean_pbx(override_path):
    if override_path:
        pbx_path = override_path
    return

def main(args):
    remove_empty_translation_files()
    remove_translation_files_without_xib()
    clean_pbx(args.get("path", False))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path",
        help="Path to your pbxproj file. (optional if you've manually added a default path)")
    ap.add_argument("-d", "--dry", type=bool, default=False,
        help="Dry run mode; running in this mode won't alter your files")
    args = vars(ap.parse_args())
    main(args)
