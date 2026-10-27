# Installation and compatibility

[Back to README](../README.md)

## Requirements

HoudiniGTools contains SOP and OBJ digital assets, a Python helper module, and Python dependencies. It writes files for use with a CNC controller; it does not provide a machine connection or sender application.

| Dependency | Purpose |
| --- | --- |
| Houdini | Hosts the node networks, HDAs, VEX, and Python code. |
| [Houdini CurveClipper](https://github.com/handcraftedcc/Houdini-Curve-Clipper) | Supplies `CurveClipper_Boolean::1.0` and `CurveClipper_Offset::1.0`, used inside the cutting networks. Install as a separate package. |
| SideFX Labs | Supplies nodes used for silhouette extraction, preparation, and internal processing. |
| Compatible Python libraries | `pyclipr`, `pyclipper`, and `svgelements` are bundled under `python3.11libs/`. Native extensions must match the host Python and operating system. |

Labs types found in the inspected networks include Extract Silhouette, Split Primitive by Normal, Delete Small Parts, Dissolve Flat Edges, Group Invert, Thicken, and Align and Distribute. Some networks use older type names. A missing legacy Labs type may require a corresponding Labs version or a carefully checked node replacement.

## Configure the package

Keep the repository in its permanent location. Edit the supplied `HoudiniGTools.json` to point there:

```json
{
  "env": [
    {
      "HOUDINIGTOOLS": "C:/HoudiniPackages/HoudiniGTools"
    }
  ],
  "path": "$HOUDINIGTOOLS"
}
```

Replace the example path with your own. Forward slashes avoid JSON backslash escaping problems. Copy the edited JSON into the `packages` directory beneath your Houdini user preferences directory. Create `packages` if necessary, then restart Houdini.

For a typical Windows Houdini 21 setup, that directory is:

```text
%USERPROFILE%/Documents/houdini21.0/packages/
```

The actual location can differ with redirected Documents folders or custom setups. In Houdini's Python Shell, `hou.getenv("HOUDINI_USER_PREF_DIR")` reports the current user preferences directory.

Configure CurveClipper using its own package JSON and installation instructions. Keep both packages enabled.

## Verify installation

1. Open a fresh scene and enter a Geometry network.
2. Search the Tab menu for **GTools Gcode Cut** and **GTools Gcode Output File**. Most SOP tools appear under GTools.
3. Check that **CurveClipper Boolean** and **CurveClipper Offset** are available without missing-definition errors.
4. Resolve missing Labs definitions before attempting a full toolpath.
5. Build the small curve setup in the [workflow guide](workflow.md). Confirm its scale and inspect node warnings.

Useful read-only checks in Houdini's Python Shell:

```python
import hou
import sys
import pyclipr
import gtoolsUtils

print(hou.applicationVersionString())
print(sys.version)
print(hou.getenv("HOUDINIGTOOLS"))
print(pyclipr.__file__)
print(gtoolsUtils.__file__)
```

The module paths help identify an older or duplicate dependency loaded from another package.

## Compatibility

This checkout contains `pyclipr.cp311-win_amd64.pyd` and a native `pyclipper` extension in `python3.11libs/`. These are Windows binaries; `cp311` identifies CPython 3.11. Renaming a folder or extension does not make a binary compatible with another Python version.

For another platform or Python version, obtain compatible builds and make them available to that Houdini runtime. Follow CurveClipper's own instructions for its supported builds. Its compatibility does not establish compatibility for every HoudiniGTools node or dependency.

Asset definitions and representative development networks were structurally inspected with Houdini 21.0.631 for these docs. This was not a complete cooking, export, or machine validation test. A minimum Houdini version has not been established.

G-code output targets FluidNC. Other controllers may require changes to commands, startup and shutdown behavior, work coordinates, and arc handling. The default scripts contain personal machine settings.

## Package contents

| Path | Contents |
| --- | --- |
| `HoudiniGTools.json` | Package environment and search path configuration. |
| `otls/` | SOP and OBJ assets, including earlier and development versions. |
| `scripts/python/gtoolsUtils.py` | Command-building helpers used by custom-command tools. |
| `python3.11libs/` | Bundled Python libraries and native extensions. |
| `docs/` | User and technical documentation. |

The public workflow documentation is self-contained and does not require a sample HIP file.
