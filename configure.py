# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import itertools
import json
import logging
import os
import pprint
import sys
import textwrap
from collections.abc import Iterable

base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(base_dir, "python", "mach"))
sys.path.insert(0, os.path.join(base_dir, "python", "mozboot"))
sys.path.insert(0, os.path.join(base_dir, "python", "mozbuild"))
sys.path.insert(0, os.path.join(base_dir, "third_party", "python", "packaging"))
sys.path.insert(0, os.path.join(base_dir, "testing", "mozbase", "mozfile"))
sys.path.insert(0, os.path.join(base_dir, "testing", "mozbase", "mozshellutil"))
sys.path.insert(0, os.path.join(base_dir, "third_party", "python", "six"))
sys.path.insert(0, os.path.join(base_dir, "third_party", "python", "looseversion"))

if "MOZ_CONFIGURE_BUILDSTATUS" in os.environ:

    def buildstatus(message):
        print("BUILDSTATUS", message)

else:

    def buildstatus(message):
        return


def main(argv):
    # Check for CRLF line endings.
    with open(__file__) as fh:
        data = fh.read()
        if "\r" in data:
            print(
                "\n ***\n"
                " * The source tree appears to have Windows-style line endings.\n"
                " *\n"
                " * If using Git, Git is likely configured to use Windows-style\n"
                " * line endings.\n"
                " *\n"
                " * To convert the working copy to UNIX-style line endings, run\n"
                " * the following:\n"
                " *\n"
                " * $ git config core.autocrlf false\n"
                " * $ git config core.eof lf\n"
                " * $ git rm --cached -r .\n"
                " *\n"
                " * If not using Git, the tool you used to obtain the source\n"
                " * code likely converted files to Windows line endings. See\n