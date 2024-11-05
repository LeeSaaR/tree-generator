from bpy.types import Panel
import bpy

# =================================================
# FUNCTIONS
# =================================================
# IMPORTS: DEV
# =================================================
"""
texts = bpy.data.texts

fn_tree = texts['fn_tree.py'].as_module()

branches_exists     = fn_tree.branches_exists
collections_exists  = fn_tree.collections_exists
stem_exists         = fn_tree.stem_exists
twigs_exists        = fn_tree.twigs_exists

"""

# =================================================
# IMPORTS: DEPLOY
# =================================================
#"""
from . fn_tree import branches_exists
from . fn_tree import collections_exists
from . fn_tree import stem_exists
from . fn_tree import twigs_exists
#"""

data = bpy.data

class LSR_PT_tree(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LSR"
    bl_options = {"DEFAULT_CLOSED"}

    bl_idname = "LSR_PT_tree"
    bl_label = "Tree"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('lsr.start_tree')
        row = layout.row()
        row.operator('lsr.clean_up')

        if not collections_exists():
            return

        if stem_exists(context):
            row = layout.row()
            row.operator('lsr.reset_stem', text='reset stem')

        if branches_exists():
            row = layout.row()
            row.operator('lsr.reset_branches', text='reset branches')

        if twigs_exists():
            row = layout.row()
            row.operator('lsr.reset_twigs', text='reset twigs')

        is_mesh = False
        if branches_exists():
            is_mesh = bpy.data.objects['Branch'].type == 'MESH'

        if branches_exists() and is_mesh:
            row = layout.row()
            row.operator('lsr.shade_smooth', text="smooth")
            row.operator('lsr.shade_flat', text="flat")

        if twigs_exists():
            row = layout.row()
            row.operator('lsr.toggle_wire', text="wire")
            row.operator('lsr.toggle_textured', text="textured")
            row = layout.row()
            row.operator('lsr.make_tree', text='make tree', icon='CHECKMARK')
        

class LSR_PT_stem(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LSR"
    bl_options = {"DEFAULT_CLOSED"}

    bl_parent_id = "LSR_PT_tree"
    bl_idname = "LSR_PT_stem"
    bl_label = "Stem"

    def draw(self, context):
        scene    = context.scene
        pg = scene.lsr_tree
        layout = self.layout

        row = layout.row()
        row.label(text="", icon="OUTLINER_OB_CURVE")

        if not stem_exists(context):
            row = layout.row()
            row.prop(pg, 'stem_height')
            row = layout.row()
            row.prop(pg, 'stem_base_radius')
            row = layout.row()
            row.prop(pg, 'stem_radius_min')
            row = layout.row()
            row.prop(pg, 'stem_segments')
            row = layout.row()
            row.prop(pg, 'stem_random_pos_factor')
            row = layout.row()
            row.operator('lsr.add_stem')


class LSR_PT_branches(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LSR"
    bl_options = {"DEFAULT_CLOSED"}

    bl_parent_id = "LSR_PT_tree"
    bl_idname = "LSR_PT_branches"
    bl_label = "Branches"

    def draw(self, context):
        scene    = context.scene
        pg = scene.lsr_tree

        if not stem_exists(context):
            return
        
        
        layout = self.layout
        row = layout.row()
        row.label(text="", icon="OUTLINER_OB_CURVES")
        if not branches_exists():
            row = layout.row()
            row.prop(pg, 'branches_count')
            row = layout.row()
            row.prop(pg, 'branches_start_height')
            row = layout.row()
            row.prop(pg, 'branches_start_tilt')
            row = layout.row()
            row.prop(pg, 'branches_max_tilt')
            row = layout.row()
            row.prop(pg, 'branches_rotation')
            row = layout.row()
            row.prop(pg, 'branches_segments')
            row = layout.row()
            row.prop(pg, 'branches_random_pos')
            row = layout.row()
            row.prop(pg, 'branches_crown_width')
            row = layout.row()
            row.prop(pg, 'branches_crown_overtop')
            row = layout.row()
            row.operator('lsr.add_branches')

        branch_is_curve = True
        if branches_exists():
            branch_is_curve = bpy.data.objects['Branch'].type == 'CURVE'

        if branches_exists() and branch_is_curve:
            row = layout.row()
            row.operator('lsr.convert_stem_and_branch_to_mesh')


class LSR_PT_twigs(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LSR"
    bl_options = {"DEFAULT_CLOSED"}

    bl_parent_id = "LSR_PT_tree"
    bl_idname = "LSR_PT_twigs"
    bl_label = "Twigs"

    def draw(self, context):
        scene = context.scene
        if not stem_exists(context):
            return
        
        if not branches_exists():
            return

        branch_is_curve = bpy.data.objects['Branch'].type == 'CURVE'
        if branch_is_curve:
            return
        
        pg = scene.lsr_tree
        layout = self.layout
        
        row = layout.row()
        row.label(text="", icon="CURVES")
        
        if not twigs_exists():
            row = layout.row()
            row.prop_search(scene, "target_twigs", scene.collection, "children", text="")            

            row = layout.row()
            row.prop(pg, 'twigs_start_angle')
            row.prop(pg, 'twigs_end_angle')

            row = layout.row()
            row.prop(pg, 'twigs_start_factor')
            row.prop(pg, 'twigs_end_factor')

            row = layout.row()
            row.operator('lsr.add_twigs')
        
