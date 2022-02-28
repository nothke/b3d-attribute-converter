import bpy
from bpy.props import StringProperty

# OPERATOR


class NOTHKE_OT_AttributeConverter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.attrcon_apply"
    bl_label = "Convert All Attributes"

    uv_name: StringProperty(default="uv")
    color_name: StringProperty(default="color")

    def execute(self, context):
        print("Executing")

        active = context.view_layer.objects.active
        active.data.attributes. active_index = 1
        bpy.ops.geometry.attribute_convert(mode='UV_MAP')

        # meshes = []

        # # gather meshes of selected objects
        # for obj in bpy.context.selected_objects:
        #     if obj.data not in meshes:
        #         meshes.append(obj.data)

            

        # # foreach mesh
        # for mesh in meshes:
        #     for attr in mesh.attributes:
        #         print("Attr: name " + attr.name + ", type: " + attr.data_type)

        #         bpy.ops.geometry.attribute_convert(mode='UV_MAP')

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
        description="Export all objects from this collection",
        default='uv')

    bpy.types.Scene.attrcon_color_name = bpy.props.StringProperty(
        name="Color Name",
        description="Export all objects from this collection",
        default='color')

    print('properties registered')

    bpy.utils.register_class(NOTHKE_PT_AttributeConverter)
    print('panel registered')


def unregister():
    bpy.utils.unregister_class(NOTHKE_PT_AttributeConverter)
    bpy.utils.unregister_class(NOTHKE_OT_AttributeConverter)
    #del bpy.types.Scene.hofexport_layer
    #del bpy.types.Scene.hofexport_filename


if __name__ == "__main__":
    register()
