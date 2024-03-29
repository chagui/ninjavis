#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# :copyright: (c) 2019-2020 Guilhem Charles. All rights reserved.
"""Generate visualization of a ninja build from its logs."""
import argparse
import re
import sys
from os.path import getmtime
from typing import List, Optional

TIMELINE = """
<!DOCTYPE HTML>
<html>
<head>
  <title>{title}</title>

  <style type="text/css">
    body, html {{
      font-family: sans-serif;
    }}
  </style>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div id="visualization"></div>

<script type="text/javascript">
  // DOM element where the Timeline will be attached
  var container = document.getElementById('visualization');

  // Create a DataSet (allows two way data-binding)
  var items = new vis.DataSet({dataset});
  // Configuration for the Timeline
  var options = {{}};

  // Create a Timeline
  var timeline = new vis.Timeline(container, items, options);
</script>
</body>
</html>
"""


def generate_build_profile(logfile: str, time_offset: int) -> List[dict]:
    """
    Parse a ninja build log file and generates a profile. A profile consist of the list of item
    part of the build.

    :param logfile: Path to the build log file.
    :param time_offset: Start time of the visualization.
    :return: Profile of the build.
    """

    def parse_build_entry(line: str) -> Optional[dict]:
        try:
            # ignore comments
            if line[:1] != "#":
                start_time, end_time, _, command, _ = line.split()
                return {
                    "content": command,
                    "start": int(start_time) + time_offset,
                    "end": int(end_time) + time_offset,
                }
        except ValueError:
            print(f"error: could not parse {line}", file=sys.stderr)
        return None

    profile = []
    with open(logfile, "r") as build_log:
        # first line might be a header specifying ninja build log version
        header = build_log.readline()
        log_version = re.search(r"# ninja log v(\d+)", header)
        if log_version:
            parsed_version = log_version.group(1)
            if int(parsed_version) != 5:
                raise RuntimeError(f"unsupported log file version: {parsed_version}")
        else:
            # header is a log entry
            parsed_project = parse_build_entry(header)
            if parsed_project:
                profile = [parsed_project]
        # handle remaining lines, filter out entries that could not be parsed
        profile.extend(filter(None, (parse_build_entry(line) for line in build_log)))
        return profile


def generate_timeline_from(profile: List[dict], output: str, title: str):
    """
    Generate a visjs timeline from the ninja build profile.

    :param profile: Ninja build information.
    :param output: File to output the visualization.
    :param title: Title of the visualization.
    :return:
    """
    try:
        with open(output, "w") as visualization:
            visualization.write(TIMELINE.format(title=title, dataset=profile))
    except RuntimeError as exc:
        print(f"error: could not generate timeline: {exc}", file=sys.stderr)
        sys.exit(1)


def get_argparser() -> argparse.ArgumentParser:
    """
    ninjavis arguments parser.

    :return: Arguments parser.
    """
    parser = argparse.ArgumentParser(
        prog="ninjavis",
        description="Parse ninja build log file and " "generates a timeline of the build",
    )
    parser.add_argument("logfile", help="Ninja build log (.ninja_log)")
    parser.add_argument("output", help="Output file for the visualization")
    parser.add_argument("--title", help="Visualization title", default="Ninja build")
    return parser


def main():
    """
    Parse the arguments and try to generate a visualization out of the provided build log.

    :return:
    """
    args = get_argparser().parse_args(sys.argv[1:])

    try:
        profile = generate_build_profile(args.logfile, int(getmtime(args.logfile)))
        generate_timeline_from(profile, args.output, args.title)
    except (RuntimeError, FileNotFoundError) as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
