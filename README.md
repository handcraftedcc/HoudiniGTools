# HoudiniGTools

An experimental, procedural CNC/CAM toolset for Houdini, focused on woodworking with flat stock and generating G-code for FluidNC.

HoudiniGTools keeps geometry preparation, stock layout, toolpaths, and G-code output in a node graph. Change a part, adjust an offset, move a tab, or revise a cutting depth upstream, then inspect the resulting paths downstream. The tools grew out of personal projects on a LowRider V4 CNC and the desire to keep machining setups editable and repeatable inside Houdini.

> **Experimental — use with caution.** This toolset was built primarily for my personal use. Expect rough edges, incomplete features, and machine-specific assumptions. Inspect generated G-code and verify it for your controller, machine, tooling, stock, and workholding before running it. The previews are aids for inspection, not a guarantee of a safe cut.

## Features

- Lay 3D parts flat, arrange them on stock, and extract cutting curves.
- Generate outside profiles, cuts on curves, inside profiles, raster pockets, and parallel pockets.
- Control cutter diameter, feeds, plunge rate, depth per pass, cutting direction, and travel height.
- Add square or pyramid tabs with automatic placement or guide curves, plus dogbone corner relief.
- Generate straight and helical hole operations.
- Add custom commands, import G-code for inspection, and export `.gcode` files.
- Inspect dimensions, estimated time, Z heights, and approximate material removal.
- Experiment with converting linear paths into G2/G3 arcs during export.

The focus is flat-stock and 2.5D work. General 3D surface machining and broad controller compatibility are outside the documented scope.

## Installation

1. Download or clone this repository to a permanent location.
2. Install [Houdini CurveClipper](https://github.com/handcraftedcc/Houdini-Curve-Clipper) separately. The cutting tools use its Boolean and Offset HDAs; the bundled Python libraries here do not replace those node definitions.
3. Install and enable SideFX Labs. The preparation tools and parts of the internal networks use Labs nodes.
4. Edit `HoudiniGTools.json`, replacing `PATH/TO/PACKAGE/HoudiniGTools` with the absolute path to this repository. Use forward slashes in the JSON path.
5. Copy the edited JSON into the `packages` folder in your Houdini user preferences directory and restart Houdini.

For example, a Houdini 21 installation on Windows might use `Documents/houdini21.0/packages/HoudiniGTools.json`. Use your actual user preferences directory if Documents is redirected or your setup is customized.

The bundled native Python libraries target **Windows x64 / Python 3.11**. Other Python versions and operating systems need compatible dependency builds. No minimum Houdini version or complete compatibility matrix has been established. See [installation and compatibility](docs/installation.md).

## Start here

Inside a Geometry network, create a closed polygon curve in XY at Z = 0. Use Houdini geometry in meters: a 100 mm square is 0.1 × 0.1 units.

Connect it to **GTools Gcode Cut**, choose a cut mode, and explicitly set the cutter, units, depth, feeds, and travel height. Inspect the resulting path, then connect it to **GTools Gcode Output File**. Review the Start Script and End Script for your machine before pressing **Export Gcode**.

The [workflow guide](docs/workflow.md) walks through a small setup you can build from scratch. No example project is required.

## Documentation

- [Installation, dependencies, and compatibility](docs/installation.md)
- [Workflow, units, cutting settings, and export](docs/workflow.md)
- [Node reference](docs/nodes.md)
- [Geometry attributes and implementation notes](docs/technical-notes.md)
- [Limitations and troubleshooting](docs/troubleshooting.md)

## Development and AI use

Most of this toolset was created by hand. AI was used for some of the Python API work and G-code parsing logic. The procedural networks and most of the toolset were built manually.

The README and documentation were generated with AI assistance based on the project assets, code, and the author's development notes.

The repository includes earlier asset versions and a `gtools.dev` namespace. A higher version number in that development namespace does not indicate a supported upgrade. See the [node reference](docs/nodes.md) before changing asset versions in an existing scene.

## Credits and license

Created by Dominik Lange / Handcrafted Media. The project is licensed under the [MIT License](LICENSE). Bundled third-party libraries retain their own licenses.

Curve operations rely on [Houdini CurveClipper](https://github.com/handcraftedcc/Houdini-Curve-Clipper), using [pyclipr](https://github.com/drlukeparry/pyclipr) and Clipper2. Entagma's [Controlling Your 3D Printer with Houdini](https://entagma.com/controlling-your-3d-printer-with-houdini-part-1/) helped inspire the initial geometry-to-G-code approach.
