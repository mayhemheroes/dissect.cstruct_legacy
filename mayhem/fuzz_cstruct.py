#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    from dissect.cstruct import cstruct
    from dissect.cstruct.cstruct import CStyleParser
    from dissect.cstruct.exceptions import Error


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        cparser = cstruct()
        cparser.load(fdp.ConsumeRandomString())
        parser = CStyleParser(cparser)
        parser.parse(fdp.ConsumeRemainingString())
    except (Error, SyntaxError):
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
