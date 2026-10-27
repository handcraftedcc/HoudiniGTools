# Geometry and implementation notes

[Back to README](../README.md)

These notes are for inspecting or extending the toolset. Much of the implementation lives inside the HDAs as Houdini node networks, VEX, and Python SOPs. The loose Python helper is only part of the system.

## From curves to commands

Source curves describe the intended part boundaries. The Cut network offsets them for cutter compensation, constructs profile or pocket paths, creates depth layers, adds entry and travel moves, and applies optional tabs and dogbones. CurveClipper supplies the Boolean and offset operations.

Raster pocketing creates cutting lines and a network of permitted travel paths, then uses shortest-path connections between sections. Parallel pocketing builds successive offsets and connects them with direct moves, moves through previously cut sections, or new plunges as needed. These are procedural strategies with tradeoffs, not globally optimal routing guarantees.

Tabs use geometry projected onto the toolpath to raise sections of the cut. Resampling helps represent the tab profile. Automatic placement looks for qualifying straight sections; guide-curve placement uses intersections to direct locations.

## Attribute conventions

Use **GTools Utils Create Attributes** as the current starting point for command geometry. The deprecated `createGtoolAttribs()` function in `gtoolsUtils.py` uses older names and is not the current schema.

| Attribute | Class / storage | Meaning |
| --- | --- | --- |
| `P` | Point position | Current command position. Main toolpath geometry uses meters; export converts to mm. |
| `G_Gtype` | Point string | Command kind, such as `G0`, `G1`, `G2`, `G3`, or `Custom`. |
| `G_CustomGcode` | Point string | Literal text used for Custom commands. |
| `G_XYZset` | Point integer array | XYZ presence flags, used by command-building and serialization logic. |
| `G_F` | Point float | Feedrate, normally mm/min. |
| `G_IJK` | Point vector | Packed arc-center values for the arc-processing pipeline. |
| `G_P` | Point float | Command-specific P parameter, such as dwell. |
| `G_E`, `G_L`, `G_T`, `G_Q` | Point numeric values | Additional command parameters initialized by the schema. Not all are serialized by the current writer. |
| `G_Message`, `G_Comment` | Point strings | Message/comment text appended during serialization. |
| `G_LineNumber`, `G_RawLine` | Imported point attributes | Parser trace information: source line index and original text. |
| `G_OutputGcode` | Detail string | Complete serialized file text, read by the export callback. |

The importer can create additional numeric `G_<LETTER>` attributes. An attribute being present does not imply that the exporter can reproduce its original command.

**Point order is execution order.** The writer loops over `geo.points()`. Primitive connectivity alone does not determine output order. Sorting, fusing, deleting, or resampling points can change the command sequence or discard required information. Keep such operations upstream of command generation unless you deliberately rebuild the command data.

`G_XYZset` is not a general guarantee of exact source-word preservation: the current writer emits X and Y for ordinary motion and uses flags/position changes to decide whether to include Z.

## Export behavior

Inside Gcode Output File, the network scales geometry to millimeters and constructs text in a Python SOP. The button callback reads `G_OutputGcode` from `READ_GcodeOutput`, expands the output path, creates parent directories, and writes UTF-8 text. Existing files are overwritten.

The writer replaces `FILENAME` and `TIMESTAMP` tokens in the Start Script, then appends serialized commands and End Script. It has branches for Custom text, G0/G1, G2/G3, G4, probing, coordinate selections, pause, and basic spindle commands. Unsupported types print a diagnostic and are not faithfully emitted. Treat unsupported-command loss as a reason to inspect every exported file.

Arc serialization emits X/Y, optional Z, I/J, and F. This is not a general multi-plane arc postprocessor; K is not emitted by that branch. Probe and spindle branches also serialize only limited parameters. For commands outside the implemented subset, reviewed Custom text may be necessary.

Start and End Script fields are machine configuration. They are not inferred from the stock or cutting settings. Raw Custom text is passed through rather than unit-converted or geometrically validated.

## Import limitations

The importer is an inspection/conversion helper, not a full G-code interpreter. Its parser splits whitespace-delimited words, identifies a command type, collects XYZ and other numeric parameters, and carries forward missing XYZ components. It extracts parenthesized and inline comments and packs I/J/K values into `G_IJK`. A later transform scales positions by 0.001 for the meter-based scene.

Consequences to consider when importing external files:

- Compact words such as `G1X10Y20` are not reliably handled by the whitespace-based parser.
- Multiple commands on a line are not represented as a full ordered modal block.
- Carrying forward coordinates is not complete G90/G91, work-offset, or unit-mode interpretation. Do not expect inch-mode or incremental programs to be reconstructed correctly.
- Modal motion, canned cycles, macros, probing, homing, and controller-specific commands need independent interpretation.
- Comment extraction and command normalization can change information; the geometry is not a lossless representation of arbitrary source text.
- Optional G2/G3 reconstruction helps display supported arcs but does not establish support for every radius, plane, or helical convention.

Keep the original file. Do not assume import -> edit -> export preserves all behavior.

## Python helpers and unfinished paths

`scripts/python/gtoolsUtils.py` provides helpers used by the Custom tools. It includes deprecated attribute creation and a G2/G3 builder explicitly marked as a placeholder. Some incremental-move handling produces command types the file writer does not serialize. UI options, helper functions, and writer support are not a complete one-to-one mapping.

Most of the toolset was made by hand; AI assisted with some Python API work and G-code parsing logic. Evaluate behavior from the actual networks and output, particularly when extending the implementation.

## Inspection scope

This documentation was checked against the shipped asset definitions, internal networks, Python helper, and representative private development scenes. The public guides do not depend on those scenes. Inspection used manual update mode without exporting or saving the projects. It did not validate a complete machining job or establish cross-version compatibility.
