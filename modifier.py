import bpy

from common import append_from_library


def section(options):
    # Avoid transparency glitches (section is based on transparency)
    # Might be still too little for some meshes
    # (encountered models which needed 42 bounces ...)
    bpy.context.scene.cycles.transparent_max_bounces = 16

    axis = options.modifier_section_axis

    append_from_library("section", "NodeTree", "section")
    section_node_group = bpy.data.node_groups["section"]

    for mat in bpy.data.materials:
        section_node_group_node = mat.node_tree.nodes.new("ShaderNodeGroup")
        section_node_group_node.node_tree = bpy.data.node_groups["section"]

        if options.modifier_type == "animated-cross-section":
            bpy.context.scene.frame_current = 1
            section_node_group_node.inputs[axis].default_value = options.modifier_section_level_from
            section_node_group_node.inputs[axis].keyframe_insert("default_value")

            bpy.context.scene.frame_current = bpy.context.scene.frame_end
            section_node_group_node.inputs[axis].default_value = options.modifier_section_level_to
            section_node_group_node.inputs[axis].keyframe_insert("default_value")

            for fc in section_node_group_node.inputs[axis].id_data.animation_data.action.fcurves:
                fc.extrapolation = 'LINEAR'
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
        else:
            section_node_group_node.inputs[axis].default_value = options.modifier_section_level

        surface_shader = None
        for node in mat.node_tree.nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_material_node = node
                for input in node.inputs:
                    for link in input.links:
                        surface_shader = link.from_node

        mat.node_tree.links.new(surface_shader.outputs[0],
                                section_node_group_node.inputs["Shader"])

        mat.node_tree.links.new(section_node_group_node.outputs["Shader"],
                                output_material_node.inputs["Surface"])


def setup(options):
    if options.modifier_type == "none":
        pass
    elif options.modifier_type in ("cross-section", "animated-cross-section"):
        section(options)
