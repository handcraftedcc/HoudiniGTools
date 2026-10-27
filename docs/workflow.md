# Workflow guide

[Back to README](../README.md)

HoudiniGTools represents machining instructions as geometry. Curves define shapes to machine; cutting nodes turn them into ordered toolpath points with G-code attributes. Inspection nodes read those paths, and the output node serializes them to text.

```text
Model or curves
    -> prepare / lay flat / layout
    -> extract and select cutting curves
    -> Cut / Drill / Custom commands
    -> arrange operations in execution order
    -> inspect paths and material removal
    -> Gcode Output File
```

## Coordinates and units

Use the **XY plane for the stock surface**, with **Z as the cutting axis**. The usual setup puts the stock top at Z = 0, the stock below it, and travel moves above it.

Houdini geometry uses meters in this toolset. Many user-facing dimensions have mm/inch selectors that convert to the internal geometry scale. Export converts positions to millimeters. The default Start Script selects `G21`, `G90`, and `G94`.

| Value | Meaning |
| --- | --- |
| Geometry length `0.1` | 100 mm. |
| Geometry length `0.001` | 1 mm. |
| Bit Diameter `6.35`, unit mm | A 6.35 mm cutter. |
| Bit Diameter `0.25`, unit Inch | The same nominal cutter diameter. |
| Feedrate / Plunge Rate | mm/min, independent of dimension unit selectors. |
| Step Over `0.5` | A fraction: 50% of cutter diameter. |

**Cut Depth (Absolute)** is a positive depth below Z = 0. A depth of 6 mm targets Z = -6 mm. Cut Z Start changes where passes begin; it does not add to that final target. The Cut node's Read From Input button derives depth from curves at a common nonpositive Z and rejects mixed Z levels.

Low-level utility nodes do not all expose the unit conversions of the main Cut node. Check their parameters and expressions before using them independently.

## Build a first path

This setup is for learning and viewport inspection. Choose actual cutting parameters for your machine before exporting a job.

1. Create a Geometry object and a closed polygon square in XY at Z = 0, with sides of 0.1 Houdini units. Leave room around it for an outside cutter offset.
2. Append **GTools Gcode Cut** (`gtools::gtools_gcode_cut::1.1`). Select **Part (Outside lines)**.
3. Set Bit Diameter and its units. Set a small positive Cut Depth for inspecting the path and a smaller positive Max Depth of Cut so multiple passes are visible.
4. Set Feedrate, Plunge Rate, Plunge Angle, and Travelzheight explicitly. Defaults are not machining recommendations.
5. Leave Pocketing at None. For a later through-cut, choose a tab type and inspect the tabs before relying on them to retain a part.
6. Inspect the path from above and from the side. Confirm cutter offset, deepest Z, pass spacing, entry, and retract moves.
7. Branch into **GTools Analysis Stats** or **Gtools Simulate Cut** for inspection. Keep the toolpath branch connected directly to the output node; a simulated stock mesh is not export input.
8. Append **GTools Gcode Output File**, choose a new filename, and review both script fields before pressing Export Gcode.

Changing the square or cutter settings upstream should update the downstream path. Recheck the result after each change.

## Prepare a model

For flat parts modeled in 3D, use **Prep Lay Flat** to orient pieces, then **Prep Layout** to arrange them on stock. Check every part's orientation. Flip Group selects pieces needing the opposite orientation.

Layout controls stock size, allowed rotations, padding, and packing iterations. Version 1.1 adds multiple stock rectangles. Leave room for cutter compensation and the material needed between pieces. Layout alone does not establish that the final paths fit the physical stock.

Use **Prep Silhouette To Curves** for silhouette outlines, or **Prep 3D To Curves** for another edge-to-curve preparation route. Inspect resulting loops and select the appropriate flattening behavior. Separate outside boundaries, holes, and shallow features when they need different operation settings.

Keep transformations and unit conversion upstream of toolpath generation where possible. Transforming a finished path can change positions without correctly updating all command text or associated attributes.

## Profiles and engraving

