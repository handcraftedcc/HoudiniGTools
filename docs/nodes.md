# Node reference

[Back to README](../README.md) · [Workflow guide](workflow.md)

Names below are the asset labels; capitalization varies in Houdini. The type names identify exact definitions when several versions appear in the Tab menu. These descriptions cover the inspected interfaces and networks, not a promise that every exposed option is complete.

## Preparation

| Node | Type | Purpose and main controls |
| --- | --- | --- |
| Gtools Prep Lay Flat | `gtools::gtools_prep_lay_flat::1.0` | Orient separate parts for flat-stock work. Uses large planar regions to establish orientation. Flip Group selects pieces to flip. |
| GTools Prep Layout | `gtools::gtools_prep_layout::1.1` | Arrange parts on stock using a UV-layout-based network. Stock Count and Size define multiple rectangles; other controls include rotation step, cavity packing, padding, boundary padding, and iterations. |
| GTools Prep Layout, earlier version | `gtools::gtools_prep_layout::1.0` | Single Stock Size interface. Keep it when an existing scene depends on that version. |
| Gtools Prep Silhouette To Curves | `gtools::gtools_prep_silhouette_to_curves::1.0` | Extract curves from silhouettes. Controls include Tolerance, Remove Outside of Silhouette, and Flatten Mode. Inspect retained boundaries. |
| Gtools Prep 3D To Curves | `gtools::gtools_prep_3d_to_curves::1.0` | Prepare curves from 3D geometry. Controls include Tolerance, Make Isolated Loops Closed, and Flatten Mode. Useful for selecting features separately from the outer silhouette. |

All preparation nodes take geometry on their first input. Inspect curve closure, winding, units, and Z levels before creating paths.

## GTools Gcode Cut

Type: `gtools::gtools_gcode_cut::1.1`. Generates toolpath geometry from cutting curves. Version 1.0 is also shipped. Use 1.1 as the starting point for this documentation; `gtools.dev` versions have different interfaces.

Connect cutting curves to the first input. For guide-based tab placement, connect guide curves to the third input and select Tab Input Curves. The main controls are:

| Area | Controls and behavior |
| --- | --- |
| Operation | Name, coordinate-system selection, and Input Curve Fill rule. Default coordinate selection is G54; verify the actual work offset on your machine. |
| Bit Settings | Bit Diameter and unit, Feedrate and Plunge Rate in mm/min, Plunge Angle, fractional Step Over, and Max Depth of Cut with unit. |
| Cut mode | Part (Outside lines), Engrave (On lines), or Hole (Inside lines). |
| Direction and fit | Conventional/Climb and Extra Offset with unit. Inspect the compensation result. |
| Depth | Cut Depth (Absolute), Read From Input, Cut Z Start, and Travelzheight. Dimensional controls have unit selectors. |
| Pocketing | None, Raster, or Parallel; available for Hole mode. Profile Pass: First, Last, or None. Raster adds Angle; Parallel adds Direction. |
| Tabs | No Tabs, Square, or Pyramid. Width, height, Full Height, and Auto Placement/Tab Input Curves. Automatic placement adds section-angle, section-length, and spacing controls. |
| Dogbones | Enable, minimum angle, flip, closed handling, tolerance, and extra depth. |
| Guides | Toggle and color the input and cutting guides. Guides are visual aids. |

Read From Input computes positive cut depth from a planar input at Z <= 0. It does not automatically handle mixed depths in one selection. Split those features into operations or set depth manually.

## GTools Gcode Drill

Type: `gtools::gtools_gcode_drill::1.0`. Takes hole geometry on one input and generates **Straight Drill** or **Helical Drill** paths.

Controls include operation name, coordinate system, bit diameter, feed and plunge rates, plunge angle, stepover, maximum depth per pass, drill depth, start Z, and travel height. Helical settings include Divisions per Turn, cutting direction, and extra offset. Check the path and warnings for your input geometry; this node is not a general canned-cycle interface.

## Commands, import, and export

| Node | Type | Purpose |
| --- | --- | --- |
| GTools Gcode Custom | `gtools::gtools_gcode_custom::1.0` | Build a list of command points, optionally following input geometry. Command types include raw Custom text, G0, G1, G4, probing, coordinate selection, pause, and spindle controls. |
| GTools Gcode Custom Copy | `gtools::gtools_gcode_custom_copy::1.0` | Alternate command-builder asset with overlapping functionality. Inspect its implementation before relying on differences from Custom; it is not a documented general copy-to-points workflow. |
| GTools Import Gcode File | `gtools::gtools_import_gcode_file::1.0` | Read a Gcode Path into attributed geometry. Reload refreshes the file. Optional G2/G3 sampling exposes a subsampling distance. See parser limitations in the technical notes. |
| GTools Gcode Output File | `gtools::gtools_gcode_output_file::1.0` | Serialize toolpath points and write a file through Export Gcode. Includes Output Filepath, Start Script, End Script, and optional arc optimization. |

