# Copyright 2018 the Deno authors. All rights reserved. MIT license.

import os
from setup import read_gn_args, write_gn_args
from shutil import rmtree
from tempfile import mktemp


def read_gn_args_test():
    # Args file doesn't exist.
    (args, hand_edited) = read_gn_args("/baddir/hopefully/nonexistent/args.gn")
    assert args is None
    assert hand_edited == False

    # Handwritten empty args file.
    filename = mktemp()
    with open(filename, "w"):
        pass
    (args, hand_edited) = read_gn_args(filename)
    os.remove(filename)
    assert args == []
    assert hand_edited == True

    # Handwritten non-empty args file.
    expect_args = ['some_number=2', 'another_string="ran/dom#yes"']
    filename = mktemp()
    with open(filename, "w") as f:
        f.write("\n".join(expect_args + ["", "# A comment to be ignored"]))
    (args, hand_edited) = read_gn_args(filename)
    os.remove(filename)
    assert args == expect_args
    assert hand_edited == True


def write_gn_args_test():
    # Build a nonexistent path; write_gn_args() should call mkdir as needed.
    dir = mktemp()
    filename = os.path.join(dir, "args.gn")
    assert not os.path.exists(dir)
    assert not os.path.exists(filename)
    # Write some args.
    args = ['lalala=42', 'foo_bar_baz="lorem ipsum dolor#amet"']
    write_gn_args(filename, args)
    # Directory and args file should now be created.
    assert os.path.isdir(dir)
    assert os.path.isfile(filename)
    # Validate that the right contents were written.
    (check_args, hand_edited) = read_gn_args(filename)
    assert check_args == args
    assert hand_edited == False
    # Clean up.
    rmtree(dir)


def setup_test():
    read_gn_args_test()
    write_gn_args_test()


if __name__ == '__main__':
    setup_test()
