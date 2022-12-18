#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers
from dissect.cstruct import ParserError

with atheris.instrument_imports():
    from dissect import cstruct
    from dissect.cstruct.parser import CStyleParser

@atheris.instrument_func
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        cparser = cstruct.cstruct()
        cparser.load(fdp.ConsumeRandomString())
        parser = CStyleParser(cparser)
        parser.parse(fdp.ConsumeRemainingString())
    except ParserError:
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
