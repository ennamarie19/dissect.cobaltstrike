#!/usr/bin/env python3
import atheris
import sys

from lark import UnexpectedCharacters, UnexpectedToken

import fuzz_helpers


with atheris.instrument_imports():
    from dissect.cobaltstrike.beacon import BeaconConfig
    from dissect.cobaltstrike.c2profile import C2Profile
    from dissect.cobaltstrike import xordecode

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    choice = fdp.ConsumeIntInRange(0, 2)
    try:
        if choice == 0:
            BeaconConfig.from_bytes(fdp.ConsumeRemainingBytes())
        elif choice == 1:
            C2Profile.from_text(fdp.ConsumeRemainingString())
        elif choice == 2:
            with fdp.ConsumeMemoryFile() as f:
                xordecode.XorEncodedFile(f)
    except (ValueError, UnexpectedCharacters, UnexpectedToken):
        return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
