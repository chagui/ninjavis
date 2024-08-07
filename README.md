# ninjavis #
[![build](https://travis-ci.org/chagui/ninjavis.png)](https://travis-ci.org/chagui/ninjavis)
[![version](https://pypip.in/v/ninjavis/badge.png?style=flat)](https://pypi.python.org/pypi/ninjavis)
[![format](https://pypip.in/format/ninjavis/badge.png?style=flat)](https://pythonwheels.com/)
[![license](https://pypip.in/license/ninjavis/badge.png?style=flat)](https://pypi.python.org/pypi/ninjavis)


## Introduction ##
Generate visualization from [Ninja](https://github.com/ninja-build/ninja) build logs. Ninjavis parse the ninja build
logs and for each item of the build extract its target, starting and end time.
It output those information in a template containing a simple timeline ; the visualization is done by [vis.js](http://visjs.org/).

Inspired by [buildbloat](https://github.com/nico/buildbloat).

## Usage ##
```bash
usage: ninjavis --title "my build" ninja_build.log build_profile.html
```
:warning: Run ``ninja -t recompact`` first to make sure that no duplicate entries are in the build log.

## Example ##
Profile of Ninja 1.8.2 build
![Ninja 1.8.2 build profile](https://raw.githubusercontent.com/chagui/ninjavis/main/docs/example-ninja_build_1.8.2.png)


Output HAR?
https://en.wikipedia.org/wiki/HAR_(file_format)

https://github.com/firefox-devtools/profiler


https://github.com/nico/ninjatracing
https://www.speedscope.app/
https://ui.perfetto.dev/



https://github.com/google/pybadges

