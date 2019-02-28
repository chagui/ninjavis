# -*- coding: utf-8 -*-
"""Generate visualization of a ninja build from its logs."""
# :copyright: (c) 2019 Guilhem Charles. All rights reserved.
#!/usr/bin/env python3.7
import argparse
from dataclasses import dataclass
import re
import sys
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

JINJA_ENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)


@dataclass
class BuildItem:
    """
    Represents an item of the build. Match a line of the log file.
    """
    __slots__ = ['name', 'start_time', 'end_time']
    name: str
    start_time: int
    end_time: int


def generate_build_profile(logfile: str) -> List[BuildItem]:
    """
    Parse a ninja build log file and generates a profile. A profile consist of the list of item
    part of the build.

    :param logfile: Path to the build log file.
    :return: Profile of the build.
    """
    def parse_and_append(profile: List[BuildItem], line: str):
        try:
            # ignore comments
            if line[:1] != '#':
                start_time, end_time, _, command, _ = line.split()
                profile.append(BuildItem(command, start_time, end_time))
        except ValueError:
            print(f'error: could not parse {line}', file=sys.stderr)

    profile = []
    with open(logfile, 'r') as build_log:
        # we expect the line to specify ninja build log version
        header = build_log.readline()
        log_version = re.search(r'# ninja log v(\d+)', header)
        if log_version:
            if int(log_version.group(1)) != 5:
                raise RuntimeError(f'unsupported log file version: {log_version}')
        else:
            parse_and_append(profile, header)

        for line in build_log:
            parse_and_append(profile, line)

    return profile


def generate_timeline_from(profile: List[BuildItem], output: str, title: Optional[str]):
    """
    Generate a visjs timeline from the ninja build profile.

    :param profile: Ninja build information.
    :param output: File to output the visualization.
    :param title: Title of the visualization.
    :return:
    """
    if not title:
        title = 'Ninja build'

    try:
        visualization_skel = JINJA_ENV.get_template('timeline.html')
        with open(output, 'w') as visualization:
            visualization.write(visualization_skel.render(title=title, dataset=profile))
    except RuntimeError as exc:
        print(f'error: could not generate timeline: {exc}', file=sys.stderr)
        sys.exit(1)


def get_argparser() -> argparse.ArgumentParser:
    """
    ninjavis arguments parser.

    :return: Arguments parser.
    """
    parser = argparse.ArgumentParser(prog='ninjavis',
                                     description='Parse ninja build log file and '
                                                 'generates a timeline of the build')
    parser.add_argument('logfile', help='Ninja build log (.ninja_log)')
    parser.add_argument('output', help='Output file for the visualization')
    parser.add_argument('--title', help='Visualization title')
    return parser


def main():
    """
    Parse the arguments and try to generate a visualization out of the provided build log.

    :return:
    """
    args = get_argparser().parse_args(sys.argv[1:])

    try:
        profile = generate_build_profile(args.logfile)
        generate_timeline_from(profile, args.output, args.title)
    except (RuntimeError, FileNotFoundError) as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
