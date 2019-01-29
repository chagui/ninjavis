# ninjavis #
Generate visualization from [Ninja](https://github.com/ninja-build/ninja) build logs. Ninjavis parse the ninja build
logs and for each item of the build extract its target, starting and end time.
It output those information in a template containing a simple timeline ; the visualization is done by [vis.js](http://visjs.org/).