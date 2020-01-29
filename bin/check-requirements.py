#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import io
import sys
import json
import argparse
from contextlib import (
    redirect_stdout,
)

try:
    # for pip >= 10
    from pip._internal import main as pip_main
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip import main as pip_main
    from pip.req import parse_requirements


def main(args):
    exit_code = 0
    pip_stdout = io.StringIO()
    requirements = {
        req.name for req in parse_requirements(args.requirement, session='session')
    }

    with redirect_stdout(pip_stdout):
        pip_main(['list', '--outdated', '--format=json', '--not-required'])

    for package in json.loads(pip_stdout.getvalue()):
        if package['name'] in requirements:
            exit_code = 1
            print(package)

    return exit_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse requirements file and print outdated packages.',
    )
    parser.add_argument(
        '-r',
        '--requirement',
        required=True,
        help='Check packages from the given requirements file.',
        metavar='<file>',
    )
    args = parser.parse_args()

    sys.exit(main(args))
