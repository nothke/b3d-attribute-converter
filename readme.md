## No longer needed!

This plugin is no longer required since blender 3.5.0 as both colors and UVs are converted to built-in attributes automatically:
- UVs need to be 2D Vector in Face Corner domain
- Colors - can either be Color or Byte Color in Vertex or Face Corner domains

## For blender 3.4 and earlier:

In 3.2 there's been a change on how attributes work, namely "Named Attribute" and "Store Named Attribute" nodes have been added, which simplify storing attributes from nodes a lot. However, they will still not overwrite the built-in attributes, so it still needs to be converted manually.

As of 3.2 and in at least 3.3, color attributes are actually bound together between geonode-attributes and built-in-attributes, so no conversion is necessary. It is still however necessary for UVs, so this plugin will simply skip converting colors in those versions.

# Attribute Converter

Simplifies converting attributes created by geometry nodes to built-in attributes like UVs or vertex colors, as a single click operation for all selected objects.

Only compatible with blender versions 3.1.0 and above.

The operation is destructive, as it requires Geometry Node modifier to be applied, so it is ideally used just before exporting. (if you know a way this can be somehow injected into the export pipeline so it runs automatically before export, please tell me!)

### Current limitations
* Only supports uv and vertex color for now
* Only supports 1 layer of each
* Undo doesn't work

If you wish to add any more features, pull requests are welcome.

### How to use

When you install the addon, "Utils" panel will appear on the right side of the viewport where all the options are.

The addon lets you select a name for your attributes you wish to convert. For example, the uv attribute has a "uv" name by default. This is what your attribute in "Output Attributes" in GeometryNodes modifier should be called. Any attributes that don't match the names will simply be skipped.

When you select the desired objects and click on "Apply and Convert" all modifiers will be applied (including the GeometryModifier) and the corresponding resulting attributes will be converted to built-in attributes. So, note that the operations is destrcutive, and you should save just before using the operator because undo doesn't work (yet).
