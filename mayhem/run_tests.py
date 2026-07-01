#!/usr/bin/python3
"""run_tests.py — RUN dissect.cstruct's own pytest suite and print a parseable summary.

Invoked via the `/mayhem/cstruct-tests` ELF launcher (NOT directly), so the verify-repo
sabotage oracle can neuter the launcher and prove the test oracle is behavioral.

It runs the real known-answer suite (tests/test_basic.py — asserts parsed values for the C
type/struct/enum/flag machinery, packing/unpacking, hexdump/dumpstruct output; and
tests/test_expression.py — a large known-answer table of arithmetic/bitwise expression
evaluations), writes a JUnit XML, parses the counts, and prints one line:

    RUNTESTS tests=<n> passed=<p> failed=<f> skipped=<s>

Exit 0 iff failed == 0. mayhem/test.sh parses that line into a CTRF report.

tests/test_basic.py opens a CWD-relative fixture (tests/data/testdef.txt), so we chdir to
the repo root before running.
"""
from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET

import pytest

SRC = os.environ.get("SRC", "/mayhem")
XML = "/tmp/dissect-cstruct-junit.xml"
TESTS_DIR = "tests"


def main() -> int:
    os.chdir(SRC)
    pytest.main(["-q", "-p", "no:cacheprovider", TESTS_DIR, "--junitxml", XML])

    root = ET.parse(XML).getroot()
    suites = root.findall("testsuite") or ([root] if root.tag == "testsuite" else [])
    if not suites:
        print("RUNTESTS tests=0 passed=0 failed=1 skipped=0")
        return 1

    tests = failed = skipped = 0
    for s in suites:
        tests += int(s.get("tests", 0))
        failed += int(s.get("failures", 0)) + int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
    passed = tests - failed - skipped

    print(f"RUNTESTS tests={tests} passed={passed} failed={failed} skipped={skipped}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
