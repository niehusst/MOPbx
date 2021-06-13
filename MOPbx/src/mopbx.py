# if you make any additions that could also be useful for someone else,
# consider making a PR!  https://github.com/niehusst/MOPbx

import argparse


# hard-code the path to your pbxproj file here for easier use
default_pbx_path = ""
# hard-code the path to your project root directory here for eaiser use
default_project_root = ""

def remove_empty_translation_files(proj, pbx, dry):
    """
    Deletes empty/single-character translation (.strings) files 
    from the project file hierarchy.

    proj - String. path to xcode project root directory
    pbx - String. path to xcode project project.pbxproj file
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    pass

def remove_translation_files_without_source(proj, pbx, dry):
    """
    Deletes translation (.strings) files with no corresponding
    .xib/.storyboard file from the project file hierarchy. (Since the
    layout they used to provide translations for no longer exists.)

    proj - String. path to xcode project root directory
    pbx - String. path to xcode project project.pbxproj file
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    pass

def clean_pbx(proj, pbx, dry):
    """
    Remove any pbx references to files that are not in the project
    file hierarchy.

    proj - String. path to xcode project root directory
    pbx - String. path to xcode project project.pbxproj file
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    pass

def main(args):
    pbx_path = args.get("pbx", "") if args.get("pbx", "") else default_pbx_path
    project_root = args.get("project", "") if args.get("project", "") else default_project_root
    dry_run = args.get("dry")
    if not pbx_path or not project_root:
        print("ERROR: No pbx path or no project path was provided! Either hard-code them into this script or provide them as command line arguments")
        exit(1)
    remove_empty_translation_files(project_root, pbx_path, dry_run)
    remove_translation_files_without_source(project_root, pbx_path, dry_run)
    clean_pbx(project_root, pbx_path, dry_run)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project",
        help="Path to your project root directory. (optional if you've manually added a default path)")
    ap.add_argument("-x", "--pbx",
        help="Path to your pbxproj file (optional if you've manually added a default path)")
    ap.add_argument("-d", "--dry", type=bool, default=False,
        help="Dry run mode; running in this mode won't alter your files")
    args = vars(ap.parse_args())
    main(args)
