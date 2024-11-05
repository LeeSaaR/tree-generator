# =================================================
# LICENSE : GNU GPL v3
# https://www.gnu.org/licenses/gpl-3.0.txt
# =================================================
bl_info = {
    "name": "LeeSaaR TreeGenerator",
    "author": "LeeSaaR",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Generate Simple Trees",
    "category": "Object",
}

import bpy
from bpy.types import (Scene, Object, Collection)
context = bpy.context
data    = bpy.data 

# =================================================
# IMPORTS: DEPLOY
# =================================================
#"""
from . pg_tree import LSR_PG_tree
from . pt_tree import LSR_PT_tree
from . pt_tree import LSR_PT_stem
from . pt_tree import LSR_PT_branches
from . pt_tree import LSR_PT_twigs

from . ot_tree import LSR_OT_start_tree

from . ot_tree import LSR_OT_add_stem
from . ot_tree import LSR_OT_add_branches
from . ot_tree import LSR_OT_add_twigs
from . ot_tree import LSR_OT_reset_stem
from . ot_tree import LSR_OT_reset_branches
from . ot_tree import LSR_OT_clean_up
from . ot_tree import LSR_OT_reset_twigs
from . ot_tree import LSR_OT_toggle_wire
from . ot_tree import LSR_OT_toggle_textured
from . ot_tree import LSR_OT_shade_smooth
from . ot_tree import LSR_OT_shade_flat
from . ot_tree import LSR_OT_stem_and_branch_to_mesh
from . ot_tree import LSR_OT_make_tree
#"""

# =================================================
# IMPORTS: DEV
# =================================================
"""
import os
os.system('clear')
texts   = bpy.data.texts

pt_tree = texts['pt_tree.py'].as_module()
pg_tree = texts['pg_tree.py'].as_module()
ot_tree = texts['ot_tree.py'].as_module()

LSR_PG_tree     = pg_tree.LSR_PG_tree

LSR_PT_tree     = pt_tree.LSR_PT_tree
LSR_PT_stem     = pt_tree.LSR_PT_stem
LSR_PT_branches = pt_tree.LSR_PT_branches
LSR_PT_twigs    = pt_tree.LSR_PT_twigs


LSR_OT_start_tree      = ot_tree.LSR_OT_start_tree
LSR_OT_clean_up        = ot_tree.LSR_OT_clean_up
LSR_OT_add_stem        = ot_tree.LSR_OT_add_stem
LSR_OT_add_branches    = ot_tree.LSR_OT_add_branches
LSR_OT_add_twigs       = ot_tree.LSR_OT_add_twigs
LSR_OT_reset_stem      = ot_tree.LSR_OT_reset_stem
LSR_OT_reset_branches  = ot_tree.LSR_OT_reset_branches
LSR_OT_reset_twigs     = ot_tree.LSR_OT_reset_twigs
LSR_OT_toggle_wire     = ot_tree.LSR_OT_toggle_wire
LSR_OT_toggle_textured = ot_tree.LSR_OT_toggle_textured
LSR_OT_shade_smooth    = ot_tree.LSR_OT_shade_smooth
LSR_OT_shade_flat      = ot_tree.LSR_OT_shade_flat

LSR_OT_stem_and_branch_to_mesh = ot_tree.LSR_OT_stem_and_branch_to_mesh
LSR_OT_make_tree = ot_tree.LSR_OT_make_tree
"""

# =================================================
# CLASSES
# =================================================
classes = (
    LSR_PG_tree,
    LSR_PT_tree,
    LSR_PT_stem,
    LSR_PT_branches,
    LSR_PT_twigs,
    LSR_OT_start_tree,
    LSR_OT_clean_up,
    LSR_OT_add_stem,
    LSR_OT_add_branches,
    LSR_OT_add_twigs,
    LSR_OT_reset_stem,
    LSR_OT_reset_branches,
    LSR_OT_reset_twigs,
    LSR_OT_stem_and_branch_to_mesh,
    LSR_OT_toggle_wire,
    LSR_OT_toggle_textured,
    LSR_OT_shade_smooth,
    LSR_OT_shade_flat,
    LSR_OT_make_tree,
)

# =================================================
# REGISTER
# =================================================
def register():
    from bpy.utils import register_class
    from bpy.props import PointerProperty
    
    for c in classes:
        register_class(c)
        
    Scene.lsr_tree = PointerProperty(type=LSR_PG_tree)
    Scene.target_stem = PointerProperty(type=Object)
    Scene.target_twigs = PointerProperty(type=Collection)

# =================================================
# UNREGISTER
# =================================================
def unregister():
    from bpy.utils import unregister_class
    
    for c in reversed(classes):
        unregister_class(c)

    del Scene.lsr_tree
    del Scene.target_stem

if __name__ == "__main__":
    register()
