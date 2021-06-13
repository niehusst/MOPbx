import pytest
from MOPbx.src.mopbx import clean_pbx, remove_empty_translation_files, remove_translation_files_without_source

"""
To test:


* try different types of file hierarchy arrangment (will depth matter?)


how to test that project will compile after script is run???
could pbx be read into dict or something that coule be written back to file after to avoid messy formatting tweaks?
pbx_clean dry should return string (or write local file?) that we can compare to a corresponding manually fixed pbx (stored outside the ios proj) AND not delete any files that it would have, and rather just store them in array w/o rm them
"""

# helper globals
test_mode = True

valid_proj = "../tests/data/ValidData/"
valid_pbx = "../tests/data/ValidData/ExampleProj.xcodeproj/project.pbxproj"

danlging_refs_proj = ""
danlging_refs_pbx = ""

empty_strings_proj = ""
empty_string_pbx = ""

no_layout_proj = ""
no_layout_pbx = ""

last_ref_proj = ""
last_ref_pbx = ""


#>* remove .strings files from fs where source xib (or storyboard) not present in fs (and pbx)
def test_all_translation_files_without_source_removed():
    res = remove_translation_files_without_source(no_layout_proj, no_layout_pbx, test_mode)
    assert res == ["TODO"], f"List of files to remove dont match. {no_layout_proj}"


#>* clean pbx/fs not changed
def test_clean_pbx_valid_project_with_no_missing_files():
    res = clean_pbx(valid_proj, valid_pbx, test_mode)
    assert res == [], f"List of refs to remove was not empty. {valid_proj}"


#>* xibs, storyboards, swift, and strings files not in fs all get rm from pbx
#>* all references are correctly removed completely from pbx, including translation language from xib set (file comparison to manually fix?)
def test_clean_pbx_invalid_project_with_missing_files():
    res = clean_pbx(danlging_refs_proj, danlging_refs_pbx, test_mode)
    assert res == ["TODO"], f"List of refs did not contain expect refs. {danlging_refs_proj}"


#>* empty .strings files removed from file system
#>* fully empty .strings files + ones that have 1 space in it
def test_remove_empty_translation_files():
    res = remove_empty_translation_files(empty_strings_proj, empty_string_pbx, test_mode)
    assert res == ["TODO"], f"List of files to remove dont match. {empty_strings_proj}"


#>* removing a ref from pbx that is last element in array doesnt break compile (prev elem now has trailing comma)
def test_last_ref_removal_compiles():
    res = clean_pbx(last_ref_proj, last_ref_pbx, test_mode)
    assert res == ["TODO"], f"List of files to remove dont match. {last_ref_proj}"
    #TODO test proj compiles???