| Cut mode | Cutter placement |
| --- | --- |
| Part (Outside lines) | Offset outward from the selected boundary. |
| Engrave (On lines) | Follow the supplied curve. |
| Hole (Inside lines) | Offset inward; also exposes pocketing. |

Set diameter, conventional/climb direction, and Extra Offset, then inspect the compensated path. Test Extra Offset on a simple shape before using it to tune a fit.

Max Depth of Cut controls depth per pass. Plunge Angle controls entry ramps; check that a ramp fits the available path. Travelzheight must clear stock, tabs, and fixtures across every transfer. A height above stock zero can still be below a clamp.

## Pockets

Choose **Hole (Inside lines)**, then Raster or Parallel under Pocketing.

- **Raster** generates cutting lines at the selected Angle and connects them using a travel-path network. It aims to reduce repeated plunges and keep cuts continuous; it does not guarantee an optimal route.
- **Parallel** generates successive offsets. Direction offers Outside -> In, Inside -> Out, or Bottom Left -> Top Right.

Profile Pass can run First, Last, or None. Step Over is a fraction of cutter diameter. Inspect small regions, islands, corners, and links between sections after changing diameter or stepover.

Input Curve Fill rule offers Even Odd, Non Zero, Positive, and Negative. It affects how overlapping and nested loops define a region. Check the result rather than assuming every fill rule treats a nested shape identically.

## Tabs and dogbones

Tabs leave material connecting a part to surrounding stock. Choose **Square** or **Pyramid**, then set width, height, and placement.

Automatic placement uses section angle, minimum section length, and spacing. **Tab Input Curves** uses guide-curve intersections. In Cut 1.1, connect guides to the **third input**. Check that every intended intersection creates a tab and that tabs survive the deepest pass. Full Height changes tab behavior and disables the normal height field; inspect the result when switching it.

Dogbones add corner relief where a round bit would otherwise leave an internal radius. Enable them inside Cut or use **GTools Utils Create Dogbones**. Inspect affected corners, relief direction, and extra depth.

## Hole operations

**GTools Gcode Drill** accepts hole geometry and offers **Straight Drill** and **Helical Drill**. Review Divisions per Turn, diameter, direction, offset, depth, and travel height. Supply intended hole geometry rather than assuming an arbitrary point collection provides the radius information needed for helical drilling. Inspect generated paths and warnings. The node name does not imply support for a controller's canned drilling cycles.

## Operation order and custom commands

Keep operations in deliberate execution order. Shallow features, holes, and outside profiles may need different ordering to preserve workholding. Review the actual point sequence after merging or rebuilding paths. The exporter iterates points in point-number order; separate primitives do not automatically create safe transfers.

Custom tools insert explicit commands or raw G-code. Review serialized results, particularly coordinate modes, probing, and spindle commands. Raw text is not checked against your machine configuration.

## Inspect and export

Use Stats for dimensions, depth, length, and estimated time; Check Z for height inspection; and Simulate Cut for approximate material removal. Coarse previews can miss small features. Time estimates do not capture all acceleration, pauses, and controller behavior.

The output path defaults to `$HIP/$HIPNAME.$OS.gcode`. Export creates missing parent directories and **overwrites an existing file at that path**. Use distinct filenames to compare revisions.

The default Start Script includes millimeter units, absolute positioning, feed-per-minute mode, and a pause. End Script contains `M63 P1`, `$HZ`, and `M30`, including a spindle-pin comment. These reflect the author's machine setup. Replace them with commands appropriate to your controller and wiring. Explicitly establish any additional modes needed, including the intended plane for arcs.

**Attempt G1 -> G2/G3 Optimization** is optional and disabled by default. If enabled, inspect reconstructed arcs and deviation readouts. Confirm the final text and its controller interpretation; a smaller file does not establish an equivalent cut.

Before a physical job, verify scale, work coordinates, stock zero, depths, feeds, tabs, transfers, and machine-specific commands. Check the saved file in an independent viewer or controller preview and use your normal machine validation procedure. Re-import through this toolset alone is not an independent check.
