#! /usr/bin/env python3
from random import random

import atheris
import sys
import io
from contextlib import contextmanager

import fuzz_helpers as fh

with atheris.instrument_imports(include=['pygrib']):
    import pygrib

# Disable all pygrib logging
import logging
logging.disable(logging.CRITICAL)

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr


def TestOneInput(data):
    fdp = fh.EnhancedFuzzedDataProvider(data)

    try:
        with fdp.ConsumeTemporaryFile('.grib', True, True) as fp, nostdout():
            grbs = pygrib.open(fp)
            for grb in grbs:
                repr(grb)
    except RuntimeError:
        if random() > 0.99:
            raise

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
