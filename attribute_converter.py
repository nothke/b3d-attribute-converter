bl_info = {
    "name": "Attribute Converter",
    "category": "Object",
    "blender": (3, 10, 0)
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
    bl_label = "Convert All Attributes"

    uv_name: StringProperty(default="uv")
    color_name: StringProperty(default="color")
    remove_existing: BoolProperty(default=True)

    def execute(self, context):
        print("Executing")

        for obj in bpy.context.selected_objects:
            context.view_layer.objects.active = obj

            # apply modifiers
            bpy.ops.object.convert(target='MESH')

            # remove existing uv and color maps
            if self.remove_existing:
                clear_collection(obj.data.vertex_colors)
                clear_collection(obj.data.uv_layers)

            # convert attributes
            for i in reversed(range(len(obj.data.attributes))):
                attr = obj.data.attributes[i]

                obj.data.attributes.active_index = i

                print(attr.name)

                if attr.name == self.uv_name:
                    bpy.ops.geometry.attribute_convert(mode='UV_MAP')

                if attr.name == self.color_name:
                    bpy.ops.geometry.attribute_convert(mode='VERTEX_COLOR')

        return {'FINISHED'}

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


def register():

    bpy.utils.register_class(NOTHKE_OT_AttributeConverter)
    print('operator registered')

    # register properties
    bpy.types.Scene.attrcon_uv_name = bpy.props.StringProperty(
        name="UV Name",
        description="The name of the uv attribute set in the GeometryNode modifier 'Output Attribute'. If none is found it will be skipped.",
        default='uv')

    bpy.types.Scene.attrcon_color_name = bpy.props.StringProperty(
        name="Color Name",
        description="The name of the color attribute set in the GeometryNode modifier 'Output Attribute'. If none is found it will be skipped.",
        default='color')

    bpy.types.Scene.attrcon_remove_existing = bpy.props.BoolProperty(
        name="Remove existing maps?",
        description="Do you want to remove existing uv and color maps before applying the converted attributes? If false, it will keep the original and add the converted attributes.",
        default=True)

    print('properties registered')

    bpy.utils.register_class(NOTHKE_PT_AttributeConverter)
    print('panel registered')


def unregister():
    bpy.utils.unregister_class(NOTHKE_PT_AttributeConverter)
    bpy.utils.unregister_class(NOTHKE_OT_AttributeConverter)

    del bpy.types.Scene.attrcon_uv_name
    del bpy.types.Scene.attrcon_color_name
    del bpy.types.Scene.attrcon_remove_existing


if __name__ == "__main__":
    register()
