bl_info = {
    "name": "Attribute Converter",
    "author": "Nothke",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "View3D > Object > Convert > Convert Attributes",
    "description": "Simplifies converting attributes created by geometry nodes to built-in attributes like UVs or vertex colors, as a single click operations for all selected objects.",
    "warning": "",
    "doc_url": "",
    "category": "Conversion",
}

from audioop import reverse
import bpy
from bpy.props import StringProperty
from bpy.props import BoolProperty

# OPERATOR


def clear_collection(collection):
    for i in reversed(range(len(collection))):
        collection.remove(collection[i])

class NOTHKE_OT_AttributeConverter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.attrcon_apply"
    bl_label = "Convert All Attributes - by Nothke"

    uv_name: StringProperty(default="UVMap")
    color_name: StringProperty(default="Color")
    remove_existing: BoolProperty(default=True)
    skip_if_no_nodes: BoolProperty(default=False)

    def execute(self, context):
        print("## Begun converting attributes")

        original_active = context.view_layer.objects.active

        # note: in blender 3.2+ vertex colors no longer need to be converted
        #       as they are shared between "Attributes" and "Color Attributes"
        version = bpy.app.version
        b_3_2_or_better = version[0] >= 3 and version[1] >= 2

        objs = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        for obj in objs:
            obj.select_set(True)
            context.view_layer.objects.active = obj

            if obj.type != 'MESH' and obj.type != 'CURVE':
                continue

            if len(obj.modifiers) == 0:
                continue

            has_geonodes = False
            for modifier in obj.modifiers:
                if modifier.type == 'NODES':
                    has_geonodes = True

            if self.skip_if_no_nodes and not has_geonodes:
                #print("--- object " + obj.name + " has no geometry nodes modifier, skipping")
                continue

            bpy.ops.object.convert(target='MESH')

            # remove existing uv and color maps
            if self.remove_existing:
                clear_collection(obj.data.uv_layers)
                if not b_3_2_or_better:
                    clear_collection(obj.data.vertex_colors)

            for i in reversed(range(len(obj.data.attributes))):
                attr = obj.data.attributes[i]

                obj.data.attributes.active_index = i

                # print(attr.name)

                if attr.name == self.uv_name:
                    bpy.ops.geometry.attribute_convert(mode='UV_MAP')
                    print("--- Applied uv for " + obj.name)

                if attr.name == self.color_name and not b_3_2_or_better:
                    bpy.ops.geometry.attribute_convert(mode='VERTEX_COLOR')
                    print("--- Applied color for " + obj.name)

            obj.select_set(False)

        # Reselect all objects
        for obj in objs:
            obj.select_set(True)

        context.view_layer.objects.active = original_active

        print("## Finished converting attributes")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(NOTHKE_OT_AttributeConverter.bl_idname, text=NOTHKE_OT_AttributeConverter.bl_label)

# UI PANEL


class NOTHKE_PT_AttributeConverter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Attribute Converter"
    bl_idname = "NOTHKE_PT_AttributeConverter"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  # 'TOOLS'
    bl_category = 'Utils'

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.prop(scene, 'attrcon_skip_if_no_nodes')

        row = layout.row()
        row.prop(scene, 'attrcon_remove_existing')

        row = layout.row()
        row.prop(scene, 'attrcon_uv_name')

        row = layout.row()
        row.prop(scene, 'attrcon_color_name')

        # export button, create operator
        row = layout.row()
        op = row.operator('object.attrcon_apply', text='Apply and Convert')

        # set properties to operator values
        op.uv_name = scene.attrcon_uv_name
        op.color_name = scene.attrcon_color_name
        op.remove_existing = scene.attrcon_remove_existing
        op.skip_if_no_nodes = scene.attrcon_skip_if_no_nodes


def register():

    bpy.utils.register_class(NOTHKE_OT_AttributeConverter)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    print('operator registered')

    # register properties
    bpy.types.Scene.attrcon_uv_name = bpy.props.StringProperty(
        name="UV Name",
        description="The name of the uv attribute set in the GeometryNode modifier 'Output Attribute'. If none is found it will be skipped.",
        default='UVMap')

    bpy.types.Scene.attrcon_color_name = bpy.props.StringProperty(
        name="Color Name",
        description="The name of the color attribute set in the GeometryNode modifier 'Output Attribute'. If none is found it will be skipped.",
        default='Color')

    bpy.types.Scene.attrcon_remove_existing = bpy.props.BoolProperty(
        name="Remove existing maps?",
        description="Do you want to remove existing uv and color maps before applying the converted attributes? If false, it will keep the original and add the converted attributes.",
        default=True)

    bpy.types.Scene.attrcon_skip_if_no_nodes = bpy.props.BoolProperty(
        name="Skip if no nodes",
        description="If an object does not have Geometry Nodes modifier, applying attributes will be skipped without warning. This is useful when selecting many objects",
        default=False)

    print('properties registered')

    bpy.utils.register_class(NOTHKE_PT_AttributeConverter)
    print('panel registered')


def unregister():
    bpy.utils.unregister_class(NOTHKE_PT_AttributeConverter)
    bpy.utils.unregister_class(NOTHKE_OT_AttributeConverter)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    del bpy.types.Scene.attrcon_uv_name
    del bpy.types.Scene.attrcon_color_name
    del bpy.types.Scene.attrcon_remove_existing
    del bpy.types.Scene.attrcon_skip_if_no_nodes


if __name__ == "__main__":
    register()
