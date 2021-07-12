import os
import pytest
from MOPbx.src.mopbx import main, clean_pbx, remove_empty_translation_files, remove_translation_files_without_source, _reset_caches

"""
INFO: these tests have to be run from the `tests` directory, otherwise the paths checked in the tests wont match as expected
"""

# helper globals
test_mode = True

valid_proj = "../tests/data/ValidData/"
valid_pbx = "../tests/data/ValidData/ExampleProj.xcodeproj/project.pbxproj"
valid_pbx_fix = "../tests/data/ValidData/corrected_project.pbxproj"

dangling_refs_proj = "../tests/data/DanglingRefs/"
dangling_refs_pbx = "../tests/data/DanglingRefs/ExampleProj.xcodeproj/project.pbxproj"
dangling_refs_pbx_fix = "../tests/data/DanglingRefs/corrected_project.pbxproj"

empty_strings_proj = "../tests/data/EmptyStrings/"
empty_strings_pbx = "../tests/data/EmptyStrings/ExampleProj.xcodeproj/project.pbxproj"
empty_strings_pbx_fix = "../tests/data/EmptyStrings/corrected_project.pbxproj"

no_layout_proj = "../tests/data/NoLayoutFile/"
no_layout_pbx = "../tests/data/NoLayoutFile/ExampleProj.xcodeproj/project.pbxproj"
no_layout_pbx_fix = "../tests/data/NoLayoutFile/corrected_project.pbxproj"

last_ref_proj = "../tests/data/DanglingRefs/"
last_ref_pbx = "../tests/data/DanglingRefs/ExampleProj.xcodeproj/project.pbxproj"
last_ref_pbx_fix = "../tests/data/DanglingRefs/corrected_project.pbxproj"

tmp_fname = "tmp_pbx.txt"


def setup_function():
    _reset_caches()


def teardown_function():
    if os.path.isfile(tmp_fname):
        os.remove(tmp_fname)


def test_all_translation_files_without_source_removed():
    res = remove_translation_files_without_source(no_layout_proj, test_mode)
    expected = sorted(list(map(lambda x: no_layout_proj + x, ["ExampleProj/es.lproj/Main.strings"])))
    assert sorted(res) == expected, f"List of files to remove dont match. {no_layout_proj}"


def test_no_translation_files_removed_for_valid_proj():
    res = remove_translation_files_without_source(valid_proj, test_mode)
    assert res == [], f"Found translation files without source when there should be none. {valid_proj}"


def test_clean_pbx_no_references_removed_from_valid_proj():
    res = clean_pbx(valid_proj, valid_pbx, test_mode)
    assert res == [], f"List of refs to remove was not empty. {valid_proj}"


def test_clean_pbx_invalid_project_with_missing_files():
    res = clean_pbx(dangling_refs_proj, dangling_refs_pbx, test_mode)
    expected = sorted([
        "DetailViewController.swift", 
        "DetailViewController.xib", 
        "pic4.png", 
        "LaunchScreen.storyboard", 
        "Main.strings"
    ])
    assert sorted(res) == expected, f"List of refs did not contain expect refs. {dangling_refs_proj}"


def test_remove_present_empty_translation_files_found():
    res = remove_empty_translation_files(empty_strings_proj, test_mode)
    expected = sorted(list(map(lambda x: empty_strings_proj + x, ["ExampleProj/es.lproj/Main.strings", "ExampleProj/es.lproj/LaunchScreen.strings"])))
    assert sorted(res) == expected, f"List of files to remove dont match. {empty_strings_proj}"


def test_remove_no_empty_translation_files_empty():
    res = remove_empty_translation_files(valid_proj, test_mode)
    assert res == [], f"Found empty files when there should be none. {valid_proj}"


def test_valid_compiles():
    main({"project": valid_proj, "pbx": valid_pbx, "not-dry": False})
    assert os.system(f"diff -B {tmp_fname} {valid_pbx_fix}") == 0


def test_no_layout_compiles():
    main({"project": no_layout_proj, "pbx": no_layout_pbx, "not-dry": False})
    assert os.system(f"diff -B {tmp_fname} {no_layout_pbx_fix}") == 0


def test_dangling_refs_compiles():
    main({"project": dangling_refs_proj, "pbx": dangling_refs_pbx, "not-dry": False})
    assert os.system(f"diff -B {tmp_fname} {dangling_refs_pbx_fix}") == 0


def test_empty_strings_compiles():
    main({"project": empty_strings_proj, "pbx": empty_strings_pbx, "not-dry": False})
    assert os.system(f"diff -B {tmp_fname} {empty_strings_pbx_fix}") == 0

