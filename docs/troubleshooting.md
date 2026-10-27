# Limitations and troubleshooting

[Back to README](../README.md)

HoudiniGTools is experimental and primarily a personal toolset. Its defaults and preview tools do not establish that a generated job is suitable for another machine.

## Common problems

| Symptom | What to check |
| --- | --- |
| No GTools nodes in the Tab menu | Confirm the package JSON is in the active Houdini user preferences `packages` folder, the placeholder path is replaced, and Houdini has restarted. Use the correct SOP or OBJ context. |
| Missing CurveClipper definitions | Install the separate [CurveClipper package](https://github.com/handcraftedcc/Houdini-Curve-Clipper). Python libraries alone do not supply the Boolean/Offset HDAs. |
| Missing Labs node or invalid operator type | Enable SideFX Labs and check the specific type/version. Some assets use legacy Labs names. |
| Python import or DLL-load error | Check the runtime's Python version, operating system, architecture, and loaded module path. The bundled native libraries target CPython 3.11 on Windows x64. Restart after changing native extensions. |
| A shape is 1,000 times too large or small | Check meter-based Houdini geometry versus millimeter-based G-code. The output node performs the meter-to-mm conversion. |
| Missing or unexpected pocket regions | Inspect curve closure, winding, nested loops, fill rule, cutter size, and the output of CurveClipper. Isolate a small shape to locate the failing stage. |
| Unexpected cutter offset | Verify Part/Engrave/Hole mode, actual bit diameter, unit selector, and Extra Offset. |
| Read From Input refuses depth | The input must have a common Z level at or below zero. Split features at different depths or set depth manually. |
| Tabs are missing | Check Tab Type, placement mode, third-input guide connections, actual curve intersections, minimum section length, spacing, and final pass depth. Inspect from the side. |
| Unexpected entry or travel move | Check plunge angle, available ramp length, travel height, and point order. Inspect transitions between merged operations as well as inside each operation. |
| Standalone utility has bad parameter references | Some utility defaults reference parent controls such as `CONTROL`. Replace those expressions with appropriate local settings when using the utility outside its intended HDA. |
| Simulation is slow or misses details | Review resample length and voxel size. Smaller values cost more memory/time; larger values can hide tabs, narrow cuts, or thin remaining stock. |
| Time estimate differs from the machine | Check rapid-feed assumptions and units. Acceleration, pauses, controller planning, and machine limits affect actual duration. |
| Export is empty or loses commands | Check input attributes and point sequence. Inspect console diagnostics for unsupported `G_Gtype` values and compare saved text against intended commands. |
| Export went to an unexpected file | Check expanded `$HIP`, `$HIPNAME`, and `$OS`, especially after renaming the scene or output node. Existing files are overwritten. |
| Imported geometry differs from a controller preview | Check token formatting, modal commands, unit mode, work offsets, and relative coordinates. The parser is not a full interpreter. |
| Arc optimization changes the cut | Disable optimization and compare the linear path. Inspect fit settings, reconstructed geometry, deviations, final I/J values, and controller interpretation. |

## Known boundaries

- The documented workflow is flat-stock and 2.5D machining, not general 3D surface CAM.
- FluidNC is the output target. The repository does not provide verified postprocessors for arbitrary controllers.
- Default scripts contain machine-specific output and homing commands. Replace them for your setup.
- The importer and writer support subsets of G-code; arbitrary files cannot be round-tripped reliably.
- Custom command settings include incomplete paths. In particular, hand-built arcs and incremental moves need close inspection.
- Simulated material removal does not model complete machine collisions, fixtures, cutter deflection, cutting forces, or workholding failure.
- Earlier and development HDA versions coexist, and two files define the same Simulate Cut type. Definition selection can affect behavior.
- Compatible Python libraries do not by themselves establish HDA compatibility with a different Houdini release.

## When investigating a failure

Reduce the network to the smallest curve and operation that reproduces the issue. Record the exact HDA type/version, Houdini and Python versions, relevant settings and units, and whether the discrepancy starts in geometry generation, serialization, or controller interpretation. Preserve the original G-code when comparing imports and exports.

For a physical job, use your normal independent file inspection and machine validation process. Re-run that process after geometry, tooling, feeds, offsets, tabs, work coordinates, or script changes.
