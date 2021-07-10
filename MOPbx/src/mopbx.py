# if you make any additions that could also be useful for someone else,
# consider making a PR!  https://github.com/niehusst/MOPbx

import argparse
import os
import re


# hard-code the path to your pbxproj file here for easier use
default_pbx_path = ""
# hard-code the path to your project root directory here for eaiser use
default_project_root = ""

pbx_file_cache = None
filesystem_cache = None

section_begin_matcher = re.compile(r"Begin ([a-zA-Z]*) section")
section_end_matcher = re.compile(r"End ([a-zA-Z]*) section")
fname_matcher = re.compile(r"^\s*[A-Z0-9]+ \/\* ([a-zA-Z0-9]+\.[a-zA-Z0-9]+)[a-zA-Z\s]* \*\/")
strings_matcher = re.compile(r"^\s*[A-Z0-9]+ \/\* [a-zA-z\-]+ \*\/.*path = [a-zA-Z\-]+.lproj\/([a-zA-Z0-9\.]+);")

groups_to_check = set(["PBXBuildFile", "PBXFileReference", "PBXGroup", "PBXResourcesBuildPhase", "PBXSourcesBuildPhase", ]) #TODO PBXVariantGroup
# complete file names and file extensions to not remove
to_ignore = set(["xctest", "InfoPlist.strings", "app", "Assets.xcassets"])


def remove_empty_translation_files(proj, dry):
    """
    Deletes empty/single-character translation (.strings) files 
    from the project file hierarchy.

    proj - String. path to xcode project root directory
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    # TODO: skip *Plist.strings
    print("INFO: Searching for empty .strings files...")
    to_rm = []
    #find files of size less than 2 bytes
    ret_stream = os.popen(f"find {proj} -name '*.strings' -size -2c")
    for file in ret_stream.readlines():
        f = file.strip()
        print(f)
        if not dry:
            os.remove(f)
        else:
            to_rm.append(f)
    ret_stream.close()
    return list(map(_remove_dup_slashes, to_rm))

def remove_translation_files_without_source(proj, dry):
    """
    Deletes translation (.strings) files with no corresponding
    .xib/.storyboard file from the project file hierarchy. (Since the
    layout they used to provide translations for no longer exists.)

    proj - String. path to xcode project root directory
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    # TODO: skip *Plist.strings
    print("INFO: Searching for unused .strings files...")
    to_rm = []
    fs_files = _get_flattened_files(proj, not dry)

    # find strings files w/o name match
    match_layout = lambda fname: fname.split(".")[-1] == "xib" or fname.split(".")[-1] == "storyboard"
    match_strings = lambda fname: fname.split(".")[-1] == "strings"
    strip_extension = lambda fname: ".".join(fname.split(".")[:-1])
    layout_fnames = set(map(strip_extension, filter(match_layout, fs_files)))
    strings_fnames = map(strip_extension, filter(match_strings, fs_files))

    for file in strings_fnames:
        if file not in layout_fnames:
            to_rm.append(file + ".strings")

    print(f"removing: {', '.join(to_rm)}")
    dry_ret = []
    for file in to_rm:
        # get the files full path so we can remove it
        ret_stream = os.popen(f"find {proj} -name '{file}'")
        files = ret_stream.readlines()
        if len(files) != 1:
            print(f"ERROR: Oops! Found more than 1 file named {file}. You decide how to fix this.")
            print(files)
        elif not dry:
            os.remove(files[0].strip())
        else:
            dry_ret.append(files[0].strip())

        ret_stream.close()

    return list(map(_remove_dup_slashes, dry_ret))

def clean_pbx(proj, pbx, dry):
    """
    Remove any pbx references to files that are not in the project
    file hierarchy. Writes new in-progress pbxproj file to a local
    file (located at `write_target_name`) which is erased after use
    when `dry` is False.

    proj - String. path to xcode project root directory
    pbx - String. path to xcode project project.pbxproj file
    dry - Bool. whether or not to actually perform operations. 
                (Only prints actions it would take when True)
    """
    global section_begin_matcher
    global groups_to_check
    global to_ignore
    print("INFO: Searching for dangling pbx references...")
    to_rm = set()
    pbx_files = _get_pbx_files(pbx, not dry)
    fs_files = set(_get_flattened_files(proj, not dry))
    write_target_fname = "tmp_pbx.txt" 
    
    for file in pbx_files:
        file_ext = file.split(".")[-1]
        # mark for removal files that aren't in the file sys and also arent 
        # special pbx refs that should be ignored
        if file not in fs_files and file not in to_ignore and file_ext not in to_ignore:
            to_rm.add(file)

    print(f"removing references: {', '.join(to_rm)}")
    if to_rm:
        # write new pbx to temp, skipping files to rm
        rfile = open(pbx, 'r')
        wfile = open(write_target_fname, 'w')

        for line in rfile:
            section = section_begin_matcher.search(line)
            if section and section.group(1) in groups_to_check:
                # write section begin line before passing off to helper
                wfile.write(line)
                _clear_marked_files_from_section(rfile, wfile, to_rm)
            else:
                # normally write all lines we dont care about checking
                wfile.write(line)

        rfile.close()
        wfile.close()

        # copy over tmp file content to og pbx and rm tmp file
        if not dry:
            os.replace(write_target_fname, pbx)
            #os.remove(write_target_fname)
        else:
            print(f"INFO: Wrote what new pbxproj file would contain to {write_target_fname}")
    else:
        print("pbxproj file is alredy clean!")

    return list(to_rm)

