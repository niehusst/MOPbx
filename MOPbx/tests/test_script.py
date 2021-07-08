import pytest
from MOPbx.src.mopbx import clean_pbx, remove_empty_translation_files, remove_translation_files_without_source

"""
To test:

* try different types of file hierarchy arrangment (will depth matter?)
* just check that everything compiles after script run (compare against manual fix pbx?)

how to test that project will compile after script is run???
could pbx be read into dict or something that coule be written back to file after to avoid messy formatting tweaks?
pbx_clean dry should return string (or write local file?) that we can compare to a corresponding manually fixed pbx (stored outside the ios proj) AND not delete any files that it would have, and rather just store them in array w/o rm them


INFO: these tests have to be run from the `tests` directory, otherwise the paths checked in the tests wont match as expected
"""

# helper globals
test_mode = True

valid_proj = "../tests/data/ValidData/"
valid_pbx = "../tests/data/ValidData/ExampleProj.xcodeproj/project.pbxproj"

danlging_refs_proj = "../tests/data/DanglingRefs/"
danlging_refs_pbx = "../tests/data/DanglingRefs/ExampleProj.xcodeproj/project.pbxproj"

empty_strings_proj = "../tests/data/EmptyStrings/"
empty_string_pbx = "../tests/data/EmptyStrings/ExampleProj.xcodeproj/project.pbxproj"

no_layout_proj = "../tests/data/NoLayoutFile/"
no_layout_pbx = "../tests/data/NoLayoutFile/ExampleProj.xcodeproj/project.pbxproj"

last_ref_proj = "../tests/data/DanglingRefs/"
last_ref_pbx = "../tests/data/DanglingRefs/ExampleProj.xcodeproj/project.pbxproj"


def test_all_translation_files_without_source_removed():
    res = remove_translation_files_without_source(no_layout_proj, test_mode)
    expected = sorted(list(map(lambda x: no_layout_proj + x, ["ExampleProj/es.lproj/Main.strings"])))
    assert res == expected, f"List of files to remove dont match. {no_layout_proj}"


def test_no_translation_files_removed_for_valid_proj():
    res = remove_translation_files_without_source(valid_proj, test_mode)
    assert res == [], f"Found translation files without source when there should be none. {valid_proj}"


def test_clean_pbx_valid_project_with_no_missing_files():
    res = clean_pbx(valid_proj, valid_pbx, test_mode)
    assert res == [], f"List of refs to remove was not empty. {valid_proj}"


#>* xibs, storyboards, swift, and strings files not in fs all get rm from pbx
#>* all references are correctly removed completely from pbx, including translation language from xib set (file comparison to manually fix?)
def test_clean_pbx_invalid_project_with_missing_files():
    res = clean_pbx(danlging_refs_proj, danlging_refs_pbx, test_mode)
    expected = ["ExampleProj/DetailViewController.swift", "ExampleProj/DetailViewController.xib", "ExampleProj/Content/pic4.png", "ExampleProj/Base.lproj/LaunchScreen.storyboard", "ExampleProj/es.lproj/Main.strings"]
    expected = sorted(list(map(lambda x: danlging_refs_proj + x, expected)))
    assert res == expected, f"List of refs did not contain expect refs. {danlging_refs_proj}"


#>* removing a ref from pbx that is last element in array doesnt break compile (prev elem now has trailing comma)
def test_last_ref_removal_compiles():
    clean_pbx(last_ref_proj, last_ref_pbx, test_mode)
    assert False
    #TODO test proj compiles?? compare to manual fix file?


def test_remove_present_empty_translation_files_found():
    res = remove_empty_translation_files(empty_strings_proj, test_mode)
    expected = sorted(list(map(lambda x: empty_strings_proj + x, ["ExampleProj/es.lproj/Main.strings", "ExampleProj/es.lproj/LaunchScreen.strings"])))
    assert res == expected, f"List of files to remove dont match. {empty_strings_proj}"


def test_remove_no_empty_translation_files_empty():
    res = remove_empty_translation_files(valid_proj, test_mode)
    assert res == [], f"Found empty files when there should be none. {valid_proj}"