The output node exposes arc-fit controls for radial error, minimum points, turn consistency, edge ratios, and Z planarity. Preview G2G3 Arcs and the median/maximum deviation fields help inspect the result. Their existence does not validate controller behavior or arc equivalence.

The Custom interface contains settings for features that are not fully implemented in the helper/export code. In particular, do not infer complete arc, incremental-move, probing, or spindle parameter support from a parameter being visible. Inspect the written text.

## Analysis

| Node | Type | Purpose and main controls |
| --- | --- | --- |
| GTools Analysis Stats | `gtools::gtools_analysis_stats::1.0` | Cut dimensions, maximum depth, total length, and estimated time. Includes dimension units and a rapid-feed estimate. The G0 Feedrate label says mm/s, while cutting feeds use mm/min; verify estimate conventions rather than treating the result as a controller runtime prediction. |
| Gtools Analysis Check Z | `gtools::gtools_analysis_check_z::1.0` | Clip the path above or below a Z Height in mm using Mode. At Z = 0 this helps separate above-surface travel from below-surface cutting geometry. |
| Gtools Simulate Cut | `gtools::gtools_simulate_cut::1.0` | Approximate material removal from toolpath geometry. Method selects Heightfield or VDB processing. Set stock thickness, cutter diameter/length, resample length, and voxel size. |

Two HDA files in this checkout define `gtools::gtools_simulate_cut::1.0`: `sop_gtools.gtools_simulate_cut.1.0.hda` and `sop_gtools.gtools_analysis_simulate_cut.1.0.hda`. They are not separate node types. If behavior is unexpected, check which definition Houdini has selected.

Simulation resolution affects both speed and accuracy. Neither simulation method models the complete machine, fixtures, cutter forces, or workholding.

## Utilities

These nodes support the main HDAs. Some defaults reference parent controls, so standalone use requires checking expressions and units.

| Node | Exact type | Role / controls |
| --- | --- | --- |
| Create Attributes | `gtools::gtools_utils_create_attributes::1.0` | Initialize point attributes used by the command pipeline; accepts optional geometry. |
| Presort Paths | `gtools::gtools_utils_persort_paths::1.0` | Reorder paths to improve travel; Twoopt Passes and Max Swap Checks. The type and filename retain the spelling `persort`. |
| Connect Paths | `gtools::GtoolsUtilsConnectPaths::1.0` | Connect path sections with travel/plunge handling. Distance threshold, travel height, travel feedrate, and plunge rate. Defaults include parent-relative expressions. |
| Add In And Out Point | `gtools::gtools_utils_add_in_and_out_point::1.0` | Add entry/exit points using Safe Height. |
| Ramp In | `gtools::gtools_utils_ramp_in::1.0` | Ramp handling using Plunge Angle and Max Depth Of Cut. |
| Generate Tabs | `gtools::gtools_utils_generate_tabs::1.0` | Tab construction helper with cut depth, bit diameter, tab shape/size, and placement controls. Supports additional inputs. |
| Is Curve CCW | `gtools::gtools_utils_is_curve_ccw::1.0` | Classify curve winding. CCW group name and optional CW/CCW colors. |
| Check Curve Direction | `gtools::gtools_utils_check_curve_direction::1.0` | Visualize direction with resample length and arrow scale. Stored in `sop_subnet1.hda`. |
| Create Dogbones | `gtools::DogBones::1.0` | Corner relief with cutter diameter in mm, minimum angle, flip, closed handling, tolerance, and extra depth. |
| Calc IJK | `gtools::gtools_utils_calc_ijk::1.0` | Calculate packed arc-center values; exposes the extra-points group name. |
| Rebuild G2G3 Arcs | `gtools::gtools_utils_rebuild_g2g3_arcs::1.0` | Reconstruct sampled arc geometry for inspection, controlled by Arc Tolerance. |

## Reference objects

At OBJ level, **Gtools Reference Grid** (`gtools::gtools_reference_grid::1.0`) displays a work area with size, units, mark spacing, font size, and color controls.

**Gtools Reference Stock** (`gtools::gtools_reference_stock::1.0`) displays stock size and thickness, with unit selectors and display controls. These are scene references, not controller travel limits or collision checks.

## Earlier and development assets

`gtools::gtools_generate_gcode::1.0` and `::1.1` are earlier geometry-processing assets labeled GTools Generate Gcode. Despite the label, they are not the documented file writer. Use **Gcode Output File** to write `.gcode` files.

The repository also includes:

- `gtools.dev::gtools_gcode_custom::1.0`
- `gtools.dev::gtools_gcode_cut::1.3`
- `gtools.dev::gtools_generate_gcode::1.2`
- `gtools.dev::gtools_generate_gcode::1.3`

Treat these as development iterations. Their units, controls, and internal assumptions differ from the documented main nodes. Check exact types in existing scenes, and revalidate paths after changing a definition or version.