def main(args):
    pbx_path = args.get("pbx", "") if args.get("pbx", "") else default_pbx_path
    project_root = args.get("project", "") if args.get("project", "") else default_project_root
    dry_run = not args.get("not-dry")
    if not pbx_path or not project_root:
        print("ERROR: No pbx path or no project path was provided! Either hard-code them into this script or provide them as command line arguments")
        exit(1)
    if dry_run:
        print("INFO: Running in dry-run mode. Run script with the flag '--not-dry' to execute changes.")
    remove_empty_translation_files(project_root, dry_run)
    remove_translation_files_without_source(project_root, dry_run)
    clean_pbx(project_root, pbx_path, dry_run)


### Helpers ###

def _clear_marked_files_from_section(rfile, wfile, to_rm):
    """
    Given `rfile`'s pointer position is within a section of file
    names we want to clean, write to `wfile` each line from rfile 
    that does not contain the file name of a file from `to_rm`.
    (i.e. removing those lines from the new clone file being built)
    Returns when the end of the section is reached.

    rfile - File. the file to read from. Should be positioned in
            a section of interest.
    wfile - File. the file to write valid lines to
    to_rm - Set. set of file names to not include in `wfile`
    """
    global fname_matcher
    global section_end_matcher
    for line in rfile:
        fname = fname_matcher.search(line)
        sname = strings_matcher.search(line)
        
        # check line isnt a ref we want to remove
        if fname:
            if fname.group(1) in to_rm: #TODO: this alg only works for some sections. PBXVariantGroup section wont work. (only run this alg w/in sections we want?)
                continue
        elif sname:
            if sname.group(1) in to_rm:
                continue

        wfile.write(line)

        if section_end_matcher.search(line):
            return

def _get_flattened_files(root_path, use_cache):
    """
    Starting from input path, find every file in that
    directory and all its subdirectories. Return a
    1D list of those files. Saves result in cache
    to save future compuation time.

    root_path - String. path to start building the list from
    use_cache - Bool. whether or not to use cached data
    @return - List[String]. list of file names under `root_path`.
              All file names are not path prefixed
    """
    global filesystem_cache
    if filesystem_cache and use_cache:
        return filesystem_cache
    
    # recursion helper
    def _kernel(curr_path, lst):
        for target in os.listdir(curr_path):
            full_path = os.path.join(curr_path, target)
            # dont recurse into hidden directories
            if os.path.isdir(full_path) and target[0] != ".":
                _kernel(full_path, lst)
            elif os.path.isfile(full_path):
                lst.append(target)

    filesystem_cache = []
    _kernel(root_path, filesystem_cache)
    return filesystem_cache


def _get_pbx_files(pbx_path, use_cache):
    """
    Builds and returns a Set of file names that the
    pbxproj file located at `pbx_path` contains. Saves
    result in cache to save future computation time.

    pbx_path - String. path to a valid project.pbxproj file
    use_cache - Bool. whether or not to use cached data
    @return - Set[String]. set of file names referenced w/in
              the project. All file names are not path prefixed.
    """
    global pbx_file_cache
    global section_begin_matcher
    global section_end_matcher
    global fname_matcher
    global groups_to_check
    if pbx_file_cache and use_cache:
        return pbx_file_cache

    proj_files = set()
    section_of_interest = False
    with open(pbx_path, 'r') as f:
        for line in f:
            # only search for files in sections we know files are in
            if not section_of_interest:
                section = section_begin_matcher.search(line)
                if section and section.group(1) in groups_to_check:
                    section_of_interest = True
            else:
                fname = fname_matcher.search(line)
                sname = strings_matcher.search(line)
                if fname:
                    proj_files.add(fname.group(1))
                elif sname:
                    proj_files.add(sname.group(1))
                elif section_end_matcher.search(line):
                    section_of_interest = False

    pbx_file_cache = proj_files
    return pbx_file_cache

def _remove_dup_slashes(path):
    """
    Remove duplicate slashes in the given path

    path - String. a unix style path
    @return - String. the same unix style path, but with any
              previously repeated slashes removed.
    """
    new_path = []
    prev = None

    for c in path:
        if c == prev == '/':
            continue
        prev = c
        new_path.append(c)

    return "".join(new_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project",
        help="Path to your project root directory. (optional if you've manually added a default path)")
    ap.add_argument("-x", "--pbx",
        help="Path to your pbxproj file (optional if you've manually added a default path)")
    ap.add_argument("--not-dry", dest="not-dry", default=False, action="store_true",
        help="Not dry-run mode; running with this flag WILL alter your files. Don't include it to leave your project unchanged.")
    args = vars(ap.parse_args())
    main(args)
