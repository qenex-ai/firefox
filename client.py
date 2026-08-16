#!/usr/bin/python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

HG_EXCLUSIONS = [".hg", ".hgignore", ".hgtags"]

import glob
import os
import shutil
import sys
from optparse import OptionParser
from subprocess import check_call

topsrcdir = os.path.dirname(__file__)
if topsrcdir == "":
    topsrcdir = "."


def check_call_noisy(cmd, *args, **kwargs):
    print("Executing command:", cmd)
    check_call(cmd, *args, **kwargs)


def do_hg_pull(dir, repository, hg):
    fulldir = os.path.join(topsrcdir, dir)
    # clone if the dir doesn't exist, pull if it does
    if not os.path.exists(fulldir):
        check_call_noisy([hg, "clone", repository, fulldir])
    else:
        cmd = [hg, "pull", "-u", "-R", fulldir]
        if repository is not None:
            cmd.append(repository)
        check_call_noisy(cmd)
    check_call([
        hg,
        "parent",
        "-R",
        fulldir,
        "--template=Updated to revision {node}.\n",
    ])


def do_hg_replace(dir, repository, tag, exclusions, hg):
    """
    Replace the contents of dir with the contents of repository, except for
    files matching exclusions.
    """
    fulldir = os.path.join(topsrcdir, dir)
    if os.path.exists(fulldir):
        shutil.rmtree(fulldir)

    assert not os.path.exists(fulldir)
    check_call_noisy([hg, "clone", "-u", tag, repository, fulldir])

    for thing in exclusions:
        for excluded in glob.iglob(os.path.join(fulldir, thing)):
            if os.path.isdir(excluded):
                shutil.rmtree(excluded)
            else:
                os.remove(excluded)


def toggle_trailing_blank_line(depname):
    """If the trailing line is empty, then we'll delete it.
    Otherwise we'll add a blank line."""
    lines = open(depname, "rb").readlines()
    if not lines: