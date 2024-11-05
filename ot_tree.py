import bpy
from bpy.types import Operator

data  = bpy.data
# =================================================
# FUNCTIONS
# =================================================
# IMPORTS: DEV
# =================================================
"""
texts = bpy.data.texts

fn_tree = texts['fn_tree.py'].as_module()

add_branches            = fn_tree.add_branches
add_stem                = fn_tree.add_stem
add_twigs               = fn_tree.add_twigs
branches_exists         = fn_tree.branches_exists
collections_exists      = fn_tree.collections_exists
make_tree               = fn_tree.make_tree
remove_object           = fn_tree.remove_object
rotate_branches         = fn_tree.rotate_branches
stem_and_branch_to_mesh = fn_tree.stem_and_branch_to_mesh
set_display_type        = fn_tree.set_display_type
shade_smooth            = fn_tree.shade_smooth
shade_flat              = fn_tree.shade_flat
start_tree              = fn_tree.start_tree
stem_exists             = fn_tree.stem_exists

"""

# =================================================
# IMPORTS: DEPLOY
# =================================================
#"""
from . fn_tree import add_branches
from . fn_tree import add_stem
from . fn_tree import add_twigs
from . fn_tree import branches_exists
from . fn_tree import collections_exists
from . fn_tree import make_tree
from . fn_tree import remove_object
from . fn_tree import rotate_branches
from . fn_tree import stem_and_branch_to_mesh
from . fn_tree import set_display_type
from . fn_tree import shade_smooth
from . fn_tree import shade_flat
from . fn_tree import start_tree
from . fn_tree import stem_exists
#"""

# =================================================
# PREPARE
# =================================================
class LSR_OT_start_tree(Operator):
    """start tree generation"""
    bl_idname='lsr.start_tree'
    bl_label='enable'

    @classmethod
    def poll(cls, context):
        return not collections_exists()

    def execute(self, context):
        start_tree(context)
        return {'FINISHED'}
    
class LSR_OT_clean_up(Operator):
    """make join(all meshes)"""
    bl_idname='lsr.clean_up'
    bl_label='clean up'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        if stem_exists(context):
            remove_object(scene.target_stem)

        for curve in bpy.data.curves:
            if 'Stem' in curve.name:
                bpy.data.curves.remove(curve)

        for mesh in bpy.data.meshes:
            if 'Stem' in mesh.name:
                bpy.data.meshes.remove(mesh)

        if 'StemPivot' in bpy.data.collections['LSR_TREE_META_STEM'].objects:
            pivot = bpy.data.objects['StemPivot']
            remove_object(pivot)

        for curve in bpy.data.curves:
            if 'StemPivot' in curve.name:
                bpy.data.curves.remove(curve)

        for mesh in bpy.data.meshes:
            if 'StemPivot' in mesh.name:
                bpy.data.meshes.remove(mesh)

        for branch in bpy.data.collections['LSR_TREE_BRANCHES'].objects:
            remove_object(branch)

        for curve in bpy.data.curves:
            if 'Branch' in curve.name:
                bpy.data.curves.remove(curve)

        for mesh in bpy.data.meshes:
            if 'Branch' in mesh.name:
                bpy.data.meshes.remove(mesh)
        
        for twig in bpy.data.collections['LSR_TREE_TWIGS'].objects:
            remove_object(twig, True)

        bpy.context.scene.target_stem = None

        return {'FINISHED'}
    

# =================================================
# ADD
# =================================================
class LSR_OT_add_stem(Operator):
    """generate and add a stem object"""
    bl_idname='lsr.add_stem'
    bl_label='add'

    @classmethod
    def poll(cls, context):
        return not stem_exists(context)

    def execute(self, context):
        add_stem(context)
        return {'FINISHED'}


class LSR_OT_add_branches(Operator):
    """generate and add a branch objects"""
    bl_idname='lsr.add_branches'
    bl_label='add'

    @classmethod
    def poll(cls, context):
        return stem_exists(context)
    
    def execute(self, context):
        add_branches(context)
        return {'FINISHED'}
    

class LSR_OT_add_twigs(Operator):
    """add twigs to branch"""
    bl_idname='lsr.add_twigs'
    bl_label='add'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        scene = bpy.context.scene
        if scene.target_twigs is None:
            return False
        twigs = scene.target_twigs.objects
        if len(twigs) > 0:
            return True
        return False

    def execute(self, context):
        branches = bpy.data.collections['LSR_TREE_BRANCHES'].objects   
        for branch in branches:
            add_twigs(context, branch)
        return {'FINISHED'}
    

# =================================================
# RESET
# =================================================
class LSR_OT_reset_stem(Operator):
    """reset (remove) stem"""
    bl_idname='lsr.reset_stem'
    bl_label='reset'
    
    def execute(self, context):
        scene = bpy.context.scene
        stem = scene.target_stem
        data = bpy.data
        remove_object(stem)
            
        if 'StemPivot' in data.collections['LSR_TREE_META_STEM'].objects:
            pivot = data.objects['StemPivot']
            remove_object(pivot)

        for branch in data.collections['LSR_TREE_BRANCHES'].objects:
            remove_object(branch)
        
        for twig in data.collections['LSR_TREE_TWIGS'].objects:
            remove_object(twig, True)

        return {'FINISHED'}


class LSR_OT_reset_branches(Operator):
    """reset (remove) all branches"""
    bl_idname='lsr.reset_branches'
    bl_label='reset'

    @classmethod
    def poll(cls, context):
        return branches_exists()
    
    def execute(self, context):
        data = bpy.data
        for branch in data.collections['LSR_TREE_BRANCHES'].objects:
            remove_object(branch)
        
        for twig in data.collections['LSR_TREE_TWIGS'].objects:
            remove_object(twig, True)
        
        return {'FINISHED'}  


class LSR_OT_reset_twigs(Operator):
    """add twigs to branch"""
    bl_idname='lsr.reset_twigs'
    bl_label='reset'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        data = bpy.data
        for twig in data.collections['LSR_TREE_TWIGS'].objects:
            remove_object(twig, True)
        return {'FINISHED'}
    

# =================================================
# CONVERT
# =================================================
class LSR_OT_stem_and_branch_to_mesh(Operator):
    """convert generated tree to mesh"""
    bl_idname='lsr.convert_stem_and_branch_to_mesh'
    bl_label='convert to mesh'

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        stem_and_branch_to_mesh(context)
        return {'FINISHED'}


# =================================================
# DISPLAY
# =================================================
class LSR_OT_toggle_wire(Operator):
    """toggle wireframe"""
    bl_idname='lsr.toggle_wire'
    bl_label=''
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        set_display_type('WIRE')
        return {'FINISHED'}
    
class LSR_OT_toggle_textured(Operator):
    """toggle textured"""
    bl_idname='lsr.toggle_textured'
    bl_label=''
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        set_display_type('TEXTURED')
        return {'FINISHED'}
    

# =================================================
# SHADING
# =================================================
class LSR_OT_shade_smooth(Operator):
    """shade stem and branch smooth"""
    bl_idname='lsr.shade_smooth'
    bl_label=''
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shade_smooth()
        return {'FINISHED'}


class LSR_OT_shade_flat(Operator):
    """shade stem and branch flat"""
    bl_idname='lsr.shade_flat'
    bl_label=''
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shade_flat()
        return {'FINISHED'}


# =================================================
# FINISH
# =================================================
class LSR_OT_make_tree(Operator):
    """make join(all meshes)"""
    bl_idname='lsr.make_tree'
    bl_label='make'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        make_tree()
        return {'FINISHED'}
    
