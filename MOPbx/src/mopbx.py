# if you make any additions that could also be useful for someone else,
# consider making a PR!  https://github.com/niehusst/MOPbx

import argparse
import os


# hard-code the path to your pbxproj file here for easier use
default_pbx_path = ""
# hard-code the path to your project root directory here for eaiser use
default_project_root = ""

def remove_empty_translation_files(proj, dry):
    """
    Deletes empty/single-character translation (.strings) files 
    from the project file hierarchy.

    proj - String. path to xcode project root directory
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    print("INFO: Searching for empty .strings files...")
    to_rm = []
    #find files of size less than 2 bytes
    ret_stream = os.popen("find . -name '*.strings' -size -2")
    for file in ret_stream.readlines():
        print(file.strip())
        if not dry:
            os.remove(file.strip())
    ret_stream.close()
    return to_rm

def remove_translation_files_without_source(proj, dry):
    """
    Deletes translation (.strings) files with no corresponding
    .xib/.storyboard file from the project file hierarchy. (Since the
    layout they used to provide translations for no longer exists.)

    proj - String. path to xcode project root directory
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    print("INFO: Searching for unused .strings files...")
    to_rm = []

    return to_rm

def clean_pbx(proj, pbx, dry):
    """
    Remove any pbx references to files that are not in the project
    file hierarchy.

    proj - String. path to xcode project root directory
    pbx - String. path to xcode project project.pbxproj file
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    print("INFO: Searching for dangling pbx references...")
    to_rm = []
    write_target = "tmp.txt" if dry else pbx
    # recursively(?) iterate over all files under proj directory, building a set of file names (no path prefix). 
    # iter every file name in pbx proj and if not in set, rm that line of the file
    return to_rm

def main(args):
    pbx_path = args.get("pbx", "") if args.get("pbx", "") else default_pbx_path
    project_root = args.get("project", "") if args.get("project", "") else default_project_root
    dry_run = args.get("dry")
    if not pbx_path or not project_root:
        print("ERROR: No pbx path or no project path was provided! Either hard-code them into this script or provide them as command line arguments")
        exit(1)
    if dry_run:
        print("INFO: Running in dry-run mode. Run script with '--dry=False' to execute changes.")
    remove_empty_translation_files(project_root, dry_run)
    remove_translation_files_without_source(project_root, dry_run)
    clean_pbx(project_root, pbx_path, dry_run)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project",
        help="Path to your project root directory. (optional if you've manually added a default path)")
    ap.add_argument("-x", "--pbx",
        help="Path to your pbxproj file (optional if you've manually added a default path)")
    ap.add_argument("-d", "--dry", type=bool, default=True,
        help="Dry run mode; running in this mode won't alter your files")
    args = vars(ap.parse_args())
    main(args)